from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)
load_dotenv()
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

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
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    generated_text = chat_completion.choices[0].message.content
    answer = "Yes" if "yes" in generated_text.lower() else "No"
    return {"response": answer}
