import os
import json
from diff_analyzer_service import DiffAnalyzerService
from pr_body_generator import PrBodyGenerator
from pr_parser import PRParser
from prompt import Prompt
from completion import Completion

def main(diff_file, output_file, pr_file):
    """
    Main function to generate a pull request description based on a code diff.
    """
    # Step 1: Analyze the diff file
    diff_analyzer = DiffAnalyzerService(diff_file)
    diff_analysis = diff_analyzer.analyse_diff()

    # Step 2: Parse PR data from pr_file
    with open(pr_file, 'r') as f:
        pr_data = json.load(f)
    pr_parser = PRParser(pr_data)
    pr_summary = pr_parser.get_summary()

    # Step 3: Create the prompt with diff_analysis and pr_summary
    prompt = Prompt(diff_analysis=diff_analysis, pr_summary=pr_summary)

    # Step 4: Generate the PR body using PrBodyGenerator
    pr_body_generator = PrBodyGenerator(prompt=prompt)
    pr_body_generator.generate_body()

    # Step 5: Use Completion to complete the PR body
    completion = Completion(prompt=pr_body_generator)  # Pass pr_body_generator to Completion
    completion.complete()
    
    # Step 6: Write the generated PR description to output_file
    with open(output_file, 'w') as f:
        f.write(completion.result)

if __name__ == "__main__":
    main(
        diff_file=os.getenv("DIFF_FILE", "diff.txt"),
        output_file=os.getenv("OUTPUT_FILE", "output.txt"),
        pr_file=os.getenv("PR_FILE", "pr.json")
    )
