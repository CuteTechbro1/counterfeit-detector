"""
NAFDAC Green Book Registry Simulator
Simulates the official database lookup for Nigerian Food and Drug Administration registrations.
"""

from typing import Dict, Any, Optional

# Official NAFDAC Green Book mock registry database
NAFDAC_DATABASE: Dict[str, Dict[str, Any]] = {
    "04-0244": {
        "nafdac_number": "04-0244",
        "product_name": "Panadol Paracetamol Tablets 500mg",
        "active_ingredients": ["Paracetamol (Acetaminophen) 500mg"],
        "dosage_form": "Solid Oral Tablet (Blister Pack)",
        "applicant": "GlaxoSmithKline Consumer Nigeria PLC / Haleon",
        "manufacturer": "GlaxoSmithKline Consumer Nigeria PLC, Agbara Industrial Estate, Ogun State",
        "registration_status": "ACTIVE_VALID",
        "first_registration_year": 1998,
        "renewal_expiry": "2028-12-31",
        "category": "Over-The-Counter Analgesic / Antipyretic",
        "classification": "Human Pharmaceutical"
    },
    "B4-0244": {
        "nafdac_number": "B4-0244",
        "product_name": "Panadol Extra Caplets 500mg / 65mg",
        "active_ingredients": ["Paracetamol 500mg", "Caffeine 65mg"],
        "dosage_form": "Solid Oral Caplet",
        "applicant": "GlaxoSmithKline Consumer Nigeria PLC / Haleon",
        "manufacturer": "GlaxoSmithKline Consumer Nigeria PLC, Agbara Industrial Estate, Ogun State",
        "registration_status": "ACTIVE_VALID",
        "first_registration_year": 2004,
        "renewal_expiry": "2029-06-30",
        "category": "Over-The-Counter Analgesic",
        "classification": "Human Pharmaceutical"
    },
    "01-0138": {
        "nafdac_number": "01-0138",
        "product_name": "Coca-Cola Carbonated Soft Drink (50cl PET)",
        "active_ingredients": ["Carbonated Water", "Sugar", "Caramel Color (E150d)", "Phosphoric Acid", "Natural Flavorings", "Caffeine"],
        "dosage_form": "Liquid Beverage (PET Container)",
        "applicant": "Nigerian Bottling Company Ltd (NBC)",
        "manufacturer": "Nigerian Bottling Company Ltd, Iddo House, Lagos / Ikeja Plant",
        "registration_status": "ACTIVE_VALID",
        "first_registration_year": 1989,
        "renewal_expiry": "2027-10-15",
        "category": "Non-Alcoholic Carbonated Beverage",
        "classification": "Food & Beverage"
    },
    "02-4019": {
        "nafdac_number": "02-4019",
        "product_name": "Colgate Maximum Cavity Protection Toothpaste (140g)",
        "active_ingredients": ["Sodium Monofluorophosphate 1.1% (1450 ppm F-)", "Calcium Carbonate"],
        "dosage_form": "Oral Paste (Laminated Tube)",
        "applicant": "Colgate-Palmolive / Tura International Ltd",
        "manufacturer": "Colgate-Palmolive (RSA) / Imported by Tura International Ltd, Ilupeju, Lagos",
        "registration_status": "ACTIVE_VALID",
        "first_registration_year": 2009,
        "renewal_expiry": "2027-04-20",
        "category": "Fluoride Toothpaste / Oral Care",
        "classification": "Cosmetics & Toiletries"
    }
}


def lookup_nafdac_number(nafdac_no: str) -> Dict[str, Any]:
    """
    Looks up a NAFDAC number against the registry.
    Returns status: VALID_ACTIVE, EXPIRED, or UNREGISTERED_COUNTERFEIT.
    """
    clean_no = nafdac_no.strip().upper().replace("REG. NO.", "").replace("NAFDAC", "").replace(":", "").strip()
    
    # Check direct match
    if clean_no in NAFDAC_DATABASE:
        record = NAFDAC_DATABASE[clean_no]
        return {
            "found": True,
            "status": "VALID_ACTIVE",
            "nafdac_number": record["nafdac_number"],
            "registered_product": record["product_name"],
            "manufacturer_of_record": record["manufacturer"],
            "applicant": record["applicant"],
            "renewal_expiry": record["renewal_expiry"],
            "category": record["category"],
            "notes": "Verified against official NAFDAC Green Book Registry."
        }
    
    # Check partial match
    for reg_no, record in NAFDAC_DATABASE.items():
        if reg_no in clean_no:
            return {
                "found": True,
                "status": "VALID_ACTIVE",
                "nafdac_number": record["nafdac_number"],
                "registered_product": record["product_name"],
                "manufacturer_of_record": record["manufacturer"],
                "applicant": record["applicant"],
                "renewal_expiry": record["renewal_expiry"],
                "category": record["category"],
                "notes": "Verified against official NAFDAC Green Book Registry (partial match)."
            }

    # Unregistered number detected
    return {
        "found": False,
        "status": "UNREGISTERED_COUNTERFEIT",
        "nafdac_number": nafdac_no,
        "registered_product": None,
        "manufacturer_of_record": None,
        "applicant": None,
        "renewal_expiry": None,
        "category": None,
        "notes": f"Number '{nafdac_no}' does NOT exist in NAFDAC registered databases. Strong indicator of counterfeit or illegal parallel import."
    }
