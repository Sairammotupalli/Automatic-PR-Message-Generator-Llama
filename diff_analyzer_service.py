from diff_analysis import analyze_diff

class DiffAnalyzerService:
    """
    Service class for analyzing a diff file and categorizing changes into added, removed, and modified sections.
    """

    def __init__(self, diff_file):
        """
        Initializes the service with the path to a diff file.
        
        Args:
            diff_file (str): The path to the diff file to analyze.
        """
        self.diff_file = diff_file

    def analyse_diff(self):
        """
        Reads the diff file, analyzes the content, and returns structured change data.

        Returns:
            dict: A dictionary with categorized changes ('added', 'removed', and 'modified') for each file.
        """
        # Read the diff content from the file
        with open(self.diff_file, 'r') as file:
            diff_content = file.read()

        # Use analyze_diff function to process the diff content
        changes = analyze_diff(diff_content)
        
        return changes
