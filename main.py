
import os
import requests
import sys
import json

LLAMA_API_URL = os.getenv("LLAMA_API_URL")

def generate_pr_description(diff_content, pr_number):
    if not LLAMA_API_URL:
        print("❌ Error: LLAMA_API_URL is not set.")
        return "Error: LLAMA_API_URL is not configured."

    prompt = f" Generate a detailed pull request description based on the following information:\n\nPR Summary:\nPR #{pr_number}\n\nCode Changes:\n{diff_content}. Just summarize the changes using Description."
    prompt += """Next, 
**Analyze the Pull Request details and assign a score between 0 and 100 for each category listed below**. Use the provided rubric for guidance. Ensure that scores reflect the quality and specifics of the Pull Request, and do not bias scores toward high values without sufficient justification. Follow the exact format given below:

#### **Scoring Rubric**:
- **100**: Excellent, exceeds all expectations, no areas for improvement.  
- **80–99**: Very good, meets most expectations with minor improvements needed.  
- **60–79**: Satisfactory, meets minimum expectations but requires moderate improvement.  
- **40–59**: Below average, significant improvements needed.  
- **0–39**: Poor, fails to meet expectations.

#### **Scoring Categories**:
- **Category 1: Impact Analysis**  
  Evaluate the impact of the Pull Request on the overall codebase using these factors:  
  - **Bug Fix**: How effectively it resolves existing issues or bugs.  
  - **Usefulness**: The value the changes add to the project.  
  - **New Functionality**: How the new features enhance the system.  
  - **Maintainability**: The impact on the code’s maintainability and long-term stability.  

  **Impact Score**: Overall score based on Bug Fix, Usefulness, New Functionality, and Maintainability [0–100]  

---

- **Category 2: Code Quality**  
  Assess the overall quality of the code using factors such as readability, structure, and adherence to best practices.  

  **Code Quality Score**: [0–100]  

---

- **Category 3: Security**  
  Identify any security vulnerabilities or risks introduced by the code (e.g., hardcoded credentials, unsafe serialization, SQL injection).  

  **Security Score**: [0–100]  

---

- **Category 4: Creativity**  
  Determine originality and innovation. Unique and creative code gets a high score; unoriginal or heavily copied code gets a low score.  

  **Creativity Score**: [0–100]  

---
"""

    try:
        print(f"🔹 Sending request to LLAMA_API_URL: {LLAMA_API_URL}")
        
        response = requests.post(LLAMA_API_URL, json={"model": "llama3.2", "prompt": prompt})
        
        if response.status_code != 200:
            print(f" Error: Received status code {response.status_code} from Llama API")
            return "Error generating PR description."

        response_json = response.json()
        print(" Debug: Full response from FastAPI:", json.dumps(response_json, indent=2))

        # Extract response text safely
        generated_text = response_json.get("response", "No content from Llama.")
        
        if not generated_text.strip():
            print("Warning: Llama API returned an empty response.")
            return "No content from Llama."

        return generated_text

    except requests.exceptions.RequestException as e:
        print(f" Error: Failed to reach Llama API - {e}")
        return "Error: Unable to contact Llama API."

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(" Error: Missing required arguments. Usage: python main.py <diff_file_path> <pr_number>")
        sys.exit(1)

    diff_file_path = sys.argv[1]
    pr_number = sys.argv[2]

    try:
        with open(diff_file_path, "r") as f:
            diff_content = f.read().strip()
        
        if not diff_content:
            print(" Warning: The diff file is empty. No content to process.")
            pr_body = "No changes detected in this PR."
        else:
            pr_body = generate_pr_description(diff_content, pr_number)

        # Write the generated PR description to a file
        with open("pr_description.txt", "w") as f:
            f.write(pr_body)

        print("PR description saved successfully.")

    except FileNotFoundError:
        print(f" Error: Diff file '{diff_file_path}' not found.")
        sys.exit(1)

    except Exception as e:
        print(f" Unexpected Error: {e}")
        sys.exit(1)
