"""Conversation Service - Xử lý business logic hội thoại."""
from typing import Any, Callable, Dict, Optional

from controller.interfaces import IActionHandler, IAudioService, IUserController
from service.intern.text_utils import extract_location


class ActionResult:
    def __init__(self, text: str, needs_slot: Optional[str] = None, 
                 intent: Optional[str] = None):
        self.text = text
        self.needs_slot = needs_slot  # e.g., "location", "time", "name"
        self.intent = intent  # original intent needing the slot
    
    def __str__(self):
        return self.text
    
    def __repr__(self):
        return f"ActionResult(text={self.text!r}, needs_slot={self.needs_slot!r}, intent={self.intent!r})"


class ConversationContext:
    def __init__(self):
        self.pending_intent: Optional[str] = None
        self.slots: Dict[str, Any] = {} 
        self.slot_history: Dict[str, List[Any]] = {} 
    
    def set_pending(self, intent: str, **slots):
        """Set pending intent with optional slot data."""
        self.pending_intent = intent
        self.slots.update(slots)
    
    def set_slot(self, key: str, value: Any) -> bool:
        overwritten = key in self.slots
        if overwritten:
            if key not in self.slot_history:
                self.slot_history[key] = []
            self.slot_history[key].append(self.slots[key])
            print(f"[Context] Slot '{key}' changed: '{self.slots[key]}' → '{value}'")
        self.slots[key] = value
        return overwritten
    
    def clear_pending(self):
        """Clear pending intent and slots."""
        self.pending_intent = None
        self.slots.clear()
        self.slot_history.clear()
    
    def is_pending(self, intent: str) -> bool:
        """Check if specific intent is pending."""
        return self.pending_intent == intent
    
    def get_slot(self, key: str, default=None):
        """Get slot value."""
        return self.slots.get(key, default)


class ConversationService:
    def __init__(self, 
                 audio_service: IAudioService,
                 user_controller: IUserController,
                 action_handler: IActionHandler):
        self.audio = audio_service
        self.user = user_controller
        self.actions = action_handler
        
        # Lazy init services
        self._intent_service = None
        self._memory_service = None
        
        # Session-based contexts (production-safe: multi-user, multi-thread)
        # NOTE: Service is stateless - session_id passed per request, not stored
        self._contexts: Dict[str, ConversationContext] = {}
    
    def init_memory_service(self, memory_service):
        """Inject MemoryService."""
        self._memory_service = memory_service
    
    def get_or_create_context(self, session_id: str) -> ConversationContext:
        if session_id not in self._contexts:
            self._contexts[session_id] = ConversationContext()
        return self._contexts[session_id]
    
    def end_session(self, session_id: str):
        if session_id in self._contexts:
            del self._contexts[session_id]
    
    def _get_intent_service(self):
        """Lazy init IntentService."""
        if self._intent_service is None:
            from service.intern import IntentService
            self._intent_service = IntentService()
        return self._intent_service
    
    def init_intent_service(self):
        """Eager init IntentService at startup."""
        return self._get_intent_service()
    
    def process_exchange(self, user_input: str, 
                         speak_callback: Optional[Callable] = None,
                         user_name: str = "bạn",
                         session_id: str = "default") -> str:
        result_text = None  
        should_save = False  
        context = self.get_or_create_context(session_id)
        if context.is_pending("weather"):
            location = extract_location(user_input)
            if location:
               
                context.set_slot("location", location)
                result = self.actions.handle("weather", user_input, user_name, context)
                context.clear_pending()
                
                if isinstance(result, ActionResult):
                    result_text = result.text
                else:
                    result_text = str(result)
                should_save = True  
            else:
                result_text = "Bạn muốn xem thời tiết ở đâu?"
                should_save = False 
        if result_text is None:
            intent_service = self._get_intent_service()
            intent = intent_service.classify(user_input)
            
            
            if context.pending_intent and intent != context.pending_intent:
                # User changed their mind - clear old context
                print(f"[Context] User changed from '{context.pending_intent}' to '{intent}' - clearing pending")
                context.clear_pending()
            
            # 3. Check for name update (both 'update_name' and 'name' intents)
            if intent in ["update_name", "name"]:
                extracted_name = intent_service.extract_name(user_input)
                if extracted_name:
                    old_name, new_name = self.user.update_user_name(extracted_name)
                    if new_name:
                        user_name = new_name
                        self.actions.set_user_name(new_name)
                        result_text = f"Chào {new_name}! Rất vui được gặp bạn. Bạn cần mình giúp gì không?"
                    else:
                        result_text = f"Chào {extracted_name}! Rất vui được gặp bạn. Bạn cần mình giúp gì không?"
                else:
                    result_text = "Bạn có thể nói rõ tên của bạn được không?"
                should_save = True
            else:
                # 4. Handle other actions normally (reuse existing context)
                result = self.actions.handle(intent, user_input, user_name, context)
                
                # 5. Handle ActionResult and extract text
                if isinstance(result, ActionResult):
                    if result.needs_slot:
                        # Set pending intent for slot filling (incomplete)
                        context.set_pending(result.intent)
                        should_save = False
                    else:
                        should_save = True
                    result_text = result.text
                else:
                    result_text = str(result)
                    should_save = True
        
        # 6. Speak result (always speak, even if incomplete)
        if result_text:
            if speak_callback:
                speak_callback(result_text)
            else:
                self.audio.speak(result_text)
        
        # 7. Save ONLY completed exchanges (atomic at the end)
        if should_save and self._memory_service and result_text:
            try:
                # Convert session_id to int if needed
                if isinstance(session_id, int):
                    session_id_int = session_id
                elif isinstance(session_id, str) and session_id.isdigit():
                    session_id_int = int(session_id)
                else:
                    session_id_int = None
                self._memory_service.save_exchange(user_name, user_input, result_text, session_id_int)
            except Exception as e:
                # Log error but don't fail the conversation
                print(f"[Warning] Failed to save exchange: {e}")
        
        return result_text or ""
    
    def should_exit(self, user_input: str) -> bool:
        """Check if user wants to exit."""
        exit_words = ["goodbye", "tạm biệt", "bye", "thôi"]
        return any(word in user_input.lower() for word in exit_words)
