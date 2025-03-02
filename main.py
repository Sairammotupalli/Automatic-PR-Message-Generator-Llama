import os
import requests
import sys

LLAMA_API_URL = os.getenv("LLAMA_API_URL")

def generate_pr_description(diff_content, pr_number):
    
    
    prompt =  """Analyze, 
the given code changes and generate a detailed pull request description as a summary.

And give a overall score based on Readability, Maintainability and Clarity. 

The return format should be in the below json format:
{
    "readability_score": “<score within 1-3>”,
    "output": "<text explanation of the reason for the scoring and improvements that can apply>”
} 

Be careful while analyzing the code. Make sure to identify all the code changes and double-check the answer. Use the rubric and scoring criteria below while assigning the score.

—
"""
    prompt += f" information:\n\nPR Summary:\nPR #{pr_number}\n\nCode Changes:\n{diff_content}. Just summarize the changes using Description."
    prompt +=  """Checkboxes:, 
1. Clear Naming Conventions (Function and variable names are meaningful, self-explanatory and easy to understand.)
2. Documentation (Code includes meaningful inline comments explaining logic and purpose.)
3. Formatting & Styling (Code follows consistent indentation and spacing.)
4. Maintainability (Code is easy to extend or modify.)
5. Code Length (Functions are not excessively long; logic is broken down into smaller parts.)

Scoring Criteria:
- 3 (Excellent): Code meets all readability, maintainability, and clarity standards. Naming is clear, proper documentation, formatting is consistent, and code structure is easy to modify.  
- 2 (moderate): Code is readable and maintainable but has a scope for improvement.  
1 (Poor): Code is highly unreadable, with little no documentation, inconsistent naming.

"""
    response = requests.post(LLAMA_API_URL, json={
        "model": "llama3.3",
        "prompt": prompt
    })

    # Log the entire response for debugging
    print("Debug: Full response from FastAPI:", response.json())

    if response.status_code == 200:
        return response.json().get("generated_text", "No content from Llama.")
    else:
        print(f"Error: Received status code {response.status_code} from Llama API")
        return "Error generating PR description."

if __name__ == "__main__":
    diff_file_path = sys.argv[1]
    pr_number = sys.argv[2]

    with open(diff_file_path, "r") as f:
        diff_content = f.read()

    pr_body = generate_pr_description(diff_content, pr_number)

    with open("pr_description.txt", "w") as f:
        f.write(pr_body)
