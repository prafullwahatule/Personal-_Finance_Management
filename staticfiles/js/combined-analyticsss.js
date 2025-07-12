document.addEventListener("DOMContentLoaded", function () {
  const API_URL = "/dashboard/combined-analysis/";

  let monthlyCashFlowChart, budgetActualChart, spendSaveInvestChart;

  function fetchCombinedAnalysis() {
    fetch(API_URL, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      credentials: "same-origin",
    })
      .then((res) => {
        if (!res.ok) throw new Error("Network response not ok");
        return res.json();
      })
      .then((data) => {
        if (data.error) {
          alert("Error: " + data.error);
          return;
        }
        updateDashboard(data);
      })
      .catch((err) => {
        console.error(err);
        alert("Failed to fetch data from server.");
      });
  }

  function updateDashboard(data) {
    document.getElementById("total-income").textContent = `₹${Number(data.total_income).toLocaleString()}`;
    document.getElementById("total-expense").textContent = `₹${Number(data.total_expense).toLocaleString()}`;
    document.getElementById("income-expense-ratio").textContent = Number(data.income_expense_ratio).toFixed(2);
    document.getElementById("budget-accuracy-score").textContent = Number(data.budget_accuracy_score).toFixed(2) + "%";

    const monthlyCashFlowArray = Object.entries(data.monthly_cash_flow)
      .map(([month, values]) => ({
        month,
        income: Number(values.income),
        expense: Number(values.expense),
        net: Number(values.income) - Number(values.expense),
      }))
      .sort((a, b) => {
        const parseDate = (str) => {
          const [mon, yr] = str.split(" ");
          return new Date(`20${yr}`, ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].indexOf(mon), 1);
        };
        return parseDate(a.month) - parseDate(b.month);
      });

    drawMonthlyCashFlowChart(monthlyCashFlowArray);
    drawBudgetVsActualChart(data.budget_vs_actual);
    drawSpendSaveInvestChart(
      {
        spend: Number(data.ideal_vs_actual_ratio.ideal.spend),
        save: Number(data.ideal_vs_actual_ratio.ideal.save),
        invest: Number(data.ideal_vs_actual_ratio.ideal.invest),
      },
      {
        spend: parseFloat(data.ideal_vs_actual_ratio.actual.spend),
        save: parseFloat(data.ideal_vs_actual_ratio.actual.save),
        invest: parseFloat(data.ideal_vs_actual_ratio.actual.invest),
      }
    );
  }

  function chartCommonOptions() {
    return {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: "#ffffff",
            font: {
              size: 13,
              family: "Arial",
            },
          },
        },
        tooltip: {
          enabled: true,
          backgroundColor: "#333",
          titleColor: "#fff",
          bodyColor: "#fff",
        },
      },
      scales: {
        x: {
          ticks: {
            color: "#ffffff",
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: "#ffffff",
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
        },
      },
    };
  }

  function drawMonthlyCashFlowChart(data) {
    const ctx = document.getElementById("monthlyCashFlowChart").getContext("2d");

    if (monthlyCashFlowChart) monthlyCashFlowChart.destroy();

    monthlyCashFlowChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: data.map((d) => d.month),
        datasets: [
          {
            label: "Income",
            data: data.map((d) => d.income),
            borderColor: "#4caf50",
            backgroundColor: "rgba(76, 175, 80, 0.3)",
            fill: true,
            tension: 0.4,
          },
          {
            label: "Expense",
            data: data.map((d) => d.expense),
            borderColor: "#e53935",
            backgroundColor: "rgba(229, 57, 53, 0.3)",
            fill: true,
            tension: 0.4,
          },
        ],
      },
      options: chartCommonOptions(),
    });
  }

  function drawBudgetVsActualChart(data) {
    const ctx = document.getElementById("budgetActualChart").getContext("2d");

    if (budgetActualChart) budgetActualChart.destroy();

    budgetActualChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: data.map((d) => d.category),
        datasets: [
          {
            label: "Budget",
            data: data.map((d) => d.budget),
            backgroundColor: "#1e88e5",
          },
          {
            label: "Actual",
            data: data.map((d) => d.actual),
            backgroundColor: "#ef5350",
          },
        ],
      },
      options: chartCommonOptions(),
    });
  }

  function drawSpendSaveInvestChart(ideal, actual) {
    const ctx = document.getElementById("spendSaveInvestChart").getContext("2d");

    if (spendSaveInvestChart) spendSaveInvestChart.destroy();

    spendSaveInvestChart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Spend", "Save", "Invest"],
        datasets: [
          {
            label: "Ideal Ratio",
            data: [ideal.spend, ideal.save, ideal.invest],
            backgroundColor: ["#fdd835", "#43a047", "#1e88e5"],
            borderColor: 'rgb(59, 59, 59)',
            borderWidth: 2,
          },
          {
            label: "Actual Ratio",
            data: [actual.spend, actual.save, actual.invest],
            backgroundColor: ["#fff176", "#81c784", "#64b5f6"],
            borderColor: 'rgb(59, 59, 59)',
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        cutout: "60%",
        plugins: {
          legend: {
  position: "bottom",
  labels: {
    color: "#ffffff", // fallback
    generateLabels(chart) {
      const labels = [];

      chart.data.labels.forEach((label, i) => {
        labels.push({
          text: `Ideal - ${label}`,
          fillStyle: chart.data.datasets[0].backgroundColor[i],
          strokeStyle: 'rgb(59, 59, 59)',
          lineWidth: 1,
          hidden: false,
          index: i,
          fontColor: "#ffffff", // optional
          font: {
            size: 12,
            weight: "bold",
            lineHeight: 1.2,
            color: "#ffffff" // ✅ Legend text color
          }
        });
      });

      chart.data.labels.forEach((label, i) => {
        labels.push({
          text: `Actual - ${label}`,
          fillStyle: chart.data.datasets[1].backgroundColor[i],
          strokeStyle: 'rgb(59, 59, 59)',
          lineWidth: 1,
          hidden: false,
          index: i,
          font: {
            size: 12,
            weight: "bold",
            lineHeight: 1.2,
            color: "#ffffff" // ✅ Legend text color for Actual
          }
        });
      });

      return labels;
    }
  }
},

      
          tooltip: {
            enabled: true,
            backgroundColor: "#333",
            titleColor: "#ffffff",
            bodyColor: "#eeeeee", // ya "#fff" as per your theme
          },
        },
      }

    });
  }

  fetchCombinedAnalysis();
});
