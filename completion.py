from prompt import Prompt
from uuid import uuid4
import logging
from enum import Enum
import requests
import os

class Completion:
    class State(Enum):
        UNCOMPLETE = "UNCOMPLETE"
        COMPLETED = "COMPLETED"

    def __init__(self, prompt: Prompt):
        self._id = f"hash(prompt)-{uuid4()}"
        self._prompt = prompt
        self._state = self.State.UNCOMPLETE
        self._result = ""
        self._llama_api_key = os.getenv("llama3_api")
        self._llama_api_url = "https://console.llamaapi.com/1485d848-26ca-4092-a7bd-7c9f36ae8308/credits"  # Example endpoint

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
            "Authorization": f"Bearer {self._llama_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.2",  # Llama model name
            "prompt": self._prompt.text,
            "max_tokens": 1024
        }
        response = requests.post(self._llama_api_url, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            return response_data.get("choices", [{}])[0].get("text", "")
        else:
            logging.error(f"Failed to complete prompt: {response_data}")
            return "Error: Unable to retrieve response from Llama API."

    def complete(self):
        logging.info(f"completion_{self.id} - Completing prompt...")
        logging.info(f"completion_{self.id} - prompt to complete: {self._prompt.text}")
        self._result = self._complete_prompt()
        self._state = self.State.COMPLETED if self._result else self.State.UNCOMPLETE
        logging.info(f"completion_{self.id} - completion result: {self._result}")
