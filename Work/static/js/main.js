
const form = document.getElementById('login-form');

form.addEventListener('submit', function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Add your validation logic here
    if (username === 'your_username' && password === 'your_password') {
        alert('Login successful!');
    } else {
        alert('Login failed. Please check your username and password.');
    }
});
