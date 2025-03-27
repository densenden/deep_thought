document.getElementById('question-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const question = document.getElementById('question').value;
    const answerBox = document.getElementById('answer-box');
    const loadingContainer = document.getElementById('loading-container');
    const askedQuestion = document.getElementById('asked-question');
    const answerText = document.getElementById('answer');
    
    // Hide answer and show loading
    answerBox.classList.remove('visible');
    loadingContainer.style.display = 'block';
    
    // Start the API call immediately
    const apiCall = fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `question=${encodeURIComponent(question)}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
    })
    .then(html => {
        try {
            // Try to parse the response as JSON first
            const jsonMatch = html.match(/\{.*\}/);
            if (jsonMatch) {
                const jsonData = JSON.parse(jsonMatch[0]);
                return jsonData.answer || jsonData.response || jsonData.message || "No answer found in response.";
            }
            
            // If not JSON, try to parse as HTML
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const answerElement = doc.getElementById('answer');
            
            if (answerElement) {
                return answerElement.textContent;
            }
            
            // If no answer element found, try to find any text content
            const textContent = doc.body.textContent;
            if (textContent) {
                return textContent.trim();
            }
            
            return "I apologize, but I seem to be experiencing a temporary computational anomaly.";
        } catch (error) {
            console.error('Error parsing response:', error);
            return "I apologize, but I seem to be experiencing a temporary computational anomaly.";
        }
    });
    
    // Simulate loading progress
    let progress = 0;
    const progressBar = document.getElementById('progress');
    const progressText = document.getElementById('progress-text');
    
    const interval = setInterval(() => {
        progress += 0.75; // Adjusted for ~13 seconds duration
        progressBar.style.width = `${progress}%`;
        progressText.textContent = Math.round(progress);
        
        if (progress >= 100) {
            clearInterval(interval);
            // When loading is complete, show the answer
            apiCall.then(newAnswer => {
                setTimeout(() => {
                    loadingContainer.style.display = 'none';
                    askedQuestion.textContent = `You asked: ${question}`;
                    answerText.textContent = newAnswer;
                    answerBox.classList.add('visible');
                }, 500);
            })
            .catch(error => {
                console.error('API Error:', error);
                loadingContainer.style.display = 'none';
                answerText.innerHTML = `<span class="error-message">Error: ${error.message}</span>`;
                answerBox.classList.add('visible');
            });
        }
    }, 100); // Update every 100ms
}); 