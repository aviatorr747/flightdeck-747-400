from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)

FACTS = [
    {"title": "A stretched jumbo jet", "value": "The 747-400 is a long-range, wide-body airliner and a major development of the original 747 family.", "tag": "DESIGN"},
    {"title": "Four engines", "value": "The passenger 747-400 is powered by four high-bypass turbofan engines.", "tag": "POWER"},
    {"title": "Winglets", "value": "Distinctive winglets were added to the 747-400 to help reduce drag and improve fuel efficiency compared with earlier 747 variants.", "tag": "AERODYNAMICS"},
    {"title": "Two flight decks", "value": "A raised upper deck gives the 747 its unmistakable hump-shaped profile.", "tag": "LAYOUT"},
    {"title": "A modernised cockpit", "value": "The 747-400 introduced a two-crew glass cockpit, reducing the need for a dedicated flight engineer on the flight deck.", "tag": "AVIONICS"},
    {"title": "A global workhorse", "value": "747-400s served airlines around the world in passenger and freighter roles.", "tag": "SERVICE"},
]

FACT_PROMPTS = [
    "How did the 747-400 improve on the 747-300?",
    "Why does the 747-400 have winglets?",
    "What does the upper deck contain?",
    "Which engines were offered on the 747-400?",
    "How does the 747-400F differ from the passenger version?",
    "What made the 747-400 cockpit different?",
]

IMAGE_PROMPTS = [
    {"name": "Classic side profile", "prompt": "A photorealistic Boeing 747-400 in a clean full side profile, parked on an airport apron, overcast soft daylight, accurate four-engine configuration, distinctive upper deck and winglets, aviation photography, no text or watermark."},
    {"name": "Take-off rotation", "prompt": "A Boeing 747-400 rotating for take-off on a long runway, viewed from a three-quarter front angle, landing gear still visible, four engines, accurate winglets, dramatic but realistic airport photography, no text or watermark."},
    {"name": "Cockpit detail", "prompt": "A historically accurate Boeing 747-400 flight deck, wide view from behind the pilot seats, classic 747-400 glass cockpit displays and controls, realistic aviation documentary photography, no people identifiable, no text overlay."},
    {"name": "Wing and winglet", "prompt": "Close-up aviation photograph looking along the wing of a Boeing 747-400, clearly showing the distinctive blended winglet and engine nacelle, blue sky, crisp natural lighting, realistic details, no text or watermark."},
    {"name": "Cargo variant", "prompt": "A Boeing 747-400F freighter at a cargo terminal, viewed from front three-quarter angle, nose section and main-deck cargo door visible where appropriate, accurate aircraft proportions, documentary aviation photography, no text or watermark."},
    {"name": "Golden-hour arrival", "prompt": "A Boeing 747-400 on final approach above an airport at golden hour, distant runway and airport lights, realistic aircraft proportions, four engines and winglets clearly visible, telephoto aviation photograph, no text or watermark."},
]

@main_bp.get("/")
def index():
    return render_template("index.html", facts=FACTS, fact_prompts=FACT_PROMPTS,
                           image_prompts=IMAGE_PROMPTS)

@main_bp.get("/explore")
@login_required
def explore():
    return render_template("explore.html", facts=FACTS, fact_prompts=FACT_PROMPTS,
                           image_prompts=IMAGE_PROMPTS)

@main_bp.get("/api/facts")
def api_facts():
    return jsonify(FACTS)

@main_bp.get("/health")
def health():
    return jsonify(status="ok")
