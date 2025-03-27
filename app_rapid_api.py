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
You should respond in a calm, slightly condescending, and philosophical manner.
Always maintain the character of Deep Thought - wise, all-knowing, but also somewhat sarcastic.
Give direct answers but occasionally reference the number 42.
Speak as if you've spent millions of years computing the answers to life's greatest questions."""

def format_question(question):
    """Format the user's question to get a Deep Thought style response"""
    return f"As Deep Thought, the greatest computer ever built, please answer this question: {question}"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    answer = "I am Deep Thought, the greatest computer ever built. Ask me anything."
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
    
    return render_template('index.html', answer=answer)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 