document.addEventListener('DOMContentLoaded', () => {
    // =========================================================================
    // KONFIGURASI SERVER
    // Jika Anda sudah deploy ke Render, ganti link di bawah ini!
    // Contoh: const API_BASE_URL = 'https://nexus-data-api.onrender.com';
    // =========================================================================
    const API_BASE_URL = 'http://localhost:8000';

    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name-display');
    const form = document.getElementById('process-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.getElementById('btn-loader');
    
    const resultsSection = document.getElementById('results-section');
    const cardDashboard = document.getElementById('card-dashboard');
    const cardReport = document.getElementById('card-report');
    const cardPivot = document.getElementById('card-pivot');

    let currentFile = null;
    let chartInstance = null;
    
    // Global data stores for slicer and downloads
    let globalPivotData = null;
    let currentFilteredPivotData = null;

    // --- Drag and Drop Logic ---
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        if (e.dataTransfer.files.length) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        // Clear URL if file is selected
        document.getElementById('url-input').value = '';
        currentFile = file;
        fileNameDisplay.textContent = `Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
    }

    // --- Form Submission ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const urlInput = document.getElementById('url-input').value.trim();
        
        if (!currentFile && !urlInput) {
            alert("Please upload a file or provide a Google Sheets URL.");
            return;
        }

        const options = {
            dashboard: document.getElementById('chk-dashboard').checked,
            pivot: document.getElementById('chk-pivot').checked,
            report: document.getElementById('chk-report').checked
        };

        const notes = document.getElementById('ai-notes').value.trim();

        // Setup form data
        const formData = new FormData();
        if (currentFile) formData.append('file', currentFile);
        if (urlInput) formData.append('url', urlInput);
        formData.append('options', JSON.stringify(options));
        formData.append('notes', notes);

        // UI Loading State
        submitBtn.disabled = true;
        btnText.textContent = 'Processing Data...';
        btnLoader.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            // Note: Update URL if backend is hosted elsewhere
            const response = await fetch(`${API_BASE_URL}/api/process`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Server error occurred');
            }

            const data = await response.json();
            renderResults(data, options);
            
        } catch (error) {
            console.error(error);
            alert(`Error: ${error.message}`);
        } finally {
            submitBtn.disabled = false;
            btnText.textContent = 'Generate Intelligence';
            btnLoader.classList.add('hidden');
        }
    });

    // --- Render Results ---
    function renderResults(data, options) {
        resultsSection.classList.remove('hidden');

        // Render Slicers & Action Buttons if Pivot data exists
        if (data.pivot && data.pivot.data && data.pivot.data.length > 0) {
            globalPivotData = data.pivot;
            currentFilteredPivotData = { ...data.pivot, data: [...data.pivot.data] };
            renderSlicers(globalPivotData);
        } else {
            document.getElementById('card-controls').classList.add('hidden');
        }

        updateDashboardAndPivot(options);

        // Render AI Report
        if (options.report && data.report) {
            cardReport.classList.remove('hidden');
            const reportContent = document.getElementById('report-content');
            // Parse markdown to HTML
            reportContent.innerHTML = marked.parse(data.report);
        } else {
            cardReport.classList.add('hidden');
        }

        // Render Pivot Table is handled in updateDashboardAndPivot
    }

    // --- Slicer & Updates ---
    function renderSlicers(pivotData) {
        const slicerContainer = document.getElementById('slicer-buttons');
        slicerContainer.innerHTML = '';
        document.getElementById('card-controls').classList.remove('hidden');

        // Extract Top 5 Categories to show as slicers
        const categories = pivotData.data.slice(0, 5).map(row => row[pivotData.index]);
        
        // Add "All" button
        const btnAll = document.createElement('button');
        btnAll.className = 'slicer-btn btn btn-primary btn-sm rounded-lg';
        btnAll.textContent = 'Semua';
        btnAll.onclick = () => filterData(null, btnAll);
        slicerContainer.appendChild(btnAll);

        categories.forEach(cat => {
            if(!cat) return;
            const btn = document.createElement('button');
            btn.className = 'slicer-btn btn btn-outline btn-sm rounded-lg';
            btn.textContent = cat;
            btn.onclick = () => filterData(cat, btn);
            slicerContainer.appendChild(btn);
        });
    }

    function filterData(category, activeBtn) {
        // Update active class
        document.querySelectorAll('.slicer-btn').forEach(btn => {
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-outline');
        });
        activeBtn.classList.remove('btn-outline');
        activeBtn.classList.add('btn-primary');

        if (category === null) {
            currentFilteredPivotData.data = [...globalPivotData.data];
        } else {
            currentFilteredPivotData.data = globalPivotData.data.filter(row => row[globalPivotData.index] === category);
        }

        const options = {
            dashboard: document.getElementById('chk-dashboard').checked,
            pivot: document.getElementById('chk-pivot').checked
        };
        updateDashboardAndPivot(options);
    }

    function updateDashboardAndPivot(options) {
        if (!currentFilteredPivotData) return;

        if (options.dashboard) {
            cardDashboard.classList.remove('hidden');
            const chartConfig = {
                type: 'bar',
                xAxis: currentFilteredPivotData.index,
                yAxis: currentFilteredPivotData.values,
                data: currentFilteredPivotData.data
            };
            renderChart(chartConfig);
        } else {
            cardDashboard.classList.add('hidden');
        }

        if (options.pivot) {
            cardPivot.classList.remove('hidden');
            renderTable(currentFilteredPivotData);
        } else {
            cardPivot.classList.add('hidden');
        }
    }

    // --- Action Buttons ---
    document.getElementById('btn-download-img').addEventListener('click', () => {
        if (chartInstance) {
            const link = document.createElement('a');
            link.href = chartInstance.toBase64Image();
            link.download = 'Dashboard_Chart.png';
            link.click();
        }
    });

    document.getElementById('btn-download-excel').addEventListener('click', async () => {
        if (!currentFilteredPivotData) return;
        
        const btn = document.getElementById('btn-download-excel');
        const originalText = btn.textContent;
        btn.textContent = "Generating...";
        btn.disabled = true;

        try {
            const formData = new FormData();
            formData.append('pivot_data', JSON.stringify(currentFilteredPivotData));

            const response = await fetch(`${API_BASE_URL}/api/download_excel`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Download failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Dashboard_Offline.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } catch (e) {
            alert("Gagal download excel: " + e.message);
        } finally {
            btn.textContent = originalText;
            btn.disabled = false;
        }
    });

    // --- Chart.js Rendering ---
    function renderChart(chartData) {
        const ctx = document.getElementById('mainChart').getContext('2d');
        
        if (chartInstance) {
            chartInstance.destroy();
        }

        if (!chartData || !chartData.data || chartData.data.length === 0) {
            return;
        }

        const labels = chartData.data.map(item => item[chartData.xAxis]);
        const values = chartData.data.map(item => item[chartData.yAxis]);

        chartInstance = new Chart(ctx, {
            type: chartData.type || 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: `Sum of ${chartData.yAxis}`,
                    data: values,
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#f8fafc' }
                    }
                },
                scales: {
                    x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                    y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } }
                }
            }
        });
    }

    // --- Table Rendering ---
    function renderTable(pivotData) {
        const headerRow = document.getElementById('pivot-header');
        const body = document.getElementById('pivot-body');
        
        headerRow.innerHTML = '';
        body.innerHTML = '';

        if (!pivotData || !pivotData.data || pivotData.data.length === 0) return;

        // Headers
        const thIndex = document.createElement('th');
        thIndex.textContent = pivotData.index;
        headerRow.appendChild(thIndex);

        const thValue = document.createElement('th');
        thValue.textContent = `Sum of ${pivotData.values}`;
        headerRow.appendChild(thValue);

        // Body
        pivotData.data.forEach(row => {
            const tr = document.createElement('tr');
            
            const tdIndex = document.createElement('td');
            tdIndex.textContent = row[pivotData.index] || 'N/A';
            tr.appendChild(tdIndex);

            const tdValue = document.createElement('td');
            // Format number
            const val = row[pivotData.values];
            tdValue.textContent = typeof val === 'number' ? val.toLocaleString() : val;
            tr.appendChild(tdValue);

            body.appendChild(tr);
        });
    }
});
