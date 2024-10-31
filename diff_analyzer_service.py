class DiffAnalyzerService:
    def __init__(self, diff_content):
        self.diff_content = diff_content

    def analyse_diff(self):
        analysis = []
        current_file = None

        for line in self.diff_content.splitlines():
            if line.startswith('diff --git'):
                if current_file:
                    analysis.append(current_file)
                file_path = line.split()[-1]
                current_file = {"file": file_path, "changes": []}
            elif line.startswith('+') and not line.startswith('+++'):
                current_file["changes"].append({"type": "addition", "content": line[1:].strip()})
            elif line.startswith('-') and not line.startswith('---'):
                current_file["changes"].append({"type": "deletion", "content": line[1:].strip()})

        if current_file:
            analysis.append(current_file)

        return analysis
