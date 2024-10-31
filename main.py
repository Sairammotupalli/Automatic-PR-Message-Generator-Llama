import os
import requests
import sys

LLAMA_API_URL = os.getenv("LLAMA_API_URL")

def generate_pr_description(diff_content, pr_number):
    prompt = f"Generate a detailed pull request description based on the following information:\n\nPR Summary:\nPR #{pr_number}\n\nCode Changes:\n{diff_content}"

    response = requests.post(LLAMA_API_URL, json={
        "model": "llama3.2",
        "prompt": prompt
    })

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
