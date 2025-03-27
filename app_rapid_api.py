from flask import Flask, render_template, request
import requests
import json

# RapidAPI Configuration
url = "https://chatgpt-42.p.rapidapi.com/aitohuman"
headers = {
    "x-rapidapi-key": "87c1e3de80msh3a80d54ff5955dbp1416f8jsn4e95b32535c2",
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

@app.route('/', methods=['GET', 'POST'])
def home():
    answer = "I am Deep Thought, the greatest computer ever built. Ask me anything."
    question = ""
    
    if request.method == 'POST':
        question = request.form.get('question')
        print(f"User asked: {question}")
        
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
            # Send API request and log response
            print("Sending request to RapidAPI...")
            response = requests.post(url, json=payload, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Content: {response.text}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"Parsed Response: {response_data}")
                
                # Try different response structures
                if isinstance(response_data, dict):
                    # Check common response keys
                    possible_keys = ['response', 'content', 'message', 'result', 'generated_text', 'choices']
                    for key in possible_keys:
                        if key in response_data:
                            if isinstance(response_data[key], list):
                                # Get first element if response is a list
                                answer = response_data[key][0] if response_data[key] else "No response generated."
                            else:
                                answer = response_data[key]
                            break
                    else:
                        # Fallback if no known keys found
                        answer = str(response_data)
                else:
                    answer = str(response_data)
            else:
                error_message = response.json().get('message', response.text) if response.text else f"HTTP {response.status_code}"
                answer = f"API Error: {error_message}"
                
        except Exception as e:
            print(f"Error: {str(e)}")
            answer = f"Error: {str(e)}"
    
    return render_template('index.html', answer=answer, question=question)

if __name__ == '__main__':
    app.run(debug=True, port=5002) 