class Prompt:
    def __init__(self, diff_analysis, pr_summary):
        """
        Initializes the prompt with diff analysis and PR summary.
        """
        self.diff_analysis = diff_analysis  # Expecting this to be a list of dictionaries
        self.pr_summary = pr_summary
        self.text = self._create_prompt_text()

    def _create_prompt_text(self):
        """
        Create the prompt text based on the diff analysis.
        """
        prompt_text = f"Generate a detailed pull request description based on the following information:\n\n"
        prompt_text += f"### PR Summary:\n{self.pr_summary}\n\n"
        prompt_text += f"### Code Changes:\n"

        # Iterate through each file change in the diff analysis
        for file_change in self.diff_analysis:
            file_name = file_change["file"]  # Access the file name
            prompt_text += f"  - {file_name}:\n"
            for change in file_change["changes"]:
                change_type = change["type"]
                content = change["content"]
                prompt_text += f"    {change_type.capitalize()}: {content}\n"

        return prompt_text
