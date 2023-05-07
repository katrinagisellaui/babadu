// Function to show the qualification test form
function nextForm() {
    // let status = true;
    // let x = document.forms["registerForm"]["athleteDropdown"].value;
    // if (x == "") {
    // //   alert("Athlete name must be filled out");
    //   status = false;
    // }

    // if(status){
        const registrationForm = document.getElementById('registrationForm');
        const athleteList = document.getElementById('athleteList');
        registrationForm.style.display = 'none';
        athleteList.style.display = 'block';

    // }
}
