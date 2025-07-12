document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('budgetLimitForm');
    const messageDiv = document.getElementById('message');
    const budgetLimitsTable = document.querySelector('tbody');
    const noLimitsMessage = document.getElementById('no-limits-message');

    // Utility to show message for 5 seconds
    function showMessage(text, type) {
        messageDiv.innerHTML = ''; // Clear previous content
        messageDiv.style.display = 'flex';
    
        // Remove any previous classes
        messageDiv.classList.remove('success', 'error');
    
        // Add current type class and icon
        if (type === 'success') {
            messageDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${text}`;
            messageDiv.classList.add('success');
        } else if (type === 'error') {
            messageDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${text}`;
            messageDiv.classList.add('error');
        }
    
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
    



    // SET or UPDATE Budget Limit
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessage(data.message, 'success');
                form.reset();

                if (data.budget_limits && budgetLimitsTable) {
                    budgetLimitsTable.innerHTML = ''; // Clear table
                    data.budget_limits.forEach(limit => {
                        const row = document.createElement('tr');
                        row.id = `budget-row-${limit.category}-${limit.frequency}`;

                        row.innerHTML = `
                            <td>${limit.category_display}</td>
                            <td>${limit.limit}</td>
                            <td>${limit.frequency_display}</td>
                            <td>${new Date(limit.created_at).toLocaleDateString()}</td>
                            <td>
                                <span class="delete-icon" data-category="${limit.category}" data-frequency="${limit.frequency}" title="Delete">
                                    <i class="fas fa-trash-alt"></i>
                                </span>
                            </td>
                        `;
                        budgetLimitsTable.appendChild(row);
                    });

                    if (noLimitsMessage) noLimitsMessage.style.display = 'none';
                    bindDeleteEvents();
                } else if (budgetLimitsTable.children.length === 0 && noLimitsMessage) {
                    noLimitsMessage.style.display = 'block';
                }

            } else if (data.error) {
                showMessage(data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('An error occurred while submitting the form.', 'error');
        });
    });

    // DELETE Budget Limit
    function bindDeleteEvents() {
        document.querySelectorAll('.delete-icon').forEach(icon => {
            icon.addEventListener('click', function () {
                const category = this.getAttribute('data-category');
                const frequency = this.getAttribute('data-frequency');

                if (confirm('Are you sure you want to delete this budget limit?')) {
                    fetch(form.action, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
                            'X-Requested-With': 'XMLHttpRequest',
                        },
                        body: new URLSearchParams({
                            'action': 'delete',
                            'category': category,
                            'frequency': frequency
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showMessage(data.message, 'success');

                            const row = document.getElementById(`budget-row-${category}-${frequency}`);
                            if (row) row.remove();

                            if (!document.querySelectorAll('tbody tr').length && noLimitsMessage) {
                                noLimitsMessage.style.display = 'block';
                            }
                        } else if (data.error) {
                            showMessage(data.error, 'error');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showMessage('An error occurred while deleting the budget limit.', 'error');
                    });
                }
            });
        });
    }

    // Bind delete icons on page load
    bindDeleteEvents();
});
