import requests
import os
from difflib import get_close_matches

def search_material(item_query):
    api_key = os.getenv("EARTH911_API_KEY")
    if not api_key:
        print("Missing EARTH911_API_KEY in environment.")
        return None

    try:
        response = requests.get("https://api.earth911.com/earth911.getMaterials", params={"api_key": api_key})
        response.raise_for_status()
        data = response.json()

        materials = data.get("result", [])
        if not materials:
            print("No materials found from Earth911.")
            return None

        # Build a dictionary of descriptions and their IDs
        material_dict = {mat["description"]: mat["material_id"] for mat in materials}

        # Lowercase mapping to enable fuzzy match
        lowercase_map = {desc.lower(): desc for desc in material_dict}

        # Get best match using fuzzy matching
        matches = get_close_matches(item_query.lower(), lowercase_map.keys(), n=1, cutoff=0.4)

        if matches:
            best_match = lowercase_map[matches[0]]
            return {
                "description": best_match,
                "material_id": material_dict[best_match]
            }

        print("No close match found for:", item_query)
        return None

    except Exception as e:
        print("Earth911 material search failed:", e)
        return None
