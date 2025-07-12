document.addEventListener('DOMContentLoaded', function () {
    const downloadBtn = document.getElementById('download-btn');

    downloadBtn.addEventListener('click', function () {
        const duration = document.getElementById('duration-select').value;
        const format = document.getElementById('format-select').value;

        if (format === 'pdf') {
            const charts = {
                "Income Source Distribution": document.getElementById('sourcePieChart')?.toDataURL() || '',
                "Income Entries Per Month": document.getElementById('entryBarChart')?.toDataURL() || '',
                "Category-wise Spending": document.getElementById('categoryPieChart')?.toDataURL() || '',
                "Weekday Pattern": document.getElementById('weekdayChart')?.toDataURL() || '',
                "Day of Month Pattern": document.getElementById('domChart')?.toDataURL() || '',
                "Spend-Save-Invest Ratio": document.getElementById('spendSaveInvestChart')?.toDataURL() || '',
                "Budget vs Actual": document.getElementById('budgetActualChart')?.toDataURL() || '',
                "Monthly Cash Flow": document.getElementById('monthlyCashFlowChart')?.toDataURL() || ''
            };
            const chartParam = encodeURIComponent(JSON.stringify(charts));
            window.open(`/dashboard/generate-pdf-report?duration=${duration}&charts=${chartParam}`, '_blank');
        } else {
            window.open(`/generate-${format}-report?duration=${duration}`, '_blank');
        }
    });
});
