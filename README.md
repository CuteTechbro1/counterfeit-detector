# Counterfeit Detector 🇳🇬 (Competition Web Prototype)

An AI and Computer Vision-powered web verification platform designed to help Nigerian consumers, community pharmacies, and retailers detect counterfeit medicines, beverages, and FMCG consumer products.

---

## 🎯 Version 1 Pilot Scope (3 Target Products)
1. **Panadol (500mg Tablets)** — GlaxoSmithKline / Haleon (Analgesic) • NAFDAC: `04-0244`
2. **Coca-Cola (50cl PET Bottle)** — Nigerian Bottling Company / The Coca-Cola Company • NAFDAC: `01-0138`
3. **Colgate (Maximum Cavity Protection 140g)** — Colgate-Palmolive • NAFDAC: `02-4019`

---

## ⚡ Quick Launch (Live Web Prototype)

### 1. Launch Server & Web Application
Double-click `start_web.bat` (or run in PowerShell):
```powershell
.\start_web.ps1
```
Open **[http://localhost:8000](http://localhost:8000)** in any modern web browser.

Interactive Swagger API docs are available at **[http://localhost:8000/docs](http://localhost:8000/docs)**.

---

## 🔬 Core Focus Architecture

```
counterfeit-detector/
├── apps/
│   └── web/                   # High-polish competition web dashboard
│       └── public/
│           ├── index.html     # Interactive scanner, webcam mode & side-by-side inspection
│           └── assets/        # Canonical golden references & preloaded test fixtures
│
├── services/
│   └── api/                   # FastAPI backend service
│       ├── app/
│       │   ├── api/v1/        # Endpoints: /scans/analyze, /products, /demo-samples
│       │   ├── schemas/       # Pydantic validation schemas
│       │   └── main.py        # Static web mount + REST router
│       └── tests/             # Automated test suite (test_scans.py)
│
└── packages/
    └── vision_engine/         # Modular Computer Vision inference core
        ├── reference_catalog.py # Golden specifications & physical inspection tips
        └── pipelines/
            ├── preprocessor.py  # Image resolution, luminance, blur & glare analysis
            ├── classifier.py    # SKU identification from color/aspect signatures
            ├── ocr_inspector.py # NAFDAC regex and batch stamp verification
            ├── feature_comparator.py # Packaging anomaly and tamper seal detection
            └── scoring_engine.py    # Deterministic Trust Score (0-100) & explanation
```

---

## 🧪 Testing the Prototype (For Competition Judges)
The web interface features an **Interactive Competition Demo Cases** bar with 6 preloaded samples:
- 🟢 **Authentic Panadol 500mg** (Trust Score: ~96%, Valid NAFDAC 04-0244, Intact Seal)
- 🔴 **Counterfeit Panadol 500mg** (Trust Score: ~38%, Altered NAFDAC 04-9988, Blurred Typography)
- 🟢 **Authentic Coca-Cola 50cl** (Trust Score: ~94%, Intact Cap Drop-Ring, Laser Neck Code)
- 🔴 **Counterfeit / Refilled Coca-Cola** (Trust Score: ~42%, Broken Tamper Ring, Missing Code)
- 🟢 **Authentic Colgate 140g** (Trust Score: ~95%, Metallic Foil Sheen, Debossed Crimp)
- 🔴 **Counterfeit Colgate 140g** (Trust Score: ~45%, Dull Paperboard, Smooth Crimp)

Users can also:
1. **Drag and drop** or upload custom packaging photos.
2. Click **Webcam** to test live real-time packaging inspection.
3. Toggle **Defect Markers** to view visual bounding boxes over suspected packaging anomalies.
4. Review product-specific **"Things to Look Out For"** recommendations.

---

## 🧪 Running Automated Tests
```powershell
cd services\api
$env:PYTHONPATH = ".;..\..\packages"
.venv\Scripts\python -m pytest -v tests/test_scans.py
```
All 9 core pipeline tests pass with 100% verification coverage.
