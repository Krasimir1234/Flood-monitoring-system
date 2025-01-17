document.addEventListener("DOMContentLoaded", () => {
    fetch('/get_reports')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch reports.');
            }
            return response.json();
        })
        .then(data => {
            const pendingTable = document.getElementById('reports-table');
            const confirmedTable = document.getElementById('confirmed-table');
            const deniedTable = document.getElementById('denied-table');


            pendingTable.innerHTML = '';
            confirmedTable.innerHTML = '';
            deniedTable.innerHTML = '';

            if (data.length === 0) {
                pendingTable.innerHTML = '<tr><td colspan="7">No reports available.</td></tr>';
                return;
            }

            data.forEach(report => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${report.report_id}</td>
                    <td>${report.description}</td>
                    <td>${report.location}</td>
                    <td>${report.latitude}</td>
                    <td>${report.longitude}</td>
                    <td class="status">${report.status}</td>
                `;

                if (report.status === 'Pending' || report.status === 'Unverified') {
                    row.innerHTML += `
                        <td>
                            <button class="confirm-btn" data-id="${report.report_id}">Confirm</button>
                            <button class="deny-btn" data-id="${report.report_id}">Deny</button>
                        </td>
                    `;
                    pendingTable.appendChild(row);
                } else if (report.status === 'Confirmed') {
                    confirmedTable.appendChild(row);
                } else if (report.status === 'Denied') {
                    deniedTable.appendChild(row);
                }
            });

            attachEventListeners();
        })
        .catch(error => {
            console.error('Error fetching reports:', error);
            alert('Failed to load reports. Please try again.');
        });


    function attachEventListeners() {
        document.querySelectorAll('.confirm-btn').forEach(button => {
            button.addEventListener('click', () => {
                const reportId = button.getAttribute('data-id');
                updateReportStatus(reportId, 'Confirmed', 'confirmed-table');
            });
        });

        document.querySelectorAll('.deny-btn').forEach(button => {
            button.addEventListener('click', () => {
                const reportId = button.getAttribute('data-id');
                updateReportStatus(reportId, 'Denied', 'denied-table');
            });
        });

        document.getElementById('clear-confirmed').addEventListener('click', clearConfirmed);

        document.getElementById('clear-denied').addEventListener('click', clearDenied);
    }

    function updateReportStatus(reportId, status, targetTableId) {
        fetch('/update_report_status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ report_id: reportId, status: status })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update report status.');
            }
            return response.json();
        })
        .then(result => {
            if (result.success) {
                const row = document.querySelector(`button[data-id='${reportId}']`).closest('tr');
                row.querySelector('.status').innerText = status;


                const targetTable = document.getElementById(targetTableId);
                row.querySelector('td:last-child').remove();
                targetTable.appendChild(row);
            } else {
                alert('Failed to update report status.');
            }
        })
        .catch(error => {
            console.error('Error updating report status:', error);
            alert('An error occurred. Please try again.');
        });
    }

    function clearConfirmed() {
        const confirmedTable = document.getElementById('confirmed-table');
        const rows = Array.from(confirmedTable.rows);

        const reportIds = rows.map(row => row.cells[0].textContent);

        fetch('/clear_reports', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ report_ids: reportIds })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to clear confirmed reports.');
            }
            return response.json();
        })
        .then(result => {
            if (result.success) {
                confirmedTable.innerHTML = '';
            }
        })
        .catch(error => {
            console.error('Error clearing confirmed reports:', error);
        });
    }

    function clearDenied() {
        const deniedTable = document.getElementById('denied-table');
        const rows = Array.from(deniedTable.rows);

        const reportIds = rows.map(row => row.cells[0].textContent);

        fetch('/delete_reports', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ report_ids: reportIds })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to delete denied reports.');
            }
            return response.json();
        })
        .then(result => {
            if (result.success) {
                deniedTable.innerHTML = '';
            }
        })
        .catch(error => {
            console.error('Error deleting denied reports:', error);
        });
    }
});
