"""
Habit Learning Service - Business Logic Layer

Chịu trách nhiệm học và cập nhật thói quen người dùng
"""

from datetime import datetime
from typing import Dict, Optional


class HabitLearningService:
    """Service for learning and updating habits"""
    
    def __init__(self, repository):
        self.repo = repository
        self.half_life_days = 7
    
    def _calculate_decayed_confidence(self, base_confidence: float, days_inactive: int) -> float:
        """Calculate confidence after temporal decay"""
        if days_inactive <= 0:
            return base_confidence
        decay_factor = 0.5 ** (days_inactive / self.half_life_days)
        return base_confidence * decay_factor
    
    def update_habit(self, user_id: int, habit_type: str, target: str,
                     time_bucket: int, day_type: str) -> None:
        """Update or create habit with temporal decay"""
        try:
            now = datetime.now()
            
            # Check if habit exists
            existing = self.repo.find_habit(user_id, habit_type, target, time_bucket, day_type)
            
            if existing:
                habit_id, old_freq, old_conf, last_seen = existing
                
                # Calculate days since last seen
                days_inactive = (now - last_seen).days if last_seen else 0
                
                # Apply temporal decay to confidence
                new_confidence = self._calculate_decayed_confidence(old_conf, days_inactive)
                
                # Update frequency and confidence
                new_freq = old_freq + 1
                new_confidence = min(0.95, new_confidence + 0.05)  # Cap at 95%
                
                self.repo.update_habit(habit_id, new_freq, new_confidence, now)
            else:
                # Create new habit
                self.repo.insert_habit(user_id, habit_type, target, time_bucket, day_type)
                
        except Exception:
            pass
    
    def learn_sequence(self, user_id: int, app_before: str, app_after: str,
                       time_between_seconds: int) -> None:
        """Learn app transition sequence"""
        try:
            now = datetime.now()
            
            # Check if sequence exists
            existing = self.repo.find_sequence(user_id, app_before, app_after)
            
            if existing:
                seq_id, old_freq, old_conf, old_avg_time, last_updated = existing
                
                # Apply temporal decay
                days_inactive = (now - last_updated).days if last_updated else 0
                new_confidence = self._calculate_decayed_confidence(old_conf, days_inactive)
                
                # Update frequency and confidence
                new_freq = old_freq + 1
                new_confidence = min(0.95, new_confidence + 0.05)
                
                # Update average time between
                new_avg_time = (old_avg_time * old_freq + time_between_seconds) // new_freq
                
                self.repo.update_sequence(seq_id, new_freq, new_confidence, new_avg_time, now)
            else:
                self.repo.insert_sequence(user_id, app_before, app_after, time_between_seconds)
                
        except Exception:
            pass
    
    def detect_and_save_workflow(self, user_id: int, app_chain: str,
                                  session_timeout_minutes: int = 30) -> bool:
        """Detect workflow pattern and save if meaningful"""
        try:
            apps = app_chain.split(',') if app_chain else []
            
            # Only consider as workflow if 3+ apps and session is active
            if len(apps) >= 3:
                workflow_name = ' → '.join(apps)
                
                # Check if workflow exists
                existing = self.repo.find_workflow(user_id, workflow_name)
                
                if existing:
                    wf_id, old_freq, old_conf, last_executed = existing
                    
                    # Apply temporal decay
                    days_inactive = (datetime.now() - last_executed).days if last_executed else 0
                    new_confidence = self._calculate_decayed_confidence(old_conf, days_inactive)
                    
                    # Update frequency and confidence
                    new_freq = old_freq + 1
                    new_confidence = min(0.95, new_confidence + 0.05)
                    
                    self.repo.update_workflow(wf_id, new_freq, new_confidence, datetime.now())
                else:
                    self.repo.insert_workflow(user_id, workflow_name, app_chain)
                
                return True
            
            return False
            
        except Exception:
            return False
