class PrBodyGenerator:
    """
    A class to generate a pull request body based on the provided prompt.
    """

    def __init__(self, prompt):
        """
        Initializes PrBodyGenerator with a prompt.

        Args:
            prompt (Prompt): The prompt to base the PR body on.
        """
        self.prompt = prompt
        self.body = ""

    def generate_body(self):
        """
        Generates the PR body based on the prompt text.
        """
        # Here, we use the prompt's text to set the PR body
        self.body = self.prompt.text
