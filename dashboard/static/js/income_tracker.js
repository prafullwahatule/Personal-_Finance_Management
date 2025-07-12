document.addEventListener('DOMContentLoaded', function () {
  const deleteLinks = document.querySelectorAll('.delete-income');

  deleteLinks.forEach(link => {
    link.addEventListener('click', function (event) {
      event.preventDefault();

      if (!confirm('Are you sure you want to delete this income?')) {
        return;
      }

      const incomeId = this.dataset.id;
      const url = `/dashboard/income/delete/${incomeId}/`; // Update as per your URL pattern

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // ✅ Show success message with icon
            showIncomeMessage('Income deleted successfully.', 'success');

            // ⏳ Wait 5 seconds then reload page
            setTimeout(() => {
              location.reload();
            }, 5000);
          } else {
            // ❌ Show error from backend
            showIncomeMessage(`Error deleting income: ${data.error || 'Unknown error'}`, 'error');
          }
        })
        .catch(() => {
          // ❌ Fallback error message
          showIncomeMessage('Error deleting income. Please try again.', 'error');
        });
    });
  });
});

// ✅ Message box display handler with icons
function showIncomeMessage(message, type = 'success') {
  const messageBox = document.getElementById('income-message');
  if (!messageBox) return;

  // Remove previous classes
  messageBox.classList.remove('income-alert-success', 'income-alert-danger');

  // Set message and class based on type
  if (type === 'success') {
    messageBox.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
    messageBox.classList.add('income-alert-success');
  } else {
    messageBox.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    messageBox.classList.add('income-alert-danger');
  }

  messageBox.style.display = 'flex';

  // Auto hide after 5 seconds
  setTimeout(() => {
    messageBox.style.display = 'none';
  }, 5000);
}

// ✅ CSRF helper function
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
