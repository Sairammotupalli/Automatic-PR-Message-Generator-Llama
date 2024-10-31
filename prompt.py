class Prompt:
    """
    Class for creating and managing prompt text for PR description generation.
    """

    def __init__(self, diff_analysis, pr_summary):
        """
        Initializes the Prompt with diff analysis and PR summary details.

        Args:
            diff_analysis (dict): A dictionary with details about the code changes (added, removed, modified).
            pr_summary (str): A brief summary of the PR, including metadata like title and author.
        """
        self.diff_analysis = diff_analysis
        self.pr_summary = pr_summary
        self.text = self._create_prompt_text()

    def _create_prompt_text(self):
        """
        Constructs the prompt text based on the PR summary and diff analysis.

        Returns:
            str: The generated prompt text to be used for PR description generation.
        """
        prompt_text = "Generate a detailed pull request description based on the following information:\n\n"
        prompt_text += "### PR Summary:\n"
        prompt_text += f"{self.pr_summary}\n\n"
        prompt_text += "### Code Changes:\n"

        # Add added lines
        if self.diff_analysis.get("added"):
            prompt_text += "\n- **Added**:\n"
            for file_change in self.diff_analysis["added"]:
                prompt_text += f"  - {file_change['file']}:\n"
                for line in file_change["lines"]:
                    prompt_text += f"    - {line}\n"

        # Add removed lines
        if self.diff_analysis.get("removed"):
            prompt_text += "\n- **Removed**:\n"
            for file_change in self.diff_analysis["removed"]:
                prompt_text += f"  - {file_change['file']}:\n"
                for line in file_change["lines"]:
                    prompt_text += f"    - {line}\n"

        # Add modified lines
        if self.diff_analysis.get("modified"):
            prompt_text += "\n- **Modified**:\n"
            for file_change in self.diff_analysis["modified"]:
                prompt_text += f"  - {file_change['file']}:\n"
                prompt_text += "    - Added:\n"
                for line in file_change["added"]:
                    prompt_text += f"      - {line}\n"
                prompt_text += "    - Removed:\n"
                for line in file_change["removed"]:
                    prompt_text += f"      - {line}\n"

        return prompt_text

    def __str__(self):
        """
        Returns the full prompt text as a string.

        Returns:
            str: The complete prompt text.
        """
        return self.text
