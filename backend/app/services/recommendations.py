from app.schemas.api import RecommendationOut

PLAYBOOK = {
    "unemployment": [
        "Launch district skill-development cohorts tied to local employer demand.",
        "Increase job placement drives and MSME credit support in the next 30 days.",
        "Prioritize public works in high poverty blocks until private hiring recovers.",
    ],
    "inflation": [
        "Activate price monitoring cells for essential commodities.",
        "Target temporary food and transport subsidies to vulnerable households.",
        "Coordinate supply-chain decongestion for high-inflation market clusters.",
    ],
    "crime": [
        "Deploy hotspot policing for affected wards and transit corridors.",
        "Increase community reporting channels and victim-support response teams.",
        "Audit repeat-offence patterns and night-time patrol allocation.",
    ],
    "climate": [
        "Pre-position drinking water, fodder, and medical supplies in exposed blocks.",
        "Accelerate water harvesting, reservoir monitoring, and heat shelters.",
        "Issue localized advisories for crop switching and heatwave work-hour limits.",
    ],
    "sentiment": [
        "Stand up a misinformation and public grievance response cell.",
        "Publish transparent district updates through trusted local channels.",
        "Escalate field verification for viral complaints and protest signals.",
    ],
    "poverty": [
        "Expand benefit-delivery camps and resolve ration, pension, and health claims.",
        "Prioritize nutrition, school attendance, and cash-transfer coverage gaps.",
        "Route livelihoods programs to blocks with compounding socio-economic stress.",
    ],
}


def build_recommendation(region_code: str, category: str, severity_score: float) -> RecommendationOut:
    actions = PLAYBOOK.get(category, PLAYBOOK["poverty"])
    rationale = (
        f"{category.title()} is the dominant risk driver for {region_code}. "
        "The intervention mix combines immediate stabilization with medium-term resilience."
    )
    return RecommendationOut(
        region_code=region_code,
        category=category,
        severity_score=round(severity_score, 2),
        actions=actions,
        rationale=rationale,
    )
