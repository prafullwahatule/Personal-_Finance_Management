document.addEventListener('DOMContentLoaded', function () {
  const deleteLinks = document.querySelectorAll('.delete-expense');

  deleteLinks.forEach(link => {
    link.addEventListener('click', function (event) {
      event.preventDefault();

      if (!confirm('Are you sure you want to delete this expense?')) {
        return;
      }

      const expenseId = this.dataset.id;
      const url = this.href;

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
            // Remove the row smoothly
            const row = this.closest('tr');
            row.style.transition = 'opacity 0.5s ease-out';
            row.style.opacity = 0;
            setTimeout(() => row.remove(), 500);
          } else {
            alert('Error deleting expense.');
          }
        })
        .catch(() => alert('Error deleting expense.'));
    });
  });
});

// Helper function to get CSRF token from cookies
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
