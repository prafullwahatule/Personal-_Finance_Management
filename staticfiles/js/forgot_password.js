const emailForm = document.getElementById('emailForm');
const otpForm = document.getElementById('otpForm');
const resetForm = document.getElementById('resetForm');
const message = document.getElementById('message');

emailForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const formData = new FormData(this);

    fetch("{% url 'forgot_password' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest', // Indicate AJAX request
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'otp_sent') {
            emailForm.style.display = 'none';
            otpForm.style.display = 'block';
            message.style.color = 'green';
            message.textContent = `OTP sent to ${data.email}`;
        } else if (data.status === 'error') {
            message.style.color = 'red';
            message.textContent = data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        message.style.color = 'red';
        message.textContent = 'An error occurred. Please try again.';
    });
});

otpForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const otp = document.getElementById('otp').value;
    const formData = new FormData(this);

    fetch("{% url 'verify_otp' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest', // Indicate AJAX request
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            otpForm.style.display = 'none';
            resetForm.style.display = 'block';
            message.textContent = '';
        } else if (data.status === 'error') {
            message.style.color = 'red';
            message.textContent = data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        message.style.color = 'red';
        message.textContent = 'An error occurred. Please try again.';
    });
});

resetForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (newPassword !== confirmPassword) {
        message.style.color = 'red';
        message.textContent = 'Passwords do not match.';
    } else {
        this.submit(); // Let the default form submission handle the password reset
    }
});