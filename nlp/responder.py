import os
import requests
from nlp.detector import detect_intent, detect_crop, detect_symptom
from data.crop_db import CROP_DB
from data.disease_db import DISEASE_DB
from data.market import MARKET
from data.schemes import SCHEMES

# ── GROQ AI FALLBACK ────────────────────────────────────────
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')  # Set your key in app.py or env
GROQ_MODEL   = 'llama-3.1-8b-instant'  # Current fast free-tier model on Groq
GROQ_URL     = 'https://api.groq.com/openai/v1/chat/completions'

GROQ_SYSTEM_PROMPT = (
    'You are KrishiMitra, an expert AI farming assistant for Indian farmers. '
    'You answer questions about crop diseases, fertilizers, irrigation, market prices, '
    'government schemes, soil health, seeds, organic farming, weather advisories, '
    'and any other agriculture-related topics. '
    'Keep answers concise, practical, and relevant to Indian farming conditions. '
    'Always respond in the same language the user is using (Hindi, Marathi, or English). '
    'Use bullet points where helpful. Do NOT refuse farming-related questions.'
)


def ask_groq(user_text: str) -> str:
    """Send the user message to Groq API and return the AI response string."""
    key = GROQ_API_KEY or os.environ.get('GROQ_API_KEY', '')
    if not key or key == 'YOUR_GROQ_API_KEY_HERE':
        return (
            '⚠️ AI assistant is not configured.\n'
            'Please set your GROQ_API_KEY in app.py to get intelligent answers.\n'
            'Get a free key at: https://console.groq.com'
        )
    try:
        resp = requests.post(
            GROQ_URL,
            headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
            json={
                'model': GROQ_MODEL,
                'messages': [
                    {'role': 'system', 'content': GROQ_SYSTEM_PROMPT},
                    {'role': 'user',   'content': user_text}
                ],
                'max_tokens': 512,
                'temperature': 0.4,
            },
            timeout=15,
        )
        # Surface the real Groq error message for easier debugging
        if not resp.ok:
            try:
                err_body = resp.json()
                err_msg  = err_body.get('error', {}).get('message', resp.text)
            except Exception:
                err_msg = resp.text
            return f'⚠️ Groq API error ({resp.status_code}): {err_msg}'
        data = resp.json()
        return data['choices'][0]['message']['content'].strip()
    except requests.exceptions.Timeout:
        return '⚠️ AI response timed out. Please try again.'
    except requests.exceptions.ConnectionError:
        return '⚠️ Could not connect to AI service. Check your internet connection.'
    except Exception as e:
        return f'⚠️ Unexpected error: {str(e)}'


def ask_groq_vision(image_b64: str, user_question: str = None, language: str = 'en') -> str:
    """Send a crop image (base64) to Groq vision model for disease/pest diagnosis."""
    key = GROQ_API_KEY or os.environ.get('GROQ_API_KEY', '')
    if not key or key == 'YOUR_GROQ_API_KEY_HERE':
        return (
            '⚠️ AI assistant is not configured.\n'
            'Please set your GROQ_API_KEY in app.py to enable image analysis.\n'
            'Get a free key at: https://console.groq.com'
        )

    lang_instruction = {
        'hi': 'Answer in Hindi.',
        'mr': 'Answer in Marathi.',
    }.get(language, 'Answer in English.')

    question = user_question or 'Analyze this crop/plant image.'
    prompt = (
        f'You are KrishiMitra, an expert AI farming assistant for Indian farmers. '
        f'{lang_instruction} '
        f'The farmer has shared a photo of their crop or plant. '
        f'Identify any visible diseases, pest damage, nutrient deficiencies, or other issues. '
        f'Provide: 1) What you see in the image, 2) Likely problem/disease name, '
        f'3) Cause, 4) Treatment & remedies, 5) Prevention tips. '
        f'Be concise and practical for Indian farming conditions. '
        f"Farmer's question: {question}"
    )

    try:
        resp = requests.post(
            GROQ_URL,
            headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
            json={
                'model': 'meta-llama/llama-4-scout-17b-16e-instruct',
                'messages': [{
                    'role': 'user',
                    'content': [
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:image/jpeg;base64,{image_b64}'
                            }
                        },
                        {
                            'type': 'text',
                            'text': prompt
                        }
                    ]
                }],
                'max_tokens': 600,
                'temperature': 0.3,
            },
            timeout=30,
        )
        if not resp.ok:
            try:
                err_body = resp.json()
                err_msg  = err_body.get('error', {}).get('message', resp.text)
            except Exception:
                err_msg = resp.text
            return f'⚠️ Image analysis error ({resp.status_code}): {err_msg}'
        data = resp.json()
        return data['choices'][0]['message']['content'].strip()
    except requests.exceptions.Timeout:
        return '⚠️ Image analysis timed out. Please try again.'
    except Exception as e:
        return f'⚠️ Image analysis error: {str(e)}'




# ── GENERAL KNOWLEDGE  ───────────────────
GENERAL_KNOWLEDGE = {
  "fertilizer": (
    "General Fertilizer Guidelines:\n"
    "• Nitrogen (N) — promotes leaf growth; use Urea or DAP\n"
    "• Phosphorus (P) — root & flower development; use SSP/DAP\n"
    "• Potassium (K) — fruit quality & disease resistance; use MOP\n"
    "• Apply FYM (farmyard manure) 10-20 t/ha before sowing\n"
    "• Get a free Soil Health Card from nearest KVK for personalized advice\n"
    "Tip: Ask about a specific crop for exact NPK doses."
  ),
  "irrigation": (
    "General Irrigation Guidelines:\n"
    "• Drip irrigation saves 40-60% water vs flood irrigation\n"
    "• Sprinkler is ideal for wheat, vegetables & groundnuts\n"
    "• Water in early morning or evening to reduce evaporation\n"
    "• Avoid waterlogging — ensure proper drainage in all fields\n"
    "• Sandy soils need more frequent watering than clay soils\n"
    "Tip: Ask about a specific crop for its watering schedule."
  ),
  "crop_info": (
    "Available crops in our database:\n"
    "Cereals: Wheat, Rice, Maize, Sorghum, Millet\n"
    "Cash crops: Cotton, Sugarcane, Tobacco\n"
    "Vegetables: Tomato, Onion, Potato, Chilli, Brinjal, Okra\n"
    "Fruits: Banana, Mango, Apple, Grapes, Pomegranate\n"
    "Pulses: Gram, Tur, Moong, Urad, Soybean\n"
    "Oilseeds: Groundnut, Mustard, Sunflower, Sesame\n"
    "Ask about any of these crops for growing tips, season, fertilizer & harvest info."
  ),
  "disease": (
    "Common crop disease symptoms and diagnosis:\n"
    "• Yellow leaves → Nitrogen deficiency or fungal infection\n"
    "• White spots → Powdery mildew or thrips attack\n"
    "• Brown spots → Early blight or bacterial leaf spot\n"
    "• Wilting → Root rot, bacterial wilt, or drought\n"
    "• Holes in leaves → Caterpillar or flea beetle\n"
    "• Leaf curling → Virus or whitefly attack\n"
    "Describe your crop name + symptom for a precise treatment plan."
  ),
  "market": (
    "To get today's market price, ask like:\n"
    "  'What is the price of wheat?' or 'Onion market rate?'\n\n"
    "Top MSP prices (2024-25):\n"
    "• Wheat: Rs.2275/quintal\n"
    "• Rice: Rs.2183/quintal\n"
    "• Cotton: Rs.6620/quintal\n"
    "• Soybean: Rs.4600/quintal\n"
    "• Tur/Arhar: Rs.7550/quintal\n"
    "Tip: Register on enam.gov.in for online mandi access."
  ),
  "scheme": (
    "Top Government Schemes for Farmers:\n\n"
    "PM-KISAN — Rs.6,000/year | Apply: pmkisan.gov.in\n"
    "PM Fasal Bima Yojana — Crop insurance at 1.5-2% premium | Apply: nearest bank\n"
    "Kisan Credit Card — Loan up to Rs.3 lakh at 4% interest | Apply: nationalized bank\n"
    "Soil Health Card — Free soil test | Apply: nearest KVK\n"
    "PM Kusum — Solar pump subsidy | Apply: energy department\n"
    "PM Krishi Sinchai Yojana — Irrigation subsidy | Apply: state agri dept\n\n"
    "Helpline: 1800-180-1551 (Toll Free)"
  ),
  "weather": (
    "Weather & Farming Tips:\n"
    "• Check IMD forecast at imd.gov.in or Meghdoot app\n"
    "• Avoid spraying pesticides before rain — wait 24-48 hours after\n"
    "• Heavy rain alert: drain waterlogged fields immediately\n"
    "• Frost alert: cover nursery seedlings with polythene overnight\n"
    "• Heatwave: increase irrigation frequency by 30-50%\n"
    "• Monsoon onset (avg): June 1 (Kerala), June 10 (Maharashtra), June 15 (Maharashtra plateau)"
  ),
  "harvest": (
    "General Harvesting Tips:\n"
    "• Cereals: harvest when 80-90% grains turn golden-yellow\n"
    "• Tomato/vegetables: harvest at firm mature stage for distant markets\n"
    "• Dry crops (pulses, oilseeds) at 12-14% moisture content\n"
    "• Avoid harvesting in wet/rainy conditions to prevent fungal damage\n"
    "• Use combine harvester for wheat, rice and maize to save 60% labour cost\n"
    "Ask about a specific crop for its exact harvest time."
  ),
  "pesticide": (
    "Pesticide Use Guidelines:\n"
    "• For fungal diseases: Mancozeb 2g/L, Carbendazim 1g/L, Wettable Sulfur 3g/L\n"
    "• For sucking pests (aphids, whitefly): Imidacloprid 0.5ml/L or Neem oil 5ml/L\n"
    "• For caterpillars/bollworm: Chlorpyrifos 2ml/L or Bt spray 2g/L\n"
    "• Always read the label; wear gloves and mask while spraying\n"
    "• Spray early morning or late evening to avoid bee harm\n"
    "• Maintain 14-21 day pre-harvest interval before consuming crops"
  ),
  "soil": (
    "Soil Health Information:\n\n"
    "Soil Erosion:\n"
    "• Cause: Heavy rain, wind, deforestation, overgrazing\n"
    "• Prevention: Contour farming, mulching, cover crops, bunding\n"
    "• Remedy: Vetiver grass, terracing, windbreaks, agroforestry\n\n"
    "Soil Types in India:\n"
    "• Black (Regur) soil → Best for cotton (Maharashtra, MP)\n"
    "• Alluvial soil → Best for wheat, rice, sugarcane (North India)\n"
    "• Red & Laterite soil → Groundnut, pulses (Deccan Plateau)\n"
    "• Sandy loam → Vegetables, potatoes\n\n"
    "Soil Testing: Get free Soil Health Card from nearest KVK\n"
    "Ideal pH for most crops: 6.0 – 7.5"
  ),
  "seed": (
    "Seed Selection & Treatment Tips:\n"
    "• Always use certified or high-yielding variety (HYV) seeds\n"
    "• Treat seeds with Thiram 3g/kg or Carbendazim 2g/kg before sowing\n"
    "• Rhizobium inoculation for pulses increases yield 10-15%\n"
    "• Source seeds from government-approved stores or ICAR institutions\n"
    "• Seed germination test: sow 10 seeds in moist cotton — count sprouted in 7 days"
  ),
  "equipment": (
    "Farm Equipment Help:\n"
    "• Tractor: 35-45 HP suitable for most small farms\n"
    "• Rotavator: For fine seedbed preparation — saves 40% fuel vs ploughing\n"
    "• Seed drill: Ensures uniform spacing and reduces seed waste by 20%\n"
    "• Sprayer: Knapsack for small plots; power sprayer for large areas\n"
    "• Custom Hiring Centres: Rent equipment at low cost — apply at agriculture dept\n"
    "• Sub-Mission on Agricultural Mechanization: Subsidy up to 50% on farm machinery"
  ),
  "profit": (
    "Profitable Farming Strategies:\n"
    "• High-value crops: Turmeric, Garlic, Cumin, Pomegranate, Grapes\n"
    "• Vegetable farming: Higher profit per acre than cereals\n"
    "• Organic farming: Premium price + lower input cost after 3 years\n"
    "• Multiple cropping: Grow 2-3 crops per year on the same land\n"
    "• FPO (Farmer Producer Organization): Collective bargaining for better prices\n"
    "• Value addition: Processing, packaging & direct selling increases income 2-3×"
  ),
  "organic": (
    "Organic & Natural Farming Methods:\n"
    "• Zero Budget Natural Farming (ZBNF) by Subhash Palekar — proven in Maharashtra\n"
    "• Make Jeevamrit: 10L cow urine + 10kg dung + 2kg pulses + 2kg jaggery + soil\n"
    "• Neem oil spray (5ml/L) — natural pesticide for most sucking pests\n"
    "• Green manure crops: Dhaincha, Sunhemp — plough in before flowering\n"
    "• Vermicompost: 3-6 months to prepare; apply 2-4 t/ha\n"
    "• Paramparagat Krishi Vikas Yojana (PKVY): Govt support for organic farming"
  ),
  "composting": (
    "Composting & Biofertilizer Guide:\n"
    "• Farm compost: Layer green waste + dry stalks + cow dung; turn every 15 days\n"
    "• Vermicompost: Ready in 60-90 days; use earthworms (Eisenia fetida)\n"
    "• Biofertilizers: Rhizobium (legumes), Azospirillum (cereals), PSB (phosphorus)\n"
    "• Application: Mix biofertilizers with seeds just before sowing\n"
    "• Compost tea: Soak compost in water 24 hrs; spray on leaves for quick nutrition"
  ),
  "storage": (
    "Post-Harvest Storage Tips:\n"
    "• Dry grains to 12-14% moisture before storage to prevent fungal damage\n"
    "• Use hermetic bags (PICS bags) for short-term storage without chemicals\n"
    "• Fumigation: Aluminium phosphide (Celphos) tablets in sealed storage\n"
    "• Cold storage: Essential for potato, onion, fruits — avoids price crash\n"
    "• Gramin Bhandaran Yojana: Subsidy for private warehouse construction (NABARD)\n"
    "• Avoid direct soil contact — use pallets; maintain 1m gap from walls"
  ),
  "transport": (
    "Crop Transport & Market Linkage:\n"
    "• e-NAM (enam.gov.in): Online national agriculture market — sell across states\n"
    "• APMC mandis: Register your produce and transport during morning hours\n"
    "• Cold chain transport: For fruits/vegetables to reduce losses (currently 25-30%)\n"
    "• FPO collective transport: Pool produce with other farmers to cut transport cost\n"
    "• Agri Export Policy: APEDA supports direct export of fruits, spices & vegetables"
  ),
}


def generate_response(user_text: str, language: str = 'en') -> tuple:
    """
    Generate a response tuple (text, intent) for the given user message.
    For every detected intent we now always produce a useful answer —
    even when no specific crop is mentioned.
    """
    intent = detect_intent(user_text)
    crop   = detect_crop(user_text)
    sym    = detect_symptom(user_text)

    # ── DISEASE ──────────────────────────────────────────
    if intent == 'disease':
        if sym and crop and sym in DISEASE_DB and crop in CROP_DB:
            d = DISEASE_DB[sym]
            return (
                f'🌿 {crop.title()} — {sym.title()}\n'
                f'Cause: {d["cause"]}\n'
                f'Treatment: {d["treatment"]}\n'
                f'Prevention: {d["prevention"]}'
            ), 'disease'
        elif sym and sym in DISEASE_DB and not crop:
            d = DISEASE_DB[sym]
            return (
                f'🌿 Symptom: {sym.title()}\n'
                f'Cause: {d["cause"]}\n'
                f'Treatment: {d["treatment"]}\n'
                f'Prevention: {d["prevention"]}'
            ), 'disease'
        elif crop and crop in CROP_DB and not sym:
            diseases = ', '.join(CROP_DB[crop]['diseases'])
            return (
                f'⚠️ Common diseases in {crop.title()}:\n{diseases}\n\n'
                f'Describe the symptoms (e.g. yellow leaves, white spots, wilting) '
                f'for a precise treatment plan.'
            ), 'disease'
        # Crop/symptom not in local DB — ask Groq for accurate answer
        return ask_groq(user_text), 'disease'

    # ── FERTILIZER ───────────────────────────────────────
    if intent == 'fertilizer':
        if crop and crop in CROP_DB:
            c = CROP_DB[crop]
            return (
                f'🌱 Fertilizer for {crop.title()}:\n'
                f'Recommended dose: {c["fertilizer"]}\n'
                f'Best soil: {c["soil"]}\n'
                f'Tip: Get a free Soil Health Card from nearest KVK for customized dosage.'
            ), 'fertilizer'
        # Crop not in local DB — ask Groq for accurate answer
        return ask_groq(user_text), 'fertilizer'

    # ── IRRIGATION ───────────────────────────────────────
    if intent == 'irrigation':
        if crop and crop in CROP_DB:
            c = CROP_DB[crop]
            return (
                f'💧 Irrigation for {crop.title()}:\n'
                f'Schedule: {c["water"]}\n'
                f'Season: {c["season"]}\n'
                f'Tip: Drip irrigation saves 40-60% water and is eligible for PM Krishi Sinchai Yojana subsidy.'
            ), 'irrigation'
        # Crop not in local DB — ask Groq for accurate answer
        return ask_groq(user_text), 'irrigation'

    # ── CROP INFO ─────────────────────────────────────────
    if intent == 'crop_info':
        if crop and crop in CROP_DB:
            c = CROP_DB[crop]
            return (
                f'📋 Growing Guide: {crop.title()}\n'
                f'Season: {c["season"]}\n'
                f'Soil: {c["soil"]}\n'
                f'Water: {c["water"]}\n'
                f'Fertilizer: {c["fertilizer"]}\n'
                f'Harvest: {c["harvest"]}'
            ), 'crop_info'
        # Crop not in local DB — ask Groq for accurate answer
        return ask_groq(user_text), 'crop_info'

    # ── MARKET ───────────────────────────────────────────
    if intent == 'market':
        if crop and crop in MARKET:
            m = MARKET[crop]
            return (
                f'📊 Market Price: {crop.title()}\n'
                f'Current price: {m["price"]}\n'
                f'Trend: {m["trend"]}\n'
                f'Best market: {m["market"]}\n'
                f'Tip: Sell on enam.gov.in for better prices across India.'
            ), 'market'
        # Crop not in local market DB — ask Groq for accurate answer
        return ask_groq(user_text), 'market'

    # ── SCHEME ───────────────────────────────────────────
    if intent == 'scheme':
        lines = '\n\n'.join(
            f'✅ {s["name"]}\n   Benefit: {s["benefit"]}\n   Apply: {s["apply"]}'
            for s in SCHEMES
        )
        return (
            f'🏛️ Government Schemes for Farmers:\n\n{lines}\n\n'
            f'📞 Kisan Helpline: 1800-180-1551 (Toll Free)'
        ), 'scheme'

    # ── OTHER KNOWN INTENTS (weather, harvest, pesticide, soil, etc.) ─────────
    # Use local quick-tips; if user asked about a specific crop not in DB, use Groq
    if intent in GENERAL_KNOWLEDGE:
        if crop and crop not in CROP_DB:
            return ask_groq(user_text), intent
        return GENERAL_KNOWLEDGE[intent], intent

    # ── FINAL FALLBACK — ask Groq AI ─────────────────────
    ai_answer = ask_groq(user_text)
    return ai_answer, 'general'
