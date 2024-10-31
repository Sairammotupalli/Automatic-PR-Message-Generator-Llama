class DiffAnalyzerService:
    """
    Service to analyze the diff content and produce a structured analysis.
    """

    def __init__(self, diff_content):
        """
        Initializes the diff analyzer with diff content.

        Args:
            diff_content (str): The string content of the diff.
        """
        self.diff_content = diff_content

    def analyse_diff(self):
        """
        Analyzes the diff content and returns a structured summary.

        Returns:
            list: A list of dictionaries containing analyzed diff data for each file.
        """
        analysis = []
        current_file = None

        # Split the diff content into lines and parse each line
        for line in self.diff_content.splitlines():
            if line.startswith('diff --git'):
                # New file change block detected
                if current_file:
                    analysis.append(current_file)
                file_path = line.split()[-1]  # Get the file path (e.g., b/test_file.py)
                current_file = {"file": file_path, "changes": []}
            elif line.startswith('+') and not line.startswith('+++'):
                # Line added
                current_file["changes"].append({"type": "addition", "content": line[1:].strip()})
            elif line.startswith('-') and not line.startswith('---'):
                # Line removed
                current_file["changes"].append({"type": "deletion", "content": line[1:].strip()})

        # Add the last file's changes if any
        if current_file:
            analysis.append(current_file)

        return analysis
