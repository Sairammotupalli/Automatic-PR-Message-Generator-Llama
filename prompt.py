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
        prompt_text = "Generate a detailed pull request description based on the following information:\n\n"
        prompt_text += f"### PR Summary:\n{self.pr_summary}\n\n"
        prompt_text += "### Code Changes:\n"
        prompt_text += """  
Analyze the Pull Request details and assign a score between 0 and 100 for each category listed below. Ensure that scores are not biased towards high values. Consider all relevant information from the Pull Request and provide scores based on these factors. Output in the exact specified format:

### **Category 1: Impact Analysis**  
Evaluate the impact of the Pull Request on the overall codebase and provide a detailed breakdown of the following factors:  
- **Bug Fix**: [Explanation of how well it resolves existing issues or bugs]  
- **Usefulness**: [Explanation of how the changes add value to the project]  
- **New Functionality**: [Explanation of how the new features enhance the system]  
- **Maintainability**: [Explanation of how the changes affect the code’s maintainability and long-term stability]  
**Impact Score**: [Final score between 0-100 based on the above four factors]

---

### **Category 2: Code Quality**  
Assess the overall quality of the code in terms of readability, structure, and adherence to best practices:  
**Code Quality Score**: [Score between 0-100]

---

### **Category 3: Security**  
Identify any security vulnerabilities or risks introduced by the code, such as:  
- Hardcoded credentials  
- Unsafe serialization/deserialization  
- Command injection or shell execution  
- SQL injection  
- Other potential security flaws  
**Security Score**: [Score between 0-100]

---

### **Category 4: Creativity**  
Determine how original and innovative the code is. If the code appears to be copied from online sources without modification, assign a low score. If the code is unique and demonstrates creativity, assign a high score:  
**Creativity Score**: [Score between 0-100]  

---"""

        for file_change in self.diff_analysis:
            file_name = file_change.get("file", "Unknown file")
            prompt_text += f"  - {file_name}:\n"
            for change in file_change.get("changes", []):
                change_type = change.get("type", "Unknown")
                content = change.get("content", "")
                prompt_text += f"    {change_type.capitalize()}: {content}\n"

        return prompt_text
