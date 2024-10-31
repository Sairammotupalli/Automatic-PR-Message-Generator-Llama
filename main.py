import os
import sys
from diff_analyzer_service import DiffAnalyzerService
from pr_body_generator import PrBodyGenerator
from prompt import Prompt

def main(diff_content, pr_number):
    """
    Main function to generate a pull request description based on diff content.
    """
    print("Received diff content:", diff_content)  # Debugging output
    print("PR Number:", pr_number)  # Debugging output

    # Step 1: Analyze the diff content
    diff_analyzer = DiffAnalyzerService(diff_content=diff_content)  # Pass content directly
    diff_analysis = diff_analyzer.analyse_diff()

    # Step 2: Create a prompt and generate the PR body
    prompt = Prompt(diff_analysis=diff_analysis, pr_summary=f"PR #{pr_number}")
    pr_body_generator = PrBodyGenerator(prompt=prompt)
    pr_body_generator.generate_body()

    # Step 3: Output the PR body
    print(pr_body_generator.body)  # Output directly for GitHub Actions to capture

if __name__ == "__main__":
    diff_content = sys.argv[1]  # Take diff content as first argument
    pr_number = sys.argv[2]     # Take PR number as second argument
    main(diff_content, pr_number)
