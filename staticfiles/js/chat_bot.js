document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInputField = document.getElementById("user-input");
  const sendButton = document.getElementById("send-btn");
  const chatIcon = document.getElementById("chat-icon");
  const chatPopup = document.getElementById("chat-popup");

  const steps = {
    start: [
      { text: "📊 Investment Advice", next: "investment_advice" },
      { text: "💰 SIP & Mutual Funds", next: "sip_mutual_funds" },
      { text: "📈 Stock Market Insights", next: "stock_market" },
      { text: "📉 Expense Tracking", next: "expense_tracking" },
      { text: "📞 Contact Financial Advisor", next: "contact_advisor" }
    ],
    
    investment_advice: [
      { text: "🤔 How much should I invest?", next: "investment_amount" },
      { text: "📌 Best investment options?", next: "best_investments" }
    ],
    investment_amount: "📊 Your investment amount depends on your income and expenses. Use our 'Investment Planner' tool for personalized advice.",
    best_investments: "📌 The best investments depend on your risk appetite. Consider Mutual Funds, SIPs, or Stocks for long-term growth.",
    
    sip_mutual_funds: [
      { text: "📅 Best SIP plans?", next: "best_sip_plans" },
      { text: "💳 How to start SIP?", next: "start_sip" }
    ],
    best_sip_plans: "📅 Based on historical performance, some top-performing SIPs are XYZ Growth Fund, ABC Equity Fund, etc.",
    start_sip: "💳 You can start an SIP by opening an account with a brokerage platform or a mutual fund house.",
    
    stock_market: [
      { text: "📈 Top Gainers & Losers", next: "market_gainers_losers" },
      { text: "📊 Live Market Data", next: "live_market_data" }
    ],
    market_gainers_losers: "📈 You can check the top gainers and losers on our 'Market Updates' page.",
    live_market_data: "📊 Live market data is updated every minute in our dashboard section.",
    
    expense_tracking: "📉 Use our Expense Tracker to monitor your spending and optimize your financial goals.",
    contact_advisor: "📞 Contact our financial advisor via email or phone for personalized investment guidance."
  };

  function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
      if (cookie.startsWith(name + "=")) {
        return cookie.split("=")[1];
      }
    }
    return "";
  }

  function addBotMessage(text, callback) {
    let message = document.createElement("p");
    message.className = "bot-message";
    chatBox.appendChild(message);
    typeMessage(text, message, callback);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function addOptions(options) {
    let card = document.createElement("div");
    card.className = "option-card";
    options.forEach(option => {
      let btn = document.createElement("div");
      btn.className = "option";
      btn.innerText = option.text;
      btn.onclick = () => handleUserChoice(option.next);
      card.appendChild(btn);
    });
    chatBox.appendChild(card);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function handleUserChoice(choice) {
    let userMessage = document.createElement("p");
    userMessage.className = "user-message";
    userMessage.innerText = choice.replace(/_/g, ' ');
    chatBox.appendChild(userMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    setTimeout(() => {
      if (typeof steps[choice] === "string") {
        addBotMessage(steps[choice], () => addOptions(steps.start));
      } else {
        addOptions(steps[choice]);
      }
    }, 500);
  }

  function typeMessage(text, element, callback) {
    let index = 0;
    let interval = setInterval(() => {
      if (index < text.length) {
        element.innerText += text[index];
        index++;
      } else {
        clearInterval(interval);
        if (callback) callback();
      }
    }, 30);
  }

  function sendMessage() {
    let userInput = userInputField.value.trim();
    if (userInput === "") return;

    let userMessage = document.createElement("p");
    userMessage.className = "user-message";
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    userInputField.value = "";

    fetch("/dashboard/chatbot/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      },
      body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
      if (data.response) {
        addBotMessage(data.response);
      } else {
        addBotMessage("🤖 Sorry, I didn't get a proper response.");
      }
    })
    .catch(error => {
      console.error("Error:", error);
      addBotMessage("⚠️ Server error. Please try again later.");
    });
  }

  // Show chat popup on chat icon click
  chatIcon.addEventListener("click", (event) => {
    event.stopPropagation();
    chatPopup.style.display = "block";
  });

  // Close chat popup if clicked outside
  document.addEventListener("click", (event) => {
    if (!chatPopup.contains(event.target) && event.target !== chatIcon) {
      chatPopup.style.display = "none";
    }
  });

  // Prevent popup closing when clicking inside popup
  chatPopup.addEventListener("click", (event) => {
    event.stopPropagation();
  });

  // Send message on button click or Enter key press
  sendButton.addEventListener("click", sendMessage);
  userInputField.addEventListener("keypress", (event) => {
    if (event.key === "Enter") sendMessage();
  });

  // Initial greeting and options
  addBotMessage("🤖 Hello! How can I assist you with your finances today?", () => addOptions(steps.start));
});
