/**
 * InfraFlowX Interactive DataGrid & Table Filter Engine
 */

class InfraDataGrid {
    constructor(tableId, options = {}) {
        this.table = document.getElementById(tableId);
        this.searchInput = document.getElementById(options.searchInputId || 'tableSearchInput');
        this.exportBtn = document.getElementById(options.exportBtnId || 'tableExportBtn');
        this.init();
    }

    init() {
        if (!this.table) return;

        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => this.filterRows(e.target.value));
        }

        if (this.exportBtn) {
            this.exportBtn.addEventListener('click', () => this.exportToCSV());
        }

        this.enableSortableHeaders();
    }

    filterRows(query) {
        const q = query.toLowerCase().trim();
        const rows = this.table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(q) ? '' : 'none';
        });
    }

    enableSortableHeaders() {
        const headers = this.table.querySelectorAll('thead th[data-sort]');
        headers.forEach((th, colIdx) => {
            th.style.cursor = 'pointer';
            th.title = 'Click to sort column';
            th.addEventListener('click', () => this.sortTableByColumn(colIdx));
        });
    }

    sortTableByColumn(colIdx) {
        const tbody = this.table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const isAsc = this.table.getAttribute('data-sort-dir') !== 'asc';
        
        rows.sort((a, b) => {
            const valA = a.children[colIdx] ? a.children[colIdx].textContent.trim() : '';
            const valB = b.children[colIdx] ? b.children[colIdx].textContent.trim() : '';
            return isAsc ? valA.localeCompare(valB, undefined, { numeric: true }) : valB.localeCompare(valA, undefined, { numeric: true });
        });

        rows.forEach(r => tbody.appendChild(r));
        this.table.setAttribute('data-sort-dir', isAsc ? 'asc' : 'desc');
    }

    exportToCSV(filename = 'infraflowx_export.csv') {
        let csv = [];
        const rows = this.table.querySelectorAll('tr');
        rows.forEach(row => {
            if (row.style.display !== 'none') {
                const cols = row.querySelectorAll('th, td');
                const rowData = [];
                cols.forEach(col => {
                    let data = col.innerText.replace(/"/g, '""');
                    rowData.push(`"${data}"`);
                });
                csv.push(rowData.join(','));
            }
        });

        const csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
        const downloadLink = document.createElement('a');
        downloadLink.download = filename;
        downloadLink.href = window.URL.createObjectURL(csvFile);
        downloadLink.style.display = 'none';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    }
}

window.InfraDataGrid = InfraDataGrid;
