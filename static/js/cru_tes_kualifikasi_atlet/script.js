// Function to show the qualification test form
function nextForm() {

    if(status){
        const qualificationForm = document.getElementById('qualificationForm');
        const qualificationTest = document.getElementById('qualificationTest');
        qualificationForm.style.display = 'none';
        qualificationTest.style.display = 'block';

    }
}

// Function to submit the qualification test
function submitTest() {
    // Perform validation and grading logic here

    // After grading, redirect to the dashboard
    window.location.href = 'dashboard.html';
}