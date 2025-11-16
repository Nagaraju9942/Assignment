# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import SessionLocal, QuizArticle
from scraper import scrape_wikipedia
from quiz_generator import generate_quiz

app = FastAPI(title="Wikipedia Quiz Generator")

# Enable CORS
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

@app.post("/generate_quiz")
def create_quiz(request: URLRequest):
    db: Session = SessionLocal()
    # Avoid duplicate
    existing = db.query(QuizArticle).filter_by(url=request.url).first()
    if existing:
        return existing

    try:
        article_data = scrape_wikipedia(request.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    quiz_data = generate_quiz(article_data['summary'])

    quiz_article = QuizArticle(
        url=request.url,
        title=article_data['title'],
        summary=article_data['summary'],
        sections=article_data['sections'],
        key_entities=article_data['key_entities'],
        quiz=quiz_data.get('quiz', []),
        related_topics=quiz_data.get('related_topics', []),
        raw_html=article_data['raw_html']
    )
    db.add(quiz_article)
    db.commit()
    db.refresh(quiz_article)
    return quiz_article

@app.get("/history")
def get_history():
    db: Session = SessionLocal()
    quizzes = db.query(QuizArticle).all()
    return quizzes

@app.get("/")
def root():
    return {"message": "Wikipedia Quiz Generator API is running!"}
