import os
import json
from typing_extensions import Annotated
import typer
import logging

from diff_analyzer_service import DiffAnalyzerService
from pr_body_generator import PrBodyGenerator
from pull_request import PullRequest

# Set up logging to capture the process
logging.basicConfig(filename="pr_generator.log", encoding="utf-8", level=logging.INFO)

def main(
    diff_file: str = Annotated[str, typer.Option(help="Path to the diff file")],
    output_file: str = Annotated[str, typer.Option(help="Path to save the generated PR description")],
    pr_file: str = Annotated[str, typer.Option(help="Path to the PR file containing PR data")],
):
    """
    Main function to generate a pull request description based on a code diff.
    """
    logging.info("Starting PR description generation...")

    # Step 1: Analyze the diff file
    logging.info(f"Analyzing diff file: {diff_file}")
    diff_analyzer = DiffAnalyzerService(diff_file)
    diff_analysis = diff_analyzer.analyse_diff()
    logging.info(f"Diff analysis complete: {diff_analysis}")

    # Step 2: Generate PR body based on the analysis
    logging.info("Generating PR body...")
    pr_body_generator = PrBodyGenerator(diff_analysis)
    pr_body_generator.generate_body()
    pr_body = pr_body_generator.body
    logging.info(f"Generated PR body: {pr_body}")

    # Step 3: Load existing PR data from pr_file and update it with generated body
    logging.info(f"Loading PR data from: {pr_file}")
    with open(pr_file, "r") as f:
        pr_data = json.load(f)
        pull_request = PullRequest(pr_data["id"], pr_data["body"])
    
    # Update the PR body
    pull_request.update_auto_body(pr_body)

    # Step 4: Save the generated PR description to the output file
    logging.info(f"Saving generated PR description to {output_file}")
    with open(output_file, "w") as f:
        f.write(pr_body)

    logging.info("PR description generation completed successfully.")

if __name__ == "__main__":
    typer.run(main)
