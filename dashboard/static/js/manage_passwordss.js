document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".manage-password-form");
  const currentPassword = document.getElementById("current-password");
  const newPassword = document.getElementById("new-password");
  const confirmPassword = document.getElementById("confirm-password");
  const changeBtn = document.getElementById("change-btn");
  const passwordHint = document.getElementById("password-hint");
  const confirmPasswordHint = document.getElementById("confirm-password-hint");
  const messageBox = document.createElement('div');
  messageBox.style.margin = "10px 0";
  form.prepend(messageBox);

  // Password validation regex (min 8 chars, uppercase, lowercase, digit, special char)
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;

  function validatePasswords() {
    let isValid = true;

    if (!currentPassword.value.trim()) {
      isValid = false;
    }

    if (!passwordRegex.test(newPassword.value)) {
      passwordHint.style.display = "block";
      isValid = false;
    } else {
      passwordHint.style.display = "none";
    }

    if (newPassword.value !== confirmPassword.value || !confirmPassword.value) {
      confirmPasswordHint.style.display = "block";
      isValid = false;
    } else {
      confirmPasswordHint.style.display = "none";
    }

    changeBtn.disabled = !isValid;
  }

  currentPassword.addEventListener("input", validatePasswords);
  newPassword.addEventListener("input", validatePasswords);
  confirmPassword.addEventListener("input", validatePasswords);

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    validatePasswords();

    if (changeBtn.disabled) {
      return; // Prevent submit if invalid
    }

    const formData = new FormData(form);

    fetch(form.action || window.location.href, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
      },
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          messageBox.style.color = 'green';
          messageBox.textContent = data.message || 'Password changed successfully!';
          form.reset();
          changeBtn.disabled = true;
          passwordHint.style.display = "none";
          confirmPasswordHint.style.display = "none";
        } else {
          messageBox.style.color = 'red';
          messageBox.textContent = 'Error changing password:';
          // Show first error below the respective input or general message
          if (data.errors) {
            if (data.errors.current_password) {
              alert('Current Password Error: ' + data.errors.current_password);
            } else if (data.errors.new_password) {
              alert('New Password Error: ' + data.errors.new_password);
            } else if (data.errors.confirm_password) {
              alert('Confirm Password Error: ' + data.errors.confirm_password);
            } else {
              alert(JSON.stringify(data.errors));
            }
          }
        }
      })
      .catch(error => {
        messageBox.style.color = 'red';
        messageBox.textContent = 'Unexpected error occurred. Try again.';
        console.error('Error:', error);
      });
  });
});
