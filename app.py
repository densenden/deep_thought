from flask import Flask, render_template, request
import 


app = Flask(__name__)

# List of Deep Thought inspired answers
answers = [
    "42",
    "The answer is 42, but I think you need to rephrase your question.",
    "I am Deep Thought, the greatest computer ever built. The answer is 42.",
    "I've been computing the answer to the Ultimate Question of Life, the Universe, and Everything for 7.5 million years. The answer is 42.",
    "42. Though you might want to ask what the question is first.",
    "The answer is 42, but you're probably asking the wrong question.",
    "42. And remember: Don't Panic!",
    "The answer is 42. Would you like me to design an even greater computer to work out what the question is?",
    "42. Though I suspect you're not ready for the answer.",
    "The answer is 42. Would you like me to explain why? It might take a while..."
]

@app.route('/', methods=['GET', 'POST'])
def home():
    answer = "I am Deep Thought, the greatest computer ever built. Ask me anything."
    if request.method == 'POST':
        question = request.form.get('question')
        print(f"User asked: {question}")  # Print the user's question
        answer = random.choice(answers)
    return render_template('index.html', answer=answer)

if __name__ == '__main__':
    app.run(debug=True) 