document.addEventListener('DOMContentLoaded', function () {
  const deleteLinks = document.querySelectorAll('.delete-expense');

  deleteLinks.forEach(link => {
    link.addEventListener('click', function (event) {
      event.preventDefault();

      if (!confirm('Are you sure you want to delete this expense?')) {
        return;
      }

      const expenseId = this.dataset.id;
      const url = `/dashboard/expense/delete/${expenseId}/`; // Update URL pattern if needed

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
            // ✅ Show success message
            showExpenseMessage('Expense deleted successfully.', 'success');

            // ⏳ Wait 5 seconds then reload page
            setTimeout(() => {
              location.reload();
            }, 5000);
          } else {
            // ❌ Show error from backend
            showExpenseMessage(`Error deleting expense: ${data.error || 'Unknown error'}`, 'error');
          }
        })
        .catch(() => {
          // ❌ Fallback error message
          showExpenseMessage('Error deleting expense. Please try again.', 'error');
        });
    });
  });
});

// ✅ Show message with Font Awesome icons
function showExpenseMessage(message, type = 'success') {
  const messageBox = document.getElementById('expense-message');
  if (!messageBox) return;

  // Remove existing classes
  messageBox.classList.remove('expense-alert-success', 'expense-alert-danger');

  // Add icon and class
  if (type === 'success') {
    messageBox.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
    messageBox.classList.add('expense-alert-success');
  } else {
    messageBox.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    messageBox.classList.add('expense-alert-danger');
  }

  messageBox.style.display = 'flex';

  setTimeout(() => {
    messageBox.style.display = 'none';
  }, 5000);
}

// ✅ Get CSRF token from cookie
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
