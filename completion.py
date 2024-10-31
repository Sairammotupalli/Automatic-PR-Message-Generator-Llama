from prompt import Prompt
from uuid import uuid4
import logging
from enum import Enum
import os
import requests

class Completion:
    class State(Enum):
        UNCOMPLETE = "UNCOMPLETE"
        COMPLETED = "COMPLETED"

    def __init__(self, prompt: Prompt):
        self._id = f"hash(prompt)-{uuid4()}"
        self._prompt = prompt
        self._state = self.State.UNCOMPLETE
        self._result = ""
        self.api_key = os.getenv("LLAMA_API_KEY")  # Meta Llama API key from environment variables
        self.api_url = os.getenv("LLAMA_API_URL")  # Meta Llama API endpoint from environment variables

    @property
    def id(self):
        return self._id

    @property
    def result(self):
        return self._result

    @property
    def state(self):
        return self._state

    def _complete_prompt(self) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "prompt": self._prompt.text,
            "max_tokens": 1024,     # Adjust based on the desired length of the completion
            "temperature": 0.7,     # Adjust for response randomness (0 is deterministic, higher is more random)
        }

        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()  # Raises an error if the request fails

        # Assuming the response structure matches OpenAI's API format
        return response.json()["choices"][0]["text"]

    def complete(self):
        logging.info(f"completion_{self.id} - Completing prompt...")
        logging.info(f"completion_{self.id} - prompt to complete: {self._prompt}")
        self._result = self._complete_prompt()
        self._state = self.State.COMPLETED
        logging.info(f"completion_{self.id} - Complete")
        logging.info(f"completion_{self.id} - Result: {self.result}")

    def __eq__(self, completion: "Completion"):
        return self._id == completion._id

    def __repr__(self):
        return f"{self.id} - {self.state} - result: {self.result}"
