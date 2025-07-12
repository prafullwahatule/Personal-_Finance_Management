document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('budgetLimitForm');
    const messageDiv = document.getElementById('message');
    const budgetLimitsTable = document.querySelector('tbody');
    const noLimitsMessage = document.getElementById('no-limits-message');  // Make sure this ID exists in template

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
            messageDiv.classList.remove('hidden', 'error', 'success');

            if (data.success) {
                messageDiv.textContent = data.message;
                messageDiv.classList.add('success');
                form.reset();

                // Update the table
                if (data.budget_limits && budgetLimitsTable) {
                    budgetLimitsTable.innerHTML = ''; // Clear existing entries
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
                messageDiv.textContent = data.error;
                messageDiv.classList.add('error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            messageDiv.textContent = 'एक त्रुटि हुई।';
            messageDiv.classList.add('error');
        });
    });

    // DELETE Budget Limit
    function bindDeleteEvents() {
        document.querySelectorAll('.delete-icon').forEach(icon => {
            icon.addEventListener('click', function () {
                const category = this.getAttribute('data-category');
                const frequency = this.getAttribute('data-frequency');

                if (confirm('क्या आप वाकई इस बजट लिमिट को हटाना चाहते हैं?')) {
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
                        messageDiv.classList.remove('hidden', 'error', 'success');

                        if (data.success) {
                            messageDiv.textContent = data.message;
                            messageDiv.classList.add('success');

                            const row = document.getElementById(`budget-row-${category}-${frequency}`);
                            if (row) row.remove();

                            if (!document.querySelectorAll('tbody tr').length && noLimitsMessage) {
                                noLimitsMessage.style.display = 'block';
                            }

                        } else if (data.error) {
                            messageDiv.textContent = data.error;
                            messageDiv.classList.add('error');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        messageDiv.textContent = 'डिलीट करते समय एक त्रुटि हुई।';
                        messageDiv.classList.add('error');
                    });
                }
            });
        });
    }

    // Bind delete icons on page load
    bindDeleteEvents();
});
