"""
Generates friendly, human, non-technical insight copy for a plant based
on its current simulated sensor values. Talks like a gardening assistant,
never like a sensor readout.
"""


def build_insights(plant) -> list[dict]:
    insights: list[dict] = []
    name = plant.name.lower()

    # Overall health
    if plant.health_score >= 90:
        insights.append({
            "icon": "sparkles",
            "text": f"Your {name} plant is growing beautifully — it's one of the healthiest in your garden right now.",
        })
    elif plant.health_score >= 75:
        insights.append({
            "icon": "leaf",
            "text": f"Your {name} plant is doing well overall, with just a little room to thrive even more.",
        })
    else:
        insights.append({
            "icon": "alert-circle",
            "text": f"Your {name} plant needs a bit of extra attention this week.",
        })

    # Soil moisture
    if plant.soil_moisture >= 65:
        insights.append({
            "icon": "droplets",
            "text": "Soil moisture is right where it should be — no watering needed until tomorrow.",
        })
    elif plant.soil_moisture >= 45:
        insights.append({
            "icon": "droplets",
            "text": "Soil moisture looks balanced today. A light watering this evening will keep things comfortable.",
        })
    else:
        insights.append({
            "icon": "droplets",
            "text": "The soil is drying out a little faster than usual — a good drink of water would help.",
        })

    # Humidity
    if 45 <= plant.humidity <= 65:
        insights.append({
            "icon": "wind",
            "text": "Humidity is ideal for flowering, giving your plant the comfortable air it loves.",
        })
    else:
        insights.append({
            "icon": "wind",
            "text": "The air around your plant is a touch drier than ideal — a gentle misting could help.",
        })

    # Sunlight
    if plant.sunlight_hours >= 6:
        insights.append({
            "icon": "sun",
            "text": "Sunlight is excellent today — your plant is soaking up all the energy it needs.",
        })
    else:
        insights.append({
            "icon": "sun",
            "text": "Sunlight has been a little gentle today — a sunnier spot tomorrow would be lovely.",
        })

    # Temperature
    if 22 <= plant.temperature <= 30:
        insights.append({
            "icon": "thermometer",
            "text": "Temperatures are sitting in a very comfortable range for steady, happy growth.",
        })
    else:
        insights.append({
            "icon": "thermometer",
            "text": "It's a little warmer than usual — some afternoon shade could keep things cozy.",
        })

    return insights


def build_next_action(plant) -> dict:
    if plant.soil_moisture < 55:
        return {
            "title": f"Water {plant.name} Plant",
            "detail": "250ml water, poured slowly at the base",
            "duration": "2 minutes",
            "icon": "droplets",
        }
    if plant.humidity < 45:
        return {
            "title": f"Mist {plant.name} Plant",
            "detail": "A light spray around the leaves",
            "duration": "1 minute",
            "icon": "cloud-drizzle",
        }
    return {
        "title": f"Check on {plant.name} Plant",
        "detail": "A quick look at leaves and soil",
        "duration": "1 minute",
        "icon": "eye",
    }
