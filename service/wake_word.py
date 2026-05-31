"""Wake Word Detection module - Phát hiện từ khóa kích hoạt."""
import threading
import time

import speech_recognition as sr


class WakeWordDetector:

    DEFAULT_WAKE_WORDS = [
        "pop", "pop ơi", "alo", "hey pop","Alo"
        "bốp", "bốp ơi", "bot", "bot ơi",
        "hello pop", "chào pop", "xin chào pop"
    ]

    def __init__(self, audio_service, view=None, wake_words=None, sensitivity=0.7):
        self.audio_service = audio_service
        self.view = view
        self.wake_words = wake_words or self.DEFAULT_WAKE_WORDS.copy()
        self.sensitivity = sensitivity
        
        self.is_listening = False
        self.wake_detected = False
        self.listen_thread = None
        self.stop_event = threading.Event()
        
    def set_wake_words(self, wake_words):
        """Cập nhật danh sách wake words."""
        self.wake_words = [w.lower().strip() for w in wake_words]
        
    def add_wake_word(self, wake_word):
        """Thêm wake word mới."""
        wake_word = wake_word.lower().strip()
        if wake_word not in self.wake_words:
            self.wake_words.append(wake_word)
            
    def remove_wake_word(self, wake_word):
        """Xóa wake word."""
        wake_word = wake_word.lower().strip()
        if wake_word in self.wake_words:
            self.wake_words.remove(wake_word)
    
    def start_listening(self, callback=None, wake_up_callback=None):
        if self.is_listening:
            return
            
        self.is_listening = True
        self.wake_detected = False
        self.stop_event.clear()
        self._wake_up_callback = wake_up_callback
        
        self.listen_thread = threading.Thread(
            target=self._listen_loop,
            args=(callback, wake_up_callback),
            daemon=True
        )
        self.listen_thread.start()
        
    def stop_listening(self):
       
        self.stop_event.set()
        self.is_listening = False
        
    def _listen_loop(self, callback, wake_up_callback):
        while self.is_listening and not self.stop_event.is_set():
            try:
                text = self._listen_short(timeout=2.0)
                if not text or text == "...":
                    continue
                print(f"[WakeWord] '{text}'")
                text_lower = text.lower().strip()
                
                # Kiểm tra wake word
                if self._check_wake_word(text_lower):
                    self.wake_detected = True
                    
                    # Đánh thức app (hiện UI) trước - QUAN TRỌNG
                    if wake_up_callback:
                        try:
                            wake_up_callback()
                        except Exception as e:
                            import traceback
                            traceback.print_exc()
                    
                    # Cập nhật UI
                    if self.view:
                        try:
                            self.view.update_user_text(f"{text}")
                        except Exception as e:
                            print(f"[WakeWord] ✗ Error updating UI: {e}")
                    
                    # Gọi callback xử lý (optional)
                    if callback:
                        try:
                            callback(text)
                        except Exception as e:
                            print(f"[WakeWord] ✗ Error in callback: {e}")
                    
                    # Reset sau khi phát hiện
                    self.wake_detected = False
                    
                    # Nghỉ ngắn trước khi lắng nghe tiếp
                    time.sleep(1.0)
                    
            except Exception as e:
                print(f"[WakeWord] ✗ Error in listen_loop: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(0.5)
        
        # Vòng lặp kết thúc
        print(f"[WakeWord] Listen loop ended. is_listening={self.is_listening}, stop_event={self.stop_event.is_set()}")
        
    def _listen_short(self, timeout=2.0):
        """Lắng nghe ngắn - dùng AudioService để tránh xung đột microphone"""
        try:
            # Ưu tiên dùng AudioService nếu có để tránh xung đột lock
            if self.audio_service and hasattr(self.audio_service, 'listen'):
                # AudioService.listen đã xử lý gate_lock và cooldown
                text = self.audio_service.listen(timeout=timeout, phrase_time_limit=3)
                return text
            r = sr.Recognizer()
            r.pause_threshold = 0.5
            r.energy_threshold = 350
            r.dynamic_energy_threshold = True
            
            with sr.Microphone() as source:
                try:
                    audio = r.listen(source, timeout=timeout, phrase_time_limit=3)
                except sr.WaitTimeoutError:
                    return None
                    
            # Thử nhận diện
            try:
                text = r.recognize_google(audio, language="vi-VN")
                return text
            except sr.UnknownValueError:
                # Thử tiếng Anh
                try:
                    text = r.recognize_google(audio, language="en-US")
                    return text
                except:
                    return None
            except sr.RequestError:
                return None
                
        except Exception as e:
            return None 
    def _check_wake_word(self, text):
        for wake_word in self.wake_words:
            if wake_word in text:
                print(f"[WakeWord] Detected '{wake_word}' in '{text}'")
                return True
        return False
    def is_wake_detected(self):
        return self.wake_detected
    def reset(self):
        self.wake_detected = False
