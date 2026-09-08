/**
 * InfraFlowX - Dynamic Chart.js Visualization Engine
 * Provides reusable builders for Multi-Axis Trendlines, Radar Condition Charts, Doughnut Breakdowns, and Gantt Timelines.
 */

window.InfraChartEngine = {
    colors: {
        primary: '#3b82f6',
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
        info: '#06b6d4',
        purple: '#8b5cf6',
        dark: '#1e293b',
        gridLine: 'rgba(255, 255, 255, 0.08)'
    },

    createTrendChart: function(canvasId, labels, datasets, yAxisTitle = 'Value') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets.map((ds, idx) => ({
                    label: ds.label || `Series ${idx + 1}`,
                    data: ds.data || [],
                    borderColor: ds.color || Object.values(this.colors)[idx % 6],
                    backgroundColor: ds.fillColor || 'transparent',
                    borderWidth: 2,
                    tension: 0.35,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: Boolean(ds.fillColor)
                }))
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: '#cbd5e1' } },
                    tooltip: { mode: 'index', intersect: false }
                },
                scales: {
                    x: { grid: { color: this.colors.gridLine }, ticks: { color: '#94a3b8' } },
                    y: {
                        grid: { color: this.colors.gridLine },
                        ticks: { color: '#94a3b8' },
                        title: { display: true, text: yAxisTitle, color: '#94a3b8' }
                    }
                }
            }
        });
    },

    createDoughnutBreakdown: function(canvasId, labels, dataValues, backgroundColors) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const defaultColors = [this.colors.primary, this.colors.success, this.colors.warning, this.colors.danger, this.colors.purple, this.colors.info];

        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: dataValues,
                    backgroundColor: backgroundColors || defaultColors,
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#cbd5e1', padding: 16 } }
                },
                cutout: '70%'
            }
        });
    },

    createRadarHealthChart: function(canvasId, categories, scores) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        return new Chart(ctx, {
            type: 'radar',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Asset Health Index (0-100)',
                    data: scores,
                    backgroundColor: 'rgba(59, 130, 246, 0.25)',
                    borderColor: '#3b82f6',
                    pointBackgroundColor: '#3b82f6',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#3b82f6'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: this.colors.gridLine },
                        grid: { color: this.colors.gridLine },
                        pointLabels: { color: '#94a3b8', font: { size: 12 } },
                        suggestedMin: 0,
                        suggestedMax: 100,
                        ticks: { backdropColor: 'transparent', color: '#64748b' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
};
