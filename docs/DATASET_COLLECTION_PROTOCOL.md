# Dataset Collection & Calibration Protocol (Nigeria V1 Pilot)

To train and calibrate the Version 1 Computer Vision pipeline, the startup team must curate a rigorous ground-truth dataset for **Panadol**, **Coca-Cola**, and **Colgate**.

---

## 1. Physical Sample Sourcing Strategy

| Product | Authentic Source (Golden Samples) | Suspect / Counterfeit Source Candidates |
|---|---|---|
| **Panadol 500mg** | Accredited Tier-1 Retail Pharmacy chains (e.g., Medplus, HealthPlus, Nett Pharmacy) with official GSK/Haleon distributor invoices. | Unregulated open-market medicine dealers, kiosk vendors, and roadside chemists in commercial hubs (e.g., Idumota Market, Lagos; Onitsha Bridgehead, Anambra). |
| **Coca-Cola 50cl PET** | Direct Nigerian Bottling Company (NBC) distributor depots, major retail chains (Shoprite, Spar, Justrite). | Independent roadside hawkers, open-air motor parks (e.g., Oshodi, Ojota, Nyanya), unbranded street kiosks. |
| **Colgate Cavity 140g** | Formal supermarket distribution channels with direct importer/Tura International documentation. | Wholesale open markets (Trade Fair Complex, Balogun Market) and secondary discount beauty stalls. |

---

## 2. Standardized Photography Capture Protocol

For each acquired SKU, capture **minimum 15–20 high-resolution images** across varying conditions to mimic the diversity of user smartphone hardware in Nigeria:

### Angles & Features to Capture:
1. **Front Face (Hero View):** Full frontal packaging, centered, showing brand logo and primary claims.
2. **Back / Regulatory Panel:** Close-up of NAFDAC Reg. No., batch number, manufacture/expiry dates, barcode, and manufacturer address.
3. **Tamper Seals & Closures:**
   - *Panadol:* Blister foil cross-hatch pattern, tamper-evident carton glue flap.
   - *Coca-Cola:* Bottle neck profile showing tamper-evident ring and laser-etched dot matrix code.
   - *Colgate:* Tube crimp seal (front & back), outer carton metallic embossed foil reflection.

### Lighting & Hardware Variations:
- **Studio Neutral:** Clean white background under balanced 5000K diffuse lighting (baseline ground truth).
- **Fluorescent / Kiosk Lighting:** Overhead dim fluorescent tube lighting (mimicking typical Lagos chemist / kiosk interiors).
- **Direct Sunlight / Glare:** Outdoor market environment with natural harsh sunlight and shadow cast.
- **Hardware Diversity:** Photos must be taken using a mix of:
  - Budget Android phones (e.g., Tecno Spark, Infinix Hot, Itel) — testing real sensor noise and low dynamic range.
  - Mid-range / High-end phones (e.g., Samsung Galaxy A-series, iPhone).

---

## 3. Image Annotation & Folder Organization

Save collected assets into `packages/vision-engine/dataset/<product_slug>/`:

```
dataset/
├── panadol/
│   ├── authentic/
│   │   ├── panadol_auth_001_front.jpg
│   │   ├── panadol_auth_001_seal.jpg
│   │   └── panadol_auth_001_nafdac.jpg
│   └── suspect/
│       ├── panadol_fake_001_front.jpg
│       └── panadol_fake_001_nafdac.jpg
├── coca_cola/
│   ├── authentic/
│   └── suspect/
└── colgate/
    ├── authentic/
    └── suspect/
```

Each image should be paired with metadata in a companion `annotations.json` file logging:
- Purchase location (State, Market/Store name)
- Price paid (abnormally cheap prices often correlate with counterfeit batches)
- Physical anomalies observed during manual inspection
