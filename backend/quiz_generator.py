# quiz_generator.py
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json

def generate_quiz(article_text: str):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)
    prompt = ChatPromptTemplate.from_template("""
    Generate 5-10 quiz questions from the following Wikipedia article text.
    Each question should have:
    - question
    - 4 options (A-D)
    - correct answer
    - short explanation
    - difficulty (easy, medium, hard)
    - 3 suggested related Wikipedia topics
    Article Text:
    {text}
    Respond in JSON format:
    {{
      "quiz": [...],
      "related_topics": [...]
    }}
    """)
    
    response = llm.predict(prompt.format(text=article_text))

    try:
        data = json.loads(response)
    except:
        data = {"quiz": [], "related_topics": []}
    return data
