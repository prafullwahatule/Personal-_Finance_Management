document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('deleteAccountForm');
  const confirmInput = document.getElementById('confirmText');
  const passwordInput = document.getElementById('accountPassword');
  const checkbox = document.getElementById('confirmCheckbox');
  const checkboxLabel = document.getElementById('checkboxLabel');

  // Initially disable the checkbox
  checkbox.disabled = true;

  // Validation function
  function validateFields() {
    let valid = true;

    // Validate confirmInput (should be exactly "DELETE")
    if (confirmInput.value.trim() !== "DELETE") {
      confirmInput.style.border = '2px solid red';
      valid = false;
    } else {
      confirmInput.style.border = '';
    }

    // Validate password input (not empty)
    if (passwordInput.value.trim() === "") {
      passwordInput.style.border = '2px solid red';
      valid = false;
    } else {
      passwordInput.style.border = '';
    }

    // Enable or disable checkbox based on validation
    checkbox.disabled = !valid;

    // Also reset checkbox border if disabled
    if (!valid) {
      checkboxLabel.style.border = '';
      checkbox.checked = false;
    }
  }

  // Run validation on input change
  confirmInput.addEventListener('input', validateFields);
  passwordInput.addEventListener('input', validateFields);

  // On form submit
  form.addEventListener('submit', (e) => {
    if (!checkbox.checked) {
      e.preventDefault();
      checkboxLabel.style.border = '2px solid red';
      alert('Please confirm by checking the box before deleting your account.');
    } else {
      const confirmed = confirm("Are you sure you want to permanently delete your account? This action cannot be undone.");
      if (!confirmed) {
        e.preventDefault(); // Cancel form submission
      }
    }
  });
});
