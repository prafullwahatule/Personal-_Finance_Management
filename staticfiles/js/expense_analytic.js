document.addEventListener("DOMContentLoaded", function () {
  fetch("/dashboard/expense-analysis/")
    .then((response) => response.json())
    .then((data) => {
      renderExpenseCards(data);
      renderCategoryPieChart(data);
      renderMonthlyBarChart(data);
      renderWeekdayChart(data);
      renderDayOfMonthChart(data);
    })
    .catch((error) => console.error("Error fetching expense data:", error));
});

// ------------------- Helper Functions -------------------

function renderExpenseCards(data) {
  const cardContainer = document.querySelector(".expense-cards");
  cardContainer.innerHTML = `
    <div class="expense-card">
      <div class="label">Total Expenses</div>
      <div class="value">₹${(data.total_expense || 0).toLocaleString("en-IN")}</div>
    </div>
    <div class="expense-card">
      <div class="label">Most Spent Category (${data.highest_category?.category || '—'})</div>
      <div class="value">₹${(data.highest_category?.total || 0).toLocaleString("en-IN")}</div>
    </div>
    <div class="expense-card">
      <div class="label">Least Spent Category (${data.lowest_category?.category || '—'})</div>
      <div class="value">₹${(data.lowest_category?.total || 0).toLocaleString("en-IN")}</div>
    </div>
    <div class="expense-card">
      <div class="label">Avg Entry/Month</div>
      <div class="value">${(data.avg_entry_frequency || 0).toLocaleString("en-IN")}</div>
    </div>
  `;
  
}
function renderCategoryPieChart(data) {
  new Chart(document.getElementById("categoryPieChart"), {
    type: "pie",
    data: {
      labels: data.category_labels,
      datasets: [{
        data: data.category_totals,
        backgroundColor: [
          "#d32f2f", // Deep Red
          "#b71c1c", // Darker Red
          "#ff7043", // Soft Red/Orange
          "#e57373", // Light Red
          "#f44336", // Material Red
          "#ef5350"  // Medium Red
        ],
        borderColor: 'rgb(59, 59, 59)', // white border for clarity
        borderWidth: 2,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { position: "bottom", labels: { color: 'white' } } },
    },
  });
}

function renderMonthlyBarChart(data) {
  new Chart(document.getElementById("monthlyBarChart"), {
    type: "bar",
    data: {
      labels: data.bar_labels,
      datasets: [{
        label: "Monthly Expense",
        data: data.bar_values,
        backgroundColor: "#d32f2f",
        borderColor: "#b71c1c",
        borderWidth: 1,
      }],
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true, ticks: { color: '#b71c1c' } },
        x: { ticks: { color: '#b71c1c' } }
      },
      plugins: {
        legend: { labels: { color: '#b71c1c' } }
      }
    },
  });
}

function renderWeekdayChart(data) {
  new Chart(document.getElementById("weekdayChart"), {
    type: "bar",
    data: {
      labels: data.weekday_labels,
      datasets: [{
        label: "Spending by Weekday",
        data: data.weekday_data,
        backgroundColor: "#d32f2f",
        borderColor: "#b71c1c",
        borderWidth: 1,
      }],
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true, ticks: { color: '#ffffff'}, grid: { color: 'rgba(211, 47, 47, 0.43)' } },
        x: { ticks: { color: '#ffffff' }, grid: { color: 'rgba(211, 47, 47, 0.43)' } }
      },
      plugins: {
        legend: { labels: { color: '#ffffff' }, }
      }
    },
  });
}

function renderDayOfMonthChart(data) {
  new Chart(document.getElementById("domChart"), {
    type: "line",
    data: {
      labels: data.dom_labels,
      datasets: [{
        label: "Spending by Day of Month",
        data: data.dom_data,
        fill: false,
        borderColor: "#d32f2f",
        backgroundColor: "#ef5350",
        tension: 0.3,
        pointBackgroundColor: "#b71c1c",
        pointBorderColor: "#b71c1c",
      }],
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true, ticks: { color: '#ffffff' }, grid: { color: 'rgba(211, 47, 47, 0.43)' } },
        x: { ticks: { color: '#ffffff' }, grid: { color: 'rgba(211, 47, 47, 0.43)' } }
      },
      plugins: {
        legend: { labels: { color: '#ffffff' } }
      }
    },
  });
}
