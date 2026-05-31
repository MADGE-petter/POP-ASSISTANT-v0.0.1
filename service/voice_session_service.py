"""Voice session service - quản lý trạng thái thoại, sleep và idle."""
import threading
import time
from typing import Callable, Optional

from controller.interfaces import IAudioService


class VoiceSessionService:
    def __init__(self, audio_service: IAudioService, idle_timeout_seconds: int = 40):
        self.audio_service = audio_service
        self.wake_detector = None
        self.wake_word_enabled = True
        self.is_waiting_for_wake = False
        self.is_sleeping = False
        self.idle_timeout_seconds = idle_timeout_seconds
        self.last_interaction_time = time.time()
        self.awaiting_user_response = False

        self.on_wake_up = None
        self.on_go_sleep = None

    def init_wake_detector(self, wake_detector):
        """Inject wake detector after creation."""
        self.wake_detector = wake_detector

    def start_wake_word_detection(self, wake_up_callback, on_wake_word_callback=None):
        """Start listening for wake word."""
        if not self.wake_word_enabled or not self.wake_detector:
            return False
        if self.wake_detector.is_listening:
            return True
        self.wake_detector.start_listening(
            callback=on_wake_word_callback,
            wake_up_callback=wake_up_callback,
        )
        return True

    def stop_wake_word_detection(self):
        """Stop wake word detection."""
        if self.wake_detector and self.wake_detector.is_listening:
            self.wake_detector.stop_listening()

    def handle_wake_up(self):
        """Handle wake word detected."""
        self.stop_wake_word_detection()
        self.is_sleeping = False
        self.is_waiting_for_wake = False
        self.last_interaction_time = time.time()

        time.sleep(0.5)

        if self.on_wake_up:
            self.on_wake_up()

    def go_to_sleep(self, manual: bool = False, speak_callback: Optional[Callable] = None):
        """Transition assistant to sleep mode."""
        print(f"[VoiceSessionService] Going to sleep (manual={manual})")
        self.is_sleeping = True
        self.is_waiting_for_wake = True
        self.awaiting_user_response = False

        if manual and speak_callback:
            speak_callback("Tôi sẽ nghỉ ngơi. Hãy gọi tôi khi cần nhé!")
            time.sleep(2)

        if self.on_go_sleep:
            self.on_go_sleep()

        if self.wake_word_enabled:
            self.start_wake_word_detection(wake_up_callback=self.handle_wake_up)

    def start_idle_monitor(self, on_idle_timeout: Callable[[], None]):
        """Start background idle monitor."""
        def check_idle():
            while True:
                time.sleep(5)
                if self.audio_service.is_speaking:
                    continue

                if not self.awaiting_user_response:
                    continue

                if not self.is_sleeping and not self.is_waiting_for_wake:
                    idle_time = time.time() - self.last_interaction_time
                    if idle_time > self.idle_timeout_seconds:
                        print(f"[VoiceSessionService] Idle timeout ({idle_time:.0f}s)")
                        if on_idle_timeout:
                            on_idle_timeout()
                        break

        threading.Thread(target=check_idle, daemon=True).start()

    def get_voice_input(self):
        """Get voice input from user."""
        self.audio_service.wait_until_speaking_done()
        self.last_interaction_time = time.time()
        self.awaiting_user_response = True
        time.sleep(0.3)

        result = self.audio_service.listen()
        if result:
            self.last_interaction_time = time.time()
            self.awaiting_user_response = False
        else:
            time.sleep(0.2)

        return result

    def speak(self, text: str, update_ui: bool = True):
        """Speak text through audio service."""
        self.awaiting_user_response = False
        return self.audio_service.speak(text, update_ui=update_ui)
