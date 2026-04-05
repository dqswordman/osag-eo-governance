const DATA = window.OSAG_ENGINEERED_V2_DATA;
const COLORS = { Random: "#355070", "Contract-Priority": "#F4A261", OSAG: "#C44536" };
const $ = id => document.getElementById(id);
const scenarioSelect = $("scenarioSelect");
const baselineSelect = $("baselineSelect");
const stepSlider = $("stepSlider");
const prevBtn = $("prevBtn");
const nextBtn = $("nextBtn");
const playBtn = $("playBtn");
const resetBtn = $("resetBtn");
const momentButtons = $("momentButtons");
const presentationModeBtn = $("presentationModeBtn");
const committeeModeBtn = $("committeeModeBtn");
const committeeSection = $("committeeSection");
const tabButtons = Array.from(document.querySelectorAll(".tab-btn"));
let currentScenario = null;
let currentMode = "presentation";
let selectedContract = null;
let playing = false;
let timerId = null;

const pct = x => (100 * Number(x)).toFixed(1) + "%";
const num = x => Number(x).toFixed(1);
const byStep = (rows, display, step) => rows.filter(r => r.display === display && Number(r.step) === step);
const timeline = display => currentScenario.timeline.filter(r => r.display === display).sort((a, b) => a.step - b.step);
const contractState = (display, step) => currentScenario.contractState.filter(r => r.display === display && Number(r.step) === step).sort((a, b) => a.contract_id - b.contract_id);
const queueState = (display, step) => currentScenario.queue.filter(r => r.display === display && Number(r.step) === step).sort((a, b) => (b.priority - a.priority) || (b.target_gap - a.target_gap));

function buildScenarioOptions() {
  Object.values(DATA.scenarios).forEach(sc => {
    const opt = document.createElement("option");
    opt.value = sc.key;
    opt.textContent = sc.title;
    scenarioSelect.appendChild(opt);
  });
  scenarioSelect.value = DATA.ui.defaultScenario;
}

function timelineRow(display, step) {
  return timeline(display)[step];
}

function stepTakeaway(step, baselineDisplay) {
  const base = timelineRow(baselineDisplay, step);
  const osag = timelineRow("OSAG", step);
  const coverageGain = 100 * (Number(base.coverage_error) - Number(osag.coverage_error));
  const complianceGain = 100 * (Number(osag.service_compliance) - Number(base.service_compliance));
  const missedGain = Number(base.missed_service_cum) - Number(osag.missed_service_cum);
  if (coverageGain > 4 && missedGain >= 1) {
    return `OSAG is keeping policy drift ${coverageGain.toFixed(1)} pts lower while also avoiding ${missedGain} missed-service events.`;
  }
  if (complianceGain > 4) {
    return `OSAG is preserving contract compliance ${complianceGain.toFixed(1)} pts above ${baselineDisplay} instead of chasing only the hottest local queue.`;
  }
  return "OSAG is using target-gap, revisit pressure, and backlog signals together, so the dispatch stays closer to contract policy over time.";
}

function setScenario(key) {
  currentScenario = DATA.scenarios[key];
  $("scenarioTitle").textContent = currentScenario.title;
  $("scenarioSubtitle").textContent = currentScenario.subtitle;
  $("guidedScenario").textContent = currentScenario.subtitle;
  $("guidedGoal").textContent = currentScenario.operatorGoal;
  baselineSelect.innerHTML = "";
  currentScenario.baselineChoices.forEach(name => {
    const opt = document.createElement("option");
    opt.value = name;
    opt.textContent = name;
    baselineSelect.appendChild(opt);
  });
  baselineSelect.value = DATA.ui.defaultBaseline;
  stepSlider.max = String(currentScenario.steps - 1);
  stepSlider.value = String(currentScenario.keyMoments[1]);
  selectedContract = null;
  renderMomentButtons();
  renderContractLegend();
  refresh();
}

function renderMomentButtons() {
  momentButtons.innerHTML = "";
  currentScenario.keyMoments.forEach((step, idx) => {
    const btn = document.createElement("button");
    btn.className = "btn";
    btn.textContent = "Jump: " + currentScenario.keyMomentLabels[idx];
    btn.addEventListener("click", () => {
      stepSlider.value = String(step);
      refresh();
    });
    momentButtons.appendChild(btn);
  });
}

function drawMap(canvas, rows, borderColor, highlightContract) {
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const cell = 28, ox = 18, oy = 18;
  rows.forEach(row => {
    const x = ox + Number(row.col) * cell;
    const y = oy + Number(row.row) * cell;
    const hazard = Math.max(0, Math.min(1, Number(row.hazard) / 2.3));
    let red = Math.floor(245 - 42 * hazard);
    let green = Math.floor(236 - 145 * hazard);
    let blue = Math.floor(223 - 190 * hazard);
    if (highlightContract !== null && Number(row.contract_id) !== highlightContract) {
      red = Math.floor(red * 0.60 + 255 * 0.40);
      green = Math.floor(green * 0.60 + 255 * 0.40);
      blue = Math.floor(blue * 0.60 + 255 * 0.40);
    }
    ctx.fillStyle = `rgb(${red},${green},${blue})`;
    ctx.fillRect(x, y, cell - 1, cell - 1);
    ctx.strokeStyle = "#d9cdb4";
    ctx.lineWidth = 1;
    ctx.strokeRect(x + 0.5, y + 0.5, cell - 1.2, cell - 1.2);
    ctx.fillStyle = row.palette;
    ctx.beginPath();
    ctx.arc(x + 7, y + 7, 4, 0, Math.PI * 2);
    ctx.fill();
    if (Number(row.observed) === 1) {
      ctx.strokeStyle = borderColor;
      ctx.lineWidth = 3;
      ctx.strokeRect(x + 1.5, y + 1.5, cell - 3, cell - 3);
    }
    if (Number(row.annotated) === 1) {
      ctx.fillStyle = "#111";
      ctx.beginPath();
      ctx.arc(x + cell / 2, y + cell / 2, 2.5, 0, Math.PI * 2);
      ctx.fill();
    }
    if (Number(row.missed_contract) === 1) {
      ctx.strokeStyle = "#111";
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(x + 5, y + 5);
      ctx.lineTo(x + cell - 6, y + cell - 6);
      ctx.moveTo(x + cell - 6, y + 5);
      ctx.lineTo(x + 5, y + cell - 6);
      ctx.stroke();
    }
  });
}

function drawAxis(ctx, x, y, w, h, xLabel, yLabel) {
  ctx.strokeStyle = "#667788";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x, y + h);
  ctx.lineTo(x + w, y + h);
  ctx.stroke();
  ctx.fillStyle = "#667788";
  ctx.font = "12px Calibri";
  ctx.fillText(xLabel, x + w - 30, y + h + 18);
  ctx.save();
  ctx.translate(18, y + h / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText(yLabel, 0, 0);
  ctx.restore();
}

function drawShareChart(step, baselineDisplay) {
  const canvas = $("shareCanvas");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const x = 56, y = 20, w = canvas.width - 82, h = canvas.height - 60;
  drawAxis(ctx, x, y, w, h, "contracts", "share");
  const baseRows = contractState(baselineDisplay, step);
  const osagRows = contractState("OSAG", step);
  const maxVal = Math.max(...baseRows.map(r => Math.max(Number(r.actual_share), Number(r.target_share))), ...osagRows.map(r => Number(r.actual_share)), 0.25);
  const groupW = w / Math.max(baseRows.length, 1);
  baseRows.forEach((row, idx) => {
    const cid = Number(row.contract_id);
    const active = selectedContract === null || selectedContract === cid;
    const osagRow = osagRows.find(r => Number(r.contract_id) === cid);
    const gx = x + idx * groupW + 18;
    const barW = Math.max(18, groupW * 0.18);
    const baseH = (Number(row.actual_share) / maxVal) * (h - 24);
    const osagH = (Number(osagRow.actual_share) / maxVal) * (h - 24);
    const targetY = y + h - (Number(row.target_share) / maxVal) * (h - 24);
    ctx.fillStyle = active ? "#F4A261" : "#F6D0A5";
    ctx.fillRect(gx, y + h - baseH, barW, baseH);
    ctx.fillStyle = active ? "#C44536" : "#E9A49D";
    ctx.fillRect(gx + barW + 8, y + h - osagH, barW, osagH);
    ctx.strokeStyle = "#17324A";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(gx - 2, targetY);
    ctx.lineTo(gx + 2 * barW + 10, targetY);
    ctx.stroke();
    ctx.fillStyle = active ? "#495664" : "#9AA6B4";
    ctx.font = "11px Calibri";
    ctx.fillText("C" + cid, gx + barW * 0.5, y + h + 16);
  });
}

function drawTimeline(baselineDisplay) {
  const canvas = $("timelineCanvas");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const x = 56, y = 20, w = canvas.width - 84, h = canvas.height - 58;
  drawAxis(ctx, x, y, w, h, "step", "score");
  const baselineRows = timeline(baselineDisplay);
  const osagRows = timeline("OSAG");
  const relMax = Math.max(...baselineRows.map(r => Number(r.reliability_score)), ...osagRows.map(r => Number(r.reliability_score)), 1);
  const missMax = Math.max(...baselineRows.map(r => Number(r.missed_service_cum)), ...osagRows.map(r => Number(r.missed_service_cum)), 1);
  function drawSeries(rows, key, color, dashed, scale, offset) {
    ctx.strokeStyle = color;
    ctx.lineWidth = key === "reliability_score" ? 3 : 2;
    ctx.setLineDash(dashed ? [5, 5] : []);
    ctx.beginPath();
    rows.forEach((row, idx) => {
      const px = x + (Number(row.step) / Math.max(rows.length - 1, 1)) * w;
      const maxValue = key === "reliability_score" ? relMax : missMax;
      const py = y + offset + h - scale * h * (Number(row[key]) / maxValue);
      if (idx === 0) {
        ctx.moveTo(px, py);
      } else {
        ctx.lineTo(px, py);
      }
    });
    ctx.stroke();
    ctx.setLineDash([]);
  }
  drawSeries(baselineRows, "reliability_score", "#F4A261", false, 0.62, -0.05 * h);
  drawSeries(osagRows, "reliability_score", "#C44536", false, 0.62, -0.05 * h);
  drawSeries(baselineRows, "missed_service_cum", "#F4A261", true, 0.25, -0.62 * h);
  drawSeries(osagRows, "missed_service_cum", "#C44536", true, 0.25, -0.62 * h);
  ctx.fillStyle = "#556475";
  ctx.font = "12px Calibri";
  ctx.fillText("Solid = reliability, dashed = cumulative missed service", x + 18, y + 14);
}

function drawGapChart(step, baselineDisplay) {
  const canvas = $("gapCanvas");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const x = 56, y = 20, w = canvas.width - 82, h = canvas.height - 60;
  drawAxis(ctx, x, y, w, h, "contract", "|gap|");
  const baseRows = contractState(baselineDisplay, step);
  const osagRows = contractState("OSAG", step);
  const maxGap = Math.max(...baseRows.map(r => Math.abs(Number(r.coverage_gap))), ...osagRows.map(r => Math.abs(Number(r.coverage_gap))), 1);
  const barW = w / (baseRows.length * 2 + 2);
  baseRows.forEach((row, idx) => {
    const cid = Number(row.contract_id);
    const active = selectedContract === null || selectedContract === cid;
    const osagRow = osagRows.find(r => Number(r.contract_id) === cid);
    const left = x + (idx * 2 + 0.5) * barW;
    const baseH = (Math.abs(Number(row.coverage_gap)) / maxGap) * h;
    const osagH = (Math.abs(Number(osagRow.coverage_gap)) / maxGap) * h;
    ctx.fillStyle = active ? "#F4A261" : "#F6D0A5";
    ctx.fillRect(left, y + h - baseH, barW - 4, baseH);
    ctx.fillStyle = active ? "#C44536" : "#E9A49D";
    ctx.fillRect(left + barW, y + h - osagH, barW - 4, osagH);
    ctx.fillStyle = active ? "#495664" : "#9AA6B4";
    ctx.font = "10px Calibri";
    ctx.fillText("C" + cid, left - 2, y + h + 16);
  });
}

function renderContractLegend() {
  const legend = $("contractLegend");
  legend.innerHTML = "";
  currentScenario.contracts.forEach(contract => {
    const btn = document.createElement("button");
    btn.className = "contract-chip" + (selectedContract === contract.contract_id ? " active" : "");
    btn.innerHTML = `
      <span class="swatch" style="background:${contract.color}"></span>
      <span>
        <strong>${contract.name}</strong>
        <div class="contract-meta">P${contract.priority} | target ${Math.round(100 * Number(contract.target_weight))}% | deadline ${contract.deadline_steps} step</div>
      </span>
    `;
    btn.addEventListener("click", () => {
      selectedContract = selectedContract === contract.contract_id ? null : contract.contract_id;
      renderContractLegend();
      refresh();
    });
    legend.appendChild(btn);
  });
}

function renderBenchmarkTable() {
  let html = "<thead><tr><th>Dataset</th><th>Policy</th><th>Acc_all</th><th>Acc_high</th><th>PCE</th></tr></thead><tbody>";
  DATA.benchmarkAnchor.rows.forEach(row => {
    html += `<tr><td>${row.dataset}</td><td>${row.policy}</td><td>${row.acc_all}</td><td>${row.acc_high}</td><td>${row.prio_cov_err}</td></tr>`;
  });
  html += "</tbody>";
  $("benchmarkTable").innerHTML = html;
}

function renderQueue(step, baselineDisplay) {
  const baseRows = queueState(baselineDisplay, step);
  const osagRows = queueState("OSAG", step);
  let html = "<thead><tr><th>Contract</th><th>P</th><th>Pending</th><th>Deadline</th><th>Base selected</th><th>OSAG selected</th><th>OSAG reason</th></tr></thead><tbody>";
  baseRows.forEach(baseRow => {
    const cid = Number(baseRow.contract_id);
    const osagRow = osagRows.find(r => Number(r.contract_id) === cid) || osagRows[0];
    const focused = selectedContract !== null && selectedContract === cid;
    html += `<tr class="${focused ? "contract-focus" : ""}"><td>${baseRow.contract_name}</td><td>P${baseRow.priority}</td><td>${Number(osagRow.pending_jobs).toFixed(1)}</td><td>${osagRow.deadline_remaining}</td><td>${baseRow.selected_obs}</td><td>${osagRow.selected_obs}</td><td>${osagRow.reason_hint}</td></tr>`;
  });
  html += "</tbody>";
  $("queueTable").innerHTML = html;
}

function renderExplanation(step, baselineDisplay) {
  const baseExp = currentScenario.explanations.find(r => r.display === baselineDisplay && Number(r.step) === step);
  const osagExp = currentScenario.explanations.find(r => r.display === "OSAG" && Number(r.step) === step);
  const takeaway = stepTakeaway(step, baselineDisplay);
  $("explanationPanel").innerHTML = `
    <p><strong>${baselineDisplay}:</strong> ${baseExp.detail}</p>
    <p style="margin-top:8px"><strong>OSAG:</strong> ${osagExp.detail}</p>
    <p style="margin-top:10px"><strong>Takeaway:</strong> ${takeaway}</p>
  `;
  $("advantageSummary").textContent = takeaway;
  $("operatorNotes").innerHTML = `
    <p><strong>What the operator is seeing:</strong> which contracts are close to deadline, which ones are already drifting away from target, and which queue is growing fastest.</p>
    <p style="margin-top:8px"><strong>Why OSAG behaves differently:</strong> it scores actions using urgency plus governance signals, so it protects high-value contracts without letting long-run service compliance drift away.</p>
  `;
}

function updateGuidedHeader(step, baselineDisplay) {
  $("guidedCompare").textContent = `${baselineDisplay} versus OSAG at step ${step + 1} / ${currentScenario.steps}`;
  $("guidedTakeaway").textContent = stepTakeaway(step, baselineDisplay);
}

function updateCards(step, baselineDisplay) {
  const base = timelineRow(baselineDisplay, step);
  const osag = timelineRow("OSAG", step);
  $("complianceValue").textContent = pct(osag.service_compliance);
  $("complianceDelta").textContent = `${(100 * (Number(osag.service_compliance) - Number(base.service_compliance))).toFixed(1)} pts vs ${baselineDisplay}`;
  $("coverageValue").textContent = pct(osag.coverage_error);
  $("coverageDelta").textContent = `${(100 * (Number(base.coverage_error) - Number(osag.coverage_error))).toFixed(1)} pts lower`;
  $("missedValue").textContent = String(osag.missed_service_cum);
  $("missedDelta").textContent = `${Number(base.missed_service_cum) - Number(osag.missed_service_cum)} vs ${baselineDisplay}`;
  $("reliabilityValue").textContent = num(osag.reliability_score);
  $("reliabilityDelta").textContent = `${num(Number(osag.reliability_score) - Number(base.reliability_score))} vs ${baselineDisplay}`;
  $("qhighValue").textContent = pct(osag.q_high);
  $("backlogValue").textContent = num(osag.backlog_size);
  $("budgetValue").textContent = `${osag.budget_obs} / ${osag.budget_ann}`;
  $("baselineNameValue").textContent = baselineDisplay;
}

function renderCodeMapping() {
  const mapping = DATA.codeMapping;
  const items = [
    ["Scenario trace powering this page", mapping.v2_bundle, "Static local traces for the three demo scenarios."],
    ["Demo V2 builder", mapping.v2_builder, "Generates the portable HTML package, fallback visuals, and optional insert slides."],
    ["Original dispatch logic", mapping.dispatch_core, "Contains budgeted observation choice, deadline pressure, and coverage-gap logic."],
    ["Dispatch entry point", mapping.dispatch_entry, "Safe command-line entry for the underlying dispatch-style demo path."],
    ["Benchmark governance logic", mapping.benchmark_core, "Real rerun implementation for contracts, coverage monitoring, and fairness controls."],
    ["Benchmark rerun entry", mapping.benchmark_entry, "Formal experiment entry point used for the locked thesis evidence chain."]
  ];
  $("codeMapping").innerHTML = items.map(([label, path, role]) => `
    <div class="code-card">
      <div class="guide-label">${label}</div>
      <div class="code-path">${path}</div>
      <div class="code-role">${role}</div>
    </div>
  `).join("");
}

function setMode(mode) {
  currentMode = mode;
  committeeSection.classList.toggle("hidden", mode !== "committee");
  presentationModeBtn.classList.toggle("active", mode === "presentation");
  committeeModeBtn.classList.toggle("active", mode === "committee");
}

function setTab(name) {
  tabButtons.forEach(btn => btn.classList.toggle("active", btn.dataset.tab === name));
  ["overview", "queue", "evidence", "code"].forEach(tab => {
    $("tab-" + tab).classList.toggle("active", tab === name);
  });
}

function refresh() {
  const step = Number(stepSlider.value);
  const baselineDisplay = baselineSelect.value;
  $("baselineTitle").textContent = baselineDisplay;
  $("stepReadout").textContent = `Time step ${step + 1} / ${currentScenario.steps}`;
  updateGuidedHeader(step, baselineDisplay);
  updateCards(step, baselineDisplay);
  renderExplanation(step, baselineDisplay);
  drawMap($("baselineMap"), byStep(currentScenario.frames, baselineDisplay, step), COLORS[baselineDisplay], selectedContract);
  drawMap($("osagMap"), byStep(currentScenario.frames, "OSAG", step), COLORS.OSAG, selectedContract);
  drawShareChart(step, baselineDisplay);
  drawTimeline(baselineDisplay);
  drawGapChart(step, baselineDisplay);
  renderQueue(step, baselineDisplay);
}

function togglePlay() {
  playing = !playing;
  playBtn.textContent = playing ? "Pause" : "Play";
  if (playing) {
    timerId = window.setInterval(() => {
      let next = Number(stepSlider.value) + 1;
      if (next >= currentScenario.steps) {
        next = 0;
      }
      stepSlider.value = String(next);
      refresh();
    }, 1200);
  } else {
    window.clearInterval(timerId);
  }
}

function resetView() {
  if (playing) {
    togglePlay();
  }
  stepSlider.value = String(currentScenario.keyMoments[1]);
  baselineSelect.value = DATA.ui.defaultBaseline;
  selectedContract = null;
  renderContractLegend();
  refresh();
}

function shiftStep(delta) {
  const current = Number(stepSlider.value);
  const next = Math.max(0, Math.min(currentScenario.steps - 1, current + delta));
  stepSlider.value = String(next);
  refresh();
}

buildScenarioOptions();
renderBenchmarkTable();
renderCodeMapping();
scenarioSelect.addEventListener("change", e => setScenario(e.target.value));
baselineSelect.addEventListener("change", refresh);
stepSlider.addEventListener("input", refresh);
prevBtn.addEventListener("click", () => shiftStep(-1));
nextBtn.addEventListener("click", () => shiftStep(1));
playBtn.addEventListener("click", togglePlay);
resetBtn.addEventListener("click", resetView);
presentationModeBtn.addEventListener("click", () => setMode("presentation"));
committeeModeBtn.addEventListener("click", () => setMode("committee"));
tabButtons.forEach(btn => btn.addEventListener("click", () => setTab(btn.dataset.tab)));
setScenario(DATA.ui.defaultScenario);
setMode(DATA.ui.defaultMode);
setTab("overview");
