from prompt import Prompt
from completion import Completion
import inspect
import logging

class PrBodyGenerator:
    MAX_SUMMARY_DEPTH = 5
    PR_BODY_PROMPT = Prompt(
        inspect.cleandoc(
            """ 
            Format the following text into a Pull Request Body with the following sections: 
             - Summary 
             - List of changes 
             - Refactoring Target
             Remove duplicate information.

            Text to format: 
            """
        )
    )

    def __init__(self, diff_analysis: str):
        self.body = diff_analysis

    def generate_body(self):
        logging.info("Initial body")
        logging.info(self.body)

        body_formatting_prompt = self.PR_BODY_PROMPT.concat(
            Prompt(self.body).wrap("###")
        )
        # Summarize body if needed
        if not body_formatting_prompt.is_valid:
            self.body = str(self.summarize(Prompt(self.body)))
            logging.info("Summarized body")
            logging.info(self.body)

        completion = Completion(body_formatting_prompt)
        self.body = completion.complete()

    def summarize(self, prompt: Prompt) -> str:
        # Creates a completion for the summary if summarization is needed
        completion = Completion(prompt)
        return completion.complete() if completion else "Error: Unable to summarize."
