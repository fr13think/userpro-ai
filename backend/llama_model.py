from llama_cpp import Llama
import logging

class LlamaModel:
    def __init__(self, model_path):
        try:
            self.model = Llama(model_path=model_path)
            logging.info(f"LLaMA model initialized from {model_path}")
        except Exception as e:
            logging.error(f"Failed to initialize LLaMA model: {str(e)}")
            raise

    def generate_response(self, prompt, max_tokens=100):
        try:
            response = self.model.generate(prompt, max_tokens=max_tokens)
            logging.info(f"Generated response for prompt: {prompt[:50]}...")
            return response
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            raise