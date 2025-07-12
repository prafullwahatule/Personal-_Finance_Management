document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  if (!form) return;

  const emailInput = document.getElementById("email");
  const mobileInput = document.getElementById("mobileNumber");
  const savingsInput = document.getElementById("monthlySavings");
  const messageDiv = document.getElementById("formMessage");

  // ✅ Store initial values
  const initialData = {
    email: emailInput?.value,
    mobile: mobileInput?.value,
    savings: savingsInput?.value,
    preferred: [...form.querySelectorAll('input[name="preferredInvestmentType"]:checked')]
      .map(cb => cb.value).sort().join(",")
  };

  // ✅ Real-time validation
  [emailInput, mobileInput, savingsInput].forEach(input => {
    input.addEventListener("input", function () {
      this.style.borderColor = this.checkValidity() ? "green" : "red";
    });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // ✅ Get current values
    const currentData = {
      email: emailInput?.value,
      mobile: mobileInput?.value,
      savings: savingsInput?.value,
      preferred: [...form.querySelectorAll('input[name="preferredInvestmentType"]:checked')]
        .map(cb => cb.value).sort().join(",")
    };

    // ✅ Check for changes
    const isChanged = Object.keys(initialData).some(key => initialData[key] !== currentData[key]);

    if (!isChanged) {
      showMessage("⚠️ No changes detected. Please update something before submitting.", "error");
      return;
    }

    const formData = new FormData(form);

    // ✅ Handle checkbox group
    const selectedInvestments = currentData.preferred.split(",");
    formData.delete("preferredInvestmentType");
    selectedInvestments.forEach(value => formData.append("preferredInvestmentType", value));

    fetch(form.action, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": getCSRFToken()
      }
    })
    .then(response => {
      if (response.ok) {
        showMessage("✅ Profile updated successfully!", "success");

        // ✅ Refresh the page after a short delay
        setTimeout(() => {
          location.reload();
        }, 1200);
      } else {
        showMessage("❌ Something went wrong. Please try again.", "error");
      }
    })
    .catch(error => {
      console.error("Error:", error);
      showMessage("⚠️ Network error. Please try again.", "error");
    });
  });

  function showMessage(msg, type) {
    messageDiv.textContent = msg;
    messageDiv.className = `form-message ${type}`;
    messageDiv.style.display = "block";

    setTimeout(() => {
      messageDiv.textContent = "";
      messageDiv.className = "form-message";
    }, 6000);
  }

  function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
    return '';
  }
});
