document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector(".sidebar");
    const toggleSidebar = document.querySelector(".sidebar-toggle");

    if (toggleSidebar) {
        toggleSidebar.addEventListener("click", function (event) {
            event.stopPropagation();
            sidebar.classList.toggle("active");
        });
    }

    document.addEventListener("click", function (event) {
        if (
            sidebar.classList.contains("active") &&
            !sidebar.contains(event.target) &&
            !toggleSidebar.contains(event.target)
        ) {
            sidebar.classList.remove("active");
        }
    });

    // Logout confirmation
    document.body.addEventListener("click", function (event) {
        const logoutLink = event.target.closest(".logout-link");
        if (logoutLink) {
            event.preventDefault();
            if (confirm("Are you sure you want to log out?")) {
                window.location.href = logoutLink.href;
            }
        }
    });
});







document.addEventListener('DOMContentLoaded', () => {
  const searchBox = document.querySelector('.search-box');
  const input = searchBox.querySelector('input');
  const icon = searchBox.querySelector('i');

  // Use existing div #searchResults for results container instead of creating dynamically
  const resultsContainer = document.getElementById('searchResults');

  // Sample static search data (replace with your dynamic data)
  const searchResultsData = [

    // This belows urls of income trackers
    { 
      name: 'Income Tracker', 
      url: '/dashboard/income/', 
      keywords: ['income', 'tracker', 'earnings', 'salary', 'monthly income', 'income overview'], 
      description: 'Monitor and analyze your income over time' 
    },
    { 
      name: 'Add Income Entry', 
      url: '/dashboard/add-income/', 
      keywords: ['add income', 'record earnings', 'add salary', 'income input'], 
      description: 'Add new income entries including source, amount, and date' 
    },
    { 
      name: 'Download Income Report (CSV)', 
      url: '/dashboard/income/', 
      keywords: ['download income csv', 'export income csv', 'csv report', 'income raw data'], 
      description: 'Download your income data in CSV format for spreadsheet processing' 
    },
    { 
      name: 'Download Income Report (Excel)', 
      url: '/dashboard/income/', 
      keywords: ['download income excel', 'export income excel', 'excel report', 'income spreadsheet'], 
      description: 'Export your income records in Excel format for detailed analysis' 
    },
    

    // This belows Urls of Expenses Tracker
    { 
      name: 'Expense Tracker', 
      url: '/dashboard/expenses/', 
      keywords: ['expense', 'tracker', 'spending', 'cost', 'expenses summary', 'view expenses'], 
      description: 'Track and analyze all your expenses in one place' 
    },
    { 
      name: 'Add New Expense', 
      url: '/dashboard/expenses/add/', 
      keywords: ['add expense', 'new expense', 'record spending', 'log expense', 'expense entry'], 
      description: 'Quickly add and record your new expense details' 
    },
    { 
      name: 'Manage Budget Limits', 
      url: '/dashboard/manage-budget-limits/', 
      keywords: ['budget limit', 'set budget', 'manage budget', 'spending limit', 'category limit'], 
      description: 'Define and manage budget limits for each spending category' 
    },
    { 
      name: 'Download Expense Report (CSV)', 
      url: '/dashboard/expenses/', 
      keywords: ['download expense csv', 'export expenses csv', 'csv expense report', 'expense data'], 
      description: 'Export your expense records in CSV format for data analysis' 
    },
    { 
      name: 'Download Expense Report (Excel)', 
      url: '/dashboard/expenses/', 
      keywords: ['download expense excel', 'export expenses excel', 'excel expense report', 'expense spreadsheet'], 
      description: 'Download your expenses in Excel format for better insights' 
    },
        

    // This belows url of Report
    { 
      name: 'Financial Reports',
      url: '/dashboard/report',
      keywords: ['reports', 'summary', 'analytics', 'financial data', 'report dashboard'],
      description: 'View and analyze your monthly, annual, and overall financial reports'
    },
    { 
      name: 'Download PDF Report',
      url: '/dashboard/report',
      keywords: ['pdf report', 'export pdf', 'download pdf', 'report in pdf'],
      description: 'Download your financial reports in printable PDF format'
    },
    { 
      name: 'Download Excel Report',
      url: '/dashboard/report',
      keywords: ['excel report', 'export excel', 'download excel', 'spreadsheet report'],
      description: 'Export your financial data into Excel format for analysis'
    },
    { 
      name: 'Download CSV Report',
      url: '/dashboard/report',
      keywords: ['csv report', 'export csv', 'download csv', 'raw data report'],
      description: 'Download reports in CSV format for raw data access and custom processing'
    },
    
    

    // This belows urls of Dashboard
    {
      name: 'Main Dashboard Overview',
      url: '/dashboard/',
      keywords: ['dashboard', 'overview', 'home', 'main', 'summary', 'finance'],
      description: 'Get a bird’s-eye view of your income, expenses, and key financial insights'
    },
    {
      name: 'Income Analysis',
      url: '/dashboard/',
      keywords: ['income analysis', 'earnings overview', 'salary trends', 'revenue insights'],
      description: 'Analyze your income streams, trends, and monthly earning patterns'
    },
    {
      name: 'Expense Analysis',
      url: '/dashboard/',
      keywords: ['expense analysis', 'spending patterns', 'cost trends', 'where money goes'],
      description: 'Track, categorize, and understand your spending behavior'
    },
    {
      name: 'Combined Financial Overview',
      url: '/dashboard/',
      keywords: ['income vs expense', 'financial health', 'budget summary', 'spending vs savings'],
      description: 'Compare income and expenses to get a clear view of your financial balance'
    },
    {
      name: 'Smart Investment Advisor',
      url: '/dashboard/',
      keywords: [
        'advisor', 'investment suggestions', 'smart planning', 
        'crypto advice', 'mutual funds', 'stocks', 'commodities'
      ],
      description: 'Receive personalized investment suggestions in crypto, mutual funds, stocks, and commodities'
    },
    
 
    // This belows urls of Settings
    { 
      name: 'Profile Settings', 
      url: '/dashboard/setting/', 
      keywords: ['settings', 'profile', 'account info', 'personal details', 'user settings'], 
      description: 'Manage your basic profile information and preferences' 
    },
    { 
      name: 'Change Password', 
      url: '/dashboard/manage-password/', 
      keywords: ['password', 'change password', 'update password', 'security', 'credentials'], 
      description: 'Update your login password to keep your account secure' 
    },
    { 
      name: 'Delete Account', 
      url: '/dashboard/delete-account/', 
      keywords: ['delete account', 'close account', 'remove account', 'terminate profile'], 
      description: 'Permanently delete your account and all related data' 
    },
    { 
      name: 'Update Personal Info', 
      url: '/dashboard/setting/', 
      keywords: ['update email', 'update mobile number', 'update savings', 'update investment', 'edit profile', 'change contact info'], 
      description: 'Edit your email, phone number, savings, and investment preferences' 
    },
  ];
  


  // Function to filter and show results
  function showResults(query) {
    resultsContainer.innerHTML = '';
    if (!query) {
      resultsContainer.classList.remove('visible');
      return;
    }

    const filtered = searchResultsData.filter(item =>
      item.name.toLowerCase().includes(query.toLowerCase()) ||
      item.keywords.some(keyword => keyword.toLowerCase().includes(query.toLowerCase()))
    );


    if (filtered.length === 0) {
      const noResult = document.createElement('div');
      noResult.textContent = 'No results found';
      noResult.classList.add('no-result');
      resultsContainer.appendChild(noResult);
      resultsContainer.classList.add('visible');
      return;
    }

    filtered.forEach(item => {
      const div = document.createElement('div');
      div.classList.add('result-item');
    
      // Name with optional highlight (optional)
      div.innerHTML = `<strong>${item.name}</strong>`;
    
      // Description below name
      const desc = document.createElement('div');
      desc.classList.add('result-description');
      desc.textContent = item.description;
      div.appendChild(desc);
    
      // Keywords badges container
      const badges = document.createElement('div');
      badges.classList.add('result-keywords');
      item.keywords.forEach(kw => {
        const badge = document.createElement('span');
        badge.classList.add('keyword-badge');
        badge.textContent = kw;
        badges.appendChild(badge);
      });
      div.appendChild(badges);
    
      div.addEventListener('click', () => {
        window.location.href = item.url;
      });
    
      resultsContainer.appendChild(div);
    });


    resultsContainer.classList.add('visible');
  }

  input.addEventListener('input', () => {
    showResults(input.value.trim());
  });

  icon.addEventListener('click', (e) => {
    e.stopPropagation();
    if (window.innerWidth <= 480) {
      if (!searchBox.classList.contains('active')) {
        searchBox.classList.add('active');
        input.focus();
      } else {
        if (input.value === '') {
          searchBox.classList.remove('active');
          resultsContainer.classList.remove('visible');
        }
      }
    }
  });

  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 480) {
      if (!searchBox.contains(e.target)) {
        if (searchBox.classList.contains('active')) {
          searchBox.classList.remove('active');
          resultsContainer.classList.remove('visible');
        }
      }
    } else {
      if (!searchBox.contains(e.target)) {
        resultsContainer.classList.remove('visible');
      }
    }
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      const firstResult = resultsContainer.querySelector('.result-item');
      if (firstResult) {
        firstResult.click();
      }
    }
  });
});




