document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("expense-form");
  const submitButton = form.querySelector(".submit-btn");

  form.addEventListener("submit", function (e) {
    const amountInput = form.querySelector("input[name='amount']");

    // ❌ Validation failed
    if (!amountInput.value || parseFloat(amountInput.value) <= 0) {
      showAddExpenseMessage("❌ Please enter a valid amount.", "error");
      e.preventDefault();
      return;
    }

    // ✅ Disable submit button
    submitButton.disabled = true;
    submitButton.textContent = "Adding...";

    // ✅ Optional UX delay
    setTimeout(() => {
      submitButton.textContent = "Added!";
      // ✅ Show success message (you can optionally call from backend AJAX success)
      showAddExpenseMessage("✅ Expense added successfully!", "success");
    }, 300);
  });
});

// ✅ Show message function
function showAddExpenseMessage(message, type = 'success') {
  const messageBox = document.getElementById('add-expense-message');
  if (!messageBox) return;

  // Clean old state
  messageBox.classList.remove('expense-alert-success', 'expense-alert-danger');

  // Apply new class
  messageBox.classList.add(type === 'success' ? 'expense-alert-success' : 'expense-alert-danger');
  messageBox.textContent = message;
  messageBox.style.display = 'flex'; // Because CSS uses flexbox

  // Auto-hide after 5 seconds
  setTimeout(() => {
    messageBox.style.display = 'none';
  }, 5000);
}
