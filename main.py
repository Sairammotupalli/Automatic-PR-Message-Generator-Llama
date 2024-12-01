import os
import requests
import sys

LLAMA_API_URL = os.getenv("LLAMA_API_URL")

def generate_pr_description(diff_content, pr_number):
    prompt = f" 1. Generate a detailed pull request description based on the following information:\n\nPR Summary:\nPR #{pr_number}\n\nCode Changes:\n{diff_content}. Just summarize the changes using Description."
    prompt += """  
And also, along with the above details, 
2. Analyze the Pull Request details and assign a score between 0 and 100 for each category listed below. Ensure that scores are not always biased towards high values. Consider all relevant information from the Pull Request and provide scores based on the factors. Output in the exact specified format:

### **Category 1: Impact Analysis**  
Evaluate the impact of the Pull Request on the overall codebase and just provide a overall score using the following factors:  
- **Bug Fix**: [how well it resolves existing issues or bugs]  
- **Usefulness**: [how the changes add value to the project]  
- **New Functionality**: [how the new features enhance the system]  
- **Maintainability**: [how the changes affect the code’s maintainability and long-term stability]  
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

    response = requests.post(LLAMA_API_URL, json={
        "model": "llama3.2",
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
