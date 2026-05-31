import threading

import pytest

from service.voice_session_service import VoiceSessionService


class DummyAudioService:
    def __init__(self, listen_result=None, speaking=False):
        self.listen_result = listen_result
        self.is_speaking = speaking
        self.wait_called = False
        self.listen_called = False
        self.speak_calls = []

    def wait_until_speaking_done(self):
        self.wait_called = True

    def listen(self, timeout=12, phrase_time_limit=10):
        self.listen_called = True
        return self.listen_result

    def speak(self, text, update_ui=True):
        self.speak_calls.append((text, update_ui))
        return True


def test_get_voice_input_sets_waiting_state_and_returns_result():
    audio = DummyAudioService(listen_result="xin chào")
    service = VoiceSessionService(audio)

    result = service.get_voice_input()

    assert result == "xin chào"
    assert audio.wait_called is True
    assert audio.listen_called is True
    assert service.awaiting_user_response is False


def test_speak_resets_awaiting_user_response():
    audio = DummyAudioService()
    service = VoiceSessionService(audio)
    service.awaiting_user_response = True

    result = service.speak("Hello", update_ui=False)

    assert result is True
    assert service.awaiting_user_response is False
    assert audio.speak_calls == [("Hello", False)]


def test_go_to_sleep_sets_flags_and_triggers_on_go_sleep():
    audio = DummyAudioService()
    service = VoiceSessionService(audio)
    called = []

    service.on_go_sleep = lambda: called.append("sleep")
    service.go_to_sleep(manual=False)

    assert service.is_sleeping is True
    assert service.is_waiting_for_wake is True
    assert service.awaiting_user_response is False
    assert called == ["sleep"]


def test_start_idle_monitor_triggers_callback(monkeypatch):
    audio = DummyAudioService()
    service = VoiceSessionService(audio, idle_timeout_seconds=0)
    service.awaiting_user_response = True
    service.last_interaction_time = 0

    event = threading.Event()

    def idle_callback():
        event.set()

    monkeypatch.setattr("service.voice_session_service.time.sleep", lambda _: None)
    service.start_idle_monitor(idle_callback)

    assert event.wait(timeout=1)
