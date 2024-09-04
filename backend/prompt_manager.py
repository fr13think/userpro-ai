import logging
from models.prompt import Prompt
from sqlalchemy.orm import Session
from sqlalchemy import func

class PromptManager:
    def __init__(self, db: Session):
        self.db = db
        logging.info("PromptManager initialized")

    def create_prompt(self, title: str, content: str, user_id: int, tags: list = None):
        prompt = Prompt(title=title, content=content, user_id=user_id, tags=tags)
        self.db.add(prompt)
        self.db.commit()
        self.db.refresh(prompt)
        logging.info(f"Created new prompt: {prompt.title}")
        return prompt

    def get_prompt(self, prompt_id: int):
        return self.db.query(Prompt).filter(Prompt.id == prompt_id).first()

    def update_prompt(self, prompt_id: int, title: str = None, content: str = None, tags: list = None):
        prompt = self.get_prompt(prompt_id)
        if prompt:
            if title:
                prompt.title = title
            if content:
                prompt.content = content
            if tags:
                prompt.tags = tags
            self.db.commit()
            logging.info(f"Updated prompt: {prompt.title}")
            return prompt
        return None

    def delete_prompt(self, prompt_id: int):
        prompt = self.get_prompt(prompt_id)
        if prompt:
            self.db.delete(prompt)
            self.db.commit()
            logging.info(f"Deleted prompt: {prompt.title}")
            return True
        return False

    def get_user_prompts(self, user_id: int):
        return self.db.query(Prompt).filter(Prompt.user_id == user_id).all()

    def search_prompts(self, query: str):
        return self.db.query(Prompt).filter(Prompt.title.ilike(f"%{query}%") | Prompt.content.ilike(f"%{query}%")).all()

    def get_popular_prompts(self, limit: int = 10):
        return self.db.query(Prompt).order_by(Prompt.usage_count.desc()).limit(limit).all()

    def get_prompts_by_tag(self, tag: str):
        return self.db.query(Prompt).filter(Prompt.tags.contains([tag])).all()

    def increment_prompt_usage(self, prompt_id: int):
        prompt = self.get_prompt(prompt_id)
        if prompt:
            prompt.usage_count += 1
            self.db.commit()
            logging.info(f"Incremented usage count for prompt: {prompt.title}")

    def get_prompt_statistics(self):
        total_prompts = self.db.query(func.count(Prompt.id)).scalar()
        avg_usage = self.db.query(func.avg(Prompt.usage_count)).scalar()
        most_used = self.db.query(Prompt).order_by(Prompt.usage_count.desc()).first()
        return {
            "total_prompts": total_prompts,
            "average_usage": avg_usage,
            "most_used_prompt": most_used.title if most_used else None
        }