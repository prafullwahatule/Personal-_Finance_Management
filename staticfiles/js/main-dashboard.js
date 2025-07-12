async function fetchAndRenderList(url, elementId, dataKey) {
  const list = document.getElementById(elementId);

  // Optional: loader logic if you want to show spinner
  const loader = list.nextElementSibling;
  if (loader) loader.style.display = 'block';

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('Network response was not ok');

    const data = await response.json();
    list.innerHTML = ''; // Clear previous content

    const items = data[dataKey];
    if (Array.isArray(items) && items.length > 0) {
      items.forEach(item => {
        const li = document.createElement('li');

        // ✅ Custom rendering for Mutual Funds
        if (elementId === 'mutual-fund-list') {
          li.innerHTML = `
            <strong>${item.scheme_name}</strong><br>
            <span>Start NAV: ₹${item.start_nav}</span><br>
            <span>Latest NAV: ₹${item.latest_nav}</span><br>
          `;
        } else {
          // 🔁 Default rendering for stocks/crypto/commodities
          const symbol = item.symbol || item.name || 'Unnamed';
          const price = item.predictions ? item.predictions['1_month'] : 'N/A';
          const three_price = item.predictions ? item.predictions['3_months'] : 'N/A';
          li.innerHTML = `
            <strong>${symbol}</strong><br>
            <span>Price (1 Month): ₹${price}</span><br>
            <span>Price (3 Month): ₹${three_price}</span><br>
          `;
        }

        list.appendChild(li);
      });
    } else {
      const li = document.createElement('li');
      li.textContent = 'No data available';
      list.appendChild(li);
    }

  } catch (error) {
    console.error(`Error fetching ${elementId}:`, error);
    list.innerHTML = '<li>Error loading data</li>';
  } finally {
    if (loader) loader.style.display = 'none';
  }
}


// Call all APIs on DOM load
document.addEventListener('DOMContentLoaded', () => {
  fetchAndRenderList('/dashboard/suggest_top_stocks_api/', 'stock-list', 'suggested_stocks');
  fetchAndRenderList('/dashboard/suggest_top_cryptos_api/', 'crypto-list', 'suggested_cryptos');
  fetchAndRenderList('/dashboard/api/suggest_top_commodities/', 'commodity-list', 'suggested_commodities');
  fetchAndRenderList('/dashboard/api/suggest-top-mutual-funds/', 'mutual-fund-list', 'suggested_mutual_funds');
});




// this js for the compare button
document.addEventListener("DOMContentLoaded", function () {
  const compareBtn = document.getElementById("compare-btn");

  if (compareBtn) {
    compareBtn.addEventListener("click", function () {
      const assetType = document.getElementById("asset-type").value;
      const symbols = document.getElementById("asset-symbols").value.trim();

      if (!symbols) {
        alert("Please enter some asset symbols.");
        return;
      }

      fetch(`/dashboard/api/compare-assets/?asset_type=${assetType}&symbols=${symbols}`)
        .then(response => response.json())
        .then(data => {
          const resultsDiv = document.getElementById("comparison-results");
          resultsDiv.innerHTML = ""; // Clear previous results

          if (data.status === "success") {
            data.results.forEach(asset => {
              const predictionsHTML = Object.entries(asset.predictions || {})
                .map(([key, value]) => `<li>${key}: ₹${value}</li>`)
                .join("");

              const card = `
                <div class="card p-3 mb-2 shadow-sm">
                  <h5>${asset.symbol}</h5>
                  <p>📈 Latest Price: ₹${asset.latest_price || 'N/A'}</p>
                  <ul>${predictionsHTML}</ul>
                </div>
              `;
              resultsDiv.innerHTML += card;
            });
          } else {
            resultsDiv.innerHTML = `<p class="text-danger">Error: ${data.message}</p>`;
          }
        })
        .catch(error => {
          console.error("Error fetching comparison data:", error);
          document.getElementById("comparison-results").innerHTML =
            `<p class="text-danger">Something went wrong. Try again later.</p>`;
        });
    });
  }
});








// bhai aab iske bad ki js expence advices ki hai 

