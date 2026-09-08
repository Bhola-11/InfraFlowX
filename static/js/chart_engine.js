/**
 * InfraFlowX Enterprise Chart.js Visualizer
 * Pre-configured dark & light responsive charts for infrastructure analytics.
 */

const InfraChartTheme = {
    colors: {
        primary: '#3b82f6',
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
        purple: '#8b5cf6',
        teal: '#14b8a6',
        dark: '#1e293b'
    },
    font: {
        family: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        size: 12
    }
};

class InfraCharts {
    static renderDoughnut(canvasId, labels, data, colors = null) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const defaultColors = [
            InfraChartTheme.colors.primary,
            InfraChartTheme.colors.success,
            InfraChartTheme.colors.warning,
            InfraChartTheme.colors.purple,
            InfraChartTheme.colors.danger
        ];

        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors || defaultColors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: '#1e293b'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#94a3b8',
                            font: InfraChartTheme.font,
                            padding: 12
                        }
                    }
                },
                cutout: '68%'
            }
        });
    }

    static renderLineTrend(canvasId, labels, data, seriesLabel = 'Trend', borderColor = '#3b82f6') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: seriesLabel,
                    data: data,
                    borderColor: borderColor,
                    backgroundColor: 'rgba(59, 130, 246, 0.08)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.35,
                    pointRadius: 4,
                    pointBackgroundColor: borderColor
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(148, 163, 184, 0.1)' },
                        ticks: { color: '#94a3b8', font: InfraChartTheme.font }
                    },
                    y: {
                        grid: { color: 'rgba(148, 163, 184, 0.1)' },
                        ticks: { color: '#94a3b8', font: InfraChartTheme.font }
                    }
                }
            }
        });
    }

    static renderBarComparison(canvasId, labels, dataset1, dataset2, label1 = 'Allocated', label2 = 'Spent') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: label1,
                        data: dataset1,
                        backgroundColor: '#3b82f6',
                        borderRadius: 4
                    },
                    {
                        label: label2,
                        data: dataset2,
                        backgroundColor: '#f59e0b',
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: '#94a3b8', font: InfraChartTheme.font }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8', font: InfraChartTheme.font }
                    },
                    y: {
                        grid: { color: 'rgba(148, 163, 184, 0.1)' },
                        ticks: { color: '#94a3b8', font: InfraChartTheme.font }
                    }
                }
            }
        });
    }
}

window.InfraCharts = InfraCharts;
