document.addEventListener('DOMContentLoaded', function () {
  const form       = document.getElementById('expense-form');
  const msgDiv     = document.getElementById('expense-message');
  const submitBtn  = form.querySelector('.submit-btn');
  // Make sure to add id="expense-summary-body" to your <tbody>
  const tbody      = document.getElementById('expense-summary-body');

  // ─── styled alert helper ───
  function showMessage(text, type, cb) {
    msgDiv.innerHTML = '';
    msgDiv.style.display = 'flex';
    msgDiv.classList.remove('add-expense-message-success','add-expense-message-danger');

    if (type === 'success') {
      msgDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${text}`;
      msgDiv.classList.add('add-expense-message-success');
    } else {
      msgDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${text}`;
      msgDiv.classList.add('add-expense-message-danger');
    }

    setTimeout(() => {
      msgDiv.style.display = 'none';
      if (typeof cb === 'function') cb();
    }, 5000);
  }

  // ─── rebuild the table ───
  function updateTable(data) {
    tbody.innerHTML = '';

    const summary = data.category_expenses;
    if (!summary || !Object.keys(summary).length) {
      tbody.innerHTML = '<tr><td colspan="3">No expenses found.</td></tr>';
    } else {
      Object.entries(summary).forEach(([cat, vals]) => {
        tbody.insertAdjacentHTML('beforeend', `
          <tr>
            <td>${cat}</td>
            <td>${vals.recent}</td>
            <td>${vals.total}</td>
          </tr>
        `);
      });
      // footer row
      tbody.insertAdjacentHTML('beforeend', `
        <tr class="expense-table-footer">
          <td>Total</td>
          <td>${data.total_recent_sum}</td>
          <td>${data.total_expense_sum}</td>
        </tr>
      `);
    }
  }

  // ─── AJAX form submit ───
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const fd = new FormData(form);
    const amt = parseFloat(fd.get('amount'));
    if (!amt || amt <= 0) {
      showMessage('Please enter a valid expense amount.', 'error');
      return;
    }

    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span class="spinner"></span> Adding...`;

    fetch(form.action, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': fd.get('csrfmiddlewaretoken'),
      },
      body: fd
    })
    .then(r => r.json())
    .then(json => {
      if (json.success) {
        showMessage(json.message, 'success', () => updateTable(json));
        form.reset();
      } else {
        showMessage(json.error||'Something went wrong.', 'error');
      }
    })
    .catch(() => showMessage('Network error. Try again.', 'error'))
    .finally(() => {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Add Expense';
    });
  });
});
