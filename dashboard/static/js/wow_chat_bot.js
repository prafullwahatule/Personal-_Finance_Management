document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInputField = document.getElementById("user-input");
  const sendButton = document.getElementById("send-btn");
  const chatIcon = document.getElementById("chat-icon");
  const chatPopup = document.getElementById("chat-popup");

  const steps = {
    start: [
      { text: "📊 Profile Management", next: "Profile_Select_Field" },
      { text: "📉 Expense Tracking", next: "Get_expense_overview" },
      { text: "📈 Income Tracking", next: "Get_income_overview" },
      { text: "📈 Budget Management", next: "Manage_Your_budget" },
      { text: "📄 Guide me to export my report", next: "guide_generate_report" },
      { text: "📞 Contact Financial Advisor", next: "Contact_Advisor" }
    ],

    Contact_Advisor: {
      message: "📞 You can contact our financial advisor via email at advisor@example.com or call us at +91-9876543210 for personalized investment guidance. We're here to help!",
      reprompt: true // Indicates that after this message, the start options should be shown again
    },

    Profile_Select_Field: [
      { text: "🔍 View Profile Info", next: "Profile_Summery_Field" },
      { text: "✏️ Update Profile Info", next: "Profile_Update_Field" }
    ],

    Profile_Summery_Field: [
      { text: "📱 What is my mobile number?", next: "get_mobile" },
      { text: "🎂 What is my date of birth?", next: "get_dob" },
      { text: "🚻 What is my gender?", next: "get_gender" },
      { text: "💰 Show my savings amount", next: "get_savings" },
      { text: "🏦 How much have I invested?", next: "get_existing_investments" },
      { text: "📉 What is my risk appetite?", next: "get_risk_appetite" },
      { text: "🎯 What are my investment goals?", next: "get_investment_goals" },
      { text: "📋 What are my preferred investments?", next: "get_preferred_investments" },
      { text: "🛠️ Show my full profile summary", next: "get_profile_summary" }
    ],

    Profile_Update_Field: [
      { text: "📱 How do I update my mobile number?", next: "guide_update_mobile" },
      { text: "🎂 How to update date of birth?", next: "guide_update_dob" },
      { text: "🚻 How to update my gender?", next: "guide_update_gender" },
      { text: "💰 How to edit savings info?", next: "guide_update_savings" },
      { text: "🏦 How to update existing investments?", next: "guide_update_existing_investments" },
      { text: "📉 How to update risk appetite?", next: "guide_update_risk_appetite" },
      { text: "🎯 How do I update investment goals?", next: "guide_update_investment_goals" },
      { text: "📋 How to update preferred investments?", next: "guide_update_preferred_investments" },
      { text: "🛠️ How do I update my profile?", next: "guide_update_profile" },
      { text: "🗑️ How do I delete my account?", next: "guide_delete_account" }
    ],

    Get_expense_overview: [
      { text: "💸 Know Your Expense Summary", next: "Expense_Summery" },
      { text: "➕ How do I add an expense?", next: "guide_add_expense" },
      { text: "🗑️ How do I delete an expense?", next: "guide_delete_expense" }
    ],

    Expense_Summery: [
      { text: "📊 What is my total expense?", next: "get_total_expense" },
      { text: "📅 How much did I spend this month?", next: "get_total_expense" },
      { text: "📆 Show my total yearly expense", next: "get_total_expense" },
      { text: "🗓️ How much did I spend in January?", next: "get_total_expense" },
      { text: "📈 Tell me expenses for 2024", next: "get_total_expense" }
    ],

    Get_income_overview: [
      { text: "💰 Know Your Income Overview", next: "Income_Summery" },
      { text: "➕ How do I add income?", next: "guide_add_income" },
      { text: "🗑️ How do I delete income?", next: "guide_delete_income" }
    ],

    Income_Summery: [
      { text: "💰 What is my total income?", next: "query_total_income" },
      { text: "📅 How much did I earn this month?", next: "query_monthly_income" },
      { text: "📆 Show my total yearly income", next: "query_yearly_income" },
      { text: "🗓️ How much did I earn in January?", next: "query_income_january" },
      { text: "📈 Tell me income for 2024", next: "query_income_2024" }
    ],

    Manage_Your_budget: [
      { text: "🔍 View My Budget Limits", next: "Get_Budget_Limits" },
      { text: "📝 How do I set a budget limit?", next: "guide_set_budget_limit" },
      { text: "🗑️ How do I delete a budget limit?", next: "guide_delete_budget_limit" }
    ],

    Get_Budget_Limits: [
      { text: "📆 What is my total monthly budget limit?", next: "get_budget_limit" },
      { text: "📅 What is my total annual budget limit?", next: "get_budget_limit" },
      { text: "🍽️ Show me my annual budget for food", next: "get_budget_limit" },
      { text: "💡 Show me my monthly budget for utilities", next: "get_budget_limit" },
      { text: "🧾 What is my budget for other?", next: "get_budget_limit" }
    ],


    // Fallback for unrecognized commands or general queries
    fallback: {
      message: "🤖 I'm sorry, I didn't understand that. Please choose from the options above or ask a different question.",
      reprompt: true
    },
    // Add specific messages for common queries that don't need a backend trip for a simple response
    query_mobile_number: {
      message: "✅ Your mobile number is: **7875789496**", // This should ideally come from backend
      reprompt: true // After showing the info, go back to main menu
    },
    query_dob: {
      message: "✅ Your date of birth is: **29 January 2020**", // This should ideally come from backend
      reprompt: true
    },
    query_full_profile: {
      message: "🛠️ Your profile was last updated on **13 June 2025, 10:43 AM** (2 hours, 23 minutes ago).",
      reprompt: true
    }
    // ... you can add more direct responses here if they don't need a backend lookup
  };

  // Helper function to add bot messages to the chat box
  function addBotMessage(text, callback) {
    let message = document.createElement("p");
    message.className = "bot-message";
    chatBox.appendChild(message);
    typeMessage(text, message, callback); // Use typing effect for bot messages
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
  }

  // Helper function to add interactive options as cards
  function addOptions(options) {
    let card = document.createElement("div");
    card.className = "option-card";
    options.forEach(option => {
      let btn = document.createElement("div");
      btn.className = "option";
      btn.innerText = option.text;
      // Pass both key and display text to handleUserChoice
      btn.onclick = () => handleUserChoice(option.next, option.text);
      card.appendChild(btn);
    });
    chatBox.appendChild(card);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Handles user's choice from the options
  function handleUserChoice(choiceKey, displayText = null) {
    // Determine the text to display in the user message
    const userMessageText = displayText || choiceKey.replace(/_/g, ' ');

    // Add user's message to the chat box
    let userMessageElement = document.createElement("p");
    userMessageElement.className = "user-message";
    userMessageElement.innerText = userMessageText;
    chatBox.appendChild(userMessageElement);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Process the next step based on the choiceKey directly from `steps`
    // This handles navigation within the static `steps` structure
    if (typeof steps[choiceKey] === "string") {
      // Direct string message (e.g., old Contact_Advisor) - though now Contact_Advisor is an object
      addBotMessage(steps[choiceKey], () => addOptions(steps.start));
    } else if (typeof steps[choiceKey] === "object" && steps[choiceKey].message) {
      // If it's an object with a message property (like Contact_Advisor or query_mobile_number directly in JS)
      addBotMessage(steps[choiceKey].message, () => {
        if (steps[choiceKey].reprompt) {
          addOptions(steps.start); // Show start options if reprompt is true
        }
      });
    } else if (Array.isArray(steps[choiceKey])) {
      // If it's an array of options (a new menu)
      addOptions(steps[choiceKey]);
    } else {
      // If it's a 'query_' or 'update_' key, we rely on the backend for the response.
      // Send the display text to backend and let backend drive the next response/options.
      sendToBackend(userMessageText);
    }
  }

  // Typing effect for bot messages
  function typeMessage(text, element, callback) {
    let index = 0;
    let interval = setInterval(() => {
      if (index < text.length) {
        element.innerHTML += text[index]; // Use innerHTML to allow for bold markdown
        index++;
      } else {
        clearInterval(interval);
        if (callback) callback();
      }
    }, 30); // Typing speed
  }

  // Handles sending a free-text message from the user
  function sendMessage() {
    let userInput = userInputField.value.trim();
    if (userInput === "") return;

    let userMessage = document.createElement("p");
    userMessage.className = "user-message";
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    userInputField.value = ""; // Clear the input field

    // Send the free-text input to the backend
    sendToBackend(userInput);

    // After sending free-text, we wait for the backend's response.
    // The backend should then decide what to say/show next.
  }

  // Sends the user message to the backend API
  function sendToBackend(userMessage) {
    fetch(`/dashboard/chatbot/?message=${encodeURIComponent(userMessage)}`, {
      method: "GET" // Assuming your backend expects GET requests for chatbot
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.response) {
        // If the backend sends a specific response, display it
        addBotMessage(data.response, () => {
          // After showing the backend's response, always offer the main options
          addOptions(steps.start);
        });
      } else {
        // Generic fallback if backend doesn't provide a specific response
        addBotMessage("🤖 I received your request. I'll process it shortly.", () => {
          addOptions(steps.start); // Offer main options
        });
      }
    })
    .catch(error => {
      console.error("Error sending message to backend:", error);
      addBotMessage("⚠️ Server error. Please try again later.", () => {
        addOptions(steps.start); // Offer main options even on error
      });
    });
  }

  // Event listeners for chat icon, popup behavior, send button, and enter key
  // In your existing JavaScript file
  chatIcon.addEventListener("click", (event) => {
    event.stopPropagation(); // Prevent document click from immediately closing
    chatPopup.style.display = "block";
  
    // Fetch the user's first name from the backend
    // *** CHANGE THIS URL TO YOUR NEW ENDPOINT ***
    fetch('/dashboard/api/get_user_first_name/') // This is the new URL
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        const userName = data.first_name || "there"; // Use "there" as a fallback if name isn't available
        addBotMessage(`🤖 Hey ${userName}! Ready to talk finances? How can I assist?`, () => addOptions(steps.start));
      })
      .catch(error => {
        console.error("Error fetching user info:", error);
        // Fallback greeting if user info can't be fetched
        addBotMessage("🤖 Hey there! Ready to talk finances? How can I assist?", () => addOptions(steps.start));
      });
  });
  
  document.addEventListener("click", (event) => {
    // Close popup if clicked outside
    if (!chatPopup.contains(event.target) && event.target !== chatIcon) {
      chatPopup.style.display = "none";
    }
  });

  chatPopup.addEventListener("click", (event) => {
    event.stopPropagation(); // Prevent popup click from closing itself
  });

  sendButton.addEventListener("click", sendMessage);
  userInputField.addEventListener("keypress", (event) => {
    if (event.key === "Enter") sendMessage();
  });

  // Initial greeting when the popup is opened
  // This line is moved inside chatIcon.addEventListener for better control of when the initial message appears.
});