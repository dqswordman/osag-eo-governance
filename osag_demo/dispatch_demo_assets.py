from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_tables(results: dict[str, pd.DataFrame], output_dir: Path) -> None:
    results["config"].to_csv(output_dir / "dispatch_config.csv", index=False)
    results["grid"].to_csv(output_dir / "dispatch_grid.csv", index=False)
    results["contracts"].to_csv(output_dir / "dispatch_contracts.csv", index=False)
    results["frames"].to_csv(output_dir / "dispatch_frames.csv", index=False)
    results["timeline"].to_csv(output_dir / "dispatch_timeline.csv", index=False)
    results["contract_state"].to_csv(output_dir / "dispatch_contract_state.csv", index=False)
    results["summary"].to_csv(output_dir / "dispatch_policy_summary.csv", index=False)
    results["real_summary"].to_csv(output_dir / "dispatch_real_results_snapshot.csv", index=False)


def plot_policy_timeline(results: dict[str, pd.DataFrame], output_dir: Path) -> None:
    timeline = results["timeline"]
    colors = {"Random": "#355070", "Contract-Priority": "#f4a261", "OSAG": "#c44536"}
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4))
    for display, group in timeline.groupby("display", sort=False):
        group = group.sort_values("step")
        axes[0].plot(group["step"], group["reliability_score"], "-o", linewidth=2.2, color=colors[display], label=display)
        axes[1].plot(group["step"], 100.0 * group["coverage_error"], "-o", linewidth=2.2, color=colors[display], label=display)
        axes[2].plot(group["step"], group["missed_service_cum"], "-o", linewidth=2.2, color=colors[display], label=display)
    axes[0].set_title("Mission Reliability Score")
    axes[0].set_ylabel("Score")
    axes[1].set_title("Coverage Error")
    axes[1].set_ylabel("PrioCovErr (%)")
    axes[2].set_title("Cumulative Missed Service")
    axes[2].set_ylabel("Missed contracts")
    for ax in axes:
        ax.set_xlabel("Time Step")
        ax.grid(alpha=0.22)
    axes[2].legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(output_dir / "dispatch_policy_timeline.png", dpi=220)
    plt.close(fig)


def plot_step_comparison(results: dict[str, pd.DataFrame], output_dir: Path, step: int = 7) -> None:
    frames = results["frames"]
    subset = frames[(frames["step"] == step) & (frames["display"].isin(["Contract-Priority", "OSAG"]))]
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.8))
    for ax, display in zip(axes, ["Contract-Priority", "OSAG"]):
        show = subset[subset["display"] == display]
        for _, row in show.iterrows():
            ax.add_patch(
                plt.Rectangle(
                    (row["col"], row["row"]),
                    1,
                    1,
                    facecolor=plt.cm.YlOrRd(min(row["hazard"] / max(show["hazard"].max(), 1e-6), 1.0)),
                    edgecolor="#ffffff" if row["observed"] else "#d0d7de",
                    linewidth=1.8 if row["observed"] else 0.45,
                )
            )
            if row["annotated"]:
                ax.plot(row["col"] + 0.5, row["row"] + 0.5, "o", color="#111111", markersize=3.0)
        ax.set_xlim(0, 12)
        ax.set_ylim(12, 0)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Step {step + 1}: {display}")
    fig.tight_layout()
    fig.savefig(output_dir / "dispatch_step8_comparison.png", dpi=220)
    plt.close(fig)


def plot_contract_gap(results: dict[str, pd.DataFrame], output_dir: Path, step: int = 7) -> None:
    state = results["contract_state"]
    subset = state[(state["step"] == step) & (state["display"].isin(["Contract-Priority", "OSAG"]))].copy()
    subset["gap_abs"] = subset["coverage_gap"].abs()
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    width = 0.38
    names = subset["contract_name"].drop_duplicates().tolist()
    xpos = list(range(len(names)))
    for offset, display, color in [(-width / 2, "Contract-Priority", "#f4a261"), (width / 2, "OSAG", "#c44536")]:
        show = subset[subset["display"] == display].sort_values("contract_id")
        ax.bar([x + offset for x in xpos], show["gap_abs"], width=width, label=display, color=color, alpha=0.9)
    ax.set_xticks(xpos)
    ax.set_xticklabels(names, rotation=24, ha="right")
    ax.set_ylabel("|Coverage Gap|")
    ax.set_title(f"Step {step + 1}: Contract Gap Comparison")
    ax.grid(alpha=0.2, axis="y")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_dir / "dispatch_contract_gap.png", dpi=220)
    plt.close(fig)


def save_text_summary(results: dict[str, pd.DataFrame], output_dir: Path) -> None:
    summary = results["summary"].copy()
    lines = [
        "Emergency Dispatch Demo Summary",
        "==============================",
        "",
    ]
    for _, row in summary.iterrows():
        lines.append(
            f"{row['display']}: "
            f"reliability={row['reliability_score']:.2f}, "
            f"service_gain={row['total_service_gain']:.2f}, "
            f"coverage_error={100.0 * row['final_coverage_error']:.2f}%, "
            f"critical_capture={100.0 * row['critical_capture_rate']:.2f}%, "
            f"missed_service={int(row['missed_service_total'])}, "
            f"service_compliance={100.0 * row['service_compliance']:.2f}%"
        )
    (output_dir / "dispatch_summary.txt").write_text("\n".join(lines), encoding="utf-8")


def build_dashboard(results: dict[str, pd.DataFrame], output_dir: Path) -> None:
    frames = results["frames"]
    timeline = results["timeline"]
    contract_state = results["contract_state"]
    real_summary = results["real_summary"]
    contracts = results["contracts"]
    summary = results["summary"]
    config = results["config"].iloc[0].to_dict()

    baseline_choices = [row["display"] for row in summary.to_dict(orient="records") if row["display"] != "OSAG"]
    real_rows = []
    if not real_summary.empty:
        keep = real_summary[real_summary["policy"].isin(["Random", "Contract-Priority", "OSAG", "OSAG-FairLoss (l=0.5)"])]
        real_rows = keep.to_dict(orient="records")

    bundle = {
        "config": config,
        "summary": summary.to_dict(orient="records"),
        "contracts": contracts.to_dict(orient="records"),
        "frames": frames.to_dict(orient="records"),
        "timeline": timeline.to_dict(orient="records"),
        "contractState": contract_state.to_dict(orient="records"),
        "realRows": real_rows,
        "baselineChoices": baseline_choices,
    }

    html = (
        "<!doctype html><html><head><meta charset='utf-8'><title>OSAG Dispatch Demo</title>"
        "<style>:root{--ink:#15202b;--sand:#f4ede1;--panel:#fffdf8;--line:#d9c9aa;--osag:#c44536;--base:#355070;--alt:#f4a261;--muted:#5f6c7b}body{margin:0;background:radial-gradient(circle at top left,#fff8ea 0%,#efe6d6 52%,#e3dccf 100%);color:var(--ink);font-family:Georgia,'Trebuchet MS',serif}.wrap{max-width:1460px;margin:0 auto;padding:24px 24px 44px}.hero{display:grid;grid-template-columns:340px 1fr;gap:18px;margin-bottom:18px}.panel{background:rgba(255,253,248,.92);border:1px solid var(--line);border-radius:20px;padding:18px 18px 20px;box-shadow:0 18px 44px rgba(36,40,46,.08)}h1{margin:0 0 10px;font-size:34px;line-height:1.05;letter-spacing:.02em}p.lead{margin:0;color:#45515f;line-height:1.55;font-size:15px}h2{margin:0 0 12px;font-size:18px;letter-spacing:.03em}.controls label{display:block;margin:10px 0 4px;font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}select,input[type=range]{width:100%;padding:9px 10px;border-radius:12px;border:1px solid var(--line);background:#fff;font-size:14px;box-sizing:border-box}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px}.card{border:1px solid var(--line);border-radius:16px;padding:12px 14px;background:linear-gradient(180deg,#fff 0%,#faf4e7 100%)}.card .label{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:5px}.card .value{font-size:26px;font-weight:700}.card .delta{font-size:12px;color:var(--muted);margin-top:4px}.maps{display:grid;grid-template-columns:1fr 1fr;gap:16px}.mapBox,.chartBox{border:1px solid var(--line);border-radius:18px;padding:12px;background:#fff}.mapBox h3,.chartBox h3{margin:0 0 8px;font-size:16px}.chartRow{display:grid;grid-template-columns:1.1fr .9fr;gap:16px;margin-top:16px}.tableWrap{max-height:340px;overflow:auto;border:1px solid var(--line);border-radius:14px;background:#fff}.tableWrap table{width:100%;border-collapse:collapse;font-size:13px}.tableWrap th,.tableWrap td{padding:8px 8px;border-bottom:1px solid #ede4d3;text-align:left}.tableWrap th{position:sticky;top:0;background:#fff8ea;color:#5b6774}.meta{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px}.meta .mini{border:1px solid var(--line);border-radius:14px;padding:10px;background:#fff}.meta .mini .label{font-size:11px;text-transform:uppercase;color:var(--muted);letter-spacing:.12em}.meta .mini .value{font-size:18px;font-weight:700;margin-top:5px}.legend{display:flex;gap:10px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-top:10px}.legend span::before{content:'';display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle}.foot{margin-top:18px;font-size:13px;color:var(--muted)}canvas{width:100%;height:320px;border-radius:12px;background:#fff}</style></head><body><div class='wrap'><div class='hero'><div class='panel controls'><h1>OSAG Dispatch Demo</h1><p class='lead'>Scenario: emergency EO dispatch over a city-scale grid. At each time step the system must allocate a fixed observation budget, a limited annotation budget, and model-update attention under explicit service contracts and revisit deadlines.</p><div class='meta'><div class='mini'><div class='label'>Observe</div><div class='value'>"
        + str(int(config["observe_budget"]))
        + "</div></div><div class='mini'><div class='label'>Annotate</div><div class='value'>"
        + str(int(config["annotate_budget"]))
        + "</div></div><div class='mini'><div class='label'>Steps</div><div class='value'>"
        + str(int(config["steps"]))
        + "</div></div></div><label>Baseline Policy</label><select id='baselineSelect'></select><label>Time Step</label><input id='stepSlider' type='range' min='0' max='"
        + str(int(config["steps"]) - 1)
        + "' value='7'><div id='stepReadout' style='margin-top:8px;color:#5f6c7b;font-size:13px'></div><div class='legend'><span style='--c:#355070;color:#355070'>Baseline</span><span style='--c:#c44536;color:#c44536'>OSAG</span><span style='--c:#111;color:#111'>Annotated tile</span></div><div class='foot'>High-priority contracts require short revisit intervals. The dashboard emphasizes guaranteed service share, contract gap, and missed service under real-time budget pressure.</div></div><div><div class='cards'><div class='card'><div class='label'>Reliability Score</div><div class='value' id='scoreCard'>-</div><div class='delta' id='scoreDelta'>-</div></div><div class='card'><div class='label'>Service Compliance</div><div class='value' id='complianceCard'>-</div><div class='delta' id='complianceDelta'>-</div></div><div class='card'><div class='label'>Coverage Error</div><div class='value' id='coverageCard'>-</div><div class='delta' id='coverageDelta'>-</div></div><div class='card'><div class='label'>Missed Service</div><div class='value' id='missedCard'>-</div><div class='delta' id='missedDelta'>-</div></div></div><div class='maps'><div class='mapBox'><h3 id='baselineTitle'>Baseline</h3><canvas id='baselineMap' width='620' height='320'></canvas></div><div class='mapBox'><h3>OSAG</h3><canvas id='osagMap' width='620' height='320'></canvas></div></div></div></div><div class='chartRow'><div class='panel chartBox'><h2>Timeline</h2><canvas id='timelineCanvas' width='760' height='340'></canvas></div><div class='panel'><h2>Contract State At Selected Step</h2><div class='tableWrap'><table id='contractTable'></table></div></div></div><div class='chartRow'><div class='panel chartBox'><h2>Contract Gap: Baseline vs OSAG</h2><canvas id='gapCanvas' width='760' height='320'></canvas></div><div class='panel'><h2>Fresh Real Benchmark Snapshot</h2><div class='tableWrap'><table id='realTable'></table></div></div></div></div><script>const DATA="
        + json.dumps(bundle, ensure_ascii=True)
        + ";const baselineSelect=document.getElementById('baselineSelect');DATA.baselineChoices.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;baselineSelect.appendChild(o);});baselineSelect.value='Contract-Priority';const stepSlider=document.getElementById('stepSlider');const pct=x=>(100*x).toFixed(1)+'%';const num=x=>Number(x).toFixed(1);const stepReadout=document.getElementById('stepReadout');const scoreCard=document.getElementById('scoreCard');const complianceCard=document.getElementById('complianceCard');const coverageCard=document.getElementById('coverageCard');const missedCard=document.getElementById('missedCard');const scoreDelta=document.getElementById('scoreDelta');const complianceDelta=document.getElementById('complianceDelta');const coverageDelta=document.getElementById('coverageDelta');const missedDelta=document.getElementById('missedDelta');const baselineMap=document.getElementById('baselineMap');const osagMap=document.getElementById('osagMap');const baselineTitle=document.getElementById('baselineTitle');function frame(display,step){return DATA.frames.filter(r=>r.display===display&&r.step===step);}function timeline(display){return DATA.timeline.filter(r=>r.display===display).sort((a,b)=>a.step-b.step);}function contractState(display,step){return DATA.contractState.filter(r=>r.display===display&&r.step===step).sort((a,b)=>a.contract_id-b.contract_id);}function drawGrid(canvas,rows,titleColor){const ctx=canvas.getContext('2d');ctx.clearRect(0,0,canvas.width,canvas.height);const cell=24,ox=18,oy=18;rows.forEach(r=>{const x=ox+r.col*cell,y=oy+r.row*cell;const hazard=Math.max(0,Math.min(1,r.hazard/2.2));const red=Math.floor(241-30*hazard),green=Math.floor(234-120*hazard),blue=Math.floor(214-180*hazard);ctx.fillStyle=`rgb(${red},${green},${blue})`;ctx.fillRect(x,y,cell-1,cell-1);ctx.strokeStyle=r.observed?titleColor:'#d7c8ad';ctx.lineWidth=r.observed?2.4:0.45;ctx.strokeRect(x+0.6,y+0.6,cell-2.2,cell-2.2);if(r.annotated){ctx.fillStyle='#111';ctx.beginPath();ctx.arc(x+cell/2,y+cell/2,2.4,0,Math.PI*2);ctx.fill();}if(r.priority>=3){ctx.strokeStyle='rgba(196,69,54,.55)';ctx.lineWidth=1.1;ctx.strokeRect(x+3,y+3,cell-7,cell-7);}if(r.missed_contract){ctx.strokeStyle='#111';ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(x+5,y+5);ctx.lineTo(x+cell-6,y+cell-6);ctx.moveTo(x+cell-6,y+5);ctx.lineTo(x+5,y+cell-6);ctx.stroke();}});ctx.fillStyle='#485363';ctx.font='12px Georgia';ctx.fillText('Hazard field + selected tiles',18,14);}function setCards(step){const base = timeline(baselineSelect.value)[step];const osag = timeline('OSAG')[step];scoreCard.textContent = num(osag.reliability_score);complianceCard.textContent = pct(osag.service_compliance);coverageCard.textContent = pct(osag.coverage_error);missedCard.textContent = String(osag.missed_service_cum);scoreDelta.textContent = 'vs baseline: ' + num(osag.reliability_score-base.reliability_score);complianceDelta.textContent = 'vs baseline: ' + (100*(osag.service_compliance-base.service_compliance)).toFixed(1) + ' pts';coverageDelta.textContent = 'vs baseline: ' + (100*(base.coverage_error-osag.coverage_error)).toFixed(1) + ' pts lower';missedDelta.textContent = 'vs baseline: ' + (base.missed_service_cum-osag.missed_service_cum) + ' fewer';stepReadout.textContent = 'Time step ' + (step+1) + ' / ' + DATA.config.steps + ' | baseline: ' + baselineSelect.value;baselineTitle.textContent = baselineSelect.value;}function axis(ctx,x,y,w,h,xLabel,yLabel){ctx.strokeStyle='#5d6672';ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x,y+h);ctx.lineTo(x+w,y+h);ctx.stroke();ctx.fillStyle='#5d6672';ctx.font='12px Georgia';ctx.fillText(xLabel,x+w-36,y+h+24);ctx.save();ctx.translate(18,y+h/2);ctx.rotate(-Math.PI/2);ctx.fillText(yLabel,0,0);ctx.restore();}function drawTimeline(){const canvas=document.getElementById('timelineCanvas');const ctx=canvas.getContext('2d');ctx.clearRect(0,0,canvas.width,canvas.height);const x=56,y=20,w=canvas.width-80,h=canvas.height-54;axis(ctx,x,y,w,h,'step','value');const series=['Random','Contract-Priority','OSAG'];const colors={'Random':'#355070','Contract-Priority':'#f4a261','OSAG':'#c44536'};const maxScore=Math.max(...DATA.timeline.map(r=>r.reliability_score));const maxMiss=Math.max(...DATA.timeline.map(r=>r.missed_service_cum),1);series.forEach(name=>{const rows=timeline(name);ctx.strokeStyle=colors[name];ctx.lineWidth=name==='OSAG'?3.0:2.0;ctx.beginPath();rows.forEach((r,i)=>{const px=x+(r.step/(DATA.config.steps-1))*w;const py=y+h-(r.reliability_score/maxScore)*h*0.60;if(i===0)ctx.moveTo(px,py);else ctx.lineTo(px,py);});ctx.stroke();ctx.setLineDash([5,5]);ctx.beginPath();rows.forEach((r,i)=>{const px=x+(r.step/(DATA.config.steps-1))*w;const py=y+h-((r.missed_service_cum)/maxMiss)*h*0.30-h*0.62;if(i===0)ctx.moveTo(px,py);else ctx.lineTo(px,py);});ctx.stroke();ctx.setLineDash([]);ctx.fillStyle=colors[name];ctx.fillText(name,x+6,y+18+16*series.indexOf(name));});ctx.fillStyle='#5f6c7b';ctx.fillText('Solid: reliability score',x+180,y+18);ctx.fillText('Dashed: cumulative missed service',x+180,y+34);}function drawGap(step){const canvas=document.getElementById('gapCanvas');const ctx=canvas.getContext('2d');ctx.clearRect(0,0,canvas.width,canvas.height);const x=56,y=22,w=canvas.width-80,h=canvas.height-56;axis(ctx,x,y,w,h,'contract','|gap|');const base=contractState(baselineSelect.value,step),osag=contractState('OSAG',step),maxGap=Math.max(...base.map(r=>Math.abs(r.coverage_gap)).concat(osag.map(r=>Math.abs(r.coverage_gap))),1);const bw=w/(base.length*2+2);base.forEach((r,i)=>{const left=x+(i*2+0.5)*bw;const bh=(Math.abs(r.coverage_gap)/maxGap)*h;ctx.fillStyle='#f4a261';ctx.fillRect(left,y+h-bh,bw-4,bh);const ro=osag[i];const oh=(Math.abs(ro.coverage_gap)/maxGap)*h;ctx.fillStyle='#c44536';ctx.fillRect(left+bw,y+h-oh,bw-4,oh);ctx.fillStyle='#495664';ctx.font='10px Georgia';ctx.fillText('C'+r.contract_id,left-2,y+h+16);});}function renderContractTable(step){const base=contractState(baselineSelect.value,step),osag=contractState('OSAG',step);let html='<thead><tr><th>Contract</th><th>Priority</th><th>Baseline Gap</th><th>OSAG Gap</th><th>Baseline Q</th><th>OSAG Q</th></tr></thead><tbody>';base.forEach((r,i)=>{const o=osag[i];html+=`<tr><td>${r.contract_name}</td><td>P${r.priority}</td><td>${r.coverage_gap.toFixed(2)}</td><td>${o.coverage_gap.toFixed(2)}</td><td>${r.knowledge.toFixed(2)}</td><td>${o.knowledge.toFixed(2)}</td></tr>`;});html+='</tbody>';document.getElementById('contractTable').innerHTML=html;}function renderRealTable(){let html='<thead><tr><th>Dataset</th><th>Policy</th><th>Acc_high</th><th>PCE</th></tr></thead><tbody>';DATA.realRows.forEach(r=>{html+=`<tr><td>${r.dataset}</td><td>${r.policy}</td><td>${pct(r.acc_high_mean)}</td><td>${pct(r.prio_cov_err_mean)}</td></tr>`;});html+='</tbody>';document.getElementById('realTable').innerHTML=html;}function refresh(){const step=Number(stepSlider.value);setCards(step);drawGrid(baselineMap,frame(baselineSelect.value,step),'#355070');drawGrid(osagMap,frame('OSAG',step),'#c44536');drawTimeline();drawGap(step);renderContractTable(step);}baselineSelect.addEventListener('change',refresh);stepSlider.addEventListener('input',refresh);renderRealTable();refresh();</script></body></html>"
    )
    (output_dir / "demo_dashboard.html").write_text(html, encoding="utf-8")
