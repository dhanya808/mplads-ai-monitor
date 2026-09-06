// Charts controller for MPLADS AI Monitor

let financialChartInstance = null;
let sectorChartInstance = null;
let scurveChartInstance = null;
let eriRadarChartInstance = null;

function initFinancialChart(data) {
  const ctx = document.getElementById('financialChart');
  if (!ctx) return;

  if (financialChartInstance) {
    financialChartInstance.destroy();
  }

  const sanctioned = data?.sanctioned_allocation_lakhs || 74.20;
  const revised = data?.revised_estimate_lakhs || 84.80;
  const actual = data?.actual_expenditure_lakhs || 68.30;

  financialChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Sanctioned Allocation', 'Revised Estimate', 'Actual Expenditure'],
      datasets: [{
        label: '₹ in Lakhs',
        data: [sanctioned, revised, actual],
        backgroundColor: [
          '#1e3a8a', // Navy blue
          '#ea580c', // Orange
          '#dc2626'  // Red
        ],
        borderRadius: 4,
        barThickness: 40
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              return ' ₹' + Number(context.raw).toFixed(2) + ' Lakhs';
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 90,
          ticks: {
            stepSize: 10,
            callback: function(val) { return '₹' + val + 'L'; }
          },
          grid: {
            color: '#f1f5f9'
          }
        },
        x: {
          grid: { display: false },
          ticks: {
            font: { size: 11 }
          }
        }
      }
    }
  });
}

function initSectorChart(sectorList) {
  const ctx = document.getElementById('sectorChart');
  if (!ctx) return;

  if (sectorChartInstance) {
    sectorChartInstance.destroy();
  }

  const labels = sectorList.map(function(s) { return s.sector; });
  const data = sectorList.map(function(s) { return s.share_pct; });
  const colors = sectorList.map(function(s) { return s.color; });

  sectorChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors,
        hoverOffset: 6,
        borderWidth: 2,
        borderColor: '#ffffff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        legend: {
          position: 'right',
          labels: {
            boxWidth: 12,
            padding: 10,
            font: { size: 11 }
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return ' ' + context.label + ': ' + context.raw + '%';
            }
          }
        }
      }
    }
  });
}

function renderSCurveChart(timelineData) {
  const ctx = document.getElementById('scurveChart');
  if (!ctx) return;

  if (scurveChartInstance) {
    scurveChartInstance.destroy();
  }

  const labels = timelineData.map(function(t) { return t.milestone; });
  const planned = timelineData.map(function(t) { return t.planned_pct; });
  const financial = timelineData.map(function(t) { return t.financial_pct; });
  const physical = timelineData.map(function(t) { return t.physical_pct; });

  scurveChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Planned Schedule (%)',
          data: planned,
          borderColor: '#94a3b8',
          borderDash: [5, 5],
          backgroundColor: 'transparent',
          tension: 0.3
        },
        {
          label: 'Financial Drawdown (%)',
          data: financial,
          borderColor: '#dc2626',
          backgroundColor: 'rgba(220, 38, 38, 0.08)',
          fill: true,
          tension: 0.3,
          pointRadius: 5
        },
        {
          label: 'Physical Progress (%)',
          data: physical,
          borderColor: '#0284c7',
          backgroundColor: 'transparent',
          tension: 0.3,
          pointRadius: 5
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { boxWidth: 12 } },
        tooltip: {
          callbacks: {
            label: function(context) {
              var val = context.raw !== null ? context.raw + '%' : 'Pending';
              return ' ' + context.dataset.label + ': ' + val;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: { callback: function(val) { return val + '%'; } }
        },
        x: {
          ticks: { font: { size: 10 } }
        }
      }
    }
  });
}

function renderRadarBreakdown(breakdown) {
  const ctx = document.getElementById('eriRadarChart');
  if (!ctx) return;

  if (eriRadarChartInstance) {
    eriRadarChartInstance.destroy();
  }

  const keys = [
    'Progress Mismatch',
    'Time Stalling',
    'Spatial Overlap',
    'Contractor Exposure',
    'Cost Escalation',
    'Billing Anomaly'
  ];

  const values = [
    breakdown?.progress_mismatch || 0,
    breakdown?.time_stalling || 0,
    breakdown?.spatial_overlap || 0,
    breakdown?.contractor_risk || 0,
    breakdown?.cost_escalation || 0,
    breakdown?.billing_anomaly || 0
  ];

  eriRadarChartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: keys,
      datasets: [{
        label: 'Risk Contribution Points',
        data: values,
        backgroundColor: 'rgba(234, 88, 12, 0.2)',
        borderColor: '#ea580c',
        pointBackgroundColor: '#ea580c',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#ea580c'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: '#e2e8f0' },
          grid: { color: '#f1f5f9' },
          suggestedMin: 0,
          suggestedMax: 45,
          ticks: { stepSize: 10, font: { size: 9 } }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}
