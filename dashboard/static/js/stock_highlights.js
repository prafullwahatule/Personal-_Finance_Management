let isFirstLoad = true;

function fetchStockHighlights() {
  const loader = document.getElementById('loading-stock');
  const errorMsg = document.getElementById('stock-error-msg');

  // Show loader only on first load
  if (isFirstLoad) {
    loader.style.display = 'block';
    errorMsg.style.display = 'none'; // ✅ Hide error initially
    document.getElementById('most-active').style.display = 'none';
    document.getElementById('fifty-two-week').style.display = 'none';
    document.getElementById('trending').style.display = 'none';
  }

  fetch('/dashboard/get_stock_highlights/')
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      // ✅ Hide loader and error message after successful fetch
      loader.style.display = 'none';
      errorMsg.style.display = 'none';

      // Show sections only once
      if (isFirstLoad) {
        document.getElementById('most-active').style.display = 'block';
        document.getElementById('fifty-two-week').style.display = 'block';
        document.getElementById('trending').style.display = 'block';
        isFirstLoad = false;
      }

      // Clear existing data
      document.getElementById('most-active-list').innerHTML = '';
      document.getElementById('fifty-two-week-list').innerHTML = '';
      document.getElementById('trending-list').innerHTML = '';

      // 🔥 Most Active
      data.most_active.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${item.symbol}</td>
          <td>₹${item.price}</td>
          <td>${item.volume}</td>
        `;
        document.getElementById('most-active-list').appendChild(row);
      });

      // 📈 52-Week High/Low
      data.fifty_two_week.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${item.symbol}</td>
          <td>₹${item.price}</td>
          <td>₹${item.high_52}</td>
          <td>₹${item.low_52}</td>
        `;
        document.getElementById('fifty-two-week-list').appendChild(row);
      });

      // 📡 Trending
      data.trending.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${item.symbol}</td>
          <td>₹${item.price}</td>
          <td>${item.price_change_pct}%</td>
          <td>x${item.volume_spike}</td>
        `;
        document.getElementById('trending-list').appendChild(row);
      });

      // Last updated time
      document.getElementById('last-updated').textContent = `⏱ Last Updated: ${data.last_updated}`;
    })
    .catch(error => {
      loader.style.display = 'none'; // ✅ Hide spinner
      errorMsg.style.display = 'block'; // ✅ Show error only on failure
      errorMsg.innerHTML = "⚠️ Failed to load stock highlights. Retrying in 15s...";
      console.error("Error fetching stock highlights:", error);
      setTimeout(fetchStockHighlights, 15000);
    });
}

document.addEventListener("DOMContentLoaded", fetchStockHighlights);
setInterval(fetchStockHighlights, 60000);
