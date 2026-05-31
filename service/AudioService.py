import os
import threading
import time

# Try to import audio libraries
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
try:
    import gtts
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
try:
    import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False
class AudioService: 
    def __init__(self, view=None):
        
        self.view = view
        self.assistant_name = "Pop"
        
        # "Cửa một chiều": Lock đảm bảo chỉ 1 hướng hoạt động
        self.gate_lock = threading.Lock()
        self.is_speaking = False  # Loa đang mở?
        self.is_listening = False  # Mic đang mở?
        
        # Cooldown sau khi nói (giảm nghe chéo)
        self.post_speak_cooldown = 0.3  # 0.3s cooldown
        self.last_speak_end_time = 0
        
    def speak(self, text, update_ui=True):
        threading.Thread(
            target=self._speak_worker,
            args=(text, update_ui),
            daemon=True
        ).start()
        return True
    
    def _speak_worker(self, text, update_ui):

        self.gate_lock.acquire()
        self.is_speaking = True
        
        try:
            if update_ui and self.view:
                self.view.update_bot_text(text)
            
            print(f"[BOT] {text}")
            
            if GTTS_AVAILABLE and PLAYSOUND_AVAILABLE:
                tts = gtts.gTTS(text=text, lang="vi", slow=False)
                tts.save("sound.mp3")
                playsound.playsound("sound.mp3", True)
                if os.path.exists("sound.mp3"):
                    os.remove("sound.mp3")
            else:
                time.sleep(1)
            
            time.sleep(0.3)  # Cooldown nhẹ
            
        finally:
            self.is_speaking = False
            self.last_speak_end_time = time.time()
            self._mic_warmup()
            self.gate_lock.release()
    
    def _mic_warmup(self):
        time.sleep(0.1)  
    
    def listen(self, timeout=12, phrase_time_limit=10):
        if self.is_listening:
            return None
        
        # Kiểm tra cooldown sau khi bot nói
        time_since_speak = time.time() - self.last_speak_end_time
        if time_since_speak < self.post_speak_cooldown:
            return None
        got_lock = self.gate_lock.acquire(timeout=0.5)
        
        if not got_lock:
            return None
        
        try:
            self.is_listening = True
            
            if not SR_AVAILABLE:
                return "..."
            
            # Update UI
            if self.view:
                self.view.update_user_text("Đang lắng nghe...")
            
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.pause_threshold = 0.8
                    r.energy_threshold = 300
                    audio = r.listen(source, phrase_time_limit=phrase_time_limit, timeout=timeout)
                
                # Nhận diện
                try:
                    text = r.recognize_google(audio, language="vi-VN")
                except sr.UnknownValueError:
                    try:
                        text = r.recognize_google(audio, language="en-US")
                    except:
                        text = None
                
                # Update UI
                if self.view and text:
                    self.view.update_user_text(text)
                    
                print(f"[USER] {text}")
                
                return text
                
            except sr.UnknownValueError:
                if self.view:
                    self.view.update_user_text("Pop không nghe rõ...")
                return "..."
            except sr.RequestError as e:
                return "..."
            except Exception as e:
                return "..."
                
        finally:
            self.is_listening = False
            self.gate_lock.release()
    
    def get_text_with_retry(self, max_retries=3, retry_message=None):
        """Lấy text với cơ chế retry."""
        if retry_message is None:
            retry_message = f"{self.assistant_name} không nghe rõ, bạn có thể nói lại không?"
        
        for i in range(max_retries):
            text = self.listen()
            if text and text != "..." and text != 0:
                return text.lower()
            elif i < max_retries - 1:
                self.speak(retry_message)
        
        self.speak("Tôi không nghe rõ. Tôi sẽ hỏi lại sau.")
        return "..."
    
    def wait_until_speaking_done(self):
        while self.is_speaking:
            time.sleep(0.05)

    def is_gate_open(self):
        return not self.is_speaking
