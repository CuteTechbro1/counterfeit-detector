-- ==============================================================================
-- COUNTERFEIT DETECTOR DATABASE SCHEMA & INITIAL SEED (V1 PILOT)
-- Targets: Panadol, Coca-Cola, Colgate
-- Supported on PostgreSQL 16 + pgvector
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 1. Master Products Table
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug VARCHAR(64) UNIQUE NOT NULL,
    brand_name VARCHAR(100) NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    manufacturer VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'pharmaceutical', 'beverage', 'oral_care'
    standard_nafdac_no VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Authentic Reference Images & Embeddings
CREATE TABLE IF NOT EXISTS authentic_reference_images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    view_angle VARCHAR(30) NOT NULL, -- 'front', 'back', 'cap_seal', 'blister_foil', 'batch_stamp'
    image_url TEXT NOT NULL,
    thumbnail_url TEXT NOT NULL,
    feature_embedding vector(512), -- Deep metric embedding vector
    packaging_version VARCHAR(20) DEFAULT 'v1',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. SKU-Specific Verification Checkpoints
CREATE TABLE IF NOT EXISTS verification_checkpoints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    checkpoint_key VARCHAR(50) NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    weight_percentage INT NOT NULL CHECK (weight_percentage BETWEEN 1 AND 100),
    rule_type VARCHAR(30) NOT NULL, -- 'ocr_regex', 'visual_similarity', 'edge_detection'
    expected_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. User Scan Ingestion Log
CREATE TABLE IF NOT EXISTS scan_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id VARCHAR(100),
    uploaded_image_url TEXT NOT NULL,
    detected_product_id UUID REFERENCES products(id),
    network_carrier VARCHAR(50),
    client_ip_hash VARCHAR(64),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Scan Results & Trust Scores
CREATE TABLE IF NOT EXISTS scan_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scan_session_id UUID UNIQUE NOT NULL REFERENCES scan_sessions(id) ON DELETE CASCADE,
    trust_score INT NOT NULL CHECK (trust_score BETWEEN 0 AND 100),
    confidence_level VARCHAR(20) NOT NULL, -- 'HIGH_AUTHENTIC', 'CAUTION', 'HIGH_RISK'
    processing_time_ms INT NOT NULL,
    detected_nafdac_text VARCHAR(100),
    nafdac_match_status BOOLEAN DEFAULT FALSE,
    explanation_summary TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Granular Discrepancies
CREATE TABLE IF NOT EXISTS scan_discrepancies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scan_result_id UUID NOT NULL REFERENCES scan_results(id) ON DELETE CASCADE,
    checkpoint_id UUID REFERENCES verification_checkpoints(id),
    severity VARCHAR(20) NOT NULL, -- 'CRITICAL', 'WARNING', 'INFORMATIONAL'
    issue_description TEXT NOT NULL,
    region_box JSONB, -- [ymin, xmin, ymax, xmax]
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. User Reports & Ground Truth Feedback
CREATE TABLE IF NOT EXISTS user_feedback_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scan_session_id UUID NOT NULL REFERENCES scan_sessions(id),
    user_verdict VARCHAR(30) NOT NULL, -- 'CONFIRMED_FAKE', 'CONFIRMED_GENUINE', 'FALSE_ALARM'
    notes TEXT,
    purchased_location_state VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_products_slug ON products(slug);
CREATE INDEX IF NOT EXISTS idx_scan_sessions_created ON scan_sessions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_scan_results_score ON scan_results(trust_score);

-- ==============================================================================
-- SEED DATA: 3 PILOT PRODUCTS & VERIFICATION CHECKPOINTS
-- ==============================================================================

-- Insert Panadol
INSERT INTO products (id, slug, brand_name, product_name, manufacturer, category, standard_nafdac_no)
VALUES (
    'a1000000-0000-0000-0000-000000000001',
    'panadol-500mg-tablet',
    'Panadol',
    'Panadol Paracetamol 500mg (10x10 Tablets)',
    'GlaxoSmithKline Consumer Nigeria PLC / Haleon',
    'pharmaceutical',
    '04-0244'
) ON CONFLICT (slug) DO NOTHING;

-- Insert Coca-Cola
INSERT INTO products (id, slug, brand_name, product_name, manufacturer, category, standard_nafdac_no)
VALUES (
    'b2000000-0000-0000-0000-000000000002',
    'coca-cola-50cl-pet',
    'Coca-Cola',
    'Coca-Cola Original Taste 50cl PET Bottle',
    'Nigerian Bottling Company Ltd (NBC)',
    'beverage',
    '01-0138'
) ON CONFLICT (slug) DO NOTHING;

-- Insert Colgate
INSERT INTO products (id, slug, brand_name, product_name, manufacturer, category, standard_nafdac_no)
VALUES (
    'c3000000-0000-0000-0000-000000000003',
    'colgate-maximum-cavity-140g',
    'Colgate',
    'Colgate Maximum Cavity Protection Great Regular Flavor 140g',
    'Colgate-Palmolive (Tura International Ltd / Imported)',
    'oral_care',
    '02-4019'
) ON CONFLICT (slug) DO NOTHING;

-- Checkpoints for Panadol
INSERT INTO verification_checkpoints (product_id, checkpoint_key, title, description, weight_percentage, rule_type, expected_value)
VALUES
('a1000000-0000-0000-0000-000000000001', 'nafdac_reg_pattern', 'NAFDAC Registration Number Format', 'Must match official registered syntax 04-0244 or B4-0244', 30, 'ocr_regex', '04-0244'),
('a1000000-0000-0000-0000-000000000001', 'brand_logo_fidelity', 'Panadol Logo & Color Gamut', 'Checks Haleon red/navy gradient, drop-shadow sharpness and kerning', 35, 'visual_similarity', 'panadol_primary_logo'),
('a1000000-0000-0000-0000-000000000001', 'blister_foil_pattern', 'Blister Pack Grid & Debossed Expiry', 'Checks cross-hatch aluminum pattern and stamped batch/expiry date', 35, 'visual_similarity', 'panadol_foil_stamp');

-- Checkpoints for Coca-Cola
INSERT INTO verification_checkpoints (product_id, checkpoint_key, title, description, weight_percentage, rule_type, expected_value)
VALUES
('b2000000-0000-0000-0000-000000000002', 'cap_tamper_ring', 'Drop-Ring Tamper Seal', 'Ensures the plastic safety ring is unbroken and securely seated', 30, 'visual_similarity', 'coke_cap_seal'),
('b2000000-0000-0000-0000-000000000002', 'laser_batch_etching', 'Neck Laser Etched Batch Code', 'Verifies presence of laser dot-matrix batch and expiry string on bottle neck', 35, 'ocr_regex', '^(B|L)[0-9]{6,10}'),
('b2000000-0000-0000-0000-000000000002', 'label_curvature_gamut', 'Coca-Cola Dynamic Ribbon Fidelity', 'Checks iconic script font, red saturation, and ribbon curvature', 35, 'visual_similarity', 'coke_label_contour');

-- Checkpoints for Colgate
INSERT INTO verification_checkpoints (product_id, checkpoint_key, title, description, weight_percentage, rule_type, expected_value)
VALUES
('c3000000-0000-0000-0000-000000000003', 'carton_metallic_emboss', 'Holographic / Metallic Logo Reflection', 'Inspects metallic sheen and tactile embossing border on the outer carton', 35, 'visual_similarity', 'colgate_emboss_zone'),
('c3000000-0000-0000-0000-000000000003', 'tube_crimp_stamp', 'Tube Crimp Batch Code & Color Mark', 'Authentic tubes have debossed lot numbers and precise rectangular eye-marks at crimp', 35, 'visual_similarity', 'colgate_crimp_edge'),
('c3000000-0000-0000-0000-000000000003', 'nafdac_reg_pattern', 'NAFDAC Registration Verification', 'Validates NAFDAC format on outer carton panel', 30, 'ocr_regex', '02-4019');
