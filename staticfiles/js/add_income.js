document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("income-form");
  const submitButton = form.querySelector(".submit-btn");

  form.addEventListener("submit", function (e) {
    // Basic validation: check if amount is empty or invalid
    const amountInput = form.querySelector("input[name='amount']");
    if (!amountInput.value || parseFloat(amountInput.value) <= 0) {
      alert("Please enter a valid income amount.");
      e.preventDefault();
      return;
    }

    // Disable submit button to prevent multiple submissions
    submitButton.disabled = true;
    submitButton.textContent = "Adding...";

    // Optional: UX delay and confirmation message
    setTimeout(() => {
      submitButton.textContent = "Added!";
    }, 300);
  });
});
