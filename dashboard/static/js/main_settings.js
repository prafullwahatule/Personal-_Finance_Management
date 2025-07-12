document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  if (!form) return;

  const emailInput   = document.getElementById("email");
  const mobileInput  = document.getElementById("mobileNumber");
  const savingsInput = document.getElementById("monthlySavings");
  const messageDiv   = document.getElementById("setting-message");

  // Store initial values
  const initialData = {
    email:     emailInput?.value,
    mobile:    mobileInput?.value,
    savings:   savingsInput?.value,
    preferred: [...form.querySelectorAll('input[name="preferredInvestmentType"]:checked')]
                  .map(cb => cb.value).sort().join(",")
  };

  // Real-time validity highlighting
  [emailInput, mobileInput, savingsInput].forEach(input => {
    if (!input) return;
    input.addEventListener("input", () => {
      input.style.borderColor = input.checkValidity() ? "green" : "red";
    });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Collect current values
    const currentData = {
      email:     emailInput?.value,
      mobile:    mobileInput?.value,
      savings:   savingsInput?.value,
      preferred: [...form.querySelectorAll('input[name="preferredInvestmentType"]:checked')]
                    .map(cb => cb.value).sort().join(",")
    };

    // Detect no-change
    const changed = Object.keys(initialData)
      .some(key => initialData[key] !== currentData[key]);

    if (!changed) {
      showMessage("No changes detected—please update something before submitting.", "error");
      return;
    }

    // Build FormData (including checkboxes)
    const formData = new FormData(form);
    formData.delete("preferredInvestmentType");
    currentData.preferred.split(",")
      .filter(Boolean)
      .forEach(val => formData.append("preferredInvestmentType", val));

    fetch(form.action, {
      method: "POST",
      headers: { "X-CSRFToken": getCSRFToken() },
      body: formData
    })
    .then(resp => {
      if (resp.ok) {
        showMessage("Profile updated successfully!", "success");
      } else {
        showMessage("Something went wrong—please try again.", "error");
      }
    })
    .catch(() => {
      showMessage("Network error—please try again.", "error");
    });
  });

  function showMessage(text, type) {
    // type: "success" or "error"
    messageDiv.innerHTML = "";
    messageDiv.style.display = "flex";
    messageDiv.classList.remove("setting-message-success", "setting-messagee-danger");

    if (type === "success") {
      messageDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${text}`;
      messageDiv.classList.add("setting-message-success");
    } else {
      messageDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${text}`;
      messageDiv.classList.add("setting-messagee-danger");
    }

    setTimeout(() => {
      messageDiv.style.display = "none";
      messageDiv.innerHTML = "";
      messageDiv.classList.remove("setting-message-success", "setting-messagee-danger");
      if (type === "success") {
        window.location.reload();
      }
    }, 5000);
  }

  function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");
    for (let c of cookies) {
      c = c.trim();
      if (c.startsWith(name + "=")) {
        return decodeURIComponent(c.substring(name.length + 1));
      }
    }
    return "";
  }
});
