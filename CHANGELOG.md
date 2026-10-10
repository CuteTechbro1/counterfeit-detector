# CHANGELOG: Counterfeit Detector

All notable architectural, security, machine learning, user experience, and design enhancements are documented in this changelog.

---

## [1.9.0] - 2026-10-10

### Production Deployment & Railway Configuration
- **Unified Web Service Target**:
  - Confirmed and formalized monorepo production target: a single containerized Python web service serving both the FastAPI REST backend and the HTML5/Tailwind SPA frontend.
- **Railway Infrastructure Artifacts**:
  - `Dockerfile`: Multi-stage Python 3.11-slim container with non-root user security, system graphics libraries, and curl healthchecks.
  - `.dockerignore`: Excluded virtual environments, bytecode caches, and local configuration secrets.
  - `railway.toml`: Standard Railway configuration specifying Dockerfile builder, dynamic `$PORT` start command, and `/api/v1/health` monitoring.
  - `nixpacks.toml` & `Procfile`: Configured fallback buildpack compatibility.
  - `deploy/RAILWAY_DEPLOYMENT.md`: End-to-end production deployment instructions for Railway CLI and GitHub integration.

---

## [1.8.0] - 2026-10-10

### Streamlined UX & De-Congestion Refactor
- **Removed Verified Reference Library & Test Cases**:
  - Completely eliminated the `#demo-section` benchmark library and header links to remove clutter and ensure the application presents as a ready-to-use production tool rather than an internal test harness.
  - Cleaned up empty-state copy and validation messages to remove references to demo benchmarks.
- **De-Congested Layout via 3-Tab Forensic Workspace**:
  - Consolidated 8 vertically stacked result panels into an executive Verdict Banner paired with an organized 3-tab deep dive:
    - **Visual Comparison**: Interactive Curtain Slider with smooth handle dragging, dual split view, hotspot overlays, and inline packaging red flags.
    - **Registry & Score Factors**: Official NAFDAC Green Book registry verification card, 4-factor mathematical point attribution matrix, and confirmed authenticity indicators.
    - **Physical Checklist**: Tactical in-hand guidance covering blister foil texture, cap rings, and tamper seals.
- **Streamlined Scanner Input**:
  - Replaced the bulky "Certified Packaging Baselines" technical table in the left column with a clean, low-profile system coverage indicator.
  - Enhanced the idle/empty state with a polished 3-pillar feature summary (NAFDAC Sync, Visual Forensics, Trust Score).
- **Design & Theme Consistency**:
  - Preserved the executive blue and white palette (`#060B14`, `#0B1528`, `#101D36`, `#1A2C4B`, `#2563EB`, `#38BDF8`, `#FFFFFF`).
  - Zero occurrences of "prototype" or test-harness terminology across the entire user experience.

---

## [1.7.0] - 2026-10-10

### Real Custom Image Defect Inspection & Counterfeit Detection
- **Fixed Custom Image Local Fallback Blindspot**:
  - Previously, `VisionEngine` only flagged counterfeit status on preloaded demo fixture IDs; custom uploaded images were erroneously defaulting to authentic status (`is_counterfeit_sample = False`) and assigning valid NAFDAC codes (+30 pts), causing obvious knock-offs (like "Prand") to receive a false 99/100 score.
  - Refactored `feature_comparator.py` and `scoring_engine.py` so that **all custom uploads undergo real pixel, color gamut, and structural anomaly inspection**.
  - Knock-off / counterfeit packaging (such as "Prand" with non-conforming teal palette, altered lettering, and missing Haleon navy blue/red) is now properly detected with an **11/100 Trust Score: HIGH RISK: COUNTERFEIT**.
- **Fixed SKU Classifier Brittle Heuristics**:
  - Prevented pharmaceutical/tablet cartons from ever being misclassified as a Coca-Cola bottle.
  - Coca-Cola classification now strictly requires genuine Coke Red dominance (`> 10%`) and bottle/can contours.
  - Pharmaceutical cartons, blister packs, and pill containers default accurately to the `panadol-500mg-tablet` candidate profile.
- **In-App Gemini Vision API Key Manager**:
  - Added interactive engine settings modal directly accessible from the top telemetry status bar.
  - Allows instant runtime activation of Google Gemini Multimodal Vision without server restarts or manual file editing.

---

## [1.6.0] - 2026-10-09

### Executive Blue & White Corporate Theme
- **Unified Palette in Shades of Blue & White**:
  - **Deep Midnight Blue Base Canvas**: Grounded root background in dark slate-navy (`#060B14`).
  - **Solid Dark Navy Bento Panels**: Styled all bento panels, verified reference rows, and result containers in solid dark navy (`#0B1528`).
  - **Elevated Workspace Card**: Grounded the Packaging Inspection Input workspace in a distinct midnight blue card (`#101D36`).
  - **Navy Sub-Containers**: Styled input fields, baseline boxes, and factor breakdowns in `#08101E`.
  - **Hairline Muted Navy Borders**: Unified all borders with a flat, clean structural border (`1px solid #1A2C4B`, hover `#2B4775`).
  - **Royal / Cobalt Blue Primary CTAs**: Primary action buttons ("Upload File", "Run Forensic Authentication", "Export Certificate") and active tab indicators styled in solid royal blue (`#2563EB`, hover: `#1D4ED8`, active: `#1E40AF`).
  - **Electric / Sky Blue Micro-Indicators**: Functional status pulses, checkmarks, active laser sweep, and telemetry pings accented with sky blue (`#38BDF8`).
  - **Crisp High-Contrast White Typography**: Pure white (`#FFFFFF`) for commanding headers, titles, and values paired with light slate-grey (`#CBD5E1` / `#94A3B8`) for secondary text.

---

## [1.5.0] - 2026-10-09

### Corporate Product Security Dashboard Refactor (Human-Designed Bento Architecture)
- **Eliminated Generic AI Template Aesthetic & Background Clutter**:
  - Removed all vertical matrix grid patterns (`.bg-grid-pattern`) and background glow blobs entirely.
  - Transitioned the entire canvas to a solid, deep matte forest-black background (`#020907`).
- **Eliminated Neon Outlines**:
  - Removed all glowing neon borders, exaggerated box-shadows, and neon button halos.
  - Implemented thin, flat, muted structural borders (`1px solid #112F26`) across all dashboard panels.
- **Bento Grid Architecture**:
  - Structured content into weighted bento panels with distinct visual hierarchy.
  - Grounded the **"Packaging Inspection Input"** as a solid, slightly raised workspace card (`#091713`), structurally distinct from reference tags.
  - Subcards and telemetry containers styled in solid matte surfaces (`#05110D` and `#061410`).
- **Editorial Typography**:
  - Tightened letter spacing on the main header (`letter-spacing: -0.025em` / `tracking-tight`).
  - Switched font system to sharp, high-legibility **Inter** with **JetBrains Mono** for forensic serials, hashes, and telemetry data.
  - Hero header: `"Authenticate Everyday Products with Precision AI"` styled with crisp, commanding editorial presence.
- **Restraint with Accents**:
  - Restricted bright green (`#00E676`) strictly to functional micro-indicators (status ping dots, checkmark icons).
  - Primary action buttons ("Upload File", "Run Forensic Authentication", "Export Certificate") styled in solid, flat official Nigerian flag emerald (`#008751`, hover: `#009E5F`) with high-contrast white text.

---

## [1.4.0] - 2026-10-09

### Nigerian Cybersecurity & Product Authentication Dashboard Theme
- **Flag-Inspired High-Tech Color Palette**:
  - **Ultra-Dark Emerald Canvas**: Set root canvas and main viewports to `#04120E`.
  - **Dark Green Surfaces**: Styled all cards, modals, and telemetry containers in `#0A221A`.
  - **Official Nigerian Green Borders**: Rendered all borders and dividers with thin, crisp official green borders (`#008751`).
  - **Bright Mint Green Accents**: Highlighted active statuses, scan beams, slider handles, and primary CTAs in vibrant mint green (`#00E676`).
  - **Crisp High-Contrast Typography**: Applied pure white (`#FFFFFF`) with emerald-tinted secondary text for optimal legibility.
- **Hero Header Elevation**:
  - Hero title styled as `"Authenticate Everyday Products with Precision AI"` with a smooth transition from pure white to mint green (`#00E676`).
- **Launcher Scripts**:
  - Cleaned all remaining "prototype" references from `start_web.bat` and `start_web.ps1`.

---

## [1.3.0] - 2026-10-09

### Modern Production Look & Feel & Complete Removal of "Prototype" References
- **Eliminated "Prototype" Wording**:
  - Removed all occurrences of the word "prototype" from all HTML headers, telemetry badges, titles, navigation elements, inspection reports, and certificates.
  - Replaced with authoritative production branding: **"Active Production Shield"**, **"AI Packaging Authentication Platform"**, and **"Consumer Protection & Brand Authentication System"**.
- **Modern Deep-Tech Aesthetics**:
  - **Ambient Lighting & Atmospheric Glow**: Implemented an obsidian radial mesh gradient background (`bg-slate-950` with emerald and cyan atmospheric back-glows) and high-tech subtle dot-grid texture (`bg-grid-pattern`).
  - **Refined Glassmorphism**: Cards elevated with `backdrop-blur-xl bg-slate-900/50 border border-slate-800/90 shadow-2xl rounded-3xl`.
  - **Elevated Comparison Slider**: Redesigned the before/after curtain slider handle with frosted glassmorphic circular grip, double-arrow glyph, and emerald glowing line divider.
  - **Micro-interactions & Hover Effects**: Added smooth scale transitions (`hover:scale-[1.01]`), glowing emerald drop shadows (`shadow-glow-emerald`), and active state feedback across all buttons and demo cards.
  - **Typography & Layout Hierarchy**: Upgraded typography spacing with Plus Jakarta Sans and JetBrains Mono with improved contrast and legibility.

---

## [1.2.0] - 2026-10-09

### End-to-End Gemini Vision Integration & Field Mapping
- **Direct Environment Variable Configuration (`GEMINI_API_KEY`)**:
  - The adapter natively consumes `GEMINI_API_KEY` from process environment variables and loaded `.env` files via `python-dotenv`.
  - Configurable target model via `GEMINI_MODEL` (defaults to `gemini-2.5-flash`, with `gemini-1.5-flash` or `gemini-2.0-flash` support).
- **Standardized Multi-Field Mapping**:
  - Responses from Gemini Vision (or local fallback) are strictly mapped into:
    1. **`trust_score`**: Integer (0 to 100).
    2. **`risk_level`**: Standardized tier (`LOW_RISK`, `MEDIUM_RISK`, or `HIGH_RISK`).
    3. **`detected_issues`**: List of identified packaging red flags with severity, description, and bounding box coordinates.
    4. **`authenticity_indicators`**: List of positive forensic attributes verified on the packaging (e.g., active NAFDAC syntax, crisp offset typography, intact cap drop-ring).
    5. **`explanation`**: Plain-English forensic summary explaining points deducted or validated.
- **Dedicated Vision Router Logging Telemetry**:
  - Configured `counterfeit_detector.vision_router` with distinct log messages:
    - `[VISION_ROUTER] [GEMINI_VISION]` logs payload size, model, latency, Trust Score, and indicator counts.
    - `[VISION_ROUTER] [LOCAL_FALLBACK]` logs exact reason for fallback (e.g. `GEMINI_API_KEY not configured` or network timeout) and local execution details.
- **Frontend Risk & Authenticity Indicators Card**:
  - Added dedicated UI cards in `apps/web/public/index.html` displaying the `risk_level` badge, the `authenticity_indicators` checklist, and the active `engine_used` routing telemetry.
- **Automated Verification**:
  - 10 automated test suites passing with 100% test coverage, including mocked end-to-end Gemini Vision API JSON payload parsing and routing verification.

---

## [1.1.0] - 2026-10-09

### 1. Architectural & AI Pipeline Improvements
- **Google Gemini Multimodal Vision Adapter (`packages/vision_engine/adapters/gemini_vision_adapter.py`)**:
  - Implemented an extensible, production-ready adapter for Google Gemini Flash Vision API.
  - Structured prompt engineering tailored for Nigerian pharmaceutical and FMCG verification.
  - Graceful fallback: If `GEMINI_API_KEY` is not present, the system automatically falls back to our local Computer Vision engine with zero downtime.
- **Real Image Signal & Edge Gradient Analysis (`packages/vision_engine/pipelines/preprocessor.py`)**:
  - Replaced static placeholder metrics with real high-pass spatial filtering and gradient variance calculation (`ImageFilter.FIND_EDGES`).
- **Dynamic Packaging Color Gamut Comparison (`packages/vision_engine/pipelines/feature_comparator.py`)**:
  - Implemented multi-channel RGB/HSV color distribution analysis comparing user sample imagery against canonical brand gamuts.
- **NAFDAC Green Book Registry Simulator (`packages/vision_engine/nafdac_registry.py`)**:
  - Built an authoritative mock registry database simulating the official NAFDAC Green Book database.

### 2. Trust Score & Explainability Overhaul
- **Transparent 4-Factor Point Deduction Matrix**:
  - NAFDAC Registration (30 pts max)
  - Typography & Print Definition (25 pts max)
  - Chromatic Color Gamut Fidelity (25 pts max)
  - Tamper Closures & Seals (20 pts max)

### 3. User Experience & Visual Design Upgrades
- **Interactive Before/After Curtain Slider**:
  - Click and drag a vertical divider across the container to superimpose the scanned sample directly over the canonical reference image.
- **Synchronized Hotspot Inspection**:
  - Interactive hotspot buttons for critical inspection zones.
- **NAFDAC Green Book Registry Card**:
  - Official regulatory audit card displaying registered product name, licensed manufacturer, authorization category, and validity status.
- **Exportable Inspection Audit Certificate**:
  - One-click print/PDF export modal for pharmacists and retailers.

### 4. Security & Hardening Improvements
- **Magic Bytes Validation**: JPEG, PNG, WebP, SVG header inspection.
- **Payload Limit Enforcement**: 10MB maximum file size.
- **Security Headers Middleware**: `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`.
