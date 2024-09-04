import groq
import logging

class GroqClient:
    def __init__(self, api_key):
        self.client = groq.Client(api_key=api_key)
        logging.info("GROQ client initialized")

    def execute_query(self, query):
        try:
            result = self.client.query(query)
            logging.info(f"Executed GROQ query: {query[:50]}...")
            return result
        except Exception as e:
            logging.error(f"Error executing GROQ query: {str(e)}")
            raise