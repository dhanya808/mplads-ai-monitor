"""
MPLADS Dataset Generator
Generates realistic, representative MPLADS project and financial records across constituencies,
incorporating baseline sector distributions and synthetic anomalies for testing AI fraud detection.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_mplads_dataset(num_records=200, output_path=None):
    np.random.seed(42)

    # Core constituency and district mapping
    constituency_map = {
        "Uttar Pradesh": {
            "Varanasi": {
                "constituency": "Varanasi Parliamentary Constituency (PC-77)",
                "mp": "Hon. Rajeshwar Verma",
                "blocks": ["Rohania", "Sevapuri", "Arajiline", "Kashi Cantt", "Varanasi City", "Ramnagar"]
            },
            "Gorakhpur": {
                "constituency": "Gorakhpur Parliamentary Constituency (PC-64)",
                "mp": "Hon. Ravi Kishan Shukla",
                "blocks": ["Campierganj", "Pipraich", "Gorakhpur Urban", "Sahjanwa"]
            },
            "Kanpur": {
                "constituency": "Kanpur Parliamentary Constituency (PC-43)",
                "mp": "Hon. Ramesh Awasthi",
                "blocks": ["Kalyanpur", "Govind Nagar", "Sisamau", "Arya Nagar"]
            }
        },
        "Tamil Nadu": {
            "Salem": {
                "constituency": "Salem Parliamentary Constituency (PC-15)",
                "mp": "Hon. T. M. Selvaganapathi",
                "blocks": ["Ward 2", "Ward 13", "Omalur", "Attur", "Yercaud"]
            },
            "Coimbatore": {
                "constituency": "Coimbatore Parliamentary Constituency (PC-20)",
                "mp": "Hon. Ganapathi P. Rajkumar",
                "blocks": ["Ward 35", "Ward 7", "Ward 5", "Sulur", "Singanallur", "Pollachi"]
            }
        },
        "Maharashtra": {
            "Pune": {
                "constituency": "Pune Parliamentary Constituency (PC-34)",
                "mp": "Hon. Murlidhar Mohol",
                "blocks": ["Ward 17", "Ward 20", "Ward 24", "Ward 32", "Shivajinagar", "Kothrud"]
            },
            "Thane": {
                "constituency": "Thane Parliamentary Constituency (PC-25)",
                "mp": "Hon. Naresh Mhaske",
                "blocks": ["Ward 36", "Ward 11", "Kopri-Pachpakhadi", "Ovalamajiwada"]
            }
        },
        "Karnataka": {
            "Belagavi": {
                "constituency": "Belagavi Parliamentary Constituency (PC-02)",
                "mp": "Hon. Jagadish Shettar",
                "blocks": ["Ward 36", "Ward 38", "Ward 8", "Ward 6", "Gokak", "Bailhongal"]
            },
            "Hubballi": {
                "constituency": "Dharwad Parliamentary Constituency (PC-10)",
                "mp": "Hon. Pralhad Joshi",
                "blocks": ["Ward 6", "Ward 14", "Ward 3", "Navalgund", "Kundgol"]
            },
            "Bengaluru Urban": {
                "constituency": "Bengaluru South Parliamentary Constituency (PC-26)",
                "mp": "Hon. Tejasvi Surya",
                "blocks": ["Ward 30", "Jayanagar", "Basavanagudi", "Padmanabhanagar"]
            }
        }
    }

    sectors = [
        "Roads & Pathways",
        "Drinking Water Infrastructure",
        "Community Facilities",
        "Education & Schools",
        "Healthcare",
        "Energy & Solar"
    ]

    work_templates = {
        "Roads & Pathways": [
            "Road Construction work at {block} in {district}",
            "Construction of 2.4 km CC Road with RCC Drain & Solar Lighting at {block}",
            "Bituminous Road Resurfacing and Pedestrian Walkway at {block}",
            "Paver Block Road and Storm Water Drainage System in {block}"
        ],
        "Drinking Water Infrastructure": [
            "Drinking Water Borewell work at {block} in {district}",
            "Installation of 8 High-Capacity RO Water Purification Plants with Chillers at {block}",
            "Overhead Water Tank and Community Pipeline Distribution Network at {block}",
            "Deep Tubewell and Automated Solar Water Pumping System at {block}"
        ],
        "Community Facilities": [
            "Community Hall work at {block} in {district}",
            "Community Hall & Multi-Skill Youth Training Facility at {block}",
            "Public Crematorium Infrastructure & Waiting Pavilion at {block}",
            "Construction of Village Haat and Women SHG Craft Center at {block}"
        ],
        "Education & Schools": [
            "School Smart Classroom work at {block} in {district}",
            "Additional Classrooms and Digital Science Lab for Govt Higher Secondary School at {block}",
            "School Sanitation Block and Clean Drinking Water Station at {block}",
            "Library & E-Learning Resource Center at {block}"
        ],
        "Healthcare": [
            "Primary Health Center Sub-Center Modernization & Medical Equipment at {block}",
            "Emergency Ambulance Bay and Mother-Child Care Ward at {block}",
            "Diagnostic Lab Facility & Solar Backup for Community Health Centre at {block}"
        ],
        "Energy & Solar": [
            "Solar Street Lighting work at {block} in {district}",
            "Construction of Solar Mini-Grid & LED Illumination for {block} Ghats",
            "High-Mast Solar LED Lighting Systems for Rural Markets in {block}",
            "Rooftop Solar PV Installation for Community Administrative Building at {block}"
        ]
    }

    contractors = [
        "Ganga Valley Engineering Associates",
        "M/s पूर्वांचल इन्फ्राटेक Pvt Ltd",
        "Kashi Construction & Civil Works",
        "Kashi Jal Shuddhikkaran Solutions",
        "Vanguard Infrastructure & Electricals",
        "Cauvery Civil Builders Ltd",
        "Sahyadri Infrastructure Works",
        "Karnataka Rural Tech Contractors",
        "Universal Power & Solar Systems",
        "Pragati Construction Consortium"
    ]

    base_budgets = {
        "Roads & Pathways": (1200000, 3500000),
        "Drinking Water Infrastructure": (250000, 950000),
        "Community Facilities": (2500000, 6000000),
        "Education & Schools": (800000, 2200000),
        "Healthcare": (1500000, 4500000),
        "Energy & Solar": (300000, 1100000)
    }

    records = []
    base_date = datetime(2026, 9, 1)
    states = list(constituency_map.keys())

    for i in range(num_records):
        proj_id = f"MPLAD-{1001 + i}"

        state = np.random.choice(states, p=[0.35, 0.25, 0.20, 0.20])
        districts = list(constituency_map[state].keys())
        district = np.random.choice(districts)
        dist_meta = constituency_map[state][district]
        constituency = dist_meta["constituency"]
        mp_name = dist_meta["mp"]
        block = np.random.choice(dist_meta["blocks"])

        sector = np.random.choice(sectors, p=[0.25, 0.22, 0.18, 0.15, 0.10, 0.10])
        template = np.random.choice(work_templates[sector])
        work_name = template.format(block=block, district=district)
        contractor = np.random.choice(contractors)

        low, high = base_budgets[sector]
        sanction_amount = float(np.round(np.random.randint(low, high) / 10000) * 10000)
        revised_estimate = sanction_amount

        days_since_sanction = int(np.random.randint(30, 420))
        sanction_date = (base_date - timedelta(days=days_since_sanction)).strftime("%Y-%m-%d")
        target_days = int(np.random.randint(120, 270))
        target_date = (base_date - timedelta(days=days_since_sanction) + timedelta(days=target_days)).strftime("%Y-%m-%d")

        physical_progress_pct = int(np.random.randint(25, 98))
        expenditure = float(np.round((sanction_amount * (physical_progress_pct / 100.0) * np.random.uniform(0.85, 1.05)) / 10000) * 10000)
        if expenditure > sanction_amount:
            expenditure = sanction_amount

        status = "Ongoing"
        if physical_progress_pct >= 95:
            status = "Completed"
        elif days_since_sanction > target_days:
            status = "Delayed"

        records.append({
            "project_id": proj_id,
            "state": state,
            "district": district,
            "constituency": constituency,
            "mp_name": mp_name,
            "block": block,
            "category": sector,
            "work_name": work_name,
            "contractor": contractor,
            "sanction_amount": sanction_amount,
            "revised_estimate": revised_estimate,
            "expenditure": expenditure,
            "physical_progress_pct": physical_progress_pct,
            "sanction_date": sanction_date,
            "target_completion_date": target_date,
            "days_since_sanction": days_since_sanction,
            "status": status,
            "geo_verified": bool(np.random.choice([True, False], p=[0.8, 0.2]))
        })

    df = pd.DataFrame(records)

    # -------------------------------------------------------------
    # Explicitly configure standard showcase projects matching user screens
    # -------------------------------------------------------------
    # MPLAD-1002 (Salem Road Construction with MPLAD-1006 duplicate)
    df.loc[df['project_id'] == 'MPLAD-1002', 'state'] = 'Tamil Nadu'
    df.loc[df['project_id'] == 'MPLAD-1002', 'district'] = 'Salem'
    df.loc[df['project_id'] == 'MPLAD-1002', 'block'] = 'Ward 2'
    df.loc[df['project_id'] == 'MPLAD-1002', 'category'] = 'Road Construction'
    df.loc[df['project_id'] == 'MPLAD-1002', 'work_name'] = 'Road Construction work at Ward 2 in Salem'
    df.loc[df['project_id'] == 'MPLAD-1002', 'sanction_amount'] = 1560000.0
    df.loc[df['project_id'] == 'MPLAD-1002', 'revised_estimate'] = 1560000.0
    df.loc[df['project_id'] == 'MPLAD-1002', 'expenditure'] = 810000.0
    df.loc[df['project_id'] == 'MPLAD-1002', 'physical_progress_pct'] = 78
    df.loc[df['project_id'] == 'MPLAD-1002', 'status'] = 'Ongoing'

    # MPLAD-1006 (Salem Road Construction duplicate counterpart)
    df.loc[df['project_id'] == 'MPLAD-1006', 'state'] = 'Tamil Nadu'
    df.loc[df['project_id'] == 'MPLAD-1006', 'district'] = 'Salem'
    df.loc[df['project_id'] == 'MPLAD-1006', 'block'] = 'Ward 13'
    df.loc[df['project_id'] == 'MPLAD-1006', 'category'] = 'Road Construction'
    df.loc[df['project_id'] == 'MPLAD-1006', 'work_name'] = 'Road Construction work at Ward 13 in Salem'
    df.loc[df['project_id'] == 'MPLAD-1006', 'sanction_amount'] = 2600000.0
    df.loc[df['project_id'] == 'MPLAD-1006', 'revised_estimate'] = 2600000.0
    df.loc[df['project_id'] == 'MPLAD-1006', 'expenditure'] = 2230000.0
    df.loc[df['project_id'] == 'MPLAD-1006', 'physical_progress_pct'] = 76
    df.loc[df['project_id'] == 'MPLAD-1006', 'status'] = 'Ongoing'

    # MPLAD-1038 (Thane Solar Lighting)
    df.loc[df['project_id'] == 'MPLAD-1038', 'state'] = 'Maharashtra'
    df.loc[df['project_id'] == 'MPLAD-1038', 'district'] = 'Thane'
    df.loc[df['project_id'] == 'MPLAD-1038', 'block'] = 'Ward 36'
    df.loc[df['project_id'] == 'MPLAD-1038', 'category'] = 'Solar Street Lighting'
    df.loc[df['project_id'] == 'MPLAD-1038', 'work_name'] = 'Solar Street Lighting work at Ward 36 in Thane'
    df.loc[df['project_id'] == 'MPLAD-1038', 'sanction_amount'] = 650000.0
    df.loc[df['project_id'] == 'MPLAD-1038', 'revised_estimate'] = 650000.0
    df.loc[df['project_id'] == 'MPLAD-1038', 'physical_progress_pct'] = 40
    df.loc[df['project_id'] == 'MPLAD-1038', 'status'] = 'Ongoing'

    # MPLAD-1034 (Pune Solar Lighting)
    df.loc[df['project_id'] == 'MPLAD-1034', 'state'] = 'Maharashtra'
    df.loc[df['project_id'] == 'MPLAD-1034', 'district'] = 'Pune'
    df.loc[df['project_id'] == 'MPLAD-1034', 'block'] = 'Ward 17'
    df.loc[df['project_id'] == 'MPLAD-1034', 'category'] = 'Solar Street Lighting'
    df.loc[df['project_id'] == 'MPLAD-1034', 'work_name'] = 'Solar Street Lighting work at Ward 17 in Pune'
    df.loc[df['project_id'] == 'MPLAD-1034', 'sanction_amount'] = 340000.0
    df.loc[df['project_id'] == 'MPLAD-1034', 'physical_progress_pct'] = 60
    df.loc[df['project_id'] == 'MPLAD-1034', 'days_since_sanction'] = 412
    df.loc[df['project_id'] == 'MPLAD-1034', 'status'] = 'Delayed'

    # MPLAD-1018 (Pune Solar Lighting)
    df.loc[df['project_id'] == 'MPLAD-1018', 'state'] = 'Maharashtra'
    df.loc[df['project_id'] == 'MPLAD-1018', 'district'] = 'Pune'
    df.loc[df['project_id'] == 'MPLAD-1018', 'block'] = 'Ward 20'
    df.loc[df['project_id'] == 'MPLAD-1018', 'category'] = 'Solar Street Lighting'
    df.loc[df['project_id'] == 'MPLAD-1018', 'work_name'] = 'Solar Street Lighting work at Ward 20 in Pune'
    df.loc[df['project_id'] == 'MPLAD-1018', 'sanction_amount'] = 460000.0
    df.loc[df['project_id'] == 'MPLAD-1018', 'physical_progress_pct'] = 96
    df.loc[df['project_id'] == 'MPLAD-1018', 'status'] = 'Ongoing'

    # MPLAD-1022 (Belagavi Road Construction)
    df.loc[df['project_id'] == 'MPLAD-1022', 'state'] = 'Karnataka'
    df.loc[df['project_id'] == 'MPLAD-1022', 'district'] = 'Belagavi'
    df.loc[df['project_id'] == 'MPLAD-1022', 'block'] = 'Ward 36'
    df.loc[df['project_id'] == 'MPLAD-1022', 'category'] = 'Road Construction'
    df.loc[df['project_id'] == 'MPLAD-1022', 'work_name'] = 'Road Construction work at Ward 36 in Belagavi'
    df.loc[df['project_id'] == 'MPLAD-1022', 'sanction_amount'] = 2000000.0
    df.loc[df['project_id'] == 'MPLAD-1022', 'revised_estimate'] = 2000000.0
    df.loc[df['project_id'] == 'MPLAD-1022', 'physical_progress_pct'] = 55
    df.loc[df['project_id'] == 'MPLAD-1022', 'status'] = 'Ongoing'

    # Varanasi showcase projects (PC-77)
    df.loc[df['project_id'] == 'MPLAD-1023', 'state'] = 'Uttar Pradesh'
    df.loc[df['project_id'] == 'MPLAD-1023', 'district'] = 'Varanasi'
    df.loc[df['project_id'] == 'MPLAD-1023', 'block'] = 'Rohania'
    df.loc[df['project_id'] == 'MPLAD-1023', 'category'] = 'Drinking Water Infrastructure'
    df.loc[df['project_id'] == 'MPLAD-1023', 'work_name'] = 'Installation of 8 High-Capacity RO Water Purification Plants with Chillers'
    df.loc[df['project_id'] == 'MPLAD-1023', 'contractor'] = 'M/s पूर्वांचल इन्फ्राटेक Pvt Ltd'
    df.loc[df['project_id'] == 'MPLAD-1023', 'sanction_amount'] = 4500000.0
    df.loc[df['project_id'] == 'MPLAD-1023', 'revised_estimate'] = 5400000.0
    df.loc[df['project_id'] == 'MPLAD-1023', 'expenditure'] = 4095000.0 # 91% funds billed
    df.loc[df['project_id'] == 'MPLAD-1023', 'physical_progress_pct'] = 38 # only 38% physical work
    df.loc[df['project_id'] == 'MPLAD-1023', 'days_since_sanction'] = 395
    df.loc[df['project_id'] == 'MPLAD-1023', 'status'] = 'Delayed'

    # Save to file if specified
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Dataset generated with {len(df)} records at: {output_path}")

    return df

if __name__ == "__main__":
    generate_mplads_dataset(200, "data/mplads_raw_data.csv")
