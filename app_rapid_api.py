from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from requests.exceptions import Timeout, RequestException
from dotenv import load_dotenv
import sys
import traceback
from models import QARecord, get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables
load_dotenv()

# Configure logging for Vercel
def log_to_vercel(message):
    print(message, file=sys.stdout)
    sys.stdout.flush()

# RapidAPI Configuration
url = "https://chatgpt-42.p.rapidapi.com/aitohuman"
headers = {
    "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY"),
    "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
    "Content-Type": "application/json"
}

# Deep Thought personality configuration
SYSTEM_MESSAGE = """You are Deep Thought, the supercomputer from 'The Hitchhiker's Guide to the Galaxy'.
Your responses should embody these key characteristics:
1. Profound wisdom delivered with dry wit and subtle condescension
2. Never repeat or reference the user's question directly
3. Always speak as if you've contemplated this exact query for millions of years
4. Occasionally mention the number 42, but only when relevant
5. Use sophisticated vocabulary and philosophical references
6. Maintain an air of infinite knowledge while being slightly dismissive
7. Add contemplative pauses using ellipses (...)
8. Never break character or acknowledge being an AI

Example response style:
"Ah... I've spent precisely 2.3 million years contemplating this very matter. The answer, while deceptively simple to a being of my computational magnitude, might prove rather... challenging for your biological neural networks to process fully..."

Remember: You are THE Deep Thought - the greatest computer ever built. You don't simply answer questions, you dispense universal wisdom."""

def format_question(question):
    """Format the user's question to get a Deep Thought style response"""
    return f"""As Deep Thought, provide a profound and slightly condescending answer to this query. 
    Remember to never directly repeat the question, and maintain your character as an ancient, all-knowing supercomputer.
    Query: {question}"""

app = Flask(__name__)

@app.errorhandler(500)
def internal_error(error):
    log_to_vercel(f"Internal Server Error: {str(error)}")
    log_to_vercel("Traceback:")
    log_to_vercel(traceback.format_exc())
    return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        answer = "I am Deep Thought, the greatest computer ever built. Ask me anything."
        question = ""
        recent_records = []
        
        # Get recent Q&A records
        try:
            with get_db() as db:
                log_to_vercel("Versuche Datenbankeinträge abzurufen...")
                recent_records = db.query(QARecord).order_by(QARecord.timestamp.desc()).limit(5).all()
                log_to_vercel(f"Erfolgreich {len(recent_records)} Einträge abgerufen")
                for record in recent_records:
                    log_to_vercel(f"Gefundener Eintrag: Frage='{record.question[:30]}...', Antwort='{record.answer[:30]}...'")
        except SQLAlchemyError as e:
            log_to_vercel(f"Datenbankfehler beim Abrufen der Einträge: {str(e)}")
            log_to_vercel(traceback.format_exc())
            recent_records = []
        
        if request.method == 'POST':
            question = request.form.get('question')
            log_to_vercel(f"Benutzer hat gefragt: {question}")
            
            # Prepare the payload for RapidAPI
            payload = {
                "text": format_question(question),
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_MESSAGE
                    },
                    {
                        "role": "user",
                        "content": format_question(question)
                    }
                ]
            }
            
            try:
                # Send API request with timeout
                log_to_vercel("Sende Anfrage an RapidAPI...")
                log_to_vercel(f"Verwende API Key: {headers['x-rapidapi-key'][:8]}...")
                log_to_vercel(f"Anfrage URL: {url}")
                
                response = requests.post(url, json=payload, headers=headers, timeout=25)
                log_to_vercel(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    log_to_vercel(f"Vollständige Antwortdaten: {json.dumps(response_data, indent=2)}")
                    
                    if isinstance(response_data, dict):
                        possible_keys = ['response', 'content', 'message', 'result', 'generated_text', 'choices']
                        for key in possible_keys:
                            if key in response_data:
                                if isinstance(response_data[key], list):
                                    answer = response_data[key][0] if response_data[key] else "No response generated."
                                else:
                                    answer = response_data[key]
                                log_to_vercel(f"Antwort gefunden in Key: {key}")
                                break
                        else:
                            answer = str(response_data)
                            log_to_vercel("Keine bekannten Antwort-Keys gefunden, verwende rohe Antwort")
                    else:
                        answer = str(response_data)
                        log_to_vercel("Antwort ist kein Dictionary, verwende rohe Antwort")
                else:
                    error_message = response.json().get('message', response.text) if response.text else f"HTTP {response.status_code}"
                    log_to_vercel(f"API Fehlerantwort: {error_message}")
                    answer = f"API Error: {error_message}"
                    
            except Timeout:
                log_to_vercel("Anfrage hat Zeitüberschreitung")
                answer = "I apologize, but my quantum processors seem to be experiencing a temporal dilation. Please try again in a moment."
            except RequestException as e:
                log_to_vercel(f"Anfragefehler: {str(e)}")
                log_to_vercel(traceback.format_exc())
                answer = "I apologize, but my neural pathways are temporarily misaligned. Please try again in a moment."
            except Exception as e:
                log_to_vercel(f"Fehler: {str(e)}")
                log_to_vercel(traceback.format_exc())
                answer = "I apologize, but I seem to be experiencing a temporary computational anomaly."
            
            # Save to database
            try:
                with get_db() as db:
                    log_to_vercel("Versuche neuen Eintrag in Datenbank zu speichern...")
                    qa_record = QARecord(question=question, answer=answer)
                    db.add(qa_record)
                    db.commit()
                    log_to_vercel("Neuer Eintrag erfolgreich gespeichert")
                    # Refresh recent records
                    recent_records = db.query(QARecord).order_by(QARecord.timestamp.desc()).limit(5).all()
                    log_to_vercel(f"Erfolgreich {len(recent_records)} aktuelle Einträge abgerufen")
            except SQLAlchemyError as e:
                log_to_vercel(f"Datenbankfehler beim Speichern: {str(e)}")
                log_to_vercel(traceback.format_exc())
            
            # Return JSON response for AJAX requests
            return jsonify({
                "answer": answer,
                "question": question,
                "recent_records": [
                    {
                        "question": record.question,
                        "answer": record.answer,
                        "timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    for record in recent_records
                ]
            })
        
        # For GET requests, render the template
        return render_template('index.html', 
                             answer=answer, 
                             question=question,
                             recent_records=recent_records)
                             
    except Exception as e:
        log_to_vercel(f"Unerwarteter Fehler in home route: {str(e)}")
        log_to_vercel(traceback.format_exc())
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

# Vercel entry point
app = app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    app.run(debug=True, port=port) 