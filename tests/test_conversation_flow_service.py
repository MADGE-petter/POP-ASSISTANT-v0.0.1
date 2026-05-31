import pytest

from service.conversation_flow_service import ConversationFlowService


class DummyAudioService:
    def __init__(self):
        self.is_speaking = False


class DummySqlService:
    def __init__(self):
        self.started = False
        self.ended = False
        self.session_id = 101

    def start_session(self, user_name):
        self.started = True
        return self.session_id

    def end_session(self, session_id=None):
        self.ended = True


class DummyActionHandler:
    pass


class DummyUserController:
    def __init__(self, name=None):
        self._name = name

    def get_display_name(self):
        return self._name


def test_start_and_end_session_call_sql_service():
    audio = DummyAudioService()
    sql = DummySqlService()
    actions = DummyActionHandler()
    user = DummyUserController("Lan")

    flow = ConversationFlowService(audio, sql, actions, user)
    flow.start_session()
    assert sql.started is True
    assert flow._session_id == sql.session_id

    flow.end_session()
    assert sql.ended is True
    assert flow._session_id is None


def test_run_first_interaction_speaks_greeting_for_known_user(monkeypatch):
    audio = DummyAudioService()
    sql = DummySqlService()
    actions = DummyActionHandler()
    user = DummyUserController("Lan")

    flow = ConversationFlowService(audio, sql, actions, user)
    flow._process_exchange = lambda user_input, speak_callback=None: ""

    spoken = []
    flow.run_first_interaction(lambda: None, speak_callback=lambda message: spoken.append(message), from_wake_up=True)

    assert len(spoken) == 1
    assert "Pop đây! Chào Lan" in spoken[0]


def test_run_main_loop_exits_when_bye(monkeypatch):
    audio = DummyAudioService()
    sql = DummySqlService()
    actions = DummyActionHandler()
    user = DummyUserController("Lan")

    flow = ConversationFlowService(audio, sql, actions, user)
    flow._process_exchange = lambda user_input: ""
    flow._should_exit = lambda user_input: user_input == "bye"

    inputs = iter(["bye"])

    def get_input():
        return next(inputs, "bye")

    monkeypatch.setattr("service.conversation_flow_service.time.sleep", lambda _: None)
    flow.run_main_loop(get_input, on_idle_callback=None, idle_timeout=60)
