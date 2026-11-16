#!/usr/bin/env python3
"""
Generate presentation/index.html
A comprehensive, interactive academic presentation covering:
- Project A: Choroid OCT Segmentation and Thickness Measurement
- Project B: Hybrid Quantum-Classical Medical Image Classification
15 Main Slides + 4 Backup Slides (19 Slides Total)
"""

import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Two Approaches to Medical Image Analysis | Academic Presentation</title>
  <style>
    :root {
      --bg-primary: #0a0f1d;
      --bg-secondary: #111827;
      --bg-card: #1f2937;
      --bg-card-hover: #374151;
      --text-main: #f9fafb;
      --text-muted: #9ca3af;
      --accent-cyan: #38bdf8;
      --accent-teal: #2dd4bf;
      --accent-green: #34d399;
      --accent-amber: #fbbf24;
      --accent-rose: #f43f5e;
      --accent-purple: #c084fc;
      --border-color: #374151;
      --slide-ratio: 16 / 9;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-main);
      overflow: hidden;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Top Progress & Navigation Bar */
    header {
      background: rgba(17, 24, 39, 0.95);
      border-bottom: 1px solid var(--border-color);
      padding: 8px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 52px;
      z-index: 50;
      backdrop-filter: blur(8px);
    }

    .progress-bar-container {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: rgba(255, 255, 255, 0.1);
    }

    .progress-bar {
      height: 100%;
      background: linear-gradient(90deg, var(--accent-cyan), var(--accent-teal), var(--accent-purple));
      width: 5.26%;
      transition: width 0.3s ease;
    }

    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .badge-section {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 3px 8px;
      border-radius: 4px;
      background: #1e3a8a;
      color: #93c5fd;
    }

    .badge-section.oct {
      background: #064e3b;
      color: #6ee7b7;
    }

    .badge-section.quantum {
      background: #581c87;
      color: #d8b4fe;
    }

    .badge-section.backup {
      background: #78350f;
      color: #fde68a;
    }

    .header-title {
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-muted);
      max-width: 550px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .header-controls {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .btn-nav {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 0.82rem;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }

    .btn-nav:hover {
      background: var(--bg-card-hover);
      border-color: var(--accent-cyan);
    }

    .slide-counter {
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--accent-cyan);
      min-width: 80px;
      text-align: center;
    }

    /* Presentation Workspace */
    main {
      flex: 1;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 16px;
      overflow: hidden;
    }

    .slide-stage {
      width: 100%;
      max-width: 1380px;
      aspect-ratio: 16 / 9;
      max-height: calc(100vh - 84px);
      background: var(--bg-secondary);
      border-radius: 12px;
      border: 1px solid var(--border-color);
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    .slide {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      padding: 36px 44px;
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
    }

    .slide.active {
      opacity: 1;
      visibility: visible;
      z-index: 10;
    }

    /* Slide Typography */
    .slide-header {
      margin-bottom: 20px;
    }

    .slide-category {
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--accent-cyan);
      margin-bottom: 4px;
    }

    .slide-title {
      font-size: 1.85rem;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
    }

    .slide-subtitle {
      font-size: 0.95rem;
      color: var(--text-muted);
      margin-top: 4px;
    }

    .slide-body {
      flex: 1;
      display: flex;
      gap: 28px;
      min-height: 0;
    }

    .col-left, .col-right {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .col-60 { flex: 1.35; }
    .col-40 { flex: 0.95; }
    .col-50 { flex: 1; }

    /* Cards & Containers */
    .card {
      background: rgba(31, 41, 55, 0.65);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 16px 20px;
    }

    .card.highlight {
      border-color: var(--accent-cyan);
      background: rgba(14, 116, 144, 0.15);
    }

    .card.warning {
      border-color: var(--accent-amber);
      background: rgba(180, 83, 9, 0.15);
    }

    .card.success {
      border-color: var(--accent-green);
      background: rgba(6, 78, 59, 0.2);
    }

    .card-title {
      font-size: 1rem;
      font-weight: 700;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .bullet-list {
      list-style-type: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .bullet-list li {
      position: relative;
      padding-left: 20px;
      font-size: 0.9rem;
      line-height: 1.45;
      color: #e5e7eb;
    }

    .bullet-list li::before {
      content: "•";
      position: absolute;
      left: 4px;
      color: var(--accent-cyan);
      font-weight: bold;
      font-size: 1.2rem;
      line-height: 1;
    }

    .bullet-list.oct li::before { color: var(--accent-green); }
    .bullet-list.quantum li::before { color: var(--accent-purple); }
    .bullet-list.warning li::before { color: var(--accent-amber); }

    /* Image Display */
    .figure-container {
      background: #0f172a;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }

    .figure-container img {
      max-width: 100%;
      max-height: 340px;
      object-fit: contain;
      border-radius: 4px;
    }

    .figure-caption {
      font-size: 0.76rem;
      color: var(--text-muted);
      margin-top: 8px;
      text-align: center;
    }

    /* Tables */
    .data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      text-align: left;
    }

    .data-table th {
      background: rgba(17, 24, 39, 0.9);
      color: var(--accent-cyan);
      font-weight: 700;
      padding: 8px 12px;
      border-bottom: 2px solid var(--border-color);
    }

    .data-table td {
      padding: 8px 12px;
      border-bottom: 1px solid var(--border-color);
      color: #e5e7eb;
    }

    .data-table tr:hover td {
      background: rgba(255, 255, 255, 0.04);
    }

    .data-table .best-val {
      color: var(--accent-green);
      font-weight: 700;
    }

    /* Math formulas */
    .math-block {
      background: #0d1322;
      border-left: 3px solid var(--accent-purple);
      padding: 10px 14px;
      border-radius: 0 6px 6px 0;
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 0.88rem;
      color: #c084fc;
      margin: 6px 0;
    }

    /* Speaker Notes Modal */
    .speaker-drawer {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: #111827;
      border-top: 2px solid var(--accent-cyan);
      padding: 20px 32px;
      max-height: 260px;
      overflow-y: auto;
      z-index: 100;
      transform: translateY(100%);
      transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 -10px 25px rgba(0, 0, 0, 0.8);
    }

    .speaker-drawer.open {
      transform: translateY(0);
    }

    .speaker-drawer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }

    .speaker-drawer-title {
      font-size: 0.9rem;
      font-weight: 700;
      color: var(--accent-cyan);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .speaker-drawer-close {
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 1.2rem;
    }

    .speaker-drawer-content {
      font-size: 0.95rem;
      line-height: 1.6;
      color: #d1d5db;
    }

    /* Slide Grid Overview */
    .overview-modal {
      position: fixed;
      inset: 0;
      background: rgba(10, 15, 29, 0.95);
      z-index: 200;
      padding: 40px;
      display: none;
      flex-direction: column;
      overflow-y: auto;
      backdrop-filter: blur(12px);
    }

    .overview-modal.open {
      display: flex;
    }

    .overview-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }

    .overview-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 150px;
    }

    .overview-card:hover {
      border-color: var(--accent-cyan);
      transform: translateY(-2px);
    }

    .overview-card.active {
      border-color: var(--accent-teal);
      box-shadow: 0 0 12px rgba(45, 212, 191, 0.4);
    }

    .overview-card-num {
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--accent-cyan);
    }

    .overview-card-title {
      font-size: 0.9rem;
      font-weight: 600;
      color: #ffffff;
      margin-top: 4px;
    }

    .overview-card-tag {
      font-size: 0.7rem;
      padding: 2px 6px;
      border-radius: 4px;
      align-self: flex-start;
      margin-top: 10px;
    }
  </style>
</head>
<body>

  <!-- Top Bar -->
  <header>
    <div class="progress-bar-container">
      <div class="progress-bar" id="progressBar"></div>
    </div>
    <div class="header-left">
      <span class="badge-section" id="sectionBadge">OPENING</span>
      <span class="header-title" id="headerTitle">Academic Presentation</span>
    </div>
    <div class="header-controls">
      <button class="btn-nav" id="btnPrev" title="Previous Slide (Left Arrow)">◀ Prev</button>
      <span class="slide-counter" id="slideCounter">1 / 19</span>
      <button class="btn-nav" id="btnNext" title="Next Slide (Right Arrow, Space)">Next ▶</button>
      <button class="btn-nav" id="btnNotes" title="Toggle Speaker Notes (N)">📝 Notes</button>
      <button class="btn-nav" id="btnOverview" title="Slide Overview (O)">🗂 Grid</button>
      <button class="btn-nav" id="btnFullscreen" title="Toggle Fullscreen (F)">⛶ Fullscreen</button>
    </div>
  </header>

  <!-- Presentation Workspace -->
  <main>
    <div class="slide-stage">

      <!-- SLIDE 1: Title -->
      <div class="slide active" data-slide="1" data-section="OPENING" data-badge="OPENING">
        <div class="slide-header" style="text-align: center; margin-bottom: 24px;">
          <div class="slide-category">ACADEMIC MASTER'S DEFENSE / SEMESTER PRESENTATION</div>
          <h1 class="slide-title" style="font-size: 2.2rem; max-width: 1100px; margin: 0 auto;">
            Two Approaches to Medical Image Analysis: Deep Segmentation for Choroidal Thickness and Hybrid Quantum-Classical Pneumonia Detection
          </h1>
          <p class="slide-subtitle" style="font-size: 1.05rem; margin-top: 8px;">
            A Comparative Study in Model Design, Data Integrity, and Rigorous Evaluation
          </p>
          <div style="margin-top: 12px; font-size: 0.95rem; color: #cbd5e1;">
            <strong>Aditya Sahrawat</strong> &bull; Medical Image Analysis & Deep Learning &bull; Academic Year 2026
          </div>
        </div>
        <div class="slide-body" style="align-items: center; justify-content: center;">
          <div class="figure-container" style="max-width: 960px; width: 100%; padding: 12px; background: #0f172a;">
            <img src="assets/title_split.png" alt="Split view: Retinal OCT on left, Chest X-ray on right" style="max-height: 380px;">
            <div class="figure-caption">
              Figure 1: Multimodal comparative scope — High-resolution Retinal OCT B-scan segmentation (Project A) versus 28×28 Grayscale Chest X-Ray classification (Project B).
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "Good morning Professor. Today I am presenting two distinct medical image analysis projects. On the left is an automated segmentation and thickness measurement pipeline for the choroid layer in retinal OCT scans. On the right is a hybrid quantum-classical classifier for pediatric pneumonia detection in chest X-rays. While their clinical domains and architectures differ, the unifying thread of this presentation is scientific rigor: leakage-free splitting, capacity-matched baseline controls, and honest metric reporting."
        </div>
      </div>

      <!-- SLIDE 2: Roadmap and Common Thread -->
      <div class="slide" data-slide="2" data-section="OPENING" data-badge="OPENING">
        <div class="slide-header">
          <div class="slide-category">PRESENTATION ROADMAP & METHODOLOGICAL FOUNDATION</div>
          <h2 class="slide-title">Two Distinct Problems, One Uncompromising Standard of Rigor</h2>
          <p class="slide-subtitle">How honest experimental design binds specialized clinical pipelines</p>
        </div>
        <div class="slide-body">
          <div class="col-left">
            <div class="card" style="border-left: 4px solid var(--accent-green); height: 100%;">
              <div class="card-title" style="color: var(--accent-green);">
                <span>🔬 Project A: Retinal Choroid OCT</span>
              </div>
              <ul class="bullet-list oct" style="margin-top: 12px;">
                <li><strong>Clinical Task:</strong> Boundary segmentation & thickness measurement (SFCT).</li>
                <li><strong>Imaging Modality:</strong> Spectral-Domain OCT B-scans (Heidelberg Spectralis).</li>
                <li><strong>Architectures:</strong> U-Net baseline &rarr; U-Net++ with scSE spatial/channel attention.</li>
                <li><strong>Core Question:</strong> <em>"Can deep networks resolve the faint choroidal-scleral interface with sub-pixel anatomical fidelity and clinical agreement?"</em></li>
              </ul>
            </div>
          </div>
          <div class="col-right">
            <div class="card" style="border-left: 4px solid var(--accent-purple); height: 100%;">
              <div class="card-title" style="color: var(--accent-purple);">
                <span>⚛️ Project B: Quantum Chest X-Ray</span>
              </div>
              <ul class="bullet-list quantum" style="margin-top: 12px;">
                <li><strong>Clinical Task:</strong> Binary pediatric pneumonia classification (Normal vs Pneumonia).</li>
                <li><strong>Imaging Modality:</strong> PneumoniaMNIST (28 &times; 28 grayscale X-rays).</li>
                <li><strong>Architectures:</strong> Classical CNN &rarr; Parameter-matched MLP &rarr; 4-qubit Hybrid QNN.</li>
                <li><strong>Core Question:</strong> <em>"Can a 29-parameter variational quantum circuit serve as an effective, competitive classifier head against matched classical controls?"</em></li>
              </ul>
            </div>
          </div>
        </div>
        <div class="card warning" style="margin-top: 16px;">
          <div class="card-title" style="color: var(--accent-amber); font-size: 0.92rem;">
            ⚖️ The Unifying Common Thread: Scientific Honesty Over Superficial Claims
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 6px; font-size: 0.85rem; color: #e2e8f0;">
            <div><strong>1. Leakage-Free Splits:</strong> Enforcing strict patient-level isolation (OCT) and benchmark protocols to avoid illusory performance.</div>
            <div><strong>2. Fair Capacity Controls:</strong> Refusing to compare 29-param quantum heads against 100k-param classical networks without matched baselines.</div>
            <div><strong>3. Transparent Failures:</strong> Scrutinizing where and why models fail (vessel shadows, prevalence shifts, test specificity drops).</div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "Both projects ask the same fundamental question: not just 'does it work?', but 'how do we know it works, and where does it fail?'. In Project A, we address high-resolution choroid segmentation where spatial leakage from adjacent B-scans threatens validity. In Project B, we integrate variational quantum circuits into deep learning, where uncalibrated baselines often lead to exaggerated claims. The presentation consists of two 6-slide technical audits followed by cross-project synthesis and Q&A backup."
        </div>
      </div>

      <!-- SLIDE 3: Clinical Problem (Choroid OCT) -->
      <div class="slide" data-slide="3" data-section="PROJECT A: CHOROID OCT" data-badge="PROJECT A: CHOROID">
        <div class="slide-header">
          <div class="slide-category">PROJECT A: CHOROID OCT SEGMENTATION &bull; CLINICAL CONTEXT</div>
          <h2 class="slide-title">The Clinical Challenge of Choroidal Thickness Quantification</h2>
          <p class="slide-subtitle">Vascular anatomy, manual measurement bottlenecks, and data ground truth verification</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="figure-container" style="height: 100%;">
              <img src="assets/choroid_anatomy_diagram.png" alt="Choroid Anatomy Diagram" style="max-height: 280px;">
              <div class="figure-caption">
                Figure 3.1: Posterior ocular anatomy in SD-OCT. Bruch's Membrane (BM, inner boundary) and Choroidal-Scleral Interface (CSI, outer boundary).
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div class="card-title" style="color: var(--accent-cyan);">Diagnostic Significance & Limitations</div>
                <ul class="bullet-list oct" style="margin-top: 8px;">
                  <li><strong>Ocular Biomarker:</strong> The choroid supplies oxygen to the avascular fovea. Thinning occurs in pathological myopia and dry AMD; thickening occurs in pachychoroid spectrum disease (CSCR, PCV).</li>
                  <li><strong>Manual Bottleneck:</strong> Segmenting 3D volumes requires 30–60 min per eye. Expert graders disagree by 15–30 &mu;m, particularly at the faint CSI transition.</li>
                  <li><strong>Clinical Objective:</strong> Automated Subfoveal Choroidal Thickness (SFCT) measurement across full B-scans.</li>
                </ul>
              </div>
              <div class="card highlight" style="margin-top: 12px; border-color: var(--accent-teal);">
                <div class="card-title" style="color: var(--accent-teal); font-size: 0.88rem;">🚨 Critical Dataset Audit Discovery (OIMHS)</div>
                <p style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.4;">
                  The OIMHS dataset includes multiple mask channels. Our exploratory audit revealed that the green mask (~37 &mu;m above BM) corresponds to neurosensory retina, whereas the yellow mask (~214 &mu;m below BM) is the true choroidal stroma. Naive training on green masks segments retina, not choroid!
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "The choroid is the dense vascular layer behind the retina. Accurately measuring Subfoveal Choroidal Thickness is essential for detecting conditions like pachychoroid diseases and age-related macular degeneration. However, manual annotation takes up to an hour per volume, and experts disagree by 15 to 30 micrometers due to low contrast at the choroid-sclera interface. Before writing a line of code, we audited the OIMHS dataset masks and discovered that the green mask was retina, not choroid. The yellow mask was verified as the true choroidal stroma, preventing a catastrophic ground-truth error."
        </div>
      </div>

      <!-- SLIDE 4: Pipeline & Data Splitting (Choroid OCT) -->
      <div class="slide" data-slide="4" data-section="PROJECT A: CHOROID OCT" data-badge="PROJECT A: CHOROID">
        <div class="slide-header">
          <div class="slide-category">PROJECT A: CHOROID OCT SEGMENTATION &bull; METHODOLOGY</div>
          <h2 class="slide-title">Leakage-Free Patient Splitting and Processing Pipeline</h2>
          <p class="slide-subtitle">Guaranteed patient isolation across 3,859 Spectralis B-scans</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-60">
            <div class="figure-container">
              <img src="assets/choroid_pipeline_diagram.png" alt="Choroid Pipeline Diagram" style="max-height: 230px;">
              <div class="figure-caption">
                Figure 4.1: End-to-end pipeline: raw B-scan ingestion, patient-isolated training, U-Net++ scSE segmentation, anatomical post-processing, and clinical SFCT computation.
              </div>
            </div>
            <div class="card warning" style="margin-top: 10px; padding: 10px 16px;">
              <div class="card-title" style="color: var(--accent-amber); font-size: 0.86rem;">⚠️ The Severe Pitfall of Random B-Scan Splitting</div>
              <p style="font-size: 0.82rem; color: #e2e8f0; line-height: 1.4;">
                Adjacent B-scans within a Heidelberg Spectralis volume are separated by only 30–120 &mu;m. A random scan-level split places nearly identical slices of the same patient into both training and test sets, leaking patient vascular architecture and yielding deceptively inflated metrics.
              </p>
            </div>
          </div>
          <div class="col-right col-40">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-cyan);">Strict Patient-Level Partitioning</div>
              <table class="data-table" style="margin-top: 10px;">
                <thead>
                  <tr>
                    <th>Partition</th>
                    <th>Patients</th>
                    <th>Eyes</th>
                    <th>Scans</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Train</strong></td>
                    <td>83 (69.7%)</td>
                    <td>87</td>
                    <td>2,609</td>
                  </tr>
                  <tr>
                    <td><strong>Validation</strong></td>
                    <td>18 (15.1%)</td>
                    <td>19</td>
                    <td>553</td>
                  </tr>
                  <tr>
                    <td><strong>Test</strong></td>
                    <td>18 (15.1%)</td>
                    <td>19</td>
                    <td>697</td>
                  </tr>
                  <tr style="border-top: 2px solid var(--accent-cyan); font-weight: bold;">
                    <td>Total</td>
                    <td>119 Pts</td>
                    <td>125 Eyes</td>
                    <td>3,859</td>
                  </tr>
                </tbody>
              </table>
              <div style="margin-top: 16px; font-size: 0.82rem; color: #cbd5e1; line-height: 1.45;">
                <p>• Zero patient overlap between splits.</p>
                <p>• Test set consists of 18 unseen patients (19 eyes, 697 B-scans).</p>
                <p>• Input resolution standardized to 512 &times; 512 with CLAHE contrast enhancement.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "The critical methodological safeguard in Project A is patient-level partitioning. An OCT volume consists of parallel B-scans spaced only 30 to 120 micrometers apart. If you randomly partition scans, adjacent slices from the same eye land in both train and test, leaking anatomical features and fabricating artificial performance. We strictly held out 18 patients and 19 eyes for testing, ensuring that our 697 test scans represent truly unseen clinical cases."
        </div>
      </div>

      <!-- SLIDE 5: Architecture & Loss Design (Choroid OCT) -->
      <div class="slide" data-slide="5" data-section="PROJECT A: CHOROID OCT" data-badge="PROJECT A: CHOROID">
        <div class="slide-header">
          <div class="slide-category">PROJECT A: CHOROID OCT SEGMENTATION &bull; MODEL DESIGN</div>
          <h2 class="slide-title">Architecture Upgrade & Boundary-Weighted Loss Formulation</h2>
          <p class="slide-subtitle">U-Net++ with scSE attention and exponential boundary penalty</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-cyan);">Architectural Comparison</div>
              <ul class="bullet-list oct" style="margin-top: 8px;">
                <li><strong>Baseline Architecture:</strong> Standard U-Net with ResNet34 encoder (24.43M parameters). Direct skip connections span large semantic gaps.</li>
                <li><strong>Improved System Configuration:</strong> U-Net++ with ResNet34 backbone + concurrent Spatial and Channel Squeeze-and-Excitation (scSE) blocks (26.28M parameters, +7.55% capacity).</li>
                <li><strong>Dense Nested Skips:</strong> Bridges semantic disparity between encoder stages and decoder blocks via intermediate convolution dense nodes.</li>
                <li><strong>scSE Attention Blocks:</strong> Recalibrates channel feature dependencies ('what' tissue) alongside spatial excitation ('where' boundaries lie).</li>
              </ul>
              <div class="card highlight" style="margin-top: 12px; font-size: 0.82rem; color: #cbd5e1;">
                <strong>Scientific Attribution Note:</strong> Because architecture, attention, boundary loss, and effective batch size (8 via accumulation vs 2) were upgraded together, gains reflect the <em>combined improved configuration</em> rather than isolated scSE ablation. 4 training epochs.
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-teal);">Boundary-Weighted Loss Function</div>
              <p style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 8px;">
                Standard cross-entropy treats all pixels equally, allowing large interior areas to dominate gradients while fuzzy boundaries suffer. We engineered a spatial boundary distance penalty:
              </p>
              <div class="math-block">
                w(x) = 1 + 5 &bull; exp(-d(x)&sup2; / (2 &bull; &sigma;&sup2;)),   with &sigma; = 5 px
              </div>
              <div class="math-block">
                L_total = L_BCE,weighted + L_Dice
              </div>
              <ul class="bullet-list oct" style="margin-top: 10px;">
                <li>$d(x)$ is the Euclidean distance from pixel $x$ to the nearest true boundary (BM or CSI).</li>
                <li>Pixels exactly on the boundary receive a <strong>6&times; loss penalty</strong> ($1 + 5 = 6$).</li>
                <li>Exponential falloff smoothly relaxes to 1.0 in interior stroma and distant background.</li>
                <li>Directly penalizes the 1–3 pixel boundary drift that corrupts clinical thickness profiles.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "To resolve the subtle choroid-sclera interface, we upgraded from standard U-Net to U-Net++ with ResNet34 and concurrent spatial-and-channel squeeze-and-excitation blocks, adding only 7.5% parameters. In parallel, standard loss treats all pixels equally, so models easily get high Dice by predicting the fat center of the choroid while missing the edge. We implemented a boundary-weighted loss that upweights boundary pixels by up to six times with a five-pixel Gaussian sigma. To maintain academic rigor, we report this as an overall improved configuration since multiple components evolved together."
        </div>
      </div>

      <!-- SLIDE 6: Segmentation and Boundary Results (Choroid OCT) -->
      <div class="slide" data-slide="6" data-section="PROJECT A: CHOROID OCT" data-badge="PROJECT A: CHOROID">
        <div class="slide-header">
          <div class="slide-category">PROJECT A: CHOROID OCT SEGMENTATION &bull; EVALUATION</div>
          <h2 class="slide-title">Quantitative Segmentation & Boundary Localization Performance</h2>
          <p class="slide-subtitle">Comprehensive evaluation across 697 holdout test B-scans (18 patients / 19 eyes)</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-cyan);">Test Performance Comparison</div>
              <table class="data-table" style="margin-top: 10px;">
                <thead>
                  <tr>
                    <th>Evaluation Metric</th>
                    <th>Baseline U-Net</th>
                    <th>U-Net++ scSE</th>
                    <th>Change</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Choroid Dice</strong></td>
                    <td>0.9751</td>
                    <td class="best-val">0.9804</td>
                    <td>+0.54%</td>
                  </tr>
                  <tr>
                    <td><strong>BM MAE (Inner)</strong></td>
                    <td>0.562 px</td>
                    <td class="best-val">0.407 px</td>
                    <td class="best-val"><strong>-27.6%</strong></td>
                  </tr>
                  <tr>
                    <td><strong>CSI MAE (Outer)</strong></td>
                    <td>1.755 px</td>
                    <td class="best-val">1.567 px</td>
                    <td class="best-val"><strong>-10.7%</strong></td>
                  </tr>
                  <tr>
                    <td><strong>Thickness MAE</strong></td>
                    <td>1.870 px</td>
                    <td class="best-val">1.715 px</td>
                    <td class="best-val"><strong>-8.3%</strong></td>
                  </tr>
                  <tr>
                    <td><strong>Mask HD95</strong></td>
                    <td>3.98 px</td>
                    <td class="best-val">3.40 px</td>
                    <td class="best-val"><strong>-14.6%</strong></td>
                  </tr>
                </tbody>
              </table>
              <div class="card warning" style="margin-top: 12px; font-size: 0.8rem; padding: 10px;">
                <strong>Measurement Units:</strong> Pixel metrics are native and primary. Physical estimates: BM MAE &approx; <strong>1.53 &mu;m</strong>, CSI MAE &approx; <strong>5.88 &mu;m</strong> (assuming Heidelberg Spectralis 3.75 &mu;m/px axial scale). Both are well within human grader disagreement (15–30 &mu;m).
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="figure-container" style="height: 100%;">
              <img src="assets/39_10_seg.png" alt="Segmentation Result Eye 39 Scan 10" style="max-height: 290px;">
              <div class="figure-caption">
                Figure 6.1: Qualitative segmentation for holdout Eye 39, Scan 10. Raw B-scan, ground truth annotation, U-Net++ prediction, and pixel-level boundary error map.
              </div>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "Here are the test results on 697 unseen B-scans from 18 holdout patients. While Dice improved modestly from 0.975 to 0.980, the boundary-weighted loss drove double-digit reductions in boundary localization error: Bruch's membrane error dropped by 27.6% to 0.407 pixels (about 1.5 micrometers), and CSI error dropped by 10.7% to 1.57 pixels (about 5.9 micrometers). Both errors are well below the 15 to 30 micrometer inter-grader variability between human experts."
        </div>
      </div>

      <!-- SLIDE 7: Thickness Measurement & Bland-Altman (Choroid OCT) -->
      <div class="slide" data-slide="7" data-section="PROJECT A: CHOROID OCT" data-badge="PROJECT A: CHOROID">
        <div class="slide-header">
          <div class="slide-category">PROJECT A: CHOROID OCT SEGMENTATION &bull; CLINICAL VALIDATION</div>
          <h2 class="slide-title">Clinical Agreement Analysis & The Post-Processing Paradox</h2>
          <p class="slide-subtitle">Bland-Altman agreement and the peril of conventional morphological hole-filling</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="figure-container" style="height: 100%;">
              <img src="assets/bland_altman_per_scan_means.png" alt="Bland-Altman per scan means" style="max-height: 270px;">
              <div class="figure-caption">
                Figure 7.1: Bland-Altman plot of mean choroidal thickness across 697 test B-scans. Mean bias = +0.28 px (+1.05 &mu;m), 95% LoA = [-5.12, +5.68] px.
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div class="card-title" style="color: var(--accent-cyan);">Bland-Altman Clinical Concordance</div>
                <ul class="bullet-list oct" style="margin-top: 6px;">
                  <li><strong>Zero Systematic Bias:</strong> Mean bias is +0.28 px (+1.05 &mu;m), demonstrating minimal over- or under-segmentation across the entire thickness range.</li>
                  <li><strong>95% Limits of Agreement:</strong> [-5.12, +5.68] px ([-19.2, +21.3] &mu;m).</li>
                  <li><strong>Subfoveal Concordance (SFCT):</strong> Mean predicted 216.1 &mu;m vs ground truth 213.6 &mu;m across 19 test eyes. Pearson correlation $r = 0.9886$ ($p < 0.0001$).</li>
                  <li><strong>Proper Statistical Unit:</strong> Evaluated on 697 scan averages, not pooled columns, avoiding pseudoreplication artifact.</li>
                </ul>
              </div>
              <div class="card warning" style="margin-top: 10px;">
                <div class="card-title" style="color: var(--accent-amber); font-size: 0.86rem;">⚠️ The Post-Processing Paradox</div>
                <p style="font-size: 0.8rem; color: #e2e8f0; line-height: 1.35;">
                  Applying standard morphological hole-filling and smoothing drastically worsened thickness MAE from <strong>2.095 px to 11.223 px ($p < 0.001$)</strong>! Large blood vessel lumens in Haller's layer are genuine anatomical voids; filling them distorts the outer boundary contour. Our policy: retain only Largest Connected Component (LCC) and small horizontal gap bridging (&le; 15 px).
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "High Dice scores do not guarantee clinical validity. In Bland-Altman analysis on 697 per-scan means, our pipeline showed near-zero systematic bias (+1.05 micrometers) with 95% limits of agreement within ±20 micrometers, and an SFCT correlation of r=0.9886 across 19 eyes. Furthermore, we discovered a vital post-processing paradox: standard morphological hole-filling worsened thickness error by 500% from 2.1 to 11.2 pixels. Blood vessel lumens in Haller's layer are genuine anatomical voids, not artifacts. Artificially filling them pushes the boundary outward into the sclera."
        </div>
      </div>

      <!-- SLIDE 8: Limitations & Failure Analysis (Choroid OCT) -->
      <div class="slide" data-slide="8" data-section="PROJECT A: CHOROID OCT" data-badge="PROJECT A: CHOROID">
        <div class="slide-header">
          <div class="slide-category">PROJECT A: CHOROID OCT SEGMENTATION &bull; FAILURE ANALYSIS</div>
          <h2 class="slide-title">Failure Modes & Structural Limitations in Retinal OCT</h2>
          <p class="slide-subtitle">Vessel shadowing artifacts, ground truth ambiguity, and experimental constraints</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="figure-container" style="height: 100%;">
              <img src="assets/rank1_worst_CSI_eye_39_scan_8.png" alt="Worst CSI Failure Eye 39 Scan 8" style="max-height: 270px;">
              <div class="figure-caption">
                Figure 8.1: Worst test CSI failure (Eye 39, Scan 8). Dense retinal vessel shadow extinguishes choroid signal; grader truncated boundary (34.6 px) while model interpolated smooth anatomy (65.8 px).
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-rose);">Where Does the Pipeline Fail?</div>
              <ul class="bullet-list warning" style="margin-top: 8px;">
                <li><strong>Acoustic Shadowing:</strong> Retinal blood vessels absorb and scatter light, projecting dark vertical shadows down through the choroid.</li>
                <li><strong>Ground Truth Disagreement:</strong> In Scan 39_8, the grader abruptly truncated the boundary at 34.6 px due to signal loss, whereas the network interpolated a continuous 65.8 px contour. The 31.2 px 'error' reflects subjective annotation ambiguity under severe noise.</li>
              </ul>
              <div class="card-title" style="color: var(--accent-cyan); margin-top: 14px; font-size: 0.92rem;">Structural Limitations of Project A</div>
              <ul class="bullet-list" style="margin-top: 6px; font-size: 0.82rem;">
                <li><strong>Cohort Size:</strong> 697 test scans originate from 19 eyes (18 patients), introducing intra-eye scan correlation (pseudoreplication).</li>
                <li><strong>Uncalibrated Axial Scale:</strong> 3.75 &mu;m/pixel assumed from manufacturer specs; individual refractive errors affect true scale.</li>
                <li><strong>Manual Fovea Landmarking:</strong> Subfoveal location relied on volume index metadata rather than automated foveal pit detection.</li>
                <li><strong>Training Epochs:</strong> 4 epochs trained due to institutional resource limits.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "Every honest medical AI paper must report its failures. Here is our worst test failure: Scan 39_8. A major retinal vessel cast an acoustic shadow that extinguished the choroidal signal. The human grader abruptly truncated the annotation at 34.6 pixels, while U-Net++ smoothly interpolated the boundary across the shadow at 65.8 pixels. Much of the 31-pixel error is an artifact of annotation ambiguity in noise. We also recognize that our 697 test scans come from 19 eyes, and our axial calibration assumes 3.75 micrometers per pixel."
        </div>
      </div>

      <!-- SLIDE 9: Problem & Motivation (Quantum Pneumonia) -->
      <div class="slide" data-slide="9" data-section="PROJECT B: QUANTUM ML" data-badge="PROJECT B: QUANTUM">
        <div class="slide-header">
          <div class="slide-category">PROJECT B: QUANTUM CLASSIFICATION &bull; RESEARCH MOTIVATION</div>
          <h2 class="slide-title">Variational Quantum Circuits in Medical Deep Learning</h2>
          <p class="slide-subtitle">Parameter efficiency, expressive capacity, and benchmark design on PneumoniaMNIST</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="figure-container" style="height: 100%;">
              <img src="assets/dataset_samples.png" alt="PneumoniaMNIST Dataset Samples" style="max-height: 270px;">
              <div class="figure-caption">
                Figure 9.1: PneumoniaMNIST benchmark samples (28&times;28 grayscale chest X-rays). Normal (label 0, clear lung fields) vs Pneumonia (label 1, consolidation & infiltrates).
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div class="card-title" style="color: var(--accent-purple);">Research Question & Framing</div>
                <ul class="bullet-list quantum" style="margin-top: 8px;">
                  <li><strong>Core Research Question:</strong> Can a parameterized Variational Quantum Circuit (VQC) serve as an effective, highly parameter-efficient classification head on extracted CNN features?</li>
                  <li><strong>Demystifying 'Quantum Advantage':</strong> We do NOT claim quantum supremacy. Instead, we study Hilbert-space expressiveness and optimization stability with 29 quantum head parameters.</li>
                  <li><strong>Dataset (PneumoniaMNIST):</strong> 5,856 pediatric chest X-rays (4,708 train, 524 val, 624 test). Official benchmark partitions strictly maintained.</li>
                </ul>
              </div>
              <div class="card warning" style="margin-top: 10px;">
                <div class="card-title" style="color: var(--accent-amber); font-size: 0.86rem;">⚖️ Class Imbalance & Loss Weighting Nuance</div>
                <p style="font-size: 0.8rem; color: #e2e8f0; line-height: 1.35;">
                  Training set has 74.2% Pneumonia (majority) and 25.8% Normal (minority). We configured <code>pos_weight = 0.3475</code> in BCEWithLogitsLoss. Because Pneumonia is the majority class, this downweights positive sample loss to balance the classes—it does <em>not</em> artificially inflate recall.
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "Moving to Project B, we investigate whether variational quantum circuits can serve as compact, expressive classification heads in medical image analysis. PneumoniaMNIST contains 5,856 chest X-rays. We do not claim 'quantum supremacy'. Rather, we test whether a 4-qubit quantum head with just 29 parameters can achieve competitive classification accuracy against classical models. The training set is 74% pneumonia, and pos_weight=0.3475 was used to balance class loss contributions."
        </div>
      </div>

      <!-- SLIDE 10: Hybrid Architecture & Circuit Mechanics (Quantum Pneumonia) -->
      <div class="slide" data-slide="10" data-section="PROJECT B: QUANTUM ML" data-badge="PROJECT B: QUANTUM">
        <div class="slide-header">
          <div class="slide-category">PROJECT B: QUANTUM CLASSIFICATION &bull; ARCHITECTURE</div>
          <h2 class="slide-title">Hybrid Quantum-Classical Architecture & Circuit Mechanics</h2>
          <p class="slide-subtitle">Classical CNN feature compression, angle embedding, and ring-entangled VQC</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-60">
            <div class="figure-container">
              <img src="assets/quantum_circuit_diagram.png" alt="Quantum Circuit Diagram" style="max-height: 150px;">
              <div class="figure-caption">
                Figure 10.1: 4-qubit PennyLane VQC. State preparation via $R_y(\theta_i)$, 2 variational layers ($R_x, R_y, R_z$), Ring CNOT entanglers, and Pauli-$Z$ measurement.
              </div>
            </div>
            <div class="figure-container" style="margin-top: 10px;">
              <img src="assets/hybrid_qnn_pipeline_diagram.png" alt="Hybrid Pipeline Diagram" style="max-height: 130px;">
              <div class="figure-caption">
                Figure 10.2: End-to-end dataflow from 28&times;28 image to logit prediction.
              </div>
            </div>
          </div>
          <div class="col-right col-40">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-purple);">Four-Stage Hybrid Flow</div>
              <ul class="bullet-list quantum" style="margin-top: 6px; font-size: 0.83rem;">
                <li><strong>1. Classical Feature Extractor:</strong> 3 Conv blocks ($1 \to 16 \to 32 \to 64$) + AdaptiveAvgPool &rarr; Linear(64, 4) compresses image into vector $\mathbf{x} \in \mathbb{R}^4$ (11,076 parameters).</li>
                <li><strong>2. Angle Embedding:</strong> Maps $\mathbf{x}$ to qubit angles via $\theta_i = \pi \tanh(x_i) \in [-\pi, \pi]$. Applies $R_y(\theta_i)$ to state $|0000\rangle$.</li>
                <li><strong>3. Variational Layers (2 Layers):</strong> 3 rotations ($R_x, R_y, R_z$) per qubit ($3 \times 4 = 12$ wts/layer $\times 2 = 24$ quantum weights) + Ring CNOT entanglement ($0 \to 1 \to 2 \to 3 \to 0$).</li>
                <li><strong>4. Measurement & Readout:</strong> Measures Pauli expectation values $\langle Z_i \rangle \in [-1, 1]$ into Linear(4 &rarr; 1) [5 weights].</li>
              </ul>
              <div class="math-block" style="margin-top: 8px; font-size: 0.8rem;">
                Total Head Params: 24 (Quantum) + 5 (Linear) = 29
              </div>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "The hybrid architecture operates in four stages. First, a lightweight 3-block CNN compresses the 28x28 chest X-ray into four classical features. Second, these features are mapped to rotation angles via a pi-tanh non-linearity and embedded onto four qubits with Ry gates. Third, two variational layers apply RX, RY, and RZ rotations followed by a circular ring of CNOT gates that entangles all four qubits. Finally, Pauli-Z expectation values are measured and fed into a 5-parameter linear layer. The entire quantum classification head uses only 29 parameters."
        </div>
      </div>

      <!-- SLIDE 11: Experimental Design & Fair Controls (Quantum Pneumonia) -->
      <div class="slide" data-slide="11" data-section="PROJECT B: QUANTUM ML" data-badge="PROJECT B: QUANTUM">
        <div class="slide-header">
          <div class="slide-category">PROJECT B: QUANTUM CLASSIFICATION &bull; METHODOLOGY</div>
          <h2 class="slide-title">Eliminating the Capacity Confounder: Fair Classical Controls</h2>
          <p class="slide-subtitle">Parameter matching and rigorous optimization parity across all architectures</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="figure-container" style="height: 100%;">
              <img src="assets/model_comparison.png" alt="Model Parameter Comparison" style="max-height: 270px;">
              <div class="figure-caption">
                Figure 11.1: Parameter breakdown across evaluated models. The baseline CNN is heavily confounded by capacity; the CNN+MLP control isolates circuit performance.
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-cyan);">The Critical Confounder in Quantum ML</div>
              <p style="font-size: 0.84rem; color: #cbd5e1; line-height: 1.4;">
                A standard CNN has $>105,000$ parameters (1,025 in head). Comparing a 29-parameter quantum head against a 105k-parameter network is confounded by parameter capacity and capacity-induced overfitting.
              </p>
              <div class="card highlight" style="margin-top: 10px; border-color: var(--accent-purple);">
                <div class="card-title" style="color: var(--accent-purple); font-size: 0.88rem;">Our Solution: Capacity-Matched Control (CNN + MLP)</div>
                <p style="font-size: 0.82rem; color: #e2e8f0; line-height: 1.4;">
                  We built a parameter-matched classical control using the identical 4-dim CNN backbone feeding a 2-layer MLP head: Linear(4, 8) + ReLU + Linear(8, 1) = <strong>49 head parameters</strong> (11,125 total vs QNN's 11,105, $\Delta < 0.2\%$).
                </p>
              </div>
              <div class="card-title" style="color: var(--accent-teal); margin-top: 12px; font-size: 0.88rem;">Strict Optimization Parity</div>
              <ul class="bullet-list" style="margin-top: 4px; font-size: 0.8rem;">
                <li>Adam optimizer (lr = 1e-3, weight_decay = 1e-4), CosineAnnealingLR (T_max = 20).</li>
                <li>Identical BCEWithLogitsLoss with pos_weight = 0.3475, batch size 64, seed 42, 20 epochs.</li>
                <li>Simulation: PennyLane <code>default.qubit</code> state-vector with exact analytic backprop.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "A widespread problem in quantum machine learning literature is comparing a 30-parameter quantum head directly against a 100,000-parameter classical model. If the classical model overfits, authors mistakenly claim quantum advantage. We eliminated this confounder by building a capacity-matched classical control: an identical CNN backbone feeding a 49-parameter classical MLP head. The total parameter counts differ by less than 0.2%, and all models trained under identical learning rates, schedulers, and seeds."
        </div>
      </div>

      <!-- SLIDE 12: Classification Results & Statistical Tests (Quantum Pneumonia) -->
      <div class="slide" data-slide="12" data-section="PROJECT B: QUANTUM ML" data-badge="PROJECT B: QUANTUM">
        <div class="slide-header">
          <div class="slide-category">PROJECT B: QUANTUM CLASSIFICATION &bull; EVALUATION</div>
          <h2 class="slide-title">Benchmark Results & McNemar's Hypothesis Testing</h2>
          <p class="slide-subtitle">Statistical parity: competitive performance without empirical quantum supremacy</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-purple);">Test Performance ($N = 624$)</div>
              <table class="data-table" style="margin-top: 8px;">
                <thead>
                  <tr>
                    <th>Model</th>
                    <th>Head</th>
                    <th>Accuracy</th>
                    <th>F1</th>
                    <th>AUC</th>
                    <th>Spec.</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>CNN Baseline</strong></td>
                    <td>1,025</td>
                    <td>85.74%</td>
                    <td>89.26%</td>
                    <td>0.9291</td>
                    <td>65.0%</td>
                  </tr>
                  <tr>
                    <td><strong>CNN+MLP Control</strong></td>
                    <td>49</td>
                    <td>87.66%</td>
                    <td>90.72%</td>
                    <td>0.9242</td>
                    <td>75.2%</td>
                  </tr>
                  <tr>
                    <td><strong>Hybrid QNN (2-L)</strong></td>
                    <td><strong>29</strong></td>
                    <td><strong>89.10%</strong></td>
                    <td><strong>91.75%</strong></td>
                    <td><strong>0.9374</strong></td>
                    <td><strong>76.1%</strong></td>
                  </tr>
                  <tr style="color: var(--text-muted);">
                    <td><em>QNN (1-L Ablation)</em></td>
                    <td>17</td>
                    <td>90.38%</td>
                    <td>92.65%</td>
                    <td>0.9407</td>
                    <td>79.5%</td>
                  </tr>
                </tbody>
              </table>
              <div class="card highlight" style="margin-top: 12px; border-color: var(--accent-cyan); padding: 10px;">
                <div class="card-title" style="color: var(--accent-cyan); font-size: 0.86rem;">📊 McNemar's Paired Significance Tests</div>
                <div style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.4;">
                  <p>• <strong>QNN vs Baseline CNN:</strong> $\chi^2 = 9.72, p = 0.0018$ &rarr; <strong>Significant</strong> gain over unconstrained baseline.</p>
                  <p style="margin-top: 4px;">• <strong>QNN vs Matched MLP Control:</strong> $\chi^2 = 1.93, p = 0.164$ &rarr; <strong>NOT statistically significant</strong> ($\alpha = 0.05$). 95% Wilson CIs overlap ([86.7%, 91.5%] vs [85.1%, 90.2%]).</p>
                </div>
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="figure-container" style="height: 100%;">
              <img src="assets/roc_curves_combined.png" alt="Combined ROC Curves" style="max-height: 290px;">
              <div class="figure-caption">
                Figure 12.1: Test ROC curves for all models. Hybrid QNN (2-layer AUC 0.937) exhibits competitive discriminative capacity across operating thresholds.
              </div>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "Here are the test results on 624 holdout X-rays. The 2-layer QNN reached 89.1% accuracy and 0.937 AUC. While it significantly outperformed the large baseline CNN (p=0.0018), when compared against our parameter-matched MLP control, the difference was not statistically significant (p=0.164). This is the key honest finding: the quantum head matches classical efficiency, but claims of quantum advantage would be empirically unfounded."
        </div>
      </div>

      <!-- SLIDE 13: Val-to-Test Drop & 1-Layer Investigation (Quantum Pneumonia) -->
      <div class="slide" data-slide="13" data-section="PROJECT B: QUANTUM ML" data-badge="PROJECT B: QUANTUM">
        <div class="slide-header">
          <div class="slide-category">PROJECT B: QUANTUM CLASSIFICATION &bull; AUDIT & INVESTIGATION</div>
          <h2 class="slide-title">Investigating the Validation-to-Test Drop & 1-Layer Paradox</h2>
          <p class="slide-subtitle">Prevalence shift, specificity collapse, and model selection integrity</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-amber);">Investigation 1: Val-to-Test Accuracy Drop (95.8% &rarr; 89.1%)</div>
              <ul class="bullet-list warning" style="margin-top: 6px; font-size: 0.83rem;">
                <li><strong>Cause 1 (Prevalence Shift):</strong> Normal cases make up 25.76% of validation, but jump to 37.50% of the test set (+11.74% shift).</li>
                <li><strong>Cause 2 (Test Specificity Collapse):</strong> While Pneumonia recall remained high ($95.6\% \to 96.9\%$), specificity on Normal cases dropped from <strong>96.3% on validation to 76.1% on test</strong> across ALL models (down to 65.0% in CNN).</li>
                <li><strong>Joint Impact:</strong> The test set contains harder Normal cases; coupled with a higher Normal proportion, false positives heavily drag down overall test accuracy.</li>
              </ul>
              <div class="card highlight" style="margin-top: 10px; border-color: var(--accent-purple); padding: 10px;">
                <div class="card-title" style="color: var(--accent-purple); font-size: 0.86rem;">Investigation 2: Why Did 1-Layer (90.38%) Beat 2-Layer (89.10%)?</div>
                <div style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.4;">
                  <p>• <strong>Only 8 images difference</strong> out of 624 (564 vs 556 correct). McNemar's $p = 0.186$ (NOT significant).</p>
                  <p style="margin-top: 4px;">• <strong>Selection Integrity:</strong> 2-layer had lower validation loss ($0.0557$ vs $0.0584$). Model was chosen strictly by validation metrics without test-peeking.</p>
                </div>
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="figure-container" style="height: 100%;">
              <img src="assets/loss_curves.png" alt="Training and Validation Loss Curves" style="max-height: 290px;">
              <div class="figure-caption">
                Figure 13.1: Training and validation loss curves. The 2-layer QNN achieves superior validation loss convergence without divergence.
              </div>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "We investigated two critical anomalies. First, why did accuracy drop from 95.8% on validation to 89.1% on test? The test set has 12% more normal images, and normal specificity dropped across all models to 76%. Second, 1-layer QNN reached 90.38% test accuracy, beating 2-layer by 8 images. However, this difference is not statistically significant (p=0.186), and 2-layer had lower validation loss, which governed our selection."
        </div>
      </div>

      <!-- SLIDE 14: Quantum Simulation Reality & Limitations (Quantum Pneumonia) -->
      <div class="slide" data-slide="14" data-section="PROJECT B: QUANTUM ML" data-badge="PROJECT B: QUANTUM">
        <div class="slide-header">
          <div class="slide-category">PROJECT B: QUANTUM CLASSIFICATION &bull; PHYSICAL REALITY</div>
          <h2 class="slide-title">Simulation Reality, Hardware Constraints, and Limitations</h2>
          <p class="slide-subtitle">State-vector differentiation vs physical NISQ Parameter-Shift execution</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="figure-container" style="height: 100%;">
              <div style="display: flex; gap: 10px; width: 100%; justify-content: center;">
                <img src="assets/confusion_matrix_quantum_hybrid.png" alt="CM QNN" style="max-width: 48%; max-height: 220px;">
                <img src="assets/confusion_matrix_classical_hybrid.png" alt="CM MLP" style="max-width: 48%; max-height: 220px;">
              </div>
              <div class="figure-caption">
                Figure 14.1: Confusion matrices: Hybrid QNN (left) vs Classical MLP Control (right). True Pneumonia recall is nearly identical (378 vs 371); QNN misclassifies 2 fewer Normal cases.
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-cyan);">Simulation vs Physical NISQ Reality</div>
              <ul class="bullet-list quantum" style="margin-top: 6px; font-size: 0.83rem;">
                <li><strong>Current Simulator:</strong> PennyLane <code>default.qubit</code> state-vector simulator using classical floating-point matrix multiplication and reverse-mode autodiff (<code>diff_method="backprop"</code>).</li>
                <li><strong>Physical NISQ Execution:</strong> Real quantum processors cannot backpropagate through state amplitudes. Gradients require the <strong>Parameter-Shift Rule</strong>:
                  <div class="math-block" style="margin: 4px 0; font-size: 0.76rem;">
                    &part;&lang;Z&rang;/&part;&theta; = 0.5 &bull; [&lang;Z&rang;(&theta; + &pi;/2) - &lang;Z&rang;(&theta; - &pi;/2)]
                  </div>
                  Requires $2 \times 24 = 48$ physical circuit runs per sample ($>4.5 \times 10^6$ runs over 20 epochs), plus decoherence and shot noise.
                </li>
              </ul>
              <div class="card-title" style="color: var(--accent-rose); margin-top: 10px; font-size: 0.88rem;">Structural Limitations of Project B</div>
              <ul class="bullet-list warning" style="margin-top: 4px; font-size: 0.8rem;">
                <li>Evaluated under single random seed (42); multi-seed variance unmeasured.</li>
                <li>4-qubit scale limits Hilbert space dimensionality to $2^4 = 16$.</li>
                <li>Reported inference latency (0.07 ms/img) is batch-amortized on classical CPU.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "We must be transparent about the quantum simulation environment. We ran on PennyLane's state-vector simulator with backpropagation autodiff. On real NISQ quantum hardware, gradients require the parameter-shift rule—executing 48 physical circuits per sample—plus handling shot noise and decoherence. Training took 11 minutes on CPU, but hardware deployment would require substantial error mitigation."
        </div>
      </div>

      <!-- SLIDE 15: Cross-Project Synthesis & Lessons -->
      <div class="slide" data-slide="15" data-section="CLOSING" data-badge="CLOSING">
        <div class="slide-header">
          <div class="slide-category">SYNTHESIS & SCIENTIFIC TAKEAWAYS</div>
          <h2 class="slide-title">Three Core Pillars of Rigorous Medical Image AI</h2>
          <p class="slide-subtitle">Cross-project conclusions: patient integrity, matched controls, and metric honesty</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="figure-container" style="height: 100%;">
              <img src="assets/synthesis_3pillars.png" alt="Three Pillars Graphic" style="max-height: 290px;">
              <div class="figure-caption">
                Figure 15.1: The three foundational principles derived from both medical image analysis projects.
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
              <table class="data-table" style="font-size: 0.82rem;">
                <thead>
                  <tr>
                    <th>Dimension</th>
                    <th>Project A (Choroid OCT)</th>
                    <th>Project B (Quantum X-Ray)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Data Safeguard</strong></td>
                    <td>Patient split prevents 30 &mu;m slice leakage</td>
                    <td>Benchmark partitions avoid holdout contamination</td>
                  </tr>
                  <tr>
                    <td><strong>Baseline Rigor</strong></td>
                    <td>Compared against standard ResNet34 U-Net</td>
                    <td>Compared against capacity-matched 49-param MLP</td>
                  </tr>
                  <tr>
                    <td><strong>Metric Honesty</strong></td>
                    <td>Bland-Altman LoA; no hole-filling artifact</td>
                    <td>McNemar's test ($p=0.164$); specificity drop audit</td>
                  </tr>
                </tbody>
              </table>
              <div class="card highlight" style="margin-top: 12px; border-color: var(--accent-cyan); text-align: center; padding: 14px;">
                <p style="font-size: 1.05rem; font-weight: 700; color: #ffffff; line-height: 1.4;">
                  &ldquo;The hardest part of medical image AI is not achieving high numbers &mdash; it is verifying that the numbers mean what you think they mean.&rdquo;
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "To conclude, these two projects demonstrate that methodological honesty is what gives medical AI scientific value. By enforcing strict patient splits, designing matched classical controls, and looking past top-line metrics to inspect vessel shadows and specificity drops, we obtain reliable clinical conclusions. Thank you, and I look forward to your questions."
        </div>
      </div>

      <!-- SLIDE 16: Backup A1 — OIMHS Mask Audit & Post-Processing Details -->
      <div class="slide" data-slide="16" data-section="BACKUP: PROJECT A" data-badge="BACKUP: A1">
        <div class="slide-header">
          <div class="slide-category">BACKUP SLIDE A1 &bull; PROJECT A ANATOMICAL DEEP DIVE</div>
          <h2 class="slide-title">OIMHS Mask Color Coding & The Hole-Filling Failure Mechanism</h2>
          <p class="slide-subtitle">Mathematical proof of why morphological closing degraded thickness estimation</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-green);">OIMHS Dataset Color Channel Deconstruction</div>
              <ul class="bullet-list oct" style="margin-top: 8px; font-size: 0.85rem;">
                <li><strong>Green Channel ($G > 128, R < 128$):</strong> Represents neurosensory retina. Average vertical position sits ~37 &mu;m above Bruch's membrane.</li>
                <li><strong>Yellow Channel ($R > 128, G > 128$):</strong> Represents choroidal vascular bed. Average vertical depth sits ~214 &mu;m below Bruch's membrane.</li>
                <li><strong>Automated Binarization Rule:</strong> True Choroid is extracted via `(mask[..., 0] > 128) & (mask[..., 1] > 128)`.</li>
              </ul>
              <div class="card highlight" style="margin-top: 14px; font-size: 0.82rem;">
                Verified across all 3,859 masks in raw dataset. Avoided the critical error of training on retinal boundaries.
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card warning" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-amber);">Mathematical Cause of Post-Processing Paradox</div>
              <p style="font-size: 0.84rem; color: #cbd5e1; line-height: 1.4;">
                Why did morphological closing + Savitzky-Golay filtering inflate thickness MAE from 2.095 px to 11.223 px ($p < 0.001$)?
              </p>
              <ul class="bullet-list warning" style="margin-top: 8px; font-size: 0.83rem;">
                <li>Large choroidal vessels (Haller's layer) appear as hyporeflective lumens (dark circular voids).</li>
                <li>Morphological closing ($\mathcal{M} \bullet \mathcal{K}$) treats lumens as foreground holes and bridges them with outer tissue.</li>
                <li>This alters the connected component boundary, dragging the detected CSI downward into scleral tissue by 8–15 pixels.</li>
                <li><strong>Final Protocol:</strong> Largest Connected Component (LCC) + horizontal gap bridging ($\le 15$ px) only. Lumens are preserved as genuine anatomy.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "In backup A1, this explains why we rejected standard morphological closing: blood vessel lumens in the choroid are genuine empty spaces, not noise. Closing them pushed the segmented boundary into the sclera, multiplying error by five times."
        </div>
      </div>

      <!-- SLIDE 17: Backup A2 — Fovea Centering & Regional ETDRS Thickness -->
      <div class="slide" data-slide="17" data-section="BACKUP: PROJECT A" data-badge="BACKUP: A2">
        <div class="slide-header">
          <div class="slide-category">BACKUP SLIDE A2 &bull; PROJECT A CLINICAL THICKNESS MAPPING</div>
          <h2 class="slide-title">Regional ETDRS Subfield Thickness & Foveal Alignment</h2>
          <p class="slide-subtitle">Preservation of physiological nasal thinning and subfoveal peaking</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="figure-container" style="height: 100%;">
              <img src="assets/10_thickness_profile.png" alt="Thickness profile Eye 39 Scan 10" style="max-height: 270px;">
              <div class="figure-caption">
                Figure 17.1: Continuous A-scan choroidal thickness profile for Eye 39 Scan 10. Blue: ground truth; Red: U-Net++ prediction; Shaded: &plusmn;1 standard deviation confidence band.
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-cyan);">Regional Sector Analysis (ETDRS Sectors)</div>
              <ul class="bullet-list oct" style="margin-top: 8px; font-size: 0.85rem;">
                <li><strong>Physiological Gradient:</strong> In healthy human eyes, the choroid is thickest subfoveally (SFCT), thins moderately temporally, and thins steeply nasally toward the optic nerve head.</li>
                <li><strong>Model Fidelity:</strong> U-Net++ faithfully reproduces this physiological nasal gradient across all 697 test scans without boundary divergence.</li>
                <li><strong>Foveal Centering Implementation:</strong> The central foveal scan is localized via dataset volume metadata. Future work will replace this with automated 2D foveal pit detection directly on OCT surfaces.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "Backup A2 addresses how thickness varies across retinal eccentricities. The model faithfully preserves the physiological nasal thinning pattern, matching clinical literature."
        </div>
      </div>

      <!-- SLIDE 18: Backup B1 — Quantum Circuit Mechanics (Parameter-Shift vs Backprop) -->
      <div class="slide" data-slide="18" data-section="BACKUP: PROJECT B" data-badge="BACKUP: B1">
        <div class="slide-header">
          <div class="slide-category">BACKUP SLIDE B1 &bull; PROJECT B QUANTUM COMPUTATION REALITY</div>
          <h2 class="slide-title">Quantum Gradients: Parameter-Shift Rule vs Backprop</h2>
          <p class="slide-subtitle">Analytical formulation and hardware scaling feasibility</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-purple);">The Parameter-Shift Theorem</div>
              <p style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.4;">
                For quantum circuits with generators having eigenvalues $\pm \frac{1}{2}$ (such as Pauli rotations $R_x, R_y, R_z$), the exact gradient of an expectation value is given by:
              </p>
              <div class="math-block" style="font-size: 0.84rem; margin: 10px 0;">
                &part;&lang;Z&rang; / &part;&theta;_j = 0.5 &bull; [ &lang;Z&rang;(&theta;_j + &pi;/2) - &lang;Z&rang;(&theta;_j - &pi;/2) ]
              </div>
              <ul class="bullet-list quantum" style="margin-top: 8px; font-size: 0.83rem;">
                <li>Requires <strong>2 distinct quantum circuit evaluations</strong> per parameter per input sample.</li>
                <li>For $P = 24$ parameters and batch size $B = 64$: $2 \times 24 \times 64 = 3,072$ circuit runs per batch!</li>
                <li>Over 74 batches/epoch $\times$ 20 epochs $= 4.54 \times 10^6$ circuit runs.</li>
              </ul>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-teal);">Why Simulator Backpropagation?</div>
              <ul class="bullet-list" style="margin-top: 8px; font-size: 0.85rem;">
                <li><strong>State-Vector Simulation:</strong> PennyLane's <code>default.qubit</code> computes exact state amplitudes in $\mathbb{C}^{16}$ via matrix multiplication.</li>
                <li><strong>Reverse-Mode Autodiff:</strong> Backpropagation through state-vectors computes exact gradients in a single backward pass, reducing 20-epoch training from ~8 hours to <strong>11.2 minutes</strong> on CPU.</li>
                <li><strong>Scientific Validity:</strong> Simulator backprop gives identical parameter updates to noiseless parameter-shift with infinite shots, providing an ideal upper bound on VQC expressive capacity.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "Backup B1 provides the exact math of the Parameter-Shift rule. On physical quantum processors, evaluating gradients requires 4.5 million circuit executions across training. State-vector backpropagation made this semester study computationally feasible."
        </div>
      </div>

      <!-- SLIDE 19: Backup B2 — Detailed Statistical Significance Matrix -->
      <div class="slide" data-slide="19" data-section="BACKUP: PROJECT B" data-badge="BACKUP: B2">
        <div class="slide-header">
          <div class="slide-category">BACKUP SLIDE B2 &bull; PROJECT B STATISTICAL MATRIX</div>
          <h2 class="slide-title">McNemar's Contingency Matrix & Wilson Confidence Intervals</h2>
          <p class="slide-subtitle">Exhaustive statistical analysis proving absence of quantum supremacy</p>
        </div>
        <div class="slide-body">
          <div class="col-left col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-cyan);">Paired McNemar Contingency Matrix ($N=624$)</div>
              <table class="data-table" style="margin-top: 8px; font-size: 0.82rem;">
                <thead>
                  <tr>
                    <th>Model Comparison</th>
                    <th>$n_{01}$</th>
                    <th>$n_{10}$</th>
                    <th>$\chi^2$</th>
                    <th>$p$-value</th>
                    <th>Conclusion</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>QNN (2L) vs Baseline CNN</strong></td>
                    <td>48</td>
                    <td>22</td>
                    <td>9.72</td>
                    <td class="best-val"><strong>0.0018</strong></td>
                    <td class="best-val">Significant</td>
                  </tr>
                  <tr>
                    <td><strong>QNN (2L) vs MLP Control</strong></td>
                    <td>32</td>
                    <td>23</td>
                    <td>1.93</td>
                    <td>0.164</td>
                    <td>Not Sig.</td>
                  </tr>
                  <tr>
                    <td><strong>QNN (1L) vs QNN (2L)</strong></td>
                    <td>19</td>
                    <td>11</td>
                    <td>1.74</td>
                    <td>0.186</td>
                    <td>Not Sig.</td>
                  </tr>
                  <tr>
                    <td><strong>MLP Control vs Baseline CNN</strong></td>
                    <td>39</td>
                    <td>27</td>
                    <td>2.18</td>
                    <td>0.139</td>
                    <td>Not Sig.</td>
                  </tr>
                </tbody>
              </table>
              <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 8px;">
                $n_{01}$: Model A incorrect & Model B correct; $n_{10}$: Model A correct & Model B incorrect.
              </div>
            </div>
          </div>
          <div class="col-right col-50">
            <div class="card" style="height: 100%;">
              <div class="card-title" style="color: var(--accent-purple);">95% Wilson Score Confidence Intervals</div>
              <table class="data-table" style="margin-top: 8px; font-size: 0.82rem;">
                <thead>
                  <tr>
                    <th>Model</th>
                    <th>Accuracy [95% CI]</th>
                    <th>F1 Score [95% CI]</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Hybrid QNN (2-L)</strong></td>
                    <td>89.10% [86.67%, 91.46%]</td>
                    <td>0.9175 [0.898, 0.934]</td>
                  </tr>
                  <tr>
                    <td><strong>CNN + MLP Control</strong></td>
                    <td>87.66% [85.12%, 90.17%]</td>
                    <td>0.9072 [0.887, 0.925]</td>
                  </tr>
                  <tr>
                    <td><strong>Baseline CNN</strong></td>
                    <td>85.74% [83.08%, 88.35%]</td>
                    <td>0.8926 [0.871, 0.912]</td>
                  </tr>
                </tbody>
              </table>
              <div class="card highlight" style="margin-top: 12px; font-size: 0.82rem; border-color: var(--accent-amber);">
                <strong>Definitive Audit Conclusion:</strong> Because the 95% confidence intervals overlap extensively and McNemar's $p = 0.164 > 0.05$, the hybrid QNN is statistically equivalent in performance to a parameter-matched classical neural network.
              </div>
            </div>
          </div>
        </div>
        <div class="speaker-text" style="display:none;">
          "Backup B2 shows the complete contingency tables for McNemar's tests and Wilson score intervals. Notice that the QNN and MLP control confidence intervals overlap substantially, proving that the small test accuracy difference is well within statistical noise."
        </div>
      </div>

    </div>
  </main>

  <!-- Speaker Notes Drawer -->
  <div class="speaker-drawer" id="speakerDrawer">
    <div class="speaker-drawer-header">
      <span class="speaker-drawer-title">Speaker Script & Defense Talking Points (Press 'N' to Close)</span>
      <button class="speaker-drawer-close" id="btnCloseNotes">&times;</button>
    </div>
    <div class="speaker-drawer-content" id="speakerContent">
      <!-- Injected dynamically -->
    </div>
  </div>

  <!-- Slide Grid Overview Modal -->
  <div class="overview-modal" id="overviewModal">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1380px; margin: 0 auto; width: 100%;">
      <h2 style="font-size: 1.4rem; color: #fff;">Slide Grid Overview (Press 'O' or ESC to Close)</h2>
      <button class="btn-nav" id="btnCloseOverview">Close &times;</button>
    </div>
    <div class="overview-grid" id="overviewGrid" style="max-width: 1380px; margin: 20px auto 0; width: 100%;">
      <!-- Injected dynamically -->
    </div>
  </div>

  <script>
    // Slide Navigation Controller
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    let currentSlide = 1;

    const progressBar = document.getElementById('progressBar');
    const slideCounter = document.getElementById('slideCounter');
    const headerTitle = document.getElementById('headerTitle');
    const sectionBadge = document.getElementById('sectionBadge');
    const speakerDrawer = document.getElementById('speakerDrawer');
    const speakerContent = document.getElementById('speakerContent');
    const overviewModal = document.getElementById('overviewModal');
    const overviewGrid = document.getElementById('overviewGrid');

    function updateSlide(newIndex) {
      if (newIndex < 1) newIndex = 1;
      if (newIndex > totalSlides) newIndex = totalSlides;
      currentSlide = newIndex;

      slides.forEach((slide, i) => {
        if (i + 1 === currentSlide) {
          slide.classList.add('active');
          const title = slide.querySelector('.slide-title')?.textContent || 'Slide ' + currentSlide;
          const section = slide.getAttribute('data-section') || 'PRESENTATION';
          const badge = slide.getAttribute('data-badge') || 'SLIDE';
          
          headerTitle.textContent = title;
          sectionBadge.textContent = badge;
          
          // Badge styling
          sectionBadge.className = 'badge-section';
          if (badge.includes('OCT') || badge.includes('CHOROID')) {
            sectionBadge.classList.add('oct');
          } else if (badge.includes('QUANTUM')) {
            sectionBadge.classList.add('quantum');
          } else if (badge.includes('BACKUP')) {
            sectionBadge.classList.add('backup');
          }

          // Speaker text
          const speakerText = slide.querySelector('.speaker-text')?.innerHTML || 'No speaker notes available for this slide.';
          speakerContent.innerHTML = speakerText;
        } else {
          slide.classList.remove('active');
        }
      });

      slideCounter.textContent = `${currentSlide} / ${totalSlides}`;
      progressBar.style.width = `${(currentSlide / totalSlides) * 100}%`;

      // Update overview active card
      document.querySelectorAll('.overview-card').forEach((card, idx) => {
        if (idx + 1 === currentSlide) {
          card.classList.add('active');
        } else {
          card.classList.remove('active');
        }
      });
    }

    // Populate Overview Grid
    slides.forEach((slide, idx) => {
      const card = document.createElement('div');
      card.className = 'overview-card' + (idx + 1 === currentSlide ? ' active' : '');
      const title = slide.querySelector('.slide-title')?.textContent || 'Slide ' + (idx + 1);
      const badge = slide.getAttribute('data-badge') || 'SLIDE';
      
      let badgeBg = '#1e3a8a';
      if (badge.includes('OCT') || badge.includes('CHOROID')) badgeBg = '#064e3b';
      if (badge.includes('QUANTUM')) badgeBg = '#581c87';
      if (badge.includes('BACKUP')) badgeBg = '#78350f';

      card.innerHTML = `
        <div>
          <div class="overview-card-num">SLIDE ${idx + 1}</div>
          <div class="overview-card-title">${title}</div>
        </div>
        <div class="overview-card-tag" style="background:${badgeBg}; color:#fff;">${badge}</div>
      `;
      card.addEventListener('click', () => {
        updateSlide(idx + 1);
        overviewModal.classList.remove('open');
      });
      overviewGrid.appendChild(card);
    });

    // Event Handlers
    document.getElementById('btnPrev').addEventListener('click', () => updateSlide(currentSlide - 1));
    document.getElementById('btnNext').addEventListener('click', () => updateSlide(currentSlide + 1));
    
    document.getElementById('btnNotes').addEventListener('click', () => {
      speakerDrawer.classList.toggle('open');
    });
    document.getElementById('btnCloseNotes').addEventListener('click', () => {
      speakerDrawer.classList.remove('open');
    });

    document.getElementById('btnOverview').addEventListener('click', () => {
      overviewModal.classList.add('open');
    });
    document.getElementById('btnCloseOverview').addEventListener('click', () => {
      overviewModal.classList.remove('open');
    });

    document.getElementById('btnFullscreen').addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => alert(`Error: ${err.message}`));
      } else {
        document.exitFullscreen();
      }
    });

    // Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
      if (overviewModal.classList.contains('open')) {
        if (e.key === 'Escape' || e.key === 'o' || e.key === 'O') {
          overviewModal.classList.remove('open');
        }
        return;
      }

      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        updateSlide(currentSlide + 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        updateSlide(currentSlide - 1);
      } else if (e.key === 'Home') {
        e.preventDefault();
        updateSlide(1);
      } else if (e.key === 'End') {
        e.preventDefault();
        updateSlide(totalSlides);
      } else if (e.key === 'n' || e.key === 'N') {
        speakerDrawer.classList.toggle('open');
      } else if (e.key === 'o' || e.key === 'O') {
        overviewModal.classList.toggle('open');
      } else if (e.key === 'f' || e.key === 'F') {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(() => {});
        } else {
          document.exitFullscreen();
        }
      } else if (e.key === 'Escape') {
        speakerDrawer.classList.remove('open');
        overviewModal.classList.remove('open');
      }
    });

    // Initialize
    updateSlide(1);
  </script>
</body>
</html>
"""

def main():
    os.makedirs("presentation", exist_ok=True)
    with open("presentation/index.html", "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print("Successfully generated presentation/index.html (19 slides)")

if __name__ == "__main__":
    main()
