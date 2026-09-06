// Main Application Controller for MPLADS AI Monitor

let currentRole = 'MP';

const ROLE_CONFIG = {
  'MP': {
    name: 'Hon. Rajeshwar Verma',
    roleTitle: 'MP',
    jurisdiction: 'PC-77 Varanasi',
    avatar: 'MP',
    portalBadge: 'Constituency Monitoring Portal',
    title: 'Varanasi Parliamentary Constituency (PC-77)',
    subtitle: 'Member of Parliament: Hon. Rajeshwar Verma • District: Varanasi, Uttar Pradesh'
  },
  'DM': {
    name: 'Shri Satyendra Kumar, IAS',
    roleTitle: 'DM',
    jurisdiction: 'Varanasi District',
    avatar: 'DM',
    portalBadge: 'District Execution & Physical Compliance Hub',
    title: 'District Planning & Civil Execution Cell — Varanasi',
    subtitle: 'Nodal Officer: District Magistrate & DPO, Varanasi • State: Uttar Pradesh'
  },
  'SNA': {
    name: 'Dr. Rameshwar Singh',
    roleTitle: 'SNA',
    jurisdiction: 'Uttar Pradesh (80 PCs)',
    avatar: 'SNA',
    portalBadge: 'State Nodal Monitoring Cell',
    title: 'State Planning Division — Uttar Pradesh',
    subtitle: 'State Nodal Authority (SNA) • Monitoring 80 Parliamentary Constituencies'
  },
  'MOSPI': {
    name: 'Smt. Ananya Sen, ISS',
    roleTitle: 'MoSPI',
    jurisdiction: 'National Tier (All India)',
    avatar: 'GOI',
    portalBadge: 'National Early Warning & Audit Command Center',
    title: 'Ministry of Statistics & Programme Implementation (MoSPI)',
    subtitle: 'DIID National Anomaly & Early Warning Command Center • 18th Lok Sabha'
  }
};

document.addEventListener('DOMContentLoaded', () => {
  initAuthSession();
  initEventListeners();
  loadAllData();
});

function initAuthSession() {
  const stored = localStorage.getItem('mplads_user');
  if (stored) {
    try {
      const user = JSON.parse(stored);
      if (user.role && ROLE_CONFIG[user.role]) {
        currentRole = user.role;
        document.getElementById('roleSelector').value = user.role;
      }
    } catch (e) {
      console.error('Session parse error:', e);
    }
  }
  applyRoleUI(currentRole);
}

function initEventListeners() {
  // Filters
  document.getElementById('filterStatus').addEventListener('change', reloadDashboardData);
  document.getElementById('filterBlock').addEventListener('change', reloadDashboardData);
  document.getElementById('filterSector').addEventListener('change', reloadDashboardData);
  document.getElementById('filterRisk').addEventListener('change', reloadDashboardData);
  document.getElementById('globalSearchInput').addEventListener('input', debounce(reloadDashboardData, 300));

  // Role Switcher
  document.getElementById('roleSelector').addEventListener('change', (e) => {
    switchRole(e.target.value);
  });
}

function switchRole(role) {
  currentRole = role;
  const cfg = ROLE_CONFIG[role] || ROLE_CONFIG['MP'];
  
  // Update local storage session
  const currentUser = {
    role: role,
    name: cfg.name,
    jurisdiction: cfg.jurisdiction
  };
  localStorage.setItem('mplads_user', JSON.stringify(currentUser));

  applyRoleUI(role);
  reloadDashboardData();
}

function applyRoleUI(role) {
  const cfg = ROLE_CONFIG[role] || ROLE_CONFIG['MP'];

  // Update header profile pill
  document.getElementById('userAvatar').innerText = cfg.avatar;
  document.getElementById('userNameDisplay').innerText = cfg.name;
  document.getElementById('userRoleBadge').innerText = cfg.roleTitle;
  document.getElementById('userJurisdictionDisplay').innerText = cfg.jurisdiction;

  // Update hero banner
  const portalBadge = document.getElementById('heroPortalBadge');
  if (portalBadge) portalBadge.innerText = cfg.portalBadge;

  document.getElementById('constituencyTitle').innerText = cfg.title;
  document.getElementById('mpDetails').innerText = cfg.subtitle;

  // Role-specific sections visibility
  const mpSec = document.getElementById('roleSection-MP');
  const dmSec = document.getElementById('roleSection-DM');
  const snaSec = document.getElementById('roleSection-SNA');
  const mospiSec = document.getElementById('roleSection-MOSPI');

  if (mpSec) mpSec.classList.add('hidden');
  if (dmSec) dmSec.classList.add('hidden');
  if (snaSec) snaSec.classList.add('hidden');
  if (mospiSec) mospiSec.classList.add('hidden');

  if (role === 'MP' && mpSec) {
    mpSec.classList.remove('hidden');
  } else if (role === 'DM' && dmSec) {
    dmSec.classList.remove('hidden');
  } else if (role === 'SNA' && snaSec) {
    snaSec.classList.remove('hidden');
  } else if (role === 'MOSPI' && mospiSec) {
    mospiSec.classList.remove('hidden');
  }
}

function handleLogout() {
  localStorage.removeItem('mplads_user');
  fetch('/api/auth/logout', { method: 'POST' })
    .finally(() => {
      window.location.href = '/login';
    });
}

async function loadAllData() {
  await Promise.all([
    fetchKPIs(),
    fetchSectorDistribution(),
    fetchFinancialSummary(),
    fetchAnomaliesFeed(),
    fetchMilestoneSchedule(),
    fetchContractorsData()
  ]);
}

async function reloadDashboardData() {
  await Promise.all([
    fetchKPIs(),
    fetchAnomaliesFeed(),
    fetchMilestoneSchedule()
  ]);
}

function getFilterParams() {
  const status = document.getElementById('filterStatus').value;
  const block = document.getElementById('filterBlock').value;
  const sector = document.getElementById('filterSector').value;
  const risk = document.getElementById('filterRisk').value;
  const search = document.getElementById('globalSearchInput').value;

  const params = new URLSearchParams();
  if (status && status !== 'All Statuses (Ongoing & Completed)') params.append('status', status);
  if (block && block !== 'All Blocks') params.append('block', block);
  if (sector && sector !== 'All Sectors') params.append('sector', sector);
  if (risk && risk !== 'All Risk Tiers') params.append('risk_level', risk);
  if (search) params.append('search', search);

  return params.toString();
}

async function fetchKPIs() {
  try {
    const q = getFilterParams();
    const res = await fetch(`/api/analytics/kpis?${q}`);
    const kpi = await res.json();

    document.getElementById('kpiTotalProjects').innerText = kpi.total_projects;
    document.getElementById('kpiSanctioned').innerText = `₹${kpi.sanctioned_lakhs.toFixed(2)} L`;
    document.getElementById('kpiExpenditure').innerText = `₹${kpi.expenditure_lakhs.toFixed(2)} L`;
    document.getElementById('kpiExpenditurePct').innerText = `${kpi.utilization_pct}% fund utilization`;
    document.getElementById('kpiCompleted').innerText = kpi.completed_projects;
    document.getElementById('kpiOngoing').innerText = kpi.ongoing_projects;
    document.getElementById('kpiHighRisk').innerText = kpi.high_risk_projects;
    document.getElementById('kpiDelayed').innerText = kpi.delayed_projects;
    document.getElementById('kpiCriticalCount').innerText = `${kpi.critical_anomalies} Critical anomalies`;
  } catch (err) {
    console.error('Failed to fetch KPIs:', err);
  }
}

async function fetchSectorDistribution() {
  try {
    const res = await fetch('/api/analytics/sector-distribution');
    const data = await res.json();
    initSectorChart(data);
  } catch (err) {
    console.error('Failed to fetch sector distribution:', err);
  }
}

async function fetchFinancialSummary() {
  try {
    const res = await fetch('/api/analytics/financial-summary');
    const data = await res.json();
    initFinancialChart(data);
  } catch (err) {
    console.error('Failed to fetch financial summary:', err);
  }
}

async function fetchAnomaliesFeed() {
  try {
    const res = await fetch('/api/anomalies');
    const list = await res.json();
    const container = document.getElementById('anomalyFeedList');
    if (!container) return;

    container.innerHTML = '';

    if (list.length === 0) {
      container.innerHTML = '<div class="p-4 text-center text-slate-400 text-sm">No anomalies found matching current filters.</div>';
      return;
    }

    list.forEach(item => {
      const card = document.createElement('div');
      card.className = 'p-3 bg-white border border-slate-100 rounded-lg hover:border-slate-300 transition-colors';

      const dotColor = item.anomaly.severity === 'Critical' ? 'bg-red-600' : 'bg-amber-500';
      let statusClass = 'text-red-700 bg-red-50 border-red-200';
      if (item.anomaly.status === 'Under Investigation') {
        statusClass = 'text-amber-800 bg-amber-50 border-amber-200';
      } else if (item.anomaly.status === 'Clean' || item.anomaly.status === 'Resolved') {
        statusClass = 'text-emerald-800 bg-emerald-50 border-emerald-200';
      }

      card.innerHTML = `
        <div class="flex items-center justify-between text-xs text-slate-500 mb-1">
          <div class="flex items-center space-x-2">
            <span class="inline-block w-2.5 h-2.5 rounded-full ${dotColor}"></span>
            <span class="font-mono font-bold text-slate-700">${item.project_id}</span>
          </div>
          <span class="text-slate-400">${item.anomaly.date}</span>
        </div>
        <div class="text-sm font-semibold text-slate-800">${item.anomaly.type}</div>
        <div class="text-xs text-slate-500 mt-1 line-clamp-2 leading-relaxed">${item.anomaly.description}</div>
        <div class="flex items-center justify-between mt-3 pt-2 border-t border-slate-50">
          <span class="px-2 py-0.5 rounded text-[11px] font-medium border ${statusClass}">Status: ${item.anomaly.status}</span>
          <button onclick="openInvestigationModal('${item.project_id}')" class="text-sky-700 hover:text-sky-900 font-semibold text-xs flex items-center group">
            Investigate <span class="ml-1 group-hover:translate-x-0.5 transition-transform">→</span>
          </button>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.error('Failed to fetch anomalies:', err);
  }
}

async function fetchMilestoneSchedule() {
  try {
    const q = getFilterParams();
    const res = await fetch(`/api/projects?${q}`);
    const list = await res.json();
    const container = document.getElementById('milestoneScheduleList');
    if (!container) return;

    container.innerHTML = '';
    const ongoing = list.filter(p => p.status === 'Ongoing');

    if (ongoing.length === 0) {
      container.innerHTML = '<div class="p-4 text-center text-slate-400 text-sm">No scheduled civil milestones found.</div>';
      return;
    }

    ongoing.forEach(p => {
      const card = document.createElement('div');
      card.className = 'p-3 bg-white border border-slate-100 rounded-lg hover:border-slate-300 transition-colors';

      let delayBadge = '';
      if (p.delay_days > 100) {
        delayBadge = `<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-red-100 text-red-700 border border-red-200">${p.delay_days}d Delayed</span>`;
      } else if (p.delay_days > 30) {
        delayBadge = `<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-rose-100 text-rose-700 border border-rose-200">${p.delay_days}d Delayed</span>`;
      } else if (p.delay_days > 0) {
        delayBadge = `<span class="px-2 py-0.5 rounded text-[11px] font-medium bg-amber-100 text-amber-800 border border-amber-200">${p.delay_days}d Delayed</span>`;
      } else {
        delayBadge = `<span class="px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-100 text-emerald-800 border border-emerald-200">On Schedule</span>`;
      }

      card.innerHTML = `
        <div class="flex items-start justify-between">
          <div class="text-sm font-semibold text-slate-800 line-clamp-1 flex-1 pr-2">${p.title}</div>
          <div>${delayBadge}</div>
        </div>
        <div class="text-xs text-slate-500 mt-1">
          Target Date: <span class="font-medium text-slate-700">${p.target_date}</span> • Contractor: <span class="font-medium text-slate-700">${p.contractor}</span>
        </div>
        <div class="mt-2.5 flex items-center space-x-3">
          <div class="flex-1 bg-slate-100 rounded-full h-2 overflow-hidden">
            <div class="bg-sky-600 h-2 rounded-full" style="width: ${p.physical_progress_pct}%"></div>
          </div>
          <span class="text-xs font-semibold text-slate-700 min-w-[50px] text-right">${p.physical_progress_pct}% Done</span>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.error('Failed to fetch milestone schedule:', err);
  }
}

async function fetchContractorsData() {
  try {
    const res = await fetch('/api/analytics/contractors');
    const data = await res.json();

    const hhiEl = document.getElementById('hhiScoreDisplay');
    const hhiClassEl = document.getElementById('hhiClassDisplay');
    if (hhiEl && data.market_concentration) {
      hhiEl.innerText = data.market_concentration.hhi;
      hhiClassEl.innerText = data.market_concentration.classification;
    }

    const tbody = document.getElementById('contractorTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';

    (data.contractors || []).forEach(c => {
      const tr = document.createElement('tr');
      tr.className = 'border-b border-slate-100 hover:bg-slate-50 text-xs';
      const anomBadge = c.anomalies_flagged > 0 
        ? 'bg-red-50 text-red-700 border border-red-200 font-bold' 
        : 'bg-emerald-50 text-emerald-700';

      tr.innerHTML = `
        <td class="p-3 font-medium text-slate-800">${c.name}</td>
        <td class="p-3 font-mono text-slate-500">${c.pan}</td>
        <td class="p-3 text-center font-bold">${c.projects_awarded}</td>
        <td class="p-3 text-right font-semibold">₹${c.total_value_lakhs.toFixed(2)} L</td>
        <td class="p-3 text-center">${c.average_delay_days} days</td>
        <td class="p-3"><span class="px-2 py-0.5 rounded text-[11px] ${anomBadge}">${c.anomalies_flagged} Flagged</span></td>
        <td class="p-3 text-slate-600">${c.concentration_hhi_risk}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error('Failed to fetch contractors:', err);
  }
}



function resetFilters() {
  document.getElementById('filterStatus').value = 'All Statuses (Ongoing & Completed)';
  document.getElementById('filterBlock').value = 'All Blocks';
  document.getElementById('filterSector').value = 'All Sectors';
  document.getElementById('filterRisk').value = 'All Risk Tiers';
  document.getElementById('globalSearchInput').value = '';
  reloadDashboardData();
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}
