# Academic Presentation: Two Approaches to Medical Image Analysis

**Title**: Two Approaches to Medical Image Analysis: Deep Segmentation for Choroidal Thickness and Hybrid Quantum-Classical Pneumonia Detection  
**Author**: Aditya Sahrawat  
**Target Duration**: ~20 minutes (15 main slides @ ~1.3 min/slide) + 4 backup slides for Q&A (19 slides total)

---

## Deliverables

1. **PowerPoint Presentation (`combined_presentation.pptx`)**:
   - Location: [`presentation/combined_presentation.pptx`](file:///Users/adityasahrawat/dev/projects/quantum-medical-image-classification/presentation/combined_presentation.pptx)
   - 16:9 widescreen format with modern dark medical-tech styling.
   - 19 fully designed slides with embedded high-resolution figures, structured data tables, and embedded **speaker notes on every slide**.

2. **Interactive HTML Presentation (`index.html`)**:
   - Location: [`presentation/index.html`](file:///Users/adityasahrawat/dev/projects/quantum-medical-image-classification/presentation/index.html)
   - Self-contained web presentation runnable in any modern web browser.
   - **Keyboard Shortcuts**:
     - `Right Arrow` / `Space` / `Page Down`: Next slide
     - `Left Arrow` / `Page Up`: Previous slide
     - `Home` / `End`: First / Last slide
     - `N`: Toggle Speaker Notes drawer
     - `O`: Toggle Slide Overview Grid
     - `F`: Toggle Fullscreen mode
     - `ESC`: Close drawer or grid

3. **Presentation Assets (`assets/`)**:
   - Location: [`presentation/assets/`](file:///Users/adityasahrawat/dev/projects/quantum-medical-image-classification/presentation/assets)
   - All high-resolution figures, architecture schematics, and comparative plots.

---

## Slide Structure & Overview

### Opening (Slides 1–2)
- **Slide 1**: Title Slide (Multimodal split visual: Retinal OCT B-scan overlay vs. 28×28 Chest X-ray)
- **Slide 2**: Presentation Roadmap & The Unifying Thread (Leakage-free splits, capacity-matched controls, transparent failures)

### Part A: Choroid OCT Segmentation & Thickness Measurement (Slides 3–8)
- **Slide 3**: Clinical Problem & Anatomical Ground Truth (Vascular biology, 30–60 min manual tracing, OIMHS green vs yellow mask audit)
- **Slide 4**: Leakage-Free Splitting & Pipeline (3,859 scans across 119 patients; avoiding 30–120 µm adjacent B-scan leakage)
- **Slide 5**: Network Architecture & Boundary Loss (U-Net baseline vs U-Net++ scSE; boundary-weighted BCE+Dice with $\sigma = 5$ px)
- **Slide 6**: Quantitative Segmentation & Boundary Results (Dice 0.9804, BM MAE 0.407 px [-27.6%], CSI MAE 1.567 px [-10.7%])
- **Slide 7**: Clinical Agreement & The Post-Processing Paradox (Bland-Altman bias +1.05 µm, $r = 0.9886$; why hole-filling ruins anatomy)
- **Slide 8**: Failure Modes & Structural Limitations (Scan 39_8 retinal vessel shadowing; grader truncation vs model interpolation; 19 eyes)

### Part B: Hybrid Quantum-Classical Pneumonia Classification (Slides 9–14)
- **Slide 9**: Research Motivation & Benchmark Design (Variational circuits as classifier heads; PneumoniaMNIST; pos_weight=0.3475)
- **Slide 10**: Hybrid Architecture & Circuit Mechanics (CNN backbone $\to$ 4-dim features $\to$ Angle embedding $\to$ 2-layer VQC $\to$ 29 head params)
- **Slide 11**: Eliminating Capacity Confounders (Designing the parameter-matched 49-param CNN+MLP control; optimization parity)
- **Slide 12**: Classification Performance & McNemar's Testing (QNN vs CNN baseline $p = 0.0018$; QNN vs MLP control $p = 0.164$ [Not Sig.])
- **Slide 13**: Deep Investigations: Val-to-Test Drop & 1-Layer Paradox (Prevalence shift + test specificity drop; 1-layer vs 2-layer selection)
- **Slide 14**: Quantum Simulation Reality & Physical NISQ Constraints (State-vector backprop vs 48-run Parameter-Shift rule; noise and limits)

### Closing (Slide 15)
- **Slide 15**: Cross-Project Synthesis & The Three Pillars (Patient integrity, matched baselines, metric honesty; concluding quote)

### Backup Slides for Q&A (Slides 16–19)
- **Slide 16**: Backup A1 — OIMHS Color Coding & Mathematical Proof of the Hole-Filling Failure
- **Slide 17**: Backup A2 — Regional ETDRS Subfield Thickness & Foveal Alignment
- **Slide 18**: Backup B1 — Quantum Gradients: Parameter-Shift Rule vs Simulator Backprop
- **Slide 19**: Backup B2 — Detailed McNemar's Contingency Matrix & Wilson Score 95% Confidence Intervals
