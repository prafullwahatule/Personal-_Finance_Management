document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('income-form');
  const messageDiv = document.getElementById('income-message');
  const submitBtn = form.querySelector('.submit-btn');

  // Show message helper
  function showMessage(text, type) {
    messageDiv.innerHTML = '';
    messageDiv.style.display = 'flex';
    messageDiv.classList.remove('add-income-message-success', 'add-income-message-danger');

    if (type === 'success') {
      messageDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${text}`;
      messageDiv.classList.add('add-income-message-success');
    } else {
      messageDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${text}`;
      messageDiv.classList.add('add-income-message-danger');
    }

    // Hide after 5 s (and reload page if it was a success)
    setTimeout(() => {
      messageDiv.style.display = 'none';
      if (type === 'success') {
        location.reload();
      }
    }, 5000);
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(form);
    const amount = parseFloat(formData.get('amount'));
    if (!amount || amount <= 0) {
      showMessage('Please enter a valid income amount.', 'error');
      return;
    }

    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span class="spinner"></span> Adding...`;

    fetch(form.action, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
      },
      body: formData,
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        showMessage(data.message || 'Income added successfully!', 'success');
        form.reset();
      } else {
        showMessage(data.error || 'Something went wrong.', 'error');
      }
    })
    .catch(err => {
      console.error(err);
      showMessage('Network error. Try again later.', 'error');
    })
    .finally(() => {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Add Income';
    });
  });
});