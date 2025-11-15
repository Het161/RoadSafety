import sqlite3
from typing import Dict, List
from models import InterventionInput, InterventionEstimate, MaterialLineItem

def calculate_estimate(intervention: InterventionInput) -> InterventionEstimate:
    conn = sqlite3.connect('roadsafe.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get intervention details
    c.execute("SELECT * FROM interventions WHERE name=?", (intervention.type,))
    interv_row = c.fetchone()
    if not interv_row:
        raise ValueError(f"Intervention type '{intervention.type}' not supported")
    
    interv_id = interv_row['id']
    
    # Get IRC spec
    c.execute("SELECT * FROM irc_specs WHERE intervention_id=?", (interv_id,))
    spec = c.fetchone()
    
    # Calculate quantity using formula
    quantity = eval_formula(spec['quantity_formula'], intervention)
    
    # Get rate items
    c.execute("SELECT * FROM rate_items WHERE intervention_id=?", (interv_id,))
    rate_rows = c.fetchall()
    
    materials = []
    total = 0.0
    
    for rate in rate_rows:
        # Simplified: use calculated quantity for primary material
        item_qty = quantity if 'Sheeting' in rate['material_name'] or 'Concrete' in rate['material_name'] or 'Beam' in rate['material_name'] else quantity * 0.1
        cost = item_qty * rate['unit_rate']
        total += cost
        
        materials.append(MaterialLineItem(
            material_name=rate['material_name'],
            quantity=round(item_qty, 2),
            unit=rate['unit'],
            unit_rate=rate['unit_rate'],
            total_cost=round(cost, 2),
            source=rate['source'],
            source_ref=rate['source_ref']
        ))
    
    conn.close()
    
    return InterventionEstimate(
        intervention_type=intervention.type,
        location_chainage_km=intervention.location_chainage_km,
        irc_code=spec['irc_code'],
        clause_ref=spec['clause_ref'],
        materials=materials,
        total_material_cost=round(total, 2),
        tolerance_percentage=10.0
    )

def eval_formula(formula: str, intervention: InterventionInput) -> float:
    """Safely evaluate simple formulas"""
    context = {
        'height_m': intervention.height_m or 0,
        'width_m': intervention.width_m or 0,
        'length_m': intervention.length_m or 0
    }
    # Extract calculation from formula string
    calc_part = formula.split('=')[1].strip()
    return eval(calc_part, {"__builtins__": {}}, context)
