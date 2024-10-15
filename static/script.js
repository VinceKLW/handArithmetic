// List of Questions
const questions = [
    "1 + 1 = ?",
    "2 - 2 = ?",
    "3 + 1 = ?",
    "2 + 1 = ?",
    "5 - 1 = ?",
    "3 - 1 = ?",
    "2 + 3 = ?",
    "5 - 4 = ?",
    "2 + 1 = ?",
    "5 - 5 = ?"
];

// List of Answers
const answers = [
    "2",
    "0",
    "4",
    "3",
    "4",
    "2",
    "5",
    "1",
    "3",
    "0"
];

// Track Corresponding Index
let currentQuestionIndex = 0;

function changeQuestion() {
    let nextQuestionIndex; 

    // Choose a question using a random index
    do{
        nextQuestionIndex = Math.floor(Math.random() * questions.length);
    }while (nextQuestionIndex === currentQuestionIndex);

    // Change the current question to the new one
    currentQuestionIndex = nextQuestionIndex;

    // Connect variable to the 'question'
    const questionElement = document.getElementById('question');

    // Replace text with the new question
    questionElement.textContent = questions[currentQuestionIndex];

    // Every new question reset feedback
    document.getElementById('feedback').textContent = '';
}

function checkAnswer() {
    // Collect user's input for the answer
    const userAnswer = document.querySelector('.text-input').value.trim();
    
    // Receive the correct answer with the corresponding index
    const correctAnswer = answers[currentQuestionIndex];
    const feedbackElement = document.getElementById('feedback');

    // If user input is empty
    if (userAnswer === '') {
        feedbackElement.textContent = "Please enter an answer.";
        feedbackElement.style.color = "orange";
        return;
    }

    // If user input is correct
    if (userAnswer == correctAnswer) {
        feedbackElement.textContent = "Correct!";
        feedbackElement.style.color = "green";
    } 
    
    // If user input is incorrect
    else {
        feedbackElement.textContent = `Incorrect!`;
        feedbackElement.style.color = "red";
    }
}

function updateFingerCount() {
    // Retrieve the finger count from the server
    fetch('/finger_count')
        .then(response => response.json())
        .then(data => {
            const inputField = document.querySelector('.text-input');
            // Update input field with the detected finger count
            inputField.value = data.count;

            // Automatically check answer after the finger count is updated
            setTimeout(() => {
                checkAnswer();
            }, 500);
        })
        .catch(error => console.error('Error fetching finger count:', error));
}

// Automatically update finger count every second
setInterval(updateFingerCount, 1000);

// Event listener for when the user wants to generate a new question
document.getElementById('new-question').addEventListener('click', changeQuestion);

// Event listener for when the user wants to check their answer
document.getElementById('check-answer').addEventListener('click', checkAnswer);

// Automatically start camera input when the page loads
window.onload = startCamera;
