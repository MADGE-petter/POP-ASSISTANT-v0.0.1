"""Conversation flow service - xử lý luồng hội thoại và idle timeout."""
import time
from typing import Callable, Optional

from controller.interfaces import (
    IActionHandler,
    IAudioService,
    ISqlService,
    IUserController,
)
from service.conversation_service import ConversationService
from service.interactive_alert_service import InteractiveAlertService
from service.memory_service import MemoryService


class ConversationFlowService:
    def __init__(
        self,
        audio_service: IAudioService,
        sql_service: ISqlService,
        action_handler: IActionHandler,
        user_controller: IUserController,
        interactive_alert_service: Optional[InteractiveAlertService] = None,
    ):
        self.audio = audio_service
        self.sql = sql_service
        self.actions = action_handler
        self.user = user_controller
        self.interactive_alert_service = interactive_alert_service

        self._assistant_active = False
        self._session_id: Optional[int] = None
        self._last_input: Optional[str] = None

        self._conversation_service = None
        self._memory_service = None
        self._first_greeting_done = False

    def init_intent_service(self):
        if self._conversation_service:
            self._conversation_service.init_intent_service()

    def start_session(self) -> None:
        user_name = self.user.get_display_name() or "guest"
        self._session_id = self.sql.start_session(user_name)
        print(f"[ConversationFlowService] Session started: {self._session_id}")

    def end_session(self) -> None:
        if self._session_id:
            self.sql.end_session(self._session_id)
            print(f"[ConversationFlowService] Session ended: {self._session_id}")
            self._session_id = None

    def run_main_loop(
        self,
        get_input_callback: Callable[[], Optional[str]],
        on_idle_callback: Optional[Callable] = None,
        idle_timeout: int = 15,
    ) -> None:
        print("[ConversationFlowService] Main loop starting...")
        self._assistant_active = True
        last_interaction = time.time()

        try:
            while self._assistant_active:
                if getattr(self.audio, "is_speaking", False):
                    last_interaction = time.time()
                    time.sleep(0.1)
                    continue

                idle_time = time.time() - last_interaction
                if idle_time > idle_timeout:
                    if on_idle_callback:
                        on_idle_callback()
                    break

                user_input = get_input_callback()

                if not user_input or user_input in ["...", "", None, 0]:
                    time.sleep(1)
                    continue

                if user_input == self._last_input:
                    time.sleep(1)
                    continue

                self._last_input = user_input
                last_interaction = time.time()

                if self._should_exit(user_input):
                    self._assistant_active = False
                    break

                self._process_exchange(user_input)

        except Exception as e:
            print(f"[ConversationFlowService] Error in main loop: {e}")
            import traceback

            traceback.print_exc()

    def run_first_interaction(
        self,
        get_input_callback: Callable[[], Optional[str]],
        speak_callback: Optional[Callable] = None,
        from_wake_up: bool = False,
    ) -> None:
        user_name = self.user.get_display_name()

        if user_name == "bạn" or not user_name:
            greeting = "Chào bạn! Tôi là Pop. Bạn có thể cho tôi biết tên của bạn được không?"
            if speak_callback:
                speak_callback(greeting)
            else:
                self.audio.speak(greeting)

            user_input = get_input_callback()
            if user_input and user_input not in ["...", "", None, 0]:
                self._process_exchange(user_input, speak_callback)
        else:
            if not self._first_greeting_done or from_wake_up:
                if from_wake_up:
                    greeting = f"Pop đây! Chào {user_name}, bạn cần giúp gì?"
                else:
                    greeting = f"Chào {user_name}! Rất vui được gặp lại bạn. Bạn cần mình giúp gì?"
                if speak_callback:
                    speak_callback(greeting)
                else:
                    self.audio.speak(greeting)
                self._first_greeting_done = True

    def stop(self) -> None:
        self._assistant_active = False

    def set_assistant_active(self, active: bool) -> None:
        self._assistant_active = active

    def _get_conversation_service(self):
        if self._conversation_service is None:
            self._conversation_service = ConversationService(
                self.audio,
                self.user,
                self.actions,
            )
            if self._memory_service is None:
                self._memory_service = MemoryService(self.sql)
            self._conversation_service.init_memory_service(self._memory_service)
        return self._conversation_service

    def _process_exchange(
        self,
        user_input: str,
        speak_callback: Optional[Callable] = None,
    ) -> str:
        if self._is_interactive_response(user_input):
            return ""

        service = self._get_conversation_service()
        user_name = self.user.get_display_name() or "guest"
        session_id = self._session_id if self._session_id else 1
        return service.process_exchange(user_input, speak_callback, user_name, session_id)

    def _is_interactive_response(self, user_input: str) -> bool:
        if not self.interactive_alert_service:
            return False

        return self.interactive_alert_service.try_handle_response(user_input)

    def _should_exit(self, user_input: str) -> bool:
        service = self._get_conversation_service()
        return service.should_exit(user_input)
