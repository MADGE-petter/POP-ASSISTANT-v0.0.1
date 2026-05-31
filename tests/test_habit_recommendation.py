"""Simple script to test habit recommendation logic with sample usage data."""
import sys
from datetime import datetime, timedelta
from pathlib import Path

workspace_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(workspace_root))

from database.habit_repository import HabitRepository
from model.usage_tracker import UsageTracker
from service.habit.habit_recommendation_service import HabitRecommendationService


def create_sample_usage(repo: HabitRepository, user_id: int):
    """Insert sample app usage logs for habit recommendation testing."""
    now = datetime.now()
    sample_data = [
        ('edge', now - timedelta(days=6, hours=1)),
        ('hoyo', now - timedelta(days=5, hours=1)),
        ('edge', now - timedelta(days=4, hours=1)),
        ('edge', now - timedelta(days=3, hours=1)),
        ('edge', now - timedelta(days=2, hours=1)),
        ('edge', now - timedelta(days=1, hours=1)),
        ('edge', now),
        ('vscode', now - timedelta(days=6, hours=2)),
        ('vscode', now - timedelta(days=5, hours=2)),
        ('git', now - timedelta(days=4, hours=2)),
        ('vscode', now - timedelta(days=3, hours=2)),
        ('vscode', now - timedelta(days=2, hours=2)),
        ('vscode', now),
        ('AppC', now - timedelta(days=1, hours=3)),
    ]

    for app_name, timestamp in sample_data:
        repo.insert_app_usage_log(user_id, app_name, timestamp)


def print_suggestions(service: HabitRecommendationService, user_id: int):
    suggestions = service.suggest_based_on_habits(user_id)
    if not suggestions:
        print('No habit suggestions found. Hãy kiểm tra dữ liệu app_usage_logs.')
        return

    print('Habit recommendations:')
    for idx, suggestion in enumerate(suggestions, start=1):
        print(f"{idx}. app={suggestion['app']}")
        print(f"   score={suggestion['score']}, confidence={suggestion['confidence']:.2f}")
        print(f"   count={suggestion['count']}, last_opened={suggestion['last_opened']}")
        print(f"   message={suggestion['message']}")


if __name__ == '__main__':
    workspace_root = Path(__file__).resolve().parent.parent
    db_path = workspace_root / 'database' / 'conversations.db'

    print(f'Using database: {db_path}')

    tracker = UsageTracker(str(db_path))
    tracker._init_db()

    repo = HabitRepository(str(db_path))
    user_id = 1

    print('Creating sample app usage logs for user_id=1...')
    create_sample_usage(repo, user_id)

    recommendation_service = HabitRecommendationService(repo, None)
    print_suggestions(recommendation_service, user_id)
