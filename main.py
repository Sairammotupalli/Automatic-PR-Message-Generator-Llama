import os
import sys
from diff_analyzer_service import DiffAnalyzerService
from pr_body_generator import PrBodyGenerator
from prompt import Prompt

def main(diff_file_path, pr_number):
    """
    Main function to generate a pull request description based on diff content file.
    """
    # Step 1: Read diff content from file
    with open(diff_file_path, 'r') as file:
        diff_content = file.read()

    print("Received diff content:", diff_content)  # Debugging output
    print("PR Number:", pr_number)  # Debugging output

    # Step 2: Analyze the diff content
    diff_analyzer = DiffAnalyzerService(diff_content=diff_content)
    diff_analysis = diff_analyzer.analyse_diff()

    # Step 3: Create a prompt and generate the PR body
    prompt = Prompt(diff_analysis=diff_analysis, pr_summary=f"PR #{pr_number}")
    pr_body_generator = PrBodyGenerator(prompt=prompt)
    pr_body_generator.generate_body()

    # Step 4: Return the generated PR description text
    return pr_body_generator.body

if __name__ == "__main__":
    diff_file_path = sys.argv[1]  # Take diff file path as the first argument
    pr_number = sys.argv[2]       # Take PR number as the second argument

    # Generate the PR description
    pr_body = main(diff_file_path, pr_number)

    # Debugging output: Print the generated PR description to ensure it includes dynamic content
    print("Generated PR Body:\n", pr_body)

    # Save the generated PR description to a file for GitHub Actions to use
    with open("pr_description.txt", "w") as f:
        f.write(pr_body)
