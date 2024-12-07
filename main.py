import os
import requests
import sys

LLAMA_API_URL = os.getenv("LLAMA_API_URL")

def generate_pr_description(diff_content, pr_number):
    
    prompt = """  **Generate a detailed pull request description** based on the following information:
   - **PR Summary**:  
     PR #{pr_number}  
   - **Code Changes**:  
     {diff_content}  

   Summarize the changes succinctly in the "Description" section.

---

And then after, 
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

  **Impact Score**: Overall score based on Bug Fix, Usefulness, New Functionality and Maintainability[0–100]  

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

### **Few-Shot Examples for your understanding of the rubrics (This is not a PR change)**:

**Example 1:**  
- **PR Summary**:  
  PR #123: Refactor the user authentication system.  
- **Code Changes**:  
  Added JWT-based token authentication, removed legacy session-based authentication, and updated relevant endpoints.  

  **Description**:  
  Refactored the authentication system to enhance security by introducing JWT tokens. Deprecated session-based authentication and replaced it with token-based mechanisms, improving scalability. Updated endpoints and associated documentation.  

  **Impact Score**: 90  
  - **Reasoning**: Significantly enhances security and scalability. However, backward compatibility with existing systems might require additional consideration.  

  **Code Quality Score**: 85  
  - **Reasoning**: Well-structured and readable code but could benefit from more extensive documentation.  

  **Security Score**: 95  
  - **Reasoning**: Eliminates session vulnerabilities and implements JWT securely.  

  **Creativity Score**: 80  
  - **Reasoning**: Implements known best practices effectively but does not introduce novel approaches.  

---

**Example 2:**  
- **PR Summary**:  
  PR #124: Add caching for frequently accessed endpoints.  
- **Code Changes**:  
  Implemented Redis caching for GET /products and GET /categories, reducing response times by 70%.  

  **Description**:  
  Added Redis-based caching to optimize the performance of frequently accessed endpoints. Updated configuration files and ensured cache invalidation works seamlessly.  

  **Impact Score**: 85  
  - **Reasoning**: Greatly improves performance but limited to a specific use case.  

  **Code Quality Score**: 88  
  - **Reasoning**: Follows best practices, though inline comments could be clearer.  

  **Security Score**: 80  
  - **Reasoning**: No security vulnerabilities, but configuration files could be better secured.  

  **Creativity Score**: 75  
  - **Reasoning**: Effectively applies an established approach without significant innovation.  

---

**Now, evaluate the given Pull Request using the above format and rubric.**

Here are additional examples to guide the LLM further:

---
"""

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
