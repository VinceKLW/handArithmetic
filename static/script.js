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

let currentQuestionIndex = 0;

function changeQuestion() {
    let nextQuestionIndex;
    do{
        nextQuestionIndex = Math.floor(Math.random() * questions.length);
    }while (nextQuestionIndex === currentQuestionIndex);

    currentQuestionIndex = nextQuestionIndex;

    const questionElement = document.getElementById('question');
    questionElement.textContent = questions[currentQuestionIndex];

    document.getElementById('feedback').textContent = '';
}

function checkAnswer() {
    const userAnswer = document.querySelector('.text-input').value.trim();
    const correctAnswer = answers[currentQuestionIndex];
    const feedbackElement = document.getElementById('feedback');

    if (userAnswer === '') {
        feedbackElement.textContent = "Please enter an answer.";
        feedbackElement.style.color = "orange";
        return;
    }

    if (userAnswer == correctAnswer) {
        feedbackElement.textContent = "Correct!";
        feedbackElement.style.color = "green";
    } else {
        feedbackElement.textContent = `Incorrect!`;
        feedbackElement.style.color = "red";
    }
}

function updateFingerCount() {
    fetch('/finger_count')
        .then(response => response.json())
        .then(data => {
            const inputField = document.querySelector('.text-input');
            inputField.value = data.count;

            setTimeout(() => {
                checkAnswer();
            }, 500);
        })
        .catch(error => console.error('Error fetching finger count:', error));
}

setInterval(updateFingerCount, 1000);

document.getElementById('new-question').addEventListener('click', changeQuestion);
document.getElementById('check-answer').addEventListener('click', checkAnswer);
window.onload = startCamera;
