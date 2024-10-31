import os
import json
from typing_extensions import Annotated
from diff_analyzer_service import DiffAnalyzerService
import typer
from pr_body_generator import PrBodyGenerator
from pull_request import PullRequest
import logging

logging.basicConfig(filename="test.log", encoding="utf-8", level=logging.INFO)

def main(
    diff_file: str,
    output_file: Annotated[str, typer.Option()],
    pr_file: Annotated[str, typer.Option()],
):
    print("Parsing diff and generating prompts")
    diff_analyser = DiffAnalyzerService(diff_file)
    diff_analysis = diff_analyser.analyse_diff()

    # Initialize the PR body generator with the diff analysis result
    pr_body_generator = PrBodyGenerator(diff_analysis)
    pr_body_generator.generate_body()

    with open(pr_file, "r") as f:
        pr_data = json.load(f)
        pull_request = PullRequest(pr_data["id"], pr_data["body"])

    pull_request.update_auto_body(pr_body_generator.body)

    if output_file:
        with open(output_file, "w") as out_file:
            out_file.write(pull_request.body)

if __name__ == "__main__":
    typer.run(main)
