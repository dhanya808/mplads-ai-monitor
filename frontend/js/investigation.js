// Investigation Modal and Evidence Controller
let activeProjectId = null;

async function openInvestigationModal(projectId) {
  activeProjectId = projectId;
  const modal = document.getElementById('investigationModal');
  if (!modal) return;

  modal.classList.remove('hidden');

  try {
    const [projRes, scurveRes] = await Promise.all([
      fetch(`/api/projects/${projectId}`),
      fetch(`/api/projects/${projectId}/s-curve`)
    ]);

    const projData = await projRes.json();
    const scurveData = await scurveRes.json();

    const p = projData.project;
    const explain = projData.live_explainability;

    // Header & Info
    document.getElementById('modalProjectTitle').innerText = p.title;
    document.getElementById('modalProjectId').innerText = p.id;
    document.getElementById('modalSector').innerText = p.sector;
    document.getElementById('modalBlock').innerText = p.block;
    document.getElementById('modalContractor').innerText = p.contractor;

    // Financial & Progress metrics
    document.getElementById('modalSanctioned').innerText = `₹${p.sanctioned_amount_lakhs.toFixed(2)}L`;
    document.getElementById('modalDisbursed').innerText = `₹${p.expenditure_lakhs.toFixed(2)}L (${p.expenditure_pct}%)`;
    document.getElementById('modalPhysical').innerText = `${p.physical_progress_pct}%`;
    document.getElementById('modalDelay').innerText = `${p.delay_days} days overdue`;

    // ERI Score & Badge
    const eriBadge = document.getElementById('modalEriBadge');
    eriBadge.innerText = `Explainable Risk Index: ${explain.eri_score} / 100`;
    if (explain.eri_score >= 75) {
      eriBadge.className = 'px-3 py-1 rounded text-sm font-bold badge-critical';
    } else if (explain.eri_score >= 50) {
      eriBadge.className = 'px-3 py-1 rounded text-sm font-bold badge-high';
    } else {
      eriBadge.className = 'px-3 py-1 rounded text-sm font-bold badge-clean';
    }

    // Anomaly title & description
    document.getElementById('modalAnomalyType').innerText = p.anomaly.type;
    document.getElementById('modalAnomalyDesc').innerText = p.anomaly.description;

    // Evidence list
    const evList = document.getElementById('modalEvidenceList');
    evList.innerHTML = '';
    const evidence = p.anomaly.evidence || {};
    for (const [k, v] of Object.entries(evidence)) {
      const li = document.createElement('li');
      const label = k.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      li.innerHTML = `<span class="font-semibold text-slate-700">${label}:</span> ${v}`;
      evList.appendChild(li);
    }

    // Explanations
    const expContainer = document.getElementById('modalExplanations');
    expContainer.innerHTML = '';
    (explain.explanations || []).forEach(exp => {
      const pTag = document.createElement('p');
      pTag.className = 'text-xs text-amber-800 bg-amber-50 p-2 rounded border border-amber-200';
      pTag.innerHTML = `⚠️ ${exp}`;
      expContainer.appendChild(pTag);
    });

    // Form defaults
    document.getElementById('investigationStatusSelect').value = p.anomaly.status || 'New';
    document.getElementById('assignedOfficerInput').value = 'Executive Engineer (PWD Rural)';
    document.getElementById('investigationNotes').value = '';
    document.getElementById('chkFreezePayment').checked = (explain.eri_score > 85);
    document.getElementById('chkGeotagProof').checked = true;
    document.getElementById('chkShowCause').checked = (explain.eri_score > 80);

    // Charts
    renderRadarBreakdown(explain.risk_breakdown);
    renderSCurveChart(scurveData.timeline);

    // Spatial Proximity Discrepancy Reconciliation (Map Removed)
    const mapSection = document.getElementById('spatialMapSection');
    if (explain.spatial_result && explain.spatial_result.has_duplicate) {
      mapSection.classList.remove('hidden');
      const topMatch = explain.spatial_result.matches[0];
      document.getElementById('spatialOverlapText').innerText = `Proximity: ${topMatch.distance_meters}m (${topMatch.confidence_pct}% Match)`;
      document.getElementById('modalThisWorkTitle').innerText = p.title;
      document.getElementById('modalThisWorkCoords').innerText = `GPS: ${p.coordinates.lat.toFixed(4)}° N, ${p.coordinates.lng.toFixed(4)}° E (Block: ${p.block})`;
      document.getElementById('modalExternalWorkTitle').innerText = `${topMatch.scheme_name} (ID: ${topMatch.external_project_id})`;
      document.getElementById('modalExternalWorkDistance').innerText = `Distance: ${topMatch.distance_meters}m • Severity: High Duplicate Risk`;
    } else {
      mapSection.classList.add('hidden');
    }

  } catch (err) {
    console.error('Failed to load investigation data:', err);
  }
}

function closeInvestigationModal() {
  const modal = document.getElementById('investigationModal');
  if (modal) modal.classList.add('hidden');
  activeProjectId = null;
}

async function submitInvestigationAction() {
  if (!activeProjectId) return;

  const status = document.getElementById('investigationStatusSelect').value;
  const officer = document.getElementById('assignedOfficerInput').value;
  const notes = document.getElementById('investigationNotes').value;
  const freeze = document.getElementById('chkFreezePayment').checked;
  const geotag = document.getElementById('chkGeotagProof').checked;
  const showCause = document.getElementById('chkShowCause').checked;

  try {
    const res = await fetch(`/api/anomalies/${activeProjectId}/investigate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        status: status,
        assigned_officer: officer,
        investigation_notes: notes,
        freeze_payment: freeze,
        require_geotagged_proof: geotag,
        issue_show_cause_notice: showCause
      })
    });

    if (res.ok) {
      alert(`Investigation Action Saved! Status updated to "${status}". Action logged in statutory audit record.`);
      closeInvestigationModal();
      if (typeof reloadDashboardData === 'function') {
        reloadDashboardData();
      }
    }
  } catch (err) {
    console.error('Failed to submit investigation action:', err);
    alert('Error submitting investigation update.');
  }
}

function openAuditReport() {
  if (!activeProjectId) return;
  window.open(`/api/reports/dossier/${activeProjectId}/print`, '_blank');
}

