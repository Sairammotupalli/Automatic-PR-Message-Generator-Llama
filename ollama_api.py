from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.post("/generate")
async def generate_text(prompt: str, model: str = "llama3.3"):
    """
    Endpoint to generate text using Ollama's Llama model API.

    Args:
        prompt (str): The prompt text for the Llama model.
        model (str): The Llama model to use (default is "llama3.3").

    Returns:
        dict: JSON response with the generated text.
    """
    try:
        # Call Ollama’s local API directly
        response = requests.post(
            'http://localhost:11434/api/chat',
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }
        )
        response.raise_for_status()

        # Extract generated content from Ollama’s response
        generated_text = response.json()["choices"][0]["message"]["content"]
        return {"generated_text": generated_text}
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ollama API error: {str(e)}")
