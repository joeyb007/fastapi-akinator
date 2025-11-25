from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
import os



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
HF_API_KEY = os.getenv("HF_API_KEY")


class Question(BaseModel):
    question: str 

class Guess(BaseModel):
    guess: str 

@app.post("/guess")
def guess_answer(g: Guess):
    if g.guess:
        if g.guess.lower() == 'radio':
            return {"response": "Yes the answer is the first letter of that word"}
        else:
            return {"response": "Nope, that's not it. Keep guessing!"}

@app.post("/ask")
def ask_question(q: Question):
    prompt = f"Answer ONLY yes or no to this question about a radio: {q.question}"

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 50}
    }

    response = requests.post(HF_API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        return {"response": "Error contacting model API"}

    model_out = response.json()
    generated_text = model_out[0]["generated_text"]

    answer = "Yes" if "yes" in generated_text.lower() else "No"
    return {"response": answer}