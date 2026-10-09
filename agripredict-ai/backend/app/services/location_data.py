"""Location data for Andhra Pradesh districts with coordinates."""

# Andhra Pradesh district coordinates (approximate centers)
AP_DISTRICTS = {
    "Anantapur": {"lat": 14.6819, "lon": 77.6006, "mandals": ["Anantapur", "Dharmavaram", "Hindupur", "Kadiri", "Kalyanadurgam", "Penukonda", "Rayadurg", "Tadipatri", "Uravakonda"]},
    "Chittoor": {"lat": 13.2172, "lon": 79.1003, "mandals": ["Chittoor", "Tirupati", "Madanapalle", "Punganur", "Palamaner", "Puttur", "Srikalahasti", "Nagari", "Kuppam", "Pileru"]},
    "East Godavari": {"lat": 17.3212, "lon": 82.0537, "mandals": ["Kakinada", "Rajahmundry", "Amalapuram", "Ramachandrapuram", "Peddapuram", "Tuni", "Rampachodavaram", "Mandapeta"]},
    "Guntur": {"lat": 16.3067, "lon": 80.4365, "mandals": ["Guntur", "Tenali", "Narasaraopet", "Mangalagiri", "Bapatla", "Vinukonda", "Macherla", "Piduguralla", "Sattenapalle"]},
    "Krishna": {"lat": 16.6100, "lon": 80.7214, "mandals": ["Vijayawada", "Machilipatnam", "Gudivada", "Nuzvid", "Jaggaiahpet", "Nandigama", "Tiruvuru", "Mylavaram"]},
    "Kurnool": {"lat": 15.8281, "lon": 78.0373, "mandals": ["Kurnool", "Nandyal", "Adoni", "Yemmiganur", "Dhone", "Atmakur", "Nandikotkur", "Allagadda"]},
    "Nellore": {"lat": 14.4426, "lon": 79.9865, "mandals": ["Nellore", "Gudur", "Kavali", "Atmakur", "Venkatagiri", "Sullurpeta", "Kovur"]},
    "Prakasam": {"lat": 15.3500, "lon": 79.5500, "mandals": ["Ongole", "Markapur", "Chirala", "Kandukur", "Darsi", "Giddalur", "Addanki", "Kanigiri"]},
    "Srikakulam": {"lat": 18.2949, "lon": 83.8938, "mandals": ["Srikakulam", "Palasa", "Tekkali", "Narasannapeta", "Rajam", "Amadalavalasa", "Ichapuram"]},
    "Visakhapatnam": {"lat": 17.6868, "lon": 83.2185, "mandals": ["Visakhapatnam", "Anakapalli", "Bheemunipatnam", "Narsipatnam", "Yelamanchili", "Paderu", "Araku Valley", "Chodavaram"]},
    "Vizianagaram": {"lat": 18.1067, "lon": 83.3956, "mandals": ["Vizianagaram", "Parvathipuram", "Bobbili", "Salur", "Rajam", "Nellimarla", "Cheepurupalli"]},
    "West Godavari": {"lat": 16.9174, "lon": 81.3399, "mandals": ["Eluru", "Bhimavaram", "Tadepalligudem", "Narasapuram", "Tanuku", "Nidadavole", "Kovvur", "Palacole"]},
    "YSR Kadapa": {"lat": 14.4674, "lon": 78.8241, "mandals": ["Kadapa", "Proddatur", "Rajampet", "Jammalamadugu", "Pulivendla", "Rayachoti", "Badvel", "Mydukur"]},
}

# Soil types common in AP
SOIL_TYPES = [
    {"value": "red", "label": "Red Soil", "label_te": "ఎర్ర నేల"},
    {"value": "black", "label": "Black / Cotton Soil", "label_te": "నల్ల నేల"},
    {"value": "alluvial", "label": "Alluvial Soil", "label_te": "ఒండ్రు నేల"},
    {"value": "sandy", "label": "Sandy Soil", "label_te": "ఇసుక నేల"},
    {"value": "clayey", "label": "Clayey Soil", "label_te": "బంక నేల"},
    {"value": "loamy", "label": "Loamy Soil", "label_te": "గుల్ల నేల"},
    {"value": "laterite", "label": "Laterite Soil", "label_te": "లేటరైట్ నేల"},
    {"value": "unknown", "label": "Unknown / Not Sure", "label_te": "తెలియదు"},
]

# Irrigation types
IRRIGATION_TYPES = [
    {"value": "rainfed", "label": "Rain-fed Only", "label_te": "వర్షాధారం"},
    {"value": "borewell", "label": "Borewell", "label_te": "బోరు బావి"},
    {"value": "canal", "label": "Canal Irrigation", "label_te": "కాల్వ నీరు"},
    {"value": "drip", "label": "Drip Irrigation", "label_te": "డ్రిప్ నీరు"},
    {"value": "sprinkler", "label": "Sprinkler", "label_te": "స్ప్రింక్లర్"},
    {"value": "tank", "label": "Tank / Pond", "label_te": "చెరువు"},
    {"value": "other", "label": "Other", "label_te": "ఇతరం"},
]

# Farming seasons
FARMING_SEASONS = [
    {"value": "kharif", "label": "Kharif (June-October)", "label_te": "ఖరీఫ్ (జూన్-అక్టోబర్)", "months": [6, 7, 8, 9, 10]},
    {"value": "rabi", "label": "Rabi (November-March)", "label_te": "రబీ (నవంబర్-మార్చి)", "months": [11, 12, 1, 2, 3]},
    {"value": "zaid", "label": "Zaid / Summer (March-June)", "label_te": "వేసవి (మార్చి-జూన్)", "months": [3, 4, 5, 6]},
    {"value": "annual", "label": "Annual / Year-round", "label_te": "వార్షిక", "months": list(range(1, 13))},
]


def get_district_coords(district: str):
    """Get coordinates for a district."""
    dist = AP_DISTRICTS.get(district)
    if dist:
        return dist["lat"], dist["lon"]
    return None, None


def get_district_mandals(district: str):
    """Get mandals for a district."""
    dist = AP_DISTRICTS.get(district)
    if dist:
        return dist.get("mandals", [])
    return []


def resolve_coordinates(state: str, district: str, mandal: str = None, lat: float = None, lon: float = None):
    """Resolve coordinates from location inputs."""
    if lat and lon:
        return lat, lon
    if district:
        return get_district_coords(district)
    return None, None
