document.addEventListener("DOMContentLoaded", function () {
  fetch("/dashboard/income-analysis/")
    .then(response => response.json())
    .then(data => {
      const cardsContainer = document.querySelector('.income-cards');
      cardsContainer.innerHTML = `
        <div class="income-card">
          <div class="label">Total Income</div>
          <div class="value">₹${Number(data.total_income).toLocaleString('en-IN')}</div>
        </div>
        <div class="income-card">
          <div class="label">Highest Source (${data.highest_source?.source || '—'})</div>
          <div class="value">₹${Number(data.highest_source?.total || 0).toLocaleString('en-IN')}</div>
        </div>
        <div class="income-card">
          <div class="label">Lowest Source (${data.lowest_source?.source || '—'})</div>
          <div class="value">₹${Number(data.lowest_source?.total || 0).toLocaleString('en-IN')}</div>
        </div>
        <div class="income-card">
          <div class="label">Avg Monthly Income</div>
          <div class="value">₹${Number(data.average_monthly_income).toLocaleString('en-IN')}</div>
        </div>
        <div class="income-card">
          <div class="label">Passive Income %</div>
          <div class="value">${Number(data.passive_ratio).toFixed(2)}%</div>
        </div>
        <div class="income-card">
          <div class="label">Avg Entries/Month</div>
          <div class="value">${Number(data.avg_entry_frequency).toFixed(1)}</div>
        </div>
      `;

      const formattedBarLabels = data.bar_labels.map(label => {
        const [year, month] = label.split('-');
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        return `${monthNames[parseInt(month, 10) - 1]}-${year.slice(2)}`;
      });

      // PIE CHART — Income by Source with % display
      new Chart(document.getElementById('sourcePieChart').getContext('2d'), {
        type: 'pie',
        data: {
          labels: data.source_labels,
          datasets: [{
            label: 'Income by Source',
            data: data.source_amounts,
            backgroundColor: [
              "#009688", // Refined Teal
              "#3f72af", // Muted Blue
              "#2c7a7b", // Blue-Green
              "#6b7280", // Slate Gray
              "#00695c", // Deep Teal
              "#95a5a6", // Soft Gray
              "#0f4c5c", // Slate Blue-Green
              "#5c677d"  // Muted Grayish Blue
            ],
            borderColor: '#999999',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                color: '#ffffff',
                boxWidth: 16,
                padding: 10
              }
            },
            tooltip: {
              backgroundColor: '#2c7a7b',
              titleColor: '#ffffff',
              bodyColor: '#ffffff',
              borderColor: '#009688',
              borderWidth: 1
            },
            datalabels: {
              color: '#ffffff',
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

      // BAR CHART — Entries Per Month
      new Chart(document.getElementById('entryBarChart').getContext('2d'), {
        type: 'bar',
        data: {
          labels: formattedBarLabels,
          datasets: [{
            label: 'Entries Per Month',
            data: data.bar_values,
            backgroundColor: '#009688',
            borderColor: '#00695c',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { color: '#ffffff' },
              grid: { color: 'rgba(0, 150, 136, 0.3)' }
            },
            x: {
              ticks: { color: '#ffffff' },
              grid: { color: 'rgba(0, 150, 136, 0.2)' }
            }
          },
          plugins: {
            legend: {
              labels: {
                color: '#ffffff'
              }
            },
            tooltip: {
              backgroundColor: '#2c7a7b',
              titleColor: '#ffffff',
              bodyColor: '#ffffff',
              borderColor: '#009688',
              borderWidth: 1
            }
          }
        }
      });

    })
    .catch(err => console.error("Error fetching income analysis data:", err));
});
