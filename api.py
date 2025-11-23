from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_model = pipeline("text-generation", model="gpt2") 

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
    question_text = q.question.lower()
    prompt = f"Answer ONLY yes or no to this question about a radio: {q.question}"
    model_out = chat_model(prompt, max_length=50)[0]['generated_text']
    response = "Yes" if "yes" in model_out.lower() else "No"

    return {"response": response}