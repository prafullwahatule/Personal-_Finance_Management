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


      // Format bar labels from 'YYYY-MM' to 'Mon-YY'
      // Format month labels like "May-24"
      const formattedBarLabels = data.bar_labels.map(label => {
        const [year, month] = label.split('-');
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        return `${monthNames[parseInt(month, 10) - 1]}-${year.slice(2)}`;
      });
      
      // Income by Source - Pie Chart
      new Chart(document.getElementById('sourcePieChart').getContext('2d'), {
        type: 'pie',
        data: {
          labels: data.source_labels,
          datasets: [{
            label: 'Income by Source',
            data: data.source_amounts,
            backgroundColor: [
              '#66bb6a', '#81c784', '#a5d6a7',
              '#43a047', '#2e7d32', '#1b5e20',
              '#4caf50', '#388e3c'
            ],
            borderColor: 'rgb(59, 59, 59)',
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
              backgroundColor: '#2e7d32',
              titleColor: '#ffffff',
              bodyColor: '#ffffff',
              borderColor: '#81c784',
              borderWidth: 1
            }
          }
        }
      });
      
      // Entries Per Month - Bar Chart
      new Chart(document.getElementById('entryBarChart').getContext('2d'), {
        type: 'bar',
        data: {
          labels: formattedBarLabels,
          datasets: [{
            label: 'Entries Per Month',
            data: data.bar_values,
            backgroundColor: '#66bb6a',
            borderColor: 'rgb(59, 59, 59)',
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
              grid: { color: '#4caf5055' }
            },
            x: {
              ticks: { color: '#ffffff' },
              grid: { color: '#4caf5033' }
            }
          },
          plugins: {
            legend: {
              labels: {
                color: '#ffffff'
              }
            },
            tooltip: {
              backgroundColor: '#388e3c',
              titleColor: '#ffffff',
              bodyColor: '#ffffff',
              borderColor: '#81c784',
              borderWidth: 1
            }
          }
        }
      });
      

    })
    .catch(err => console.error("Error fetching income analysis data:", err));
});
