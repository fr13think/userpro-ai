from collections import defaultdict
import logging
from datetime import datetime, timedelta

class AnalyticsEngine:
    def __init__(self):
        self.user_stats = defaultdict(lambda: {
            "total_conversations": 0,
            "total_messages": 0,
            "conversation_lengths": [],
            "daily_usage": defaultdict(int),
            "favorite_topics": defaultdict(int)
        })
        self.overall_stats = {
            "total_users": 0,
            "total_conversations": 0,
            "total_prompts": 0,
            "daily_active_users": defaultdict(int),
            "hourly_usage": defaultdict(int)
        }
        logging.info("Enhanced AnalyticsEngine initialized")

    def log_conversation(self, user_id, message_count, duration, topic):
        self.user_stats[user_id]["total_conversations"] += 1
        self.user_stats[user_id]["total_messages"] += message_count
        self.user_stats[user_id]["conversation_lengths"].append(duration)
        self.user_stats[user_id]["daily_usage"][datetime.now().date()] += 1
        self.user_stats[user_id]["favorite_topics"][topic] += 1

        self.overall_stats["total_conversations"] += 1
        self.overall_stats["daily_active_users"][datetime.now().date()] += 1
        self.overall_stats["hourly_usage"][datetime.now().hour] += 1

        logging.info(f"Logged conversation for user {user_id}: {message_count} messages, {duration} seconds, topic: {topic}")

    def get_user_stats(self, user_id):
        stats = self.user_stats[user_id]
        avg_messages = stats["total_messages"] / stats["total_conversations"] if stats["total_conversations"] > 0 else 0
        avg_duration = sum(stats["conversation_lengths"]) / len(stats["conversation_lengths"]) if stats["conversation_lengths"] else 0
        
        return {
            "total_conversations": stats["total_conversations"],
            "avg_messages_per_conversation": avg_messages,
            "avg_conversation_duration": avg_duration,
            "daily_usage": dict(stats["daily_usage"]),
            "favorite_topics": dict(sorted(stats["favorite_topics"].items(), key=lambda x: x[1], reverse=True)[:5])
        }

    def get_overall_stats(self):
        self.overall_stats["total_users"] = len(self.user_stats)
        
        # Calculate daily active users for the last 30 days
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        dau = {date: count for date, count in self.overall_stats["daily_active_users"].items() if date >= thirty_days_ago}
        
        return {
            "total_users": self.overall_stats["total_users"],
            "total_conversations": self.overall_stats["total_conversations"],
            "total_prompts": self.overall_stats["total_prompts"],
            "daily_active_users": dict(sorted(dau.items())),
            "hourly_usage": dict(sorted(self.overall_stats["hourly_usage"].items()))
        }

    def get_user_engagement_score(self, user_id):
        stats = self.user_stats[user_id]
        total_conversations = stats["total_conversations"]
        avg_messages = stats["total_messages"] / total_conversations if total_conversations > 0 else 0
        recent_activity = sum(count for date, count in stats["daily_usage"].items() if date >= datetime.now().date() - timedelta(days=7))
        
        # Simple engagement score calculation
        engagement_score = (total_conversations * 0.5) + (avg_messages * 0.3) + (recent_activity * 0.2)
        return min(engagement_score, 100)  # Cap the score at 100

    def get_trending_topics(self, n=5):
        all_topics = defaultdict(int)
        for user_stats in self.user_stats.values():
            for topic, count in user_stats["favorite_topics"].items():
                all_topics[topic] += count
        return dict(sorted(all_topics.items(), key=lambda x: x[1], reverse=True)[:n])