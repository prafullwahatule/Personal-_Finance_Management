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
// PIE CHART: Category-wise Expense with % Display
function renderCategoryPieChart(data) {
  new Chart(document.getElementById("categoryPieChart"), {
    type: "pie",
    data: {
      labels: data.category_labels,
      datasets: [{
        data: data.category_totals,
        backgroundColor: [
          "#009688", // Refined Teal
          "#3f72af", // Muted Blue
          "#2c7a7b", // Blue-Green
          "#6b7280", // Slate Gray
          "#00695c", // Deep Teal
          "#95a5a6"  // Soft Gray
        ],
        borderColor: '#999999',
        borderWidth: 2,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: 'white' }
        },
        datalabels: {
          color: 'white',
          formatter: (value, ctx) => {
            let total = ctx.chart._metasets[0].total;
            let percentage = (value / total * 100).toFixed(1);
            return `${percentage}%`;
          },
          font: {
            weight: 'bold',
            size: 12
          }
        }
      }
    },
    plugins: [ChartDataLabels],
  });
}


// BAR CHART: Monthly Expense
function renderMonthlyBarChart(data) {
  new Chart(document.getElementById("monthlyBarChart"), {
    type: "bar",
    data: {
      labels: data.bar_labels,
      datasets: [{
        label: "Monthly Expense",
        data: data.bar_values,
        backgroundColor: "#009688",
        borderColor: "#00695c",
        borderWidth: 1,
      }],
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true, ticks: { color: '#009688' } },
        x: { ticks: { color: '#009688' } }
      },
      plugins: {
        legend: { labels: { color: '#009688' } }
      }
    },
  });
}


// BAR CHART: Weekday-wise Spending
function renderWeekdayChart(data) {
  new Chart(document.getElementById("weekdayChart"), {
    type: "bar",
    data: {
      labels: data.weekday_labels,
      datasets: [{
        label: "Spending by Weekday",
        data: data.weekday_data,
        backgroundColor: "#3f72af",
        borderColor: "#2c7a7b",
        borderWidth: 1,
      }],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: '#ffffff' },
          grid: { color: 'rgba(63, 114, 175, 0.3)' }
        },
        x: {
          ticks: { color: '#ffffff' },
          grid: { color: 'rgba(63, 114, 175, 0.3)' }
        }
      },
      plugins: {
        legend: { labels: { color: '#ffffff' } }
      }
    },
  });
}


// LINE CHART: Spending by Day of Month
function renderDayOfMonthChart(data) {
  new Chart(document.getElementById("domChart"), {
    type: "line",
    data: {
      labels: data.dom_labels,
      datasets: [{
        label: "Spending by Day of Month",
        data: data.dom_data,
        fill: false,
        borderColor: "#2c7a7b",
        backgroundColor: "#95a5a6",
        tension: 0.3,
        pointBackgroundColor: "#009688",
        pointBorderColor: "#009688",
      }],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: '#ffffff' },
          grid: { color: 'rgba(44, 122, 123, 0.3)' }
        },
        x: {
          ticks: { color: '#ffffff' },
          grid: { color: 'rgba(44, 122, 123, 0.3)' }
        }
      },
      plugins: {
        legend: { labels: { color: '#ffffff' } }
      }
    },
  });
}

