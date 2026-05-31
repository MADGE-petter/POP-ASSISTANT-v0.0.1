from datetime import date, timedelta
from service.interactive_alert_service import InteractiveAlertService


class DummyAudioService:
    def __init__(self):
        self.speak_calls = []

    def speak(self, text, update_ui=True):
        self.speak_calls.append((text, update_ui))
        return True


class DummyAlertManager:
    def __init__(self):
        self.handled = False

    def get_active_interactive_metrics(self):
        return ["ram"]

    def get_interactive_context(self, metric):
        return {}

    def handle_interactive_response(self, metric, response, context=None):
        self.handled = True


def test_try_handle_response_calls_alert_manager():
    audio = DummyAudioService()
    alert_manager = DummyAlertManager()
    service = InteractiveAlertService(audio, alert_manager=alert_manager)

    result = service.try_handle_response("có")

    assert result is True
    assert alert_manager.handled is True


def test_on_interactive_alert_speaks_expected_text():
    audio = DummyAudioService()
    service = InteractiveAlertService(audio)

    service.on_interactive_alert(type("A", (), {"message": "Test", "metric": "ram"})(), "ask_details")

    assert len(audio.speak_calls) == 1
    assert "Bạn có muốn xem tiến trình chi tiết không" in audio.speak_calls[0][0]


def test_parse_app_selection_handles_multiple_app_indices():
    from service.alert.interactive import InteractiveAlertHandler

    handler = InteractiveAlertHandler()
    context = {
        'top_processes': [
            {'pid': 1, 'name': 'App1'},
            {'pid': 2, 'name': 'App2'},
            {'pid': 3, 'name': 'App3'},
            {'pid': 4, 'name': 'App4'},
            {'pid': 5, 'name': 'App5'},
        ]
    }

    selected = handler._parse_app_selection('đóng app 1, app 2 và app 3', context)

    assert isinstance(selected, list)
    assert len(selected) == 3
    assert selected[0]['name'] == 'App1'
    assert selected[1]['name'] == 'App2'
    assert selected[2]['name'] == 'App3'

    selected_45 = handler._parse_app_selection('đóng app 4 và app 5', context)
    assert isinstance(selected_45, list)
    assert len(selected_45) == 2
    assert selected_45[0]['name'] == 'App4'
    assert selected_45[1]['name'] == 'App5'

    selected_mixed = handler._parse_app_selection('đóng app 1 và App5', context)
    assert isinstance(selected_mixed, list)
    assert len(selected_mixed) == 2
    assert selected_mixed[0]['name'] == 'App1'
    assert selected_mixed[1]['name'] == 'App5'


def test_suggest_based_on_habits_chooses_most_recent_same_count():
    from service.habit.habit_recommendation_service import HabitRecommendationService

    class DummyRepo:
        def get_recent_app_usage(self, user_id, days=7):
            return [
                ('Hoyo', 3, '2026-05-31 21:00:00'),
                ('Lien Minh', 3, '2026-05-30 21:00:00'),
            ]

    suggestion_service = HabitRecommendationService(DummyRepo(), None)
    suggestions = suggestion_service.suggest_based_on_habits(1)

    assert suggestions[0]['app'] == 'Hoyo'
    assert suggestions[1]['app'] == 'Lien Minh'


def test_suggest_based_on_habits_uses_plus_minus_scoring_with_max_three():
    from service.habit.habit_recommendation_service import HabitRecommendationService

    today = date.today()
    def formatted(day_offset):
        return (today + timedelta(days=day_offset)).strftime('%Y-%m-%d')

    class DummyRepo:
        def get_recent_app_usage_by_day(self, user_id, days=7):
            return [
                ('AppA', formatted(-6), 1, formatted(-6) + ' 08:00:00'),
                ('AppA', formatted(-5), 1, formatted(-5) + ' 08:00:00'),
                ('AppA', formatted(-4), 1, formatted(-4) + ' 08:00:00'),
                ('AppA', formatted(-3), 1, formatted(-3) + ' 08:00:00'),
                ('AppA', formatted(-2), 1, formatted(-2) + ' 08:00:00'),
                ('AppA', formatted(-1), 1, formatted(-1) + ' 08:00:00'),
                ('AppA', formatted(0), 1, formatted(0) + ' 08:00:00'),
                ('AppB', formatted(-6), 1, formatted(-6) + ' 07:00:00'),
                ('AppB', formatted(-5), 1, formatted(-5) + ' 07:00:00'),
                ('AppB', formatted(-4), 1, formatted(-4) + ' 07:00:00'),
                ('AppB', formatted(-3), 1, formatted(-3) + ' 07:00:00'),
                ('AppB', formatted(-2), 1, formatted(-2) + ' 07:00:00'),
                ('AppB', formatted(0), 1, formatted(0) + ' 07:00:00'),
            ]

    suggestion_service = HabitRecommendationService(DummyRepo(), None)
    suggestions = suggestion_service.suggest_based_on_habits(1)

    assert suggestions
    assert suggestions[0]['app'] == 'AppA'
    assert suggestions[0]['score'] == 3
    assert suggestions[0]['count'] == 7
    assert suggestions[1]['app'] == 'AppB'
    assert suggestions[1]['score'] > 0
