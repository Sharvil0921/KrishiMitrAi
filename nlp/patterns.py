# ── NLP INTENT PATTERNS ───────────────────────────────────
PATTERNS = {
  "disease": [
    r"yellow.*lea(f|ves)|white.*spot|brown.*spot|wilt|blight|rust|fungus",
    r"pest|insect|caterpillar|aphid|bollworm|dying|dead|rot|mildew",
    r"plant.*disease|leaf.*curl|spots.*lea(f|ves)|crop.*infection|plant.*problem",
    r"keeda|rog|bimari|pest attack|insect attack|fungal|infection|attack",
    r"disease|sick.*plant|unhealthy.*crop|damaged.*crop|leaf.*spot",
  ],
  "fertilizer": [
    r"fertilizer|urea|npk|dap|khad|nitrogen|phosphorus",
    r"potash|micronutrient|best fertilizer|which fertilizer",
    r"fertilizer dose|how much fertilizer|organic fertilizer|compost",
    r"bio fertilizer|vermicompost|manure|खाद|खत",
    r"khaad|nutrient|feed.*plant|plant food",
  ],
  "irrigation": [
    r"water|irrigation|drip|sprinkler|paani|sinchai|drought",
    r"watering schedule|how much water|when to water",
    r"irrigation timing|water requirement|flood irrigation",
    r"drip setup|sprinkler system|watering method|moisture",
  ],
  "crop_info": [
    r"how to grow|cultivation|sowing|harvest|variety|seed",
    r"seed rate|spacing|crop duration|yield",
    r"best variety|hybrid seeds|crop production",
    r"planting method|growing tips|crop management",
    r"which crop|best crop|grow.*crop|crop.*grow|season.*crop|crop.*season",
  ],
  "market": [
    r"price|rate|bhav|mandi|sell|cost|market|msp",
    r"today price|market rate|crop price",
    r"mandi bhav|sell crop|best price|commodity price|auction",
  ],
  "scheme": [
    r"scheme|yojana|subsidy|pmkisan|insurance|kcc|loan",
    r"government scheme|farmer scheme|agriculture scheme",
    r"subsidy for farmer|loan for farmer|crop insurance",
    r"yojna|sarkari yojana|benefit scheme|government help|sarkar",
  ],
  "weather": [
    r"weather|mausam|rain|temperature|forecast|barish",
    r"rainfall|climate|humidity|forecast",
    r"weather update|storm|heatwave|cold wave|frost",
    r"mausam kaisa|monsoon|season forecast",
  ],
  "harvest": [
    r"harvest time|when to harvest|कटाई|harvesting",
    r"crop ready|harvest stage|maturity|cutting time|harvest period",
    r"when.*cut|time.*harvest|crop.*mature",
  ],
  "pesticide": [
    r"pesticide|spray|insecticide|medicine for crop",
    r"which pesticide|best spray|chemical spray",
    r"fungicide|herbicide|weedicide|spray schedule|pest control",
  ],
  "soil": [
    r"soil type|soil health|soil test|soil ph|soil erosion",
    r"best soil|land preparation|soil fertility|soil quality",
    r"mitti|soil nutrient|erosion|soil.*conserv|conserv.*soil",
    r"sandy soil|clay soil|loamy|black soil|red soil",
  ],
  "seed": [
    r"seed|beej|seed quality|seed treatment|seed rate",
    r"best seeds|hybrid seed|certified seed|seed selection",
  ],
  "equipment": [
    r"tractor|machine|equipment|tool|farm machinery",
    r"agri tools|harvester|sprayer machine|drill machine",
  ],
  "transport": [
    r"transport|transportation|carry crop|logistics",
    r"how to transport|market transport|vehicle for crop",
  ],
  "profit": [
    r"profit|income|earning|how to earn|increase income|farm profit",
    r"best crop for profit|most profitable|return from farming",
  ],
  "organic": [
    r"organic farming|natural farming|chemical free",
    r"organic fertilizer|bio farming|natural method|zero budget",
  ],
  "composting": [
    r"compost|vermicompost|biofertilizer|organic waste|farm waste",
    r"compost.*make|make.*compost|vermi",
  ],
  "storage": [
    r"storage|store.*crop|warehouse|cold storage|silo",
    r"post harvest|after harvest|kaise rakhe|how to store",
  ],
}
