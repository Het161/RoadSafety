import sqlite3
import json

def init_db():
    conn = sqlite3.connect('roadsafe.db')
    c = conn.cursor()
    
    # Interventions table
    c.execute('''CREATE TABLE IF NOT EXISTS interventions (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        description TEXT
    )''')
    
    # IRC specifications table
    c.execute('''CREATE TABLE IF NOT EXISTS irc_specs (
        id INTEGER PRIMARY KEY,
        intervention_id INTEGER,
        irc_code TEXT,
        clause_ref TEXT,
        quantity_formula TEXT,
        FOREIGN KEY(intervention_id) REFERENCES interventions(id)
    )''')
    
    # Rate items table (materials from CPWD SOR / GeM)
    c.execute('''CREATE TABLE IF NOT EXISTS rate_items (
        id INTEGER PRIMARY KEY,
        intervention_id INTEGER,
        material_name TEXT,
        unit TEXT,
        unit_rate REAL,
        source TEXT,
        source_ref TEXT,
        FOREIGN KEY(intervention_id) REFERENCES interventions(id)
    )''')
    
    # Seed sample data
    seed_data(c)
    conn.commit()
    conn.close()

def seed_data(cursor):
    # Sample interventions
    interventions = [
        (1, 'Warning Sign', 'Signage', 'Retro-reflective warning sign board'),
        (2, 'Speed Breaker', 'Traffic Calming', 'Concrete speed breaker'),
        (3, 'Crash Barrier', 'Safety Barrier', 'Metal beam crash barrier')
    ]
    cursor.executemany('INSERT OR IGNORE INTO interventions VALUES (?,?,?,?)', interventions)
    
    # IRC specs (simplified formulas as strings)
    specs = [
        (1, 1, 'IRC-67-2022', 'Clause 5.2', 'area = height_m * width_m'),
        (2, 2, 'IRC-99-2018', 'Clause 3.1', 'volume = length_m * width_m * 0.1'),
        (3, 3, 'IRC-SP:87-2020', 'Clause 4.3', 'length = length_m')
    ]
    cursor.executemany('INSERT OR IGNORE INTO irc_specs VALUES (?,?,?,?,?)', specs)
    
    # Rate items (mock prices from CPWD SOR / GeM)
    rates = [
        (1, 1, 'Retro-reflective Sheeting Class C', 'sqm', 2500.0, 'CPWD_SOR', 'SOR-2025/RB-405'),
        (2, 1, 'MS Frame & Post', 'kg', 85.0, 'GeM', 'GeM-MS-2025-001'),
        (3, 2, 'M20 Concrete', 'cum', 6500.0, 'CPWD_SOR', 'SOR-2025/CE-112'),
        (4, 3, 'W-Beam Metal Barrier', 'meter', 3200.0, 'GeM', 'GeM-BB-2025-045')
    ]
    cursor.executemany('INSERT OR IGNORE INTO rate_items VALUES (?,?,?,?,?,?,?)', rates)

if __name__ == '__main__':
    init_db()
    print("✅ Database initialized with seed data")
