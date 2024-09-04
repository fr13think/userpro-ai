import time
import logging
from models.conversation import Conversation

class ConversationEngine:
    def __init__(self, llama_model, groq_client):
        self.llama_model = llama_model
        self.groq_client = groq_client
        self.conversation_history = []
        self.start_time = None
        logging.info("ConversationEngine initialized")

    def start_conversation(self):
        self.start_time = time.time()
        self.conversation_history = []
        logging.info("New conversation started")

    def process_message(self, user_message):
        if self.start_time is None:
            self.start_conversation()

        elapsed_time = time.time() - self.start_time
        if elapsed_time > 300:  # 5 minutes in seconds
            logging.info("Conversation time limit reached")
            return "Conversation time limit reached. Would you like to start a new conversation?"

        self.conversation_history.append(f"User: {user_message}")
        
        try:
            groq_query = f"Generate response for: {user_message}"
            groq_result = self.groq_client.execute_query(groq_query)
            
            llama_prompt = f"{groq_result}\nAI:"
            response = self.llama_model.generate_response(llama_prompt)
            
            self.conversation_history.append(f"AI: {response}")
            logging.info(f"Processed message: {user_message[:50]}...")
            return response
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")
            return f"An error occurred: {str(e)}"

    def get_conversation_topic(self):
        # This is a simplified method to get the conversation topic
        # In a real-world scenario, you might want to use more sophisticated NLP techniques
        all_text = " ".join(self.conversation_history)
        words = all_text.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 3:  # ignore short words
                word_freq[word] = word_freq.get(word, 0) + 1
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[0][0] if sorted_words else "General"