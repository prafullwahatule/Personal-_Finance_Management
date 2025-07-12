document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("expense-form");
  const submitButton = form.querySelector(".submit-btn");

  form.addEventListener("submit", function (e) {
    // Basic validation: check if amount is empty
    const amountInput = form.querySelector("input[name='amount']");
    if (!amountInput.value || parseFloat(amountInput.value) <= 0) {
      alert("Please enter a valid amount.");
      e.preventDefault();
      return;
    }

    // Disable submit button to prevent multiple submissions
    submitButton.disabled = true;
    submitButton.textContent = "Adding...";

    // Optionally add a slight delay to mimic a nice UX
    setTimeout(() => {
      submitButton.textContent = "Added!";
    }, 300);
  });
});
