"""Voice Controller - Quản lý voice, wake word và sleep mode."""

from typing import Callable, Optional

from controller.interfaces import IAudioService
from service.voice_session_service import VoiceSessionService


class VoiceController:
    def __init__(self, audio_service: IAudioService, view=None):
        self.audio_service = audio_service
        self.view = view
        self.session_service = VoiceSessionService(audio_service)

        self.session_service.on_wake_up = None
        self.session_service.on_go_sleep = None

    def init_wake_detector(self, wake_detector):
        """Inject wake detector sau khi tạo."""
        self.session_service.init_wake_detector(wake_detector)

    def start_wake_word_detection(self, wake_up_callback, on_wake_word_callback=None):
        """Bắt đầu lắng nghe wake word."""
        return self.session_service.start_wake_word_detection(
            wake_up_callback=wake_up_callback,
            on_wake_word_callback=on_wake_word_callback,
        )

    def stop_wake_word_detection(self):
        """Dừng lắng nghe wake word."""
        self.session_service.stop_wake_word_detection()

    def handle_wake_up(self):
        """Xử lý wake up."""
        self.session_service.handle_wake_up()

    def go_to_sleep(self, manual=False, speak_callback=None):
        """Chuyển sang sleep mode."""
        self.session_service.go_to_sleep(manual=manual, speak_callback=speak_callback)

    def start_idle_monitor(self, on_idle_timeout):
        """Bắt đầu monitor idle time."""
        self.session_service.start_idle_monitor(on_idle_timeout)

    def get_voice_input(self):
        """Lấy input từ voice."""
        return self.session_service.get_voice_input()

    def speak(self, text, update_ui=True):
        """Bot nói."""
        return self.session_service.speak(text, update_ui=update_ui)

    @property
    def is_sleeping(self):
        return self.session_service.is_sleeping

    @property
    def on_wake_up(self):
        return self.session_service.on_wake_up

    @on_wake_up.setter
    def on_wake_up(self, callback):
        self.session_service.on_wake_up = callback

    @property
    def on_go_sleep(self):
        return self.session_service.on_go_sleep

    @on_go_sleep.setter
    def on_go_sleep(self, callback):
        self.session_service.on_go_sleep = callback
