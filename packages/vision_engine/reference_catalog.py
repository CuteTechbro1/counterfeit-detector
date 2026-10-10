"""
Canonical Reference Catalog & Demo Samples for V1 Pilot
Supported SKUs: Panadol (500mg), Coca-Cola (50cl PET), Colgate (140g)
"""

from typing import Dict, Any, List

PRODUCTS_CATALOG: Dict[str, Dict[str, Any]] = {
    "panadol-500mg-tablet": {
        "id": "a1000000-0000-0000-0000-000000000001",
        "slug": "panadol-500mg-tablet",
        "brand_name": "Panadol",
        "product_name": "Panadol Paracetamol 500mg (10x10 Tablets)",
        "manufacturer": "GlaxoSmithKline Consumer Nigeria PLC / Haleon",
        "category": "pharmaceutical",
        "standard_nafdac_no": "04-0244",
        "reference_image": "/assets/references/panadol_reference.svg",
        "key_features": [
            "Deep Navy & GlaxoSmithKline / Haleon Red branding",
            "Cross-hatch aluminum blister foil debossing",
            "NAFDAC Reg No. 04-0244 on side flap",
            "Tamper-evident carton seal flap"
        ],
        "things_to_look_out_for": [
            {
                "title": "Blister Foil Grid & Debossed Expiry",
                "detail": "Inspect the silver aluminum foil on the back of the blister pack. Authentic Panadol features a sharp, diagonal cross-hatch pattern with cleanly debossed batch and expiry stamps.",
                "importance": "CRITICAL"
            },
            {
                "title": "NAFDAC Registration Number Syntax",
                "detail": "Verify that 'NAFDAC Reg. No. 04-0244' (or 'B4-0244') is printed cleanly on the carton side panel. Counterfeits often exhibit blurry numerals, missing hyphens, or fake prefixes.",
                "importance": "CRITICAL"
            },
            {
                "title": "Haleon / GSK Hologram & Packaging Finish",
                "detail": "Tilt the carton under light. Authentic packaging has a smooth, semi-gloss sheen and a light-shifting security seal on the flap that tears paper fibers when peeled.",
                "importance": "HIGH"
            },
            {
                "title": "Tablet Color & Compression",
                "detail": "Panadol tablets are chalk-white, uniformly compressed with 'PANADOL' debossed on one face without chipping, powdery residue, or mottled discoloration.",
                "importance": "MEDIUM"
            }
        ],
        "checkpoints": [
            {
                "key": "nafdac_reg_pattern",
                "title": "NAFDAC Registration Number Check",
                "expected": "04-0244",
                "weight": 30,
                "type": "ocr_regex"
            },
            {
                "key": "brand_logo_fidelity",
                "title": "Panadol Typography & Color Gamut",
                "expected": "Haleon Navy/Red Gradient (#001E62 & #E31837)",
                "weight": 35,
                "type": "visual_similarity"
            },
            {
                "key": "blister_foil_pattern",
                "title": "Tamper Seal & Foil Integrity",
                "expected": "Cross-hatch debossed grid with lot stamp",
                "weight": 35,
                "type": "visual_similarity"
            }
        ]
    },
    "coca-cola-50cl-pet": {
        "id": "b2000000-0000-0000-0000-000000000002",
        "slug": "coca-cola-50cl-pet",
        "brand_name": "Coca-Cola",
        "product_name": "Coca-Cola Original Taste 50cl PET Bottle",
        "manufacturer": "Nigerian Bottling Company Ltd (NBC)",
        "category": "beverage",
        "standard_nafdac_no": "01-0138",
        "reference_image": "/assets/references/coca_cola_reference.svg",
        "key_features": [
            "Coca-Cola Red (#F40009) dynamic contour ribbon",
            "Screw cap drop-ring tamper-evident seal",
            "Laser-etched dot matrix batch code on bottle neck",
            "NAFDAC Reg No. 01-0138"
        ],
        "things_to_look_out_for": [
            {
                "title": "Cap Drop-Ring Tamper Seal",
                "detail": "Check the plastic ring under the screw cap. The ring must be tightly seated and connected by thin plastic bridges that cleanly snap open with audible resistance upon first turn.",
                "importance": "CRITICAL"
            },
            {
                "title": "Laser-Etched Neck Code",
                "detail": "Authentic NBC 50cl bottles have a two-line dot-matrix laser etching directly on the PET shoulder showing date, production time, and factory line code (e.g. 'B24 10:45 EXP 12/26'). Counterfeits either completely omit this or use easily wiped ink.",
                "importance": "CRITICAL"
            },
            {
                "title": "Label Adhesion & Dynamic Ribbon",
                "detail": "Look at the red wrap-around label. Genuine labels use precision hot-melt adhesive with zero glue seepage or bubbling, and the iconic white Spencerian script is crisp without color bleed.",
                "importance": "HIGH"
            },
            {
                "title": "Uniform Fill Line",
                "detail": "In automated NBC bottling lines, fill heights are uniform to within 2mm. Noticeably under-filled or over-filled bottles in a crate indicate manual street refilling.",
                "importance": "MEDIUM"
            }
        ],
        "checkpoints": [
            {
                "key": "cap_tamper_ring",
                "title": "Drop-Ring Tamper Seal Integrity",
                "expected": "Intact 28mm PCO closure with unbroken bridges",
                "weight": 35,
                "type": "visual_similarity"
            },
            {
                "key": "laser_batch_etching",
                "title": "Laser Dot-Matrix Neck Batch Stamp",
                "expected": "Laser dot matrix on PET shoulder",
                "weight": 35,
                "type": "ocr_regex"
            },
            {
                "key": "label_curvature_gamut",
                "title": "Dynamic Ribbon & Red Gamut Saturation",
                "expected": "Coca-Cola Signature Red (#F40009) & Crisp Script",
                "weight": 30,
                "type": "visual_similarity"
            }
        ]
    },
    "colgate-maximum-cavity-140g": {
        "id": "c3000000-0000-0000-0000-000000000003",
        "slug": "colgate-maximum-cavity-140g",
        "brand_name": "Colgate",
        "product_name": "Colgate Maximum Cavity Protection 140g",
        "manufacturer": "Colgate-Palmolive (Tura International Ltd / Imported)",
        "category": "oral_care",
        "standard_nafdac_no": "02-4019",
        "reference_image": "/assets/references/colgate_reference.svg",
        "key_features": [
            "Metallic foil sheen on red/white shield logo",
            "Debossed lot code on bottom tube crimp",
            "Printed rectangular eye-mark square at crimp center",
            "NAFDAC Reg No. 02-4019"
        ],
        "things_to_look_out_for": [
            {
                "title": "Tube Crimp Lot Stamp & Eye-Mark",
                "detail": "Examine the sealed bottom crimp of the inner tube. Authentic Colgate tubes feature a debossed expiration and lot number along with a centered, sharp rectangular color eye-mark.",
                "importance": "CRITICAL"
            },
            {
                "title": "Metallic Reflective Carton Sheen",
                "detail": "The red Colgate logo and tooth shield on the outer carton are printed on reflective foil-laminated board. Counterfeit boxes use plain white paperboard with flat, dull red ink.",
                "importance": "HIGH"
            },
            {
                "title": "NAFDAC Registration & Distributor Info",
                "detail": "Check the back and side panels for 'NAFDAC Reg. No. 02-4019' and official Nigerian distribution info (Tura International Ltd or authorized importer).",
                "importance": "HIGH"
            },
            {
                "title": "Paste Texture & Fragrance",
                "detail": "Authentic Colgate paste is homogeneous, firm, with a clean wintergreen/peppermint fragrance, and does not exhibit liquid separation or gritty granules.",
                "importance": "MEDIUM"
            }
        ],
        "checkpoints": [
            {
                "key": "carton_metallic_emboss",
                "title": "Carton Metallic Sheen & Emboss",
                "expected": "Reflective foil-board laminate with crisp borders",
                "weight": 35,
                "type": "visual_similarity"
            },
            {
                "key": "tube_crimp_stamp",
                "title": "Tube Crimp Lot Stamp & Eye-Mark",
                "expected": "Debossed lot stamp with centered eye-mark",
                "weight": 35,
                "type": "visual_similarity"
            },
            {
                "key": "nafdac_reg_pattern",
                "title": "NAFDAC Registration Verification",
                "expected": "02-4019",
                "weight": 30,
                "type": "ocr_regex"
            }
        ]
    }
}

DEMO_SAMPLES: List[Dict[str, Any]] = [
    {
        "id": "sample-panadol-authentic",
        "product_slug": "panadol-500mg-tablet",
        "label": "Panadol 500mg (Authentic Sample)",
        "source": "Purchased from Medplus Pharmacy, Yaba, Lagos",
        "expected_trust_score": 96,
        "verdict": "AUTHENTIC",
        "image_url": "/assets/demo/panadol_authentic.svg",
        "description": "Crisp Haleon branding, verified NAFDAC Reg 04-0244, cross-hatch foil intact, tamper seal unbroken."
    },
    {
        "id": "sample-panadol-counterfeit",
        "product_slug": "panadol-500mg-tablet",
        "label": "Panadol 500mg (Counterfeit Sample)",
        "source": "Confiscated batch from open market kiosk, Idumota, Lagos",
        "expected_trust_score": 38,
        "verdict": "HIGH_RISK",
        "image_url": "/assets/demo/panadol_counterfeit.svg",
        "description": "Falsified NAFDAC number ('04-9988'), blurred logo kerning, flat aluminum foil lacking debossed lot pattern."
    },
    {
        "id": "sample-coke-authentic",
        "product_slug": "coca-cola-50cl-pet",
        "label": "Coca-Cola 50cl (Authentic Sample)",
        "source": "Direct NBC depot batch, Ikeja, Lagos",
        "expected_trust_score": 94,
        "verdict": "AUTHENTIC",
        "image_url": "/assets/demo/coke_authentic.svg",
        "description": "Intact cap tamper drop-ring, crisp laser-etched neck batch stamp, standard fill level, official NAFDAC 01-0138."
    },
    {
        "id": "sample-coke-counterfeit",
        "product_slug": "coca-cola-50cl-pet",
        "label": "Coca-Cola 50cl (Counterfeit / Refilled Sample)",
        "source": "Roadside vendor sample, Oshodi Motor Park, Lagos",
        "expected_trust_score": 42,
        "verdict": "HIGH_RISK",
        "image_url": "/assets/demo/coke_counterfeit.svg",
        "description": "Broken cap tamper-ring bridges, completely missing laser batch code on neck, uneven manual fill line."
    },
    {
        "id": "sample-colgate-authentic",
        "product_slug": "colgate-maximum-cavity-140g",
        "label": "Colgate Cavity 140g (Authentic Sample)",
        "source": "Supermarket retail stock, Victoria Island, Lagos",
        "expected_trust_score": 95,
        "verdict": "AUTHENTIC",
        "image_url": "/assets/demo/colgate_authentic.svg",
        "description": "Reflective metallic carton finish, debossed lot stamp on crimp, centered eye-mark, valid NAFDAC 02-4019."
    },
    {
        "id": "sample-colgate-counterfeit",
        "product_slug": "colgate-maximum-cavity-140g",
        "label": "Colgate Cavity 140g (Counterfeit Sample)",
        "source": "Wholesale discount stall, Trade Fair Complex, Lagos",
        "expected_trust_score": 45,
        "verdict": "HIGH_RISK",
        "image_url": "/assets/demo/colgate_counterfeit.svg",
        "description": "Dull paperboard carton with no metallic reflection, smooth crimp with no debossed lot stamp, smudged print."
    }
]
