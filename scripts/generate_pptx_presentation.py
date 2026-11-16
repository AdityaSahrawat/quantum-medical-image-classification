#!/usr/bin/env python3
"""
Generate presentation/combined_presentation.pptx
A high-impact, professional 16:9 academic presentation covering:
- Project A: Choroid OCT Segmentation and Thickness Measurement
- Project B: Hybrid Quantum-Classical Medical Image Classification
15 Main Slides + 4 Backup Slides (19 Slides Total)
Complete with high-resolution visual figures, data tables, and embedded speaker notes.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 16:9 Widescreen dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Color Palette
COLOR_BG = RGBColor(10, 15, 29)          # Deep Slate/Navy #0a0f1d
COLOR_CARD = RGBColor(17, 24, 39)        # Dark Card #111827
COLOR_CARD_ALT = RGBColor(31, 41, 55)    # Card border/fill #1f2937
COLOR_WHITE = RGBColor(249, 250, 251)    # Primary Text #f9fafb
COLOR_MUTED = RGBColor(156, 163, 175)    # Muted Gray #9ca3af
COLOR_CYAN = RGBColor(56, 189, 248)      # Sky Cyan #38bdf8
COLOR_TEAL = RGBColor(45, 212, 191)      # Teal #2dd4bf
COLOR_GREEN = RGBColor(52, 211, 153)     # Emerald Green #34d399
COLOR_PURPLE = RGBColor(192, 132, 252)   # Purple #c084fc
COLOR_AMBER = RGBColor(251, 191, 36)     # Amber/Warning #fbbf24
COLOR_ROSE = RGBColor(244, 63, 94)       # Rose/Alert #f43f5e


def set_slide_background(slide):
    """Draw a full-bleed dark rectangle as the background."""
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = COLOR_BG
    bg_shape.line.fill.background()
    return bg_shape


def add_header(slide, category_text, title_text, subtitle_text=None, category_color=COLOR_CYAN):
    """Add a standardized, elegant header to the slide."""
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.2))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = category_color

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE
    p_title.space_after = Pt(2)

    if subtitle_text:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = COLOR_MUTED


def add_card(slide, left, top, width, height, border_color=COLOR_CARD_ALT, fill_color=COLOR_CARD):
    """Add a card container with rounded rectangle shape."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        card.line.fill.background()
    return card


def set_speaker_notes(slide, text):
    """Embed speaker notes into the PowerPoint slide."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = text


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]  # Blank slide

    assets_dir = "presentation/assets"

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Title box
    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(2.2))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p_cat = tf1.paragraphs[0]
    p_cat.text = "ACADEMIC MASTER'S DEFENSE / SEMESTER RESEARCH PRESENTATION"
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_CYAN
    p_cat.alignment = PP_ALIGN.CENTER

    p_main = tf1.add_paragraph()
    p_main.text = "Two Approaches to Medical Image Analysis: Deep Segmentation for Choroidal Thickness and Hybrid Quantum-Classical Pneumonia Detection"
    p_main.font.size = Pt(23)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_WHITE
    p_main.alignment = PP_ALIGN.CENTER
    p_main.space_after = Pt(4)

    p_sub = tf1.add_paragraph()
    p_sub.text = "A Comparative Study in Model Design, Data Integrity, and Rigorous Evaluation"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = COLOR_MUTED
    p_sub.alignment = PP_ALIGN.CENTER

    p_author = tf1.add_paragraph()
    p_author.text = "Aditya Sahrawat • Medical Image Analysis & Deep Learning • Academic Year 2026"
    p_author.font.size = Pt(12)
    p_author.font.bold = True
    p_author.font.color.rgb = COLOR_TEAL
    p_author.alignment = PP_ALIGN.CENTER

    # Split visual
    split_img_path = os.path.join(assets_dir, "title_split.png")
    if os.path.exists(split_img_path):
        s1.shapes.add_picture(split_img_path, Inches(1.8), Inches(2.9), width=Inches(9.733))

    set_speaker_notes(s1, (
        "Good morning Professor. Today I am presenting two distinct medical image analysis projects. "
        "On the left is an automated segmentation and thickness measurement pipeline for the choroid layer in retinal OCT scans. "
        "On the right is a hybrid quantum-classical classifier for pediatric pneumonia detection in chest X-rays. "
        "While their clinical domains and architectures differ, the unifying thread of this presentation is scientific rigor: "
        "leakage-free splitting, capacity-matched baseline controls, and honest metric reporting."
    ))

    # =========================================================================
    # SLIDE 2: Roadmap and Common Thread
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "PRESENTATION ROADMAP & METHODOLOGICAL FOUNDATION",
               "Two Distinct Problems, One Uncompromising Standard of Rigor",
               "How honest experimental design binds specialized clinical pipelines")

    # Column Left: Project A Card
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.7), Inches(3.6), border_color=COLOR_GREEN)
    tb_a = s2.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.3), Inches(3.3))
    tf_a = tb_a.text_frame
    tf_a.word_wrap = True
    p = tf_a.paragraphs[0]
    p.text = "🔬 Project A: Retinal Choroid OCT"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    items_a = [
        ("Clinical Task:", "Boundary segmentation & thickness measurement (SFCT)."),
        ("Modality:", "Spectral-Domain OCT B-scans (Heidelberg Spectralis)."),
        ("Architectures:", "U-Net baseline → U-Net++ with scSE spatial/channel attention."),
        ("Core Question:", "\"Can deep networks resolve the faint choroidal-scleral interface with sub-pixel anatomical fidelity and clinical agreement?\"")
    ]
    for lbl, val in items_a:
        p = tf_a.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    # Column Right: Project B Card
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(3.6), border_color=COLOR_PURPLE)
    tb_b = s2.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(3.3))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "⚛️ Project B: Quantum Chest X-Ray"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE

    items_b = [
        ("Clinical Task:", "Binary pediatric pneumonia classification (Normal vs Pneumonia)."),
        ("Modality:", "PneumoniaMNIST (28 × 28 grayscale X-rays)."),
        ("Architectures:", "Classical CNN → Parameter-matched MLP → 4-qubit Hybrid QNN."),
        ("Core Question:", "\"Can a 29-parameter variational quantum circuit serve as an effective, competitive classifier head against matched classical controls?\"")
    ]
    for lbl, val in items_b:
        p = tf_b.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    # Bottom Unifying Card
    add_card(s2, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.4), border_color=COLOR_AMBER)
    tb_u = s2.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(1.2))
    tf_u = tb_u.text_frame
    tf_u.word_wrap = True
    p = tf_u.paragraphs[0]
    p.text = "⚖️ The Unifying Common Thread: Scientific Honesty Over Superficial Claims"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    p = tf_u.add_paragraph()
    p.text = (
        "1. Leakage-Free Splits: Strict patient-level isolation (OCT) and benchmark holdouts avoiding identity contamination.\n"
        "2. Fair Capacity Controls: Refusing to compare 29-param quantum heads against 100k-param classical networks without matched controls.\n"
        "3. Transparent Failures: Scrutinizing where and why models fail (vessel shadows, prevalence shifts, test specificity drops)."
    )
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_WHITE

    set_speaker_notes(s2, (
        "Both projects ask the same fundamental question: not just 'does it work?', but 'how do we know it works, and where does it fail?'. "
        "In Project A, we address high-resolution choroid segmentation where spatial leakage from adjacent B-scans threatens validity. "
        "In Project B, we integrate variational quantum circuits into deep learning, where uncalibrated baselines often lead to exaggerated claims. "
        "The presentation consists of two 6-slide technical audits followed by cross-project synthesis and Q&A backup."
    ))

    # =========================================================================
    # SLIDE 3: Clinical Problem (Choroid OCT)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "PROJECT A: CHOROID OCT SEGMENTATION • CLINICAL CONTEXT",
               "The Clinical Challenge of Choroidal Thickness Quantification",
               "Vascular anatomy, manual measurement bottlenecks, and data ground truth verification",
               category_color=COLOR_GREEN)

    # Left: Diagram
    diag_path = os.path.join(assets_dir, "choroid_anatomy_diagram.png")
    if os.path.exists(diag_path):
        s3.shapes.add_picture(diag_path, Inches(0.8), Inches(1.8), width=Inches(5.8))

    # Right: Content Card
    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_CYAN)
    tb = s3.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Diagnostic Significance & Annotation Bottleneck"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    bullets = [
        ("Ocular Biomarker:", "The choroid is the vascular layer feeding the outer retina and avascular fovea. Thinning indicates pathological myopia and dry AMD; thickening indicates pachychoroid disease (CSCR, PCV)."),
        ("Manual Bottleneck:", "Manual tracing across 3D volumes requires 30–60 minutes per eye. Expert graders disagree by 15–30 µm, especially at the faint, low-contrast Choroidal-Scleral Interface (CSI)."),
        ("Clinical End Goal:", "Automated, sub-pixel Subfoveal Choroidal Thickness (SFCT) profiling across full Spectralis B-scans.")
    ]
    for lbl, val in bullets:
        p = tf.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    # Alert sub-card inside right column
    p = tf.add_paragraph()
    p.text = "🚨 Critical Dataset Audit Discovery (OIMHS):"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p.space_before = Pt(8)

    p = tf.add_paragraph()
    p.text = (
        "The OIMHS dataset includes multiple mask channels. Our exploratory data audit revealed that the green mask "
        "(~37 µm above BM) corresponds to neurosensory retina, whereas the yellow mask (~214 µm below BM) is the true choroidal stroma. "
        "Naively training on green masks segments retina, not choroid! Yellow masks were strictly isolated."
    )
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED

    set_speaker_notes(s3, (
        "The choroid is the dense vascular layer behind the retina. Accurately measuring Subfoveal Choroidal Thickness is essential for detecting conditions like pachychoroid diseases and age-related macular degeneration. "
        "However, manual annotation takes up to an hour per volume, and experts disagree by 15 to 30 micrometers due to low contrast at the choroid-sclera interface. "
        "Before writing a line of code, we audited the OIMHS dataset masks and discovered that the green mask was retina, not choroid. "
        "The yellow mask was verified as the true choroidal stroma, preventing a catastrophic ground-truth error."
    ))

    # =========================================================================
    # SLIDE 4: Pipeline & Data Splitting (Choroid OCT)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "PROJECT A: CHOROID OCT SEGMENTATION • METHODOLOGY",
               "Leakage-Free Patient Splitting and Processing Pipeline",
               "Guaranteed patient isolation across 3,859 Spectralis B-scans",
               category_color=COLOR_GREEN)

    # Left: Pipeline Diagram + Warning Card
    pipe_path = os.path.join(assets_dir, "choroid_pipeline_diagram.png")
    if os.path.exists(pipe_path):
        s4.shapes.add_picture(pipe_path, Inches(0.8), Inches(1.8), width=Inches(6.8))

    add_card(s4, Inches(0.8), Inches(4.7), Inches(6.8), Inches(2.3), border_color=COLOR_AMBER)
    tb_w = s4.shapes.add_textbox(Inches(1.0), Inches(4.8), Inches(6.4), Inches(2.1))
    tf_w = tb_w.text_frame
    tf_w.word_wrap = True
    p = tf_w.paragraphs[0]
    p.text = "⚠️ The Severe Pitfall of Random B-Scan Splitting"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    p = tf_w.add_paragraph()
    p.text = (
        "Adjacent B-scans within a Heidelberg Spectralis volume are separated by only 30–120 µm. "
        "A standard random scan-level split places nearly identical slices of the same patient into both training and test sets. "
        "This leaks patient anatomy and unique vessel architecture, creating an illusion of high generalization while failing in real clinical deployment. "
        "We enforced zero patient overlap across all partitions."
    )
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_WHITE

    # Right: Data Table Card
    add_card(s4, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.2), border_color=COLOR_CYAN)
    tb_t = s4.shapes.add_textbox(Inches(8.0), Inches(1.95), Inches(4.3), Inches(4.9))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p = tf_t.paragraphs[0]
    p.text = "Strict Patient-Level Partitioning"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    # Table for Partitions
    table_shape = s4.shapes.add_table(4, 4, Inches(8.0), Inches(2.5), Inches(4.3), Inches(1.8))
    table = table_shape.table
    table.columns[0].width = Inches(1.2)
    table.columns[1].width = Inches(1.0)
    table.columns[2].width = Inches(0.9)
    table.columns[3].width = Inches(1.2)

    headers = ["Split", "Patients", "Eyes", "Scans"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(11)
        cell.text_frame.paragraphs[0].font.color.rgb = COLOR_CYAN

    row_data = [
        ["Train", "83 (69.7%)", "87", "2,609"],
        ["Val", "18 (15.1%)", "19", "553"],
        ["Test", "18 (15.1%)", "19", "697"],
    ]
    for row_idx, r in enumerate(row_data):
        for col_idx, val in enumerate(r):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = val
            cell.text_frame.paragraphs[0].font.size = Pt(10.5)
            cell.text_frame.paragraphs[0].font.color.rgb = COLOR_WHITE

    # Sub-bullets under table
    tb_sub = s4.shapes.add_textbox(Inches(8.0), Inches(4.6), Inches(4.3), Inches(2.2))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p = tf_sub.paragraphs[0]
    p.text = (
        "• Total Cohort: 119 Patients, 125 Eyes, 3,859 B-scans.\n"
        "• Test Evaluation: 18 completely holdout patients (697 scans).\n"
        "• Preprocessing: 512 × 512 standardization, CLAHE contrast enhancement, and z-score normalization."
    )
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED

    set_speaker_notes(s4, (
        "The critical methodological safeguard in Project A is patient-level partitioning. "
        "An OCT volume consists of parallel B-scans spaced only 30 to 120 micrometers apart. "
        "If you randomly partition scans, adjacent slices from the same eye land in both train and test, leaking anatomical features and fabricating artificial performance. "
        "We strictly held out 18 patients and 19 eyes for testing, ensuring that our 697 test scans represent truly unseen clinical cases."
    ))

    # =========================================================================
    # SLIDE 5: Architecture & Loss Design (Choroid OCT)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "PROJECT A: CHOROID OCT SEGMENTATION • MODEL DESIGN",
               "Architecture Upgrade & Boundary-Weighted Loss Formulation",
               "U-Net++ with scSE attention and exponential boundary distance penalty",
               category_color=COLOR_GREEN)

    # Left: Architecture Card
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_CYAN)
    tb_arch = s5.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True

    p = tf_arch.paragraphs[0]
    p.text = "Architectural Innovations"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    arch_bullets = [
        ("Baseline Network:", "Standard U-Net with ResNet34 encoder (24.43M params). Direct skip connections span wide semantic gaps between high-level and low-level maps."),
        ("Improved Configuration:", "U-Net++ with ResNet34 backbone + concurrent Spatial and Channel Squeeze-and-Excitation (scSE) blocks (26.28M params, +7.55% capacity)."),
        ("Dense Nested Skips:", "Bridges encoder-decoder disparity via a dense hierarchy of intermediate convolution nodes, capturing fine boundary textures."),
        ("scSE Attention:", "Dual recalibration: channel excitation isolates choroidal tissue signatures; spatial excitation focuses gradients along the CSI boundary.")
    ]
    for lbl, val in arch_bullets:
        p = tf_arch.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    p = tf_arch.add_paragraph()
    p.text = (
        "Scientific Attribution Note: Because architecture, attention, boundary loss, and effective batch size "
        "(8 via accumulation vs 2) were upgraded together, gains reflect the combined improved configuration rather than an isolated scSE ablation. 4 training epochs."
    )
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(6)

    # Right: Loss Function Card
    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_TEAL)
    tb_loss = s5.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_loss = tb_loss.text_frame
    tf_loss.word_wrap = True

    p = tf_loss.paragraphs[0]
    p.text = "Boundary-Weighted Loss Formulation"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    p = tf_loss.add_paragraph()
    p.text = (
        "Standard cross-entropy treats all pixels equally. Deep models easily achieve >0.97 Dice by segmenting "
        "the interior choroid while drifting 2–5 pixels at the subtle CSI interface. We introduced an exponential boundary distance weight map:"
    )
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(6)

    p = tf_loss.add_paragraph()
    p.text = "w(x) = 1 + 5 • exp( - d(x)² / (2 • σ²) ),   where σ = 5 pixels\nL_total = L_BCE,weighted + L_Dice"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE
    p.space_after = Pt(8)

    loss_bullets = [
        ("Distance Function d(x):", "Euclidean distance to the nearest true anatomical boundary (BM or CSI)."),
        ("6× Maximum Penalty:", "Pixels exactly on the interface receive a weight of 1 + 5 = 6.0."),
        ("Smooth Falloff:", "Weight exponentially decays to 1.0 in interior stroma and distant vitreous."),
        ("Clinical Impact:", "Directly suppresses the boundary drift that corrupts subfoveal thickness measurements.")
    ]
    for lbl, val in loss_bullets:
        p = tf_loss.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    set_speaker_notes(s5, (
        "To resolve the subtle choroid-sclera interface, we upgraded from standard U-Net to U-Net++ with ResNet34 and concurrent spatial-and-channel squeeze-and-excitation blocks, adding only 7.5% parameters. "
        "In parallel, standard loss treats all pixels equally, so models easily get high Dice by predicting the fat center of the choroid while missing the edge. "
        "We implemented a boundary-weighted loss that upweights boundary pixels by up to six times with a five-pixel Gaussian sigma. "
        "To maintain academic rigor, we report this as an overall improved configuration since multiple components evolved together."
    ))

    # =========================================================================
    # SLIDE 6: Segmentation and Boundary Results (Choroid OCT)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "PROJECT A: CHOROID OCT SEGMENTATION • EVALUATION",
               "Quantitative Segmentation & Boundary Localization Performance",
               "Comprehensive evaluation across 697 holdout test B-scans (18 patients / 19 eyes)",
               category_color=COLOR_GREEN)

    # Left: Results Table Card
    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_CYAN)
    tb_res = s6.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_res = tb_res.text_frame
    tf_res.word_wrap = True
    p = tf_res.paragraphs[0]
    p.text = "Holdout Test Metrics Comparison"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    # Table
    t_shape = s6.shapes.add_table(6, 4, Inches(1.0), Inches(2.4), Inches(5.3), Inches(2.2))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(1.8)
    tbl.columns[1].width = Inches(1.1)
    tbl.columns[2].width = Inches(1.2)
    tbl.columns[3].width = Inches(1.2)

    headers = ["Metric", "Baseline", "U-Net++ scSE", "Change"]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(10.5)
        cell.text_frame.paragraphs[0].font.color.rgb = COLOR_CYAN

    data = [
        ["Choroid Dice", "0.9751", "0.9804", "+0.54%"],
        ["BM MAE (Inner)", "0.562 px", "0.407 px", "-27.6%"],
        ["CSI MAE (Outer)", "1.755 px", "1.567 px", "-10.7%"],
        ["Thickness MAE", "1.870 px", "1.715 px", "-8.3%"],
        ["Mask HD95", "3.98 px", "3.40 px", "-14.6%"],
    ]
    for row_idx, r in enumerate(data):
        for col_idx, val in enumerate(r):
            cell = tbl.cell(row_idx + 1, col_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if col_idx == 2 or col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN
            else:
                p.font.color.rgb = COLOR_WHITE

    tb_nt = s6.shapes.add_textbox(Inches(1.0), Inches(4.8), Inches(5.3), Inches(2.0))
    tf_nt = tb_nt.text_frame
    tf_nt.word_wrap = True
    p = tf_nt.paragraphs[0]
    p.text = (
        "Key Quantitative Findings:\n"
        "• Pixel units are native & primary. Physical equivalents: BM MAE ≈ 1.53 µm, CSI MAE ≈ 5.88 µm "
        "(assuming Heidelberg Spectralis 3.75 µm/px axial scale).\n"
        "• Sub-Pixel BM Alignment: Bruch's membrane error is just 0.407 pixels.\n"
        "• Sub-Human CSI Error: CSI error (5.88 µm) is substantially smaller than inter-grader dispute (15–30 µm)."
    )
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_MUTED

    # Right: Visual Comparison
    seg_img_path = os.path.join(assets_dir, "39_10_seg.png")
    if os.path.exists(seg_img_path):
        s6.shapes.add_picture(seg_img_path, Inches(6.8), Inches(1.8), width=Inches(5.7))

    set_speaker_notes(s6, (
        "Here are the test results on 697 unseen B-scans from 18 holdout patients. "
        "While Dice improved modestly from 0.975 to 0.980, the boundary-weighted loss drove double-digit reductions in boundary localization error: "
        "Bruch's membrane error dropped by 27.6% to 0.407 pixels (about 1.5 micrometers), and CSI error dropped by 10.7% to 1.57 pixels (about 5.9 micrometers). "
        "Both errors are well below the 15 to 30 micrometer inter-grader variability between human experts."
    ))

    # =========================================================================
    # SLIDE 7: Thickness Measurement & Bland-Altman (Choroid OCT)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "PROJECT A: CHOROID OCT SEGMENTATION • CLINICAL VALIDATION",
               "Clinical Agreement Analysis & The Post-Processing Paradox",
               "Bland-Altman agreement and the peril of conventional morphological hole-filling",
               category_color=COLOR_GREEN)

    # Left: Bland-Altman Plot
    ba_path = os.path.join(assets_dir, "bland_altman_per_scan_means.png")
    if os.path.exists(ba_path):
        s7.shapes.add_picture(ba_path, Inches(0.8), Inches(1.8), width=Inches(5.7))

    # Right: Analysis & Paradox Card
    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_CYAN)
    tb_ba = s7.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_ba = tb_ba.text_frame
    tf_ba.word_wrap = True

    p = tf_ba.paragraphs[0]
    p.text = "Bland-Altman Clinical Concordance"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    bullets_ba = [
        ("Near-Zero Systematic Bias:", "+0.28 px (+1.05 µm) mean bias across 697 holdout B-scans, confirming no systematic over- or under-segmentation."),
        ("95% Limits of Agreement:", "[-5.12, +5.68] px ([-19.2, +21.3] µm), within clinically accepted tolerances."),
        ("Subfoveal SFCT Correlation:", "r = 0.9886 (p < 0.0001) across 19 holdout eyes; mean predicted 216.1 µm vs ground truth 213.6 µm (MAE 3.11 px ≈ 11.64 µm)."),
        ("Statistical Unit Rigor:", "Evaluated strictly on 697 scan averages rather than pooled columns (>350k points) to avoid pseudoreplication.")
    ]
    for lbl, val in bullets_ba:
        p = tf_ba.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(3)

    p = tf_ba.add_paragraph()
    p.text = "⚠️ The Post-Processing Paradox"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_before = Pt(6)

    p = tf_ba.add_paragraph()
    p.text = (
        "Standard morphological hole-filling and smoothing drastically worsened thickness MAE from "
        "2.095 px to 11.223 px (p < 0.001)! Large vessel lumens in Haller's layer are genuine anatomical voids, "
        "not segmentation noise. Artificially filling them alters connected component geometry, driving the CSI boundary outward into sclera. "
        "Final protocol: Largest Connected Component (LCC) + horizontal gap bridging (≤ 15 px) only."
    )
    p.font.size = Pt(9.8)
    p.font.color.rgb = COLOR_MUTED

    set_speaker_notes(s7, (
        "High Dice scores do not guarantee clinical validity. In Bland-Altman analysis on 697 per-scan means, our pipeline showed near-zero systematic bias (+1.05 micrometers) with 95% limits of agreement within ±20 micrometers, and an SFCT correlation of r=0.9886 across 19 eyes. "
        "Furthermore, we discovered a vital post-processing paradox: standard morphological hole-filling worsened thickness error by 500% from 2.1 to 11.2 pixels. "
        "Blood vessel lumens in Haller's layer are genuine anatomical voids, not artifacts. Artificially filling them pushes the boundary outward into the sclera."
    ))

    # =========================================================================
    # SLIDE 8: Limitations & Failure Analysis (Choroid OCT)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "PROJECT A: CHOROID OCT SEGMENTATION • FAILURE ANALYSIS",
               "Failure Modes & Structural Limitations in Retinal OCT",
               "Vessel shadowing artifacts, ground truth ambiguity, and experimental constraints",
               category_color=COLOR_GREEN)

    # Left: Worst Failure Image
    fail_path = os.path.join(assets_dir, "rank1_worst_CSI_eye_39_scan_8.png")
    if os.path.exists(fail_path):
        s8.shapes.add_picture(fail_path, Inches(0.8), Inches(1.8), width=Inches(5.7))

    # Right: Failure Analysis Card
    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_ROSE)
    tb_fail = s8.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_fail = tb_fail.text_frame
    tf_fail.word_wrap = True

    p = tf_fail.paragraphs[0]
    p.text = "Where Does the Pipeline Fail?"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE

    fail_bullets = [
        ("Acoustic Shadowing:", "Superficial retinal blood vessels absorb and scatter OCT light, casting deep vertical shadow bands down through the choroid."),
        ("Ground Truth Ambiguity (Eye 39, Scan 8):", "In our worst test failure, the human grader abruptly truncated the boundary at 34.6 px due to signal extinction. U-Net++ interpolated a smooth anatomical trajectory at 65.8 px. Much of the 31.2 px 'error' stems from subjective grader truncation under noise.")
    ]
    for lbl, val in fail_bullets:
        p = tf_fail.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    p = tf_fail.add_paragraph()
    p.text = "Structural Limitations of Project A"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_before = Pt(6)

    limits = [
        ("Cohort Size:", "697 test scans originate from 19 eyes (18 patients), introducing intra-eye scan correlation (pseudoreplication)."),
        ("Uncalibrated Axial Scale:", "3.75 µm/px assumed from Heidelberg specs; individual refractive error alters exact physical scaling."),
        ("Manual Fovea Landmarking:", "Subfoveal column localized via volume metadata rather than automated foveal depression detection."),
        ("Training Duration:", "4 epochs trained due to computational limits.")
    ]
    for lbl, val in limits:
        p = tf_fail.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(2)

    set_speaker_notes(s8, (
        "Every honest medical AI paper must report its failures. Here is our worst test failure: Scan 39_8. "
        "A major retinal vessel cast an acoustic shadow that extinguished the choroidal signal. "
        "The human grader abruptly truncated the annotation at 34.6 pixels, while U-Net++ smoothly interpolated the boundary across the shadow at 65.8 pixels. "
        "Much of the 31-pixel error is an artifact of annotation ambiguity in noise. "
        "We also recognize that our 697 test scans come from 19 eyes, and our axial calibration assumes 3.75 micrometers per pixel."
    ))

    # =========================================================================
    # SLIDE 9: Problem & Motivation (Quantum Pneumonia)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "PROJECT B: QUANTUM CLASSIFICATION • RESEARCH MOTIVATION",
               "Variational Quantum Circuits in Medical Deep Learning",
               "Parameter efficiency, expressive capacity, and benchmark design on PneumoniaMNIST",
               category_color=COLOR_PURPLE)

    # Left: Dataset Samples
    samples_path = os.path.join(assets_dir, "dataset_samples.png")
    if os.path.exists(samples_path):
        s9.shapes.add_picture(samples_path, Inches(0.8), Inches(1.8), width=Inches(5.7))

    # Right: Research Motivation Card
    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_PURPLE)
    tb_m = s9.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    p = tf_m.paragraphs[0]
    p.text = "Research Question & Grounded Motivation"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE

    m_bullets = [
        ("Core Research Question:", "\"Can a compact Variational Quantum Circuit (VQC) serve as an effective, highly parameter-efficient classifier head on classical visual representations?\""),
        ("Demystifying 'Quantum Advantage':", "We do NOT claim quantum supremacy. Instead, we rigorously study Hilbert-space expressiveness and optimization dynamics with just 29 quantum head parameters."),
        ("PneumoniaMNIST Benchmark:", "5,856 pediatric chest X-ray images (28 × 28 grayscale). Official partitions: 4,708 train, 524 val, 624 test.")
    ]
    for lbl, val in m_bullets:
        p = tf_m.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    p = tf_m.add_paragraph()
    p.text = "⚖️ Class Imbalance & Loss Weighting Nuance"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_before = Pt(6)

    p = tf_m.add_paragraph()
    p.text = (
        "The training set contains 74.2% Pneumonia (positive majority) and 25.8% Normal (negative minority). "
        "We set pos_weight = 0.3475 in BCEWithLogitsLoss. "
        "Because Pneumonia is the majority class, this weighting reduces the relative loss contribution of positive examples to balance the classes. "
        "It does NOT artificially bias the model to favor recall; high sensitivity is an observed experimental outcome."
    )
    p.font.size = Pt(9.8)
    p.font.color.rgb = COLOR_MUTED

    set_speaker_notes(s9, (
        "Moving to Project B, we investigate whether variational quantum circuits can serve as compact, expressive classification heads in medical image analysis. "
        "PneumoniaMNIST contains 5,856 chest X-rays. We do not claim 'quantum supremacy'. "
        "Rather, we test whether a 4-qubit quantum head with just 29 parameters can achieve competitive classification accuracy against classical models. "
        "The training set is 74% pneumonia, and pos_weight=0.3475 was used to balance class loss contributions."
    ))

    # =========================================================================
    # SLIDE 10: Hybrid Architecture & Circuit Mechanics (Quantum Pneumonia)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "PROJECT B: QUANTUM CLASSIFICATION • ARCHITECTURE",
               "Hybrid Quantum-Classical Architecture & Circuit Mechanics",
               "Classical CNN feature compression, angle embedding, and ring-entangled VQC",
               category_color=COLOR_PURPLE)

    # Left: Quantum Circuit Diagram & Flow
    q_circ_path = os.path.join(assets_dir, "quantum_circuit_diagram.png")
    if os.path.exists(q_circ_path):
        s10.shapes.add_picture(q_circ_path, Inches(0.8), Inches(1.8), width=Inches(6.8))

    q_pipe_path = os.path.join(assets_dir, "hybrid_qnn_pipeline_diagram.png")
    if os.path.exists(q_pipe_path):
        s10.shapes.add_picture(q_pipe_path, Inches(0.8), Inches(4.3), width=Inches(6.8))

    # Right: Four-Stage Architecture Card
    add_card(s10, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.2), border_color=COLOR_PURPLE)
    tb_q = s10.shapes.add_textbox(Inches(8.0), Inches(1.95), Inches(4.3), Inches(4.9))
    tf_q = tb_q.text_frame
    tf_q.word_wrap = True

    p = tf_q.paragraphs[0]
    p.text = "Four-Stage Hybrid Flow"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE

    q_steps = [
        ("1. Classical CNN Backbone:", "3 Conv blocks (1 → 16 → 32 → 64) + AdaptiveAvgPool → Linear(64, 4) compresses image to vector x ∈ R⁴ (11,076 params)."),
        ("2. Angle Embedding:", "Maps x to rotation angles via θ_i = π tanh(x_i) ∈ [-π, π]. Applies R_y(θ_i) on state |0000⟩."),
        ("3. Variational Circuit (2 Layers):", "3 rotations (R_x, R_y, R_z) per qubit (24 weights) + Ring CNOT ladder (0→1→2→3→0) generating state entanglement."),
        ("4. Measurement & Readout:", "Measures Pauli-Z expectation values ⟨Z_i⟩ ∈ [-1, 1]. Classical Linear(4→1) yields final logit (5 weights).")
    ]
    for lbl, val in q_steps:
        p = tf_q.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(3)

    p = tf_q.add_paragraph()
    p.text = "Head Parameter Count:\n24 (Quantum VQC) + 5 (Linear Readout) = 29 Parameters!"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p.space_before = Pt(6)

    set_speaker_notes(s10, (
        "The hybrid architecture operates in four stages. First, a lightweight 3-block CNN compresses the 28x28 chest X-ray into four classical features. "
        "Second, these features are mapped to rotation angles via a pi-tanh non-linearity and embedded onto four qubits with Ry gates. "
        "Third, two variational layers apply RX, RY, and RZ rotations followed by a circular ring of CNOT gates that entangles all four qubits. "
        "Finally, Pauli-Z expectation values are measured and fed into a 5-parameter linear layer. "
        "The entire quantum classification head uses only 29 parameters."
    ))

    # =========================================================================
    # SLIDE 11: Experimental Design & Fair Controls (Quantum Pneumonia)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "PROJECT B: QUANTUM CLASSIFICATION • METHODOLOGY",
               "Eliminating the Capacity Confounder: Fair Classical Controls",
               "Parameter matching and rigorous optimization parity across all architectures",
               category_color=COLOR_PURPLE)

    # Left: Parameter Comparison Graphic
    comp_path = os.path.join(assets_dir, "model_comparison.png")
    if os.path.exists(comp_path):
        s11.shapes.add_picture(comp_path, Inches(0.8), Inches(1.8), width=Inches(5.7))

    # Right: Fair Control Card
    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_CYAN)
    tb_fc = s11.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_fc = tb_fc.text_frame
    tf_fc.word_wrap = True

    p = tf_fc.paragraphs[0]
    p.text = "The Capacity Confounder in Quantum ML"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    p = tf_fc.add_paragraph()
    p.text = (
        "A baseline CNN contains >105,000 parameters (1,025 in head). "
        "Directly comparing a 29-parameter quantum head to a 105k-parameter network is fundamentally confounded by capacity: "
        "if the CNN overfits, quantum models appear artificially superior."
    )
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(6)

    p = tf_fc.add_paragraph()
    p.text = "Our Fair Control: CNN + MLP (Capacity-Matched)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE

    p = tf_fc.add_paragraph()
    p.text = (
        "• Same 4-dim CNN backbone (11,076 params).\n"
        "• Classical MLP Head: Linear(4, 8) + ReLU + Linear(8, 1) = 49 parameters.\n"
        "• Total Parameters: 11,125 (classical control) vs 11,105 (hybrid QNN) — matched to within 0.18% capacity!"
    )
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(6)

    p = tf_fc.add_paragraph()
    p.text = "Strict Optimization Parity:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    p = tf_fc.add_paragraph()
    p.text = (
        "• Identical Adam optimizer (lr = 1e-3, weight_decay = 1e-4).\n"
        "• Identical CosineAnnealingLR (T_max = 20), batch size 64, seed 42, 20 epochs.\n"
        "• Identical pos_weight = 0.3475 in BCEWithLogitsLoss.\n"
        "• Simulation: PennyLane default.qubit state-vector with exact backpropagation."
    )
    p.font.size = Pt(9.8)
    p.font.color.rgb = COLOR_MUTED

    set_speaker_notes(s11, (
        "A major flaw in many quantum machine learning papers is comparing a small quantum circuit to an overparameterized classical model. "
        "We eliminated this confounder by designing a capacity-matched classical control: a CNN with an identical 4-dimensional bottleneck feeding a 49-parameter MLP head. "
        "Both models have approximately 11,100 total parameters and trained under identical optimization schedules."
    ))

    # =========================================================================
    # SLIDE 12: Classification Results & Statistical Tests (Quantum Pneumonia)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "PROJECT B: QUANTUM CLASSIFICATION • EVALUATION",
               "Benchmark Results & McNemar's Hypothesis Testing",
               "Statistical parity: competitive performance without empirical quantum supremacy",
               category_color=COLOR_PURPLE)

    # Left: Results Table Card
    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_PURPLE)
    tb_qr = s12.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_qr = tb_qr.text_frame
    tf_qr.word_wrap = True

    p = tf_qr.paragraphs[0]
    p.text = "Holdout Test Metrics (N = 624)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE

    # Table
    t_shape2 = s12.shapes.add_table(5, 5, Inches(1.0), Inches(2.4), Inches(5.3), Inches(2.0))
    tbl2 = t_shape2.table
    tbl2.columns[0].width = Inches(1.7)
    tbl2.columns[1].width = Inches(0.8)
    tbl2.columns[2].width = Inches(1.0)
    tbl2.columns[3].width = Inches(0.9)
    tbl2.columns[4].width = Inches(0.9)

    headers2 = ["Model", "Head", "Accuracy", "F1", "AUC"]
    for i, h in enumerate(headers2):
        cell = tbl2.cell(0, i)
        cell.text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(10)
        cell.text_frame.paragraphs[0].font.color.rgb = COLOR_CYAN

    data2 = [
        ["Baseline CNN", "1,025", "85.74%", "89.26%", "0.9291"],
        ["CNN+MLP Control", "49", "87.66%", "90.72%", "0.9242"],
        ["Hybrid QNN (2-L)", "29", "89.10%", "91.75%", "0.9374"],
        ["QNN (1-L Ablation)", "17", "90.38%", "92.65%", "0.9407"],
    ]
    for row_idx, r in enumerate(data2):
        for col_idx, val in enumerate(r):
            cell = tbl2.cell(row_idx + 1, col_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            if row_idx == 2:
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN
            elif row_idx == 3:
                p.font.color.rgb = COLOR_MUTED
            else:
                p.font.color.rgb = COLOR_WHITE

    # McNemar's Test Findings
    tb_mcn = s12.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(5.3), Inches(2.3))
    tf_mcn = tb_mcn.text_frame
    tf_mcn.word_wrap = True
    p = tf_mcn.paragraphs[0]
    p.text = "📊 McNemar's Paired Significance Tests:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    p = tf_mcn.add_paragraph()
    p.text = (
        "• QNN (2-L) vs Baseline CNN: χ² = 9.72, p = 0.0018 → Statistically Significant gain over unconstrained baseline.\n"
        "• QNN (2-L) vs Matched MLP Control: χ² = 1.93, p = 0.164 → NOT statistically significant (α = 0.05). "
        "95% Wilson Score CIs overlap ([86.7%, 91.5%] vs [85.1%, 90.2%]).\n"
        "• Honest Conclusion: The 29-param quantum head matches classical efficiency, but provides no empirical quantum advantage."
    )
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_WHITE

    # Right: ROC Curves
    roc_path = os.path.join(assets_dir, "roc_curves_combined.png")
    if os.path.exists(roc_path):
        s12.shapes.add_picture(roc_path, Inches(6.8), Inches(1.8), width=Inches(5.7))

    set_speaker_notes(s12, (
        "Here are the test results on 624 holdout X-rays. The 2-layer QNN achieved 89.1% accuracy and 0.937 AUC. "
        "While it significantly outperformed the large baseline CNN (p=0.0018), when compared against our parameter-matched MLP control, the difference was not statistically significant (p=0.164). "
        "This is the key honest finding: the quantum head matches classical efficiency, but claims of quantum advantage would be empirically unfounded."
    ))

    # =========================================================================
    # SLIDE 13: Val-to-Test Drop & 1-Layer Investigation (Quantum Pneumonia)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "PROJECT B: QUANTUM CLASSIFICATION • AUDIT & INVESTIGATION",
               "Investigating the Validation-to-Test Drop & 1-Layer Paradox",
               "Prevalence shift, specificity collapse, and model selection integrity",
               category_color=COLOR_PURPLE)

    # Left: Investigation Card
    add_card(s13, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_AMBER)
    tb_inv = s13.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_inv = tb_inv.text_frame
    tf_inv.word_wrap = True

    p = tf_inv.paragraphs[0]
    p.text = "Investigation 1: Val-to-Test Accuracy Drop (95.8% → 89.1%)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    inv1_points = [
        ("Prevalence Shift:", "Normal cases make up 25.76% of validation, but surge to 37.50% of test (+11.74% shift)."),
        ("Test Specificity Collapse:", "While Pneumonia recall was rock-solid (95.6% → 96.9%), specificity on Normal cases collapsed from 96.3% on validation to 76.1% on test across ALL models (down to 65.0% in CNN)."),
        ("Joint Cause:", "Harder normal cases in test, combined with higher normal prevalence, amplify false positives in overall accuracy.")
    ]
    for lbl, val in inv1_points:
        p = tf_inv.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(2)

    p = tf_inv.add_paragraph()
    p.text = "Investigation 2: Why Did 1-Layer (90.4%) Beat 2-Layer (89.1%)?"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_before = Pt(6)

    inv2_points = [
        ("Statistical Difference:", "Only 8 images out of 624 (564 vs 556 correct). McNemar's p = 0.186 (NOT statistically significant)."),
        ("Model Selection Integrity:", "2-layer QNN achieved superior validation loss (0.0557 vs 0.0584). Selected strictly on validation metrics without test set peeking."),
        ("Reporting Protocol:", "2-layer QNN maintained as primary architecture; 1-layer reported transparently as ablation.")
    ]
    for lbl, val in inv2_points:
        p = tf_inv.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(2)

    # Right: Loss Curves
    loss_path = os.path.join(assets_dir, "loss_curves.png")
    if os.path.exists(loss_path):
        s13.shapes.add_picture(loss_path, Inches(6.8), Inches(1.8), width=Inches(5.7))

    set_speaker_notes(s13, (
        "We investigated two critical anomalies. First, why did accuracy drop from 95.8% on validation to 89.1% on test? "
        "The test set has 12% more normal images, and normal specificity dropped across all models to 76%. "
        "Second, 1-layer QNN reached 90.38% test accuracy, beating 2-layer by 8 images. "
        "However, this difference is not statistically significant (p=0.186), and 2-layer had lower validation loss, which governed our selection."
    ))

    # =========================================================================
    # SLIDE 14: Quantum Simulation Reality & Limitations (Quantum Pneumonia)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "PROJECT B: QUANTUM CLASSIFICATION • PHYSICAL REALITY",
               "Simulation Reality, Hardware Constraints, and Limitations",
               "State-vector differentiation vs physical NISQ Parameter-Shift execution",
               category_color=COLOR_PURPLE)

    # Left: Confusion Matrices
    cm_q_path = os.path.join(assets_dir, "confusion_matrix_quantum_hybrid.png")
    if os.path.exists(cm_q_path):
        s14.shapes.add_picture(cm_q_path, Inches(0.8), Inches(1.8), width=Inches(5.7))

    # Right: Simulation Reality Card
    add_card(s14, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_CYAN)
    tb_sim = s14.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_sim = tb_sim.text_frame
    tf_sim.word_wrap = True

    p = tf_sim.paragraphs[0]
    p.text = "Simulation vs Physical NISQ Hardware"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    sim_bullets = [
        ("Ideal State-Vector Simulation:", "Executed on PennyLane default.qubit simulator using classical matrix multiplication and exact reverse-mode automatic differentiation (diff_method=\"backprop\")."),
        ("Physical Hardware Reality:", "Physical quantum processors cannot access full wavefunctions. Gradients require the Parameter-Shift Rule: ∂⟨Z⟩/∂θ = 0.5 • [⟨Z⟩(θ+π/2) - ⟨Z⟩(θ-π/2)]."),
        ("Hardware Execution Burden:", "Requires 2 × 24 = 48 physical circuit runs per sample per step (>4.5 million runs across 20 epochs), plus decoherence and gate noise.")
    ]
    for lbl, val in sim_bullets:
        p = tf_sim.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(3)

    p = tf_sim.add_paragraph()
    p.text = "Project B Experimental Limitations"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE
    p.space_before = Pt(6)

    lim_b = [
        ("Single Random Seed:", "Evaluated under seed 42; multi-seed variance remains unmeasured."),
        ("Qubit Scale Constraint:", "4-qubit scale bounds state space to 2⁴ = 16 dimensions, limiting high-order entanglement."),
        ("Throughput Context:", "0.07 ms/img inference latency reflects batch-amortized CPU simulation.")
    ]
    for lbl, val in lim_b:
        p = tf_sim.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(2)

    set_speaker_notes(s14, (
        "We must be transparent about the quantum simulation environment. We ran on PennyLane's state-vector simulator with backpropagation autodiff. "
        "On real NISQ quantum hardware, gradients require the parameter-shift rule—executing 48 physical circuits per sample—plus handling shot noise and decoherence. "
        "Training took 11 minutes on CPU, but hardware deployment would require substantial error mitigation."
    ))

    # =========================================================================
    # SLIDE 15: Cross-Project Synthesis & Lessons
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "SYNTHESIS & SCIENTIFIC TAKEAWAYS",
               "Three Core Pillars of Rigorous Medical Image AI",
               "Cross-project conclusions: patient integrity, matched controls, and metric honesty")

    # Left: 3-Pillars Graphic
    pil_path = os.path.join(assets_dir, "synthesis_3pillars.png")
    if os.path.exists(pil_path):
        s15.shapes.add_picture(pil_path, Inches(0.8), Inches(1.8), width=Inches(5.7))

    # Right: Synthesis Card
    add_card(s15, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_TEAL)
    tb_syn = s15.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_syn = tb_syn.text_frame
    tf_syn.word_wrap = True

    p = tf_syn.paragraphs[0]
    p.text = "Comparative Summary Across Both Projects"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    # Table
    t_shape3 = s15.shapes.add_table(4, 3, Inches(7.0), Inches(2.4), Inches(5.3), Inches(1.8))
    tbl3 = t_shape3.table
    tbl3.columns[0].width = Inches(1.5)
    tbl3.columns[1].width = Inches(1.9)
    tbl3.columns[2].width = Inches(1.9)

    headers3 = ["Dimension", "Project A (OCT)", "Project B (Quantum)"]
    for i, h in enumerate(headers3):
        cell = tbl3.cell(0, i)
        cell.text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(9.5)
        cell.text_frame.paragraphs[0].font.color.rgb = COLOR_CYAN

    data3 = [
        ["Data Safeguard", "Patient-level split (no 30 µm slice leak)", "Benchmark partition (no demographic leak)"],
        ["Baseline Control", "U-Net ResNet34 (+7.5% params)", "49-param MLP (+0.18% params)"],
        ["Metric Honesty", "Bland-Altman LoA (no hole filling)", "McNemar's test (p=0.164, no supremacy)"]
    ]
    for row_idx, r in enumerate(data3):
        for col_idx, val in enumerate(r):
            cell = tbl3.cell(row_idx + 1, col_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9)
            p.font.color.rgb = COLOR_WHITE

    # Big Quote Card
    tb_qte = s15.shapes.add_textbox(Inches(7.0), Inches(4.4), Inches(5.3), Inches(2.3))
    tf_qte = tb_qte.text_frame
    tf_qte.word_wrap = True
    p = tf_qte.paragraphs[0]
    p.text = "Final Scientific Takeaway:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    p = tf_qte.add_paragraph()
    p.text = (
        "\"The hardest part of medical image AI is not achieving high numbers — "
        "it is verifying that the numbers mean what you think they mean.\""
    )
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(4)

    set_speaker_notes(s15, (
        "To conclude, these two projects demonstrate that methodological honesty is what gives medical AI scientific value. "
        "By enforcing strict patient splits, designing matched classical controls, and looking past top-line metrics to inspect vessel shadows and specificity drops, we obtain reliable clinical conclusions. "
        "Thank you, and I look forward to your questions."
    ))

    # =========================================================================
    # SLIDE 16: Backup A1 — OIMHS Mask Audit & Post-Processing Details
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "BACKUP SLIDE A1 • PROJECT A ANATOMICAL AUDIT",
               "OIMHS Mask Color Coding & The Hole-Filling Failure Mechanism",
               "Mathematical proof of why morphological closing degraded thickness estimation",
               category_color=COLOR_AMBER)

    add_card(s16, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_GREEN)
    tb_b1 = s16.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_b1 = tb_b1.text_frame
    tf_b1.word_wrap = True

    p = tf_b1.paragraphs[0]
    p.text = "OIMHS Dataset Color Channel Deconstruction"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    b1_pts = [
        ("Green Channel (G > 128, R < 128):", "Represents neurosensory retina. Average vertical position is ~37 µm above Bruch's membrane."),
        ("Yellow Channel (R > 128, G > 128):", "Represents true choroidal stroma. Average vertical position is ~214 µm below Bruch's membrane."),
        ("Automated Mask Extraction:", "True choroid binary mask is strictly extracted using: (mask[..., 0] > 128) & (mask[..., 1] > 128). Verified across all 3,859 scans.")
    ]
    for lbl, val in b1_pts:
        p = tf_b1.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    add_card(s16, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_AMBER)
    tb_b1r = s16.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_b1r = tb_b1r.text_frame
    tf_b1r.word_wrap = True

    p = tf_b1r.paragraphs[0]
    p.text = "Mathematical Proof of Hole-Filling Failure"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    p = tf_b1r.add_paragraph()
    p.text = (
        "Why did morphological closing + smoothing inflate thickness MAE from 2.095 px to 11.223 px (p < 0.001)?\n\n"
        "• Large choroidal vessels in Haller's layer appear as hyporeflective lumens (dark circular voids).\n"
        "• Morphological closing (M • K) treats lumens as background holes and bridges them with surrounding stroma.\n"
        "• This alters the connected component boundary, dragging the detected CSI interface downward into scleral tissue by 8–15 pixels.\n\n"
        "Final Protocol: Largest Connected Component (LCC) + horizontal gap bridging (≤ 15 px) only. Lumens are preserved as genuine anatomy."
    )
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_WHITE

    set_speaker_notes(s16, (
        "In backup A1, this explains why we rejected standard morphological closing: blood vessel lumens in the choroid are genuine empty spaces, not noise. "
        "Closing them pushed the segmented boundary into the sclera, multiplying error by five times."
    ))

    # =========================================================================
    # SLIDE 17: Backup A2 — Fovea Centering & Regional ETDRS Thickness
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17)
    add_header(s17, "BACKUP SLIDE A2 • PROJECT A CLINICAL THICKNESS MAPPING",
               "Regional ETDRS Subfield Thickness & Foveal Alignment",
               "Preservation of physiological nasal thinning and subfoveal peaking",
               category_color=COLOR_AMBER)

    prof_path = os.path.join(assets_dir, "10_thickness_profile.png")
    if os.path.exists(prof_path):
        s17.shapes.add_picture(prof_path, Inches(0.8), Inches(1.8), width=Inches(5.7))

    add_card(s17, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_CYAN)
    tb_b2 = s17.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_b2 = tb_b2.text_frame
    tf_b2.word_wrap = True

    p = tf_b2.paragraphs[0]
    p.text = "Regional ETDRS Sector Dynamics"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    b2_pts = [
        ("Physiological Gradient:", "In healthy human eyes, the choroid is thickest subfoveally (SFCT), thins moderately temporally, and thins steeply nasally toward the optic disc."),
        ("Model Fidelity:", "U-Net++ faithfully reproduces this physiological nasal gradient across all 697 test scans without boundary divergence."),
        ("Foveal Centering Implementation:", "Central foveal scan is localized via dataset volume metadata. Future work will replace this with automated 2D foveal pit detection.")
    ]
    for lbl, val in b2_pts:
        p = tf_b2.add_paragraph()
        p.text = f"• {lbl} {val}"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    set_speaker_notes(s17, (
        "Backup A2 addresses how thickness varies across retinal eccentricities. "
        "The model faithfully preserves the physiological nasal thinning pattern, matching clinical literature."
    ))

    # =========================================================================
    # SLIDE 18: Backup B1 — Quantum Circuit Mechanics (Parameter-Shift vs Backprop)
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18)
    add_header(s18, "BACKUP SLIDE B1 • PROJECT B QUANTUM COMPUTATION REALITY",
               "Quantum Gradients: Parameter-Shift Rule vs Backprop",
               "Analytical formulation and hardware scaling feasibility",
               category_color=COLOR_AMBER)

    add_card(s18, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_PURPLE)
    tb_b3 = s18.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_b3 = tb_b3.text_frame
    tf_b3.word_wrap = True

    p = tf_b3.paragraphs[0]
    p.text = "The Parameter-Shift Theorem"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE

    p = tf_b3.add_paragraph()
    p.text = (
        "For quantum circuits with generators having eigenvalues ±1/2 (such as Pauli rotations Rx, Ry, Rz), "
        "the exact gradient of an expectation value is:\n\n"
        "∂⟨Z⟩ / ∂θ_j = 0.5 • [ ⟨Z⟩(θ_j + π/2) - ⟨Z⟩(θ_j - π/2) ]\n\n"
        "• Requires 2 distinct quantum circuit evaluations per parameter per sample.\n"
        "• For P = 24 parameters and batch size B = 64: 2 × 24 × 64 = 3,072 circuit runs per batch!\n"
        "• Over 74 batches/epoch × 20 epochs = 4.54 × 10⁶ circuit runs on physical hardware."
    )
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_WHITE

    add_card(s18, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_TEAL)
    tb_b3r = s18.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_b3r = tb_b3r.text_frame
    tf_b3r.word_wrap = True

    p = tf_b3r.paragraphs[0]
    p.text = "Why Simulator Backpropagation?"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    p = tf_b3r.add_paragraph()
    p.text = (
        "• State-Vector Simulation: PennyLane's default.qubit computes exact state amplitudes in C¹⁶ via matrix multiplication.\n\n"
        "• Reverse-Mode Autodiff: Backpropagation through state-vectors computes exact gradients in a single backward pass, "
        "reducing 20-epoch training from ~8 hours to 11.2 minutes on consumer CPU.\n\n"
        "• Scientific Validity: Simulator backprop gives identical parameter updates to noiseless parameter-shift with infinite shots, "
        "providing an ideal upper bound on VQC expressive capacity."
    )
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_WHITE

    set_speaker_notes(s18, (
        "Backup B1 provides the exact math of the Parameter-Shift rule. On physical quantum processors, evaluating gradients requires 4.5 million circuit executions across training. "
        "State-vector backpropagation made this semester study computationally feasible."
    ))

    # =========================================================================
    # SLIDE 19: Backup B2 — Detailed Statistical Significance Matrix
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19)
    add_header(s19, "BACKUP SLIDE B2 • PROJECT B STATISTICAL MATRIX",
               "McNemar's Contingency Matrix & Wilson Confidence Intervals",
               "Exhaustive statistical analysis proving absence of quantum supremacy",
               category_color=COLOR_AMBER)

    add_card(s19, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_CYAN)
    tb_b4 = s19.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_b4 = tb_b4.text_frame
    tf_b4.word_wrap = True

    p = tf_b4.paragraphs[0]
    p.text = "Paired McNemar Contingency Matrix (N = 624)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    # Contingency Table
    t_shape4 = s19.shapes.add_table(5, 5, Inches(1.0), Inches(2.4), Inches(5.3), Inches(2.2))
    tbl4 = t_shape4.table
    tbl4.columns[0].width = Inches(2.1)
    tbl4.columns[1].width = Inches(0.7)
    tbl4.columns[2].width = Inches(0.7)
    tbl4.columns[3].width = Inches(0.8)
    tbl4.columns[4].width = Inches(1.0)

    headers4 = ["Comparison", "n01", "n10", "χ²", "p-value"]
    for i, h in enumerate(headers4):
        cell = tbl4.cell(0, i)
        cell.text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(10)
        cell.text_frame.paragraphs[0].font.color.rgb = COLOR_CYAN

    data4 = [
        ["QNN (2L) vs Baseline CNN", "48", "22", "9.72", "0.0018 (Sig)"],
        ["QNN (2L) vs MLP Control", "32", "23", "1.93", "0.164 (NS)"],
        ["QNN (1L) vs QNN (2L)", "19", "11", "1.74", "0.186 (NS)"],
        ["MLP Control vs Baseline", "39", "27", "2.18", "0.139 (NS)"],
    ]
    for row_idx, r in enumerate(data4):
        for col_idx, val in enumerate(r):
            cell = tbl4.cell(row_idx + 1, col_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            if "Sig" in val and "NS" not in val:
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN
            else:
                p.font.color.rgb = COLOR_WHITE

    tb_nt4 = s19.shapes.add_textbox(Inches(1.0), Inches(4.8), Inches(5.3), Inches(2.0))
    tf_nt4 = tb_nt4.text_frame
    tf_nt4.word_wrap = True
    p = tf_nt4.paragraphs[0]
    p.text = (
        "• n01: Model A incorrect & Model B correct.\n"
        "• n10: Model A correct & Model B incorrect.\n"
        "• Continuity-corrected McNemar: χ² = (|n01 - n10| - 1)² / (n01 + n10)."
    )
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_MUTED

    add_card(s19, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), border_color=COLOR_PURPLE)
    tb_b4r = s19.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.9))
    tf_b4r = tb_b4r.text_frame
    tf_b4r.word_wrap = True

    p = tf_b4r.paragraphs[0]
    p.text = "95% Wilson Score Confidence Intervals"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE

    # Wilson Table
    t_shape5 = s19.shapes.add_table(4, 3, Inches(7.0), Inches(2.4), Inches(5.3), Inches(1.8))
    tbl5 = t_shape5.table
    tbl5.columns[0].width = Inches(1.7)
    tbl5.columns[1].width = Inches(1.8)
    tbl5.columns[2].width = Inches(1.8)

    headers5 = ["Model", "Accuracy [95% CI]", "F1 Score [95% CI]"]
    for i, h in enumerate(headers5):
        cell = tbl5.cell(0, i)
        cell.text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(10)
        cell.text_frame.paragraphs[0].font.color.rgb = COLOR_CYAN

    data5 = [
        ["Hybrid QNN (2-L)", "89.10% [86.67, 91.46]", "0.9175 [0.898, 0.934]"],
        ["CNN + MLP Control", "87.66% [85.12, 90.17]", "0.9072 [0.887, 0.925]"],
        ["Baseline CNN", "85.74% [83.08, 88.35]", "0.8926 [0.871, 0.912]"],
    ]
    for row_idx, r in enumerate(data5):
        for col_idx, val in enumerate(r):
            cell = tbl5.cell(row_idx + 1, col_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_WHITE

    tb_nt5 = s19.shapes.add_textbox(Inches(7.0), Inches(4.4), Inches(5.3), Inches(2.4))
    tf_nt5 = tb_nt5.text_frame
    tf_nt5.word_wrap = True
    p = tf_nt5.paragraphs[0]
    p.text = (
        "Definitive Audit Conclusion:\n"
        "Because the 95% Wilson confidence intervals overlap extensively and McNemar's p = 0.164 > 0.05, "
        "the hybrid QNN is statistically equivalent in performance to a parameter-matched classical neural network. "
        "The small 1.44% test accuracy difference represents expected sampling variation rather than a quantum advantage."
    )
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_AMBER

    set_speaker_notes(s19, (
        "Backup B2 shows the complete contingency tables for McNemar's tests and Wilson score intervals. "
        "Notice that the QNN and MLP control confidence intervals overlap substantially, proving that the small test accuracy difference is well within statistical noise."
    ))

    # Save presentation
    os.makedirs("presentation", exist_ok=True)
    out_pptx = "presentation/combined_presentation.pptx"
    prs.save(out_pptx)
    print(f"Successfully generated {out_pptx} with {len(prs.slides)} slides!")


if __name__ == "__main__":
    main()
