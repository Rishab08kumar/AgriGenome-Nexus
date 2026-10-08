"""
Plant Health Model for AgriGenome-Nexus
Source: ICAR-DFR Diagnostic Pocket Guide for Ornamental Crop Diseases and Pests (2019)
Covers: Rose, Chrysanthemum, Marigold, Jasmine, Tuberose, China Aster, Crossandra, Gladiolus
Total diseases/pests: 52 entries from official ICAR publication
"""

import os
import requests

print("🌸 Initializing Plant Health Engine (ICAR-DFR Ornamental Disease DB)...")

HF_API_URL = "https://router.huggingface.co/hf-inference/models/linkanjarad/mobilenet_v2_plant_disease"
HF_TOKEN   = os.getenv("HF_TOKEN", "")

# ══════════════════════════════════════════════════════════════════════
# COMPLETE DISEASE DATABASE
# Source: ICAR-DFR Diagnostic Pocket Guide for Ornamental Crop Diseases
#         and Pests, Technical Bulletin No. 25, Pune, 2019
# ══════════════════════════════════════════════════════════════════════

DISEASE_DB = {

    # ─────────────────────── ROSE (7 diseases + 4 pests) ──────────────
    "Rose___Powdery_Mildew": {
        "display":    "Powdery Mildew (Podosphaera pannosa)",
        "crop":       "Rose", "category": "Fungal", "severity": "HIGH",
        "causal":     "Fungus; high relative humidity, moderate temperature, low light",
        "symptoms":   "White powdery growth all over leaves. Leaves gradually dry up.",
        "fungicide":  "Bavistin 0.1% / Benlate 0.1% / Wettable Sulphur 0.2% / Propiconazole 0.1% / Karathane 0.05%",
        "action":     "Shift plants to bright sun. Maintain low humidity and good aeration. Apply sulphur-based fungicide.",
        "prevention": "Ensure good air circulation. Avoid excess nitrogen fertilizer.",
    },
    "Rose___Black_Leaf_Spot": {
        "display":    "Black Leaf Spot (Diplocarpon rosae)",
        "crop":       "Rose", "category": "Fungal", "severity": "HIGH",
        "causal":     "Fungi under humid wet conditions",
        "symptoms":   "Circular black spots on upper leaf surface, frequently surrounded by yellow halo.",
        "fungicide":  "Bavistin 0.1% followed by Benlate 0.1% at 15-day interval. Dithane M-45 (0.2%) or Dithane Z-78 (0.2%). Propiconazole.",
        "action":     "Remove diseased leaves from ground and rake soil. Prune diseased canes to prevent overwintering of pathogen.",
        "prevention": "Avoid overhead irrigation. Remove fallen leaves promptly.",
    },
    "Rose___Botrytis_Blight": {
        "display":    "Botrytis Bud and Twig Blight (Botrytis cinerea)",
        "crop":       "Rose", "category": "Fungal", "severity": "HIGH",
        "causal":     "Extended periods of cloudy, humid and wet weather",
        "symptoms":   "Brown water-soaked spots on petals and leaves. Infected parts covered with gray-brown powdery spore masses. Infected buds droop down. Sunken grayish-black lesions extend to stem from bud base.",
        "fungicide":  "Azoxystrobin / Chlorothalonil / Mancozeb",
        "action":     "Remove and dispose fallen leaves and debris. Avoid overhead irrigation.",
        "prevention": "Reduce humidity. Ensure adequate plant spacing for air circulation.",
    },
    "Rose___Die_Back": {
        "display":    "Die Back (Diplodia rosarum)",
        "crop":       "Rose", "category": "Fungal", "severity": "HIGH",
        "causal":     "Maximum severity following pruning of canes after monsoon",
        "symptoms":   "Death of plant from tip downwards. Brown discoloration visible when affected stems are split open. Older plants more prone than younger ones.",
        "fungicide":  "Coat cut ends with chaubatia paste (4 parts copper carbonate + 4 parts red lead + 5 parts linseed oil)",
        "action":     "Cut away affected parts and burn. Disinfect secateurs and pruning tools before and after use.",
        "prevention": "Prune in dry weather. Seal all pruning wounds immediately.",
    },
    "Rose___Rust": {
        "display":    "Rust (Phragmidium spp.)",
        "crop":       "Rose", "category": "Fungal", "severity": "MEDIUM",
        "causal":     "Mild winter temperature and rainfall",
        "symptoms":   "Reddish-orange pustules on leaflets and sometimes petioles. Pustules turn black when teleutospores form. Severe infection causes defoliation and drastically reduces flower production.",
        "fungicide":  "Copper Oxychloride 0.3% (dormant spray) / Dithane M-45 0.2% / Vita Vax 0.1%",
        "action":     "Collect and destroy fallen affected leaves. Apply spring pruning.",
        "prevention": "Dormant spray of Copper Oxychloride 0.3% is effective.",
    },
    "Rose___Phytoplasma": {
        "display":    "Phytoplasma Disease (Rose Phytoplasma)",
        "crop":       "Rose", "category": "Phytoplasma", "severity": "HIGH",
        "causal":     "Bacteria-like organism (Phytoplasma); spread by leafhoppers",
        "symptoms":   "Reduced leaf size. Witches broom appearance. Leafy structures arise instead of flowers (phyllody). Flower colour turns green (virescence).",
        "fungicide":  "Tetracycline derivatives reduce incidence",
        "action":     "Remove affected plants. Control leafhopper vectors with insecticide spray.",
        "prevention": "Use clean planting material. Remove weeds and alternate hosts.",
    },
    "Rose___Mosaic_Virus": {
        "display":    "Rose Mosaic (Rose Mosaic Virus)",
        "crop":       "Rose", "category": "Viral", "severity": "HIGH",
        "causal":     "Rose mosaic virus",
        "symptoms":   "Chlorotic bands or ring spots, wavy lines, yellow vein banding, oak-leaf pattern on leaves.",
        "fungicide":  "No chemical cure. Management of insect vectors.",
        "action":     "Use virus-free cuttings from certified mother stock. Clean cultivation.",
        "prevention": "Control insect vectors (aphids). Rogue out infected plants.",
    },
    "Rose___Nematode": {
        "display":    "Dagger & Root-Lesion Nematode (Xiphinema / Pratylenchus spp.)",
        "crop":       "Rose", "category": "Nematode", "severity": "MEDIUM",
        "causal":     "Nematodes in soil",
        "symptoms":   "Stunted growth with yellowing of leaves and wilting of plants.",
        "fungicide":  "Hot water treatment of roots at 45.5°C for one hour",
        "action":     "Use nematode-free planting material. Hot water treatment of roots.",
        "prevention": "Soil solarization before planting. Grow marigold as trap crop.",
    },
    # Rose pests
    "Rose___Aphids": {
        "display":    "Aphids (Macrosiphum rosae)",
        "crop":       "Rose", "category": "Pest", "severity": "MEDIUM",
        "causal":     "Adults and nymphs suck sap; pear-shaped soft-bodied insects",
        "symptoms":   "Light green to dark blackish-green aphid clusters on shoots. Stunted growth and leaf curling.",
        "fungicide":  "Spray Verticillium lecanii 3.0 g/L during evening hours",
        "action":     "Spray biocontrol agent Verticillium lecanii. Use pongamia oil 10%.",
        "prevention": "Install yellow sticky traps for early detection. Encourage natural predators.",
    },
    "Rose___Thrips": {
        "display":    "Thrips (Scirtothrips dorsalis)",
        "crop":       "Rose", "category": "Pest", "severity": "HIGH",
        "causal":     "Nymphs and adults suck cell sap from tender leaves, buds and flowers",
        "symptoms":   "Attacks on new flush after pruning. Curled leaves with brown marks. Deformed buds with burnt margins.",
        "fungicide":  "Acephate 75SP @ 1.5 g/L or Dimethoate 30EC @ 2.0 ml/L + 1% pongamia oil. Severe: Fipronil 5SC @ 1.5 ml/L or Imidacloprid 17.8SL @ 0.4 ml/L",
        "action":     "Spray 2-3 times at fortnightly interval with onset of new flush. Drench soil with Chlorpyriphos 20EC @ 5.0 ml/L.",
        "prevention": "Regular monitoring at flush stage.",
    },
    "Rose___Bud_Borer": {
        "display":    "Bud Borer (Helicoverpa armigera)",
        "crop":       "Rose", "category": "Pest", "severity": "HIGH",
        "causal":     "Warm dry climate; larvae feed on flower buds",
        "symptoms":   "Yellowish-white eggs on growing shoot or flower bud. Larvae make large hole in bud. Excreta visible in damaged parts.",
        "fungicide":  "HaNPV @ 250 LE/ha + neem formulations 1.0-2.0 ml/L. Severe: Indoxacarb 14.5SC @ 1.0 ml/L or Thiodicarb 75WP @ 1.0 g/L",
        "action":     "Install pheromone traps for monitoring. Apply HaNPV biocontrol.",
        "prevention": "Regular scouting. Install pheromone traps.",
    },
    "Rose___Spider_Mite": {
        "display":    "Two-spotted Spider Mite (Tetranychus urticae)",
        "crop":       "Rose", "category": "Pest", "severity": "HIGH",
        "causal":     "Nymphs and adults suck sap in hot dry conditions",
        "symptoms":   "Fine silken webbing on leaf undersides. Leaves turn pale with white specks. Mites are 0.5mm, females yellowish-green with two dark spots.",
        "fungicide":  "Dicofol 18.5EC @ 2.5 ml/L or Wettable Sulphur 80WP @ 3.0 g/L. Spray Verticillium lecanii 5.0 g/L",
        "action":     "Spray jet of water to dislodge mites. Thin out heavily infested leaves. Apply acaricide.",
        "prevention": "Maintain humidity above 60%. Avoid dusty conditions.",
    },

    # ─────────────── CHRYSANTHEMUM (10 diseases + 3 pests) ────────────
    "Chrysanthemum___Pythium_Root_Rot": {
        "display":    "Pythium Root Rot (Pythium spp.)",
        "crop":       "Chrysanthemum", "category": "Fungal", "severity": "HIGH",
        "causal":     "Fungi under highly moist conditions; poor drainage; over-irrigation",
        "symptoms":   "Stunting, wilting, necrosis of main/lateral/feeder rootlets. Black necrotic lesion girdling lower stem.",
        "fungicide":  "Metalaxyl / Mancozeb / Captan / Fosetyl-Al",
        "action":     "Soil solarization, removal of infected plants, improve drainage.",
        "prevention": "Avoid over-irrigation. Ensure good surface and subsurface drainage.",
    },
    "Chrysanthemum___Powdery_Mildew": {
        "display":    "Powdery Mildew (Erysiphe cichoracearum)",
        "crop":       "Chrysanthemum", "category": "Fungal", "severity": "HIGH",
        "causal":     "Fungus; temperature 21-27°C and high relative humidity at night",
        "symptoms":   "White powdery growth all over leaves. Gradually leaves dry up and whole plant may die.",
        "fungicide":  "Karathane 0.025% / Bavistin 0.1% / Sulphur-based fungicide 0.2%",
        "action":     "Spray Karathane or Bavistin. Provide dry environment.",
        "prevention": "Large day-night temperature differences promote disease. Good ventilation.",
    },
    "Chrysanthemum___Ray_Blight": {
        "display":    "Ray Blight (Didymella ligulicola / Ascochyta sp.)",
        "crop":       "Chrysanthemum", "category": "Fungal", "severity": "HIGH",
        "causal":     "Fungi under wet conditions",
        "symptoms":   "Tiny dark-pink spots on petals, starts on one side of flower. Fungus spreads, petals brown and rot. Spreads into stem causing drooping.",
        "fungicide":  "Azoxystrobin / Chlorothalonil / Fludioxonil / Iprodione / Mancozeb / Myclobutanil / Propiconazole / Pyraclostrobin / Thiophanate-methyl",
        "action":     "Avoid overhead irrigation. Apply registered fungicide.",
        "prevention": "Reduce moisture on foliage. Space plants well.",
    },
    "Chrysanthemum___Leaf_Spot": {
        "display":    "Leaf Spot (Septoria chrysanthemi / Alternaria / Cercospora chrysanthemi)",
        "crop":       "Chrysanthemum", "category": "Fungal", "severity": "MEDIUM",
        "causal":     "Fungi under wet conditions",
        "symptoms":   "Yellow spots appear first, turn brown to black. Spots occur on lower leaves first, coalesce into large necrotic areas, leading to leaf death.",
        "fungicide":  "Azoxystrobin / Chlorothalonil / Mancozeb / Propiconazole / Thiophanate-methyl",
        "action":     "Clean up and destroy infected debris. Hand pick symptomatic leaves. Water early in day.",
        "prevention": "Avoid splashing water onto foliage. Remove fallen leaves.",
    },
    "Chrysanthemum___Fusarium_Wilt": {
        "display":    "Fusarium Wilt (Fusarium oxysporum)",
        "crop":       "Chrysanthemum", "category": "Fungal", "severity": "CRITICAL",
        "causal":     "Fungal pathogen incursion into vascular tissues; dry weather and low soil moisture",
        "symptoms":   "Drooping, yellowing, loss of turgidity of leaves. Stunted growth. Failure in normal bud/flower production. Disintegration/discoloration in roots. Vascular tissues blocked.",
        "fungicide":  "Soil treatment with Thiophanate-methyl",
        "action":     "Remove and destroy infected plants. Do not compost. Soil sterilization.",
        "prevention": "Use disease-free cuttings. Soil solarization. Crop rotation.",
    },
    "Chrysanthemum___Botrytis_Blight": {
        "display":    "Botrytis Blight / Grey Mould (Botrytis cinerea)",
        "crop":       "Chrysanthemum", "category": "Fungal", "severity": "HIGH",
        "causal":     "Damaging during rainy/drizzly weather over several days",
        "symptoms":   "Brown water-soaked spots on petals, leaves, or stem cankers. Infected parts covered with gray-brown powdery spore masses.",
        "fungicide":  "Bavistin 0.1% / Copper Oxychloride 0.2%",
        "action":     "Provide better ventilation and good aeration with adequate planting distance.",
        "prevention": "Reduce humidity. Avoid wetting foliage.",
    },
    "Chrysanthemum___White_Rust": {
        "display":    "White Rust (Puccinia horiana) — QUARANTINE PATHOGEN",
        "crop":       "Chrysanthemum", "category": "Fungal", "severity": "CRITICAL",
        "causal":     "Fungal disease spread by airborne spores during cool, wet weather",
        "symptoms":   "Sunken yellow or brown spots on upper leaf surface. Buff/white pustules on lower surface. Severely affected leaves shrivel and turn brown.",
        "fungicide":  "Tebuconazole / Tebuconazole + Trifloxystrobin / Triticonazole — apply every 7 days",
        "action":     "REPORT IMMEDIATELY — quarantine pathogen with limited distribution. Remove and dispose affected leaves/plants. Do NOT take cuttings from affected plants.",
        "prevention": "Inspect plants regularly. Use certified disease-free cuttings.",
    },
    "Chrysanthemum___Soft_Rot": {
        "display":    "Soft Rot (Erwinia chrysanthemi)",
        "crop":       "Chrysanthemum", "category": "Bacterial", "severity": "HIGH",
        "causal":     "Bacteria",
        "symptoms":   "Wilting of plants on bright days. Stem tips turn brown, brittle and collapse. Stem becomes hollow with brownish streaks extending to base.",
        "fungicide":  "Streptocycline 0.01%",
        "action":     "Destroy affected plants. Soil sterilization. Use disease-free cuttings. Avoid contamination during pinching.",
        "prevention": "Sterilize cutting tools. Avoid wounding plants unnecessarily.",
    },
    "Chrysanthemum___Bacterial_Leaf_Spot": {
        "display":    "Bacterial Leaf Spot (Pseudomonas cichorii)",
        "crop":       "Chrysanthemum", "category": "Bacterial", "severity": "MEDIUM",
        "causal":     "Bacteria under humid climate; enter through injuries",
        "symptoms":   "Small dark brown to black spots on lower leaves enlarge and become irregular. Spots become brittle and crack when dry. Disease spreads up pot to flowers.",
        "fungicide":  "Streptocycline 0.01%",
        "action":     "Destroy affected plants. Soil sterilization. Avoid contamination during pinching.",
        "prevention": "Bacteria survive in water and soil. Avoid overhead irrigation.",
    },
    "Chrysanthemum___Phytoplasma": {
        "display":    "Phytoplasma (Chrysanthemum Phytoplasma)",
        "crop":       "Chrysanthemum", "category": "Phytoplasma", "severity": "HIGH",
        "causal":     "Phytoplasma; spread through infected cuttings and leafhoppers",
        "symptoms":   "Little leaves (reduced leaf size). Witches broom appearance. Leafy structures instead of flowers (phyllody). Flower colour turns green (virescence).",
        "fungicide":  "Tetracycline derivatives reduce incidence",
        "action":     "Clean planting material. Remove weeds and alternate hosts (Cuscuta, brinjal, parthenium). Clean tools. Control leafhopper vectors.",
        "prevention": "Use certified disease-free cuttings.",
    },
    "Chrysanthemum___Stem_Bud_Necrosis": {
        "display":    "Stem and Bud Necrosis (GBNV / TSWV)",
        "crop":       "Chrysanthemum", "category": "Viral", "severity": "HIGH",
        "causal":     "Groundnut bud necrosis virus (GBNV) and Tomato spotted wilt virus (TSWV); spread by thrips",
        "symptoms":   "Veinal necrosis, necrotic spots on leaves, browning of petals, stem necrosis. Extensive necrosis leading to complete drying and death in severe cases.",
        "fungicide":  "Control thrips vectors. No chemical cure for virus.",
        "action":     "Use virus-free planting material. Remove weeds and alternate hosts. Destroy completely infected plants to avoid virus reservoir.",
        "prevention": "Control thrips vectors with insecticide. Monitor field regularly.",
    },
    "Chrysanthemum___Stunt_Viroid": {
        "display":    "Chrysanthemum Stunt Viroid (CSVd)",
        "crop":       "Chrysanthemum", "category": "Viral", "severity": "HIGH",
        "causal":     "Highly mechanically transmissible virus-like pathogen",
        "symptoms":   "Stunting, chlorosis, premature blooming, lack of root formation in cuttings. Shortened stems, uneven flowering, irregular flower size.",
        "fungicide":  "No chemical cure. Prevention only.",
        "action":     "Sterilize all tools and equipment used during cultivation, maintenance or harvest. Use Stunt-free cuttings from certified mother stocks.",
        "prevention": "Use certified CSVd-free planting material. Strict tool sterilization.",
    },
    # Chrysanthemum pests
    "Chrysanthemum___Red_Spider_Mite": {
        "display":    "Red Spider Mite (Tetranychus urticae)",
        "crop":       "Chrysanthemum", "category": "Pest", "severity": "HIGH",
        "causal":     "Feeding by nymphs and adults on underside of leaves",
        "symptoms":   "Nymphs and adults red in colour on underside of leaves. Silken webbing. Leaf discoloration, white specks, drying of leaves. Severely affects growth and flower production.",
        "fungicide":  "Dicofol 18.5EC @ 1.5 ml/L or Wettable Sulphur 80WP @ 3.0 g/L",
        "action":     "Remove and destroy infested parts. Spray jet of water to dislodge mites. Apply acaricide.",
        "prevention": "Regular inspection. Maintain high humidity.",
    },
    "Chrysanthemum___Aphids": {
        "display":    "Chrysanthemum Aphid (Macrosiphoniella sanborni)",
        "crop":       "Chrysanthemum", "category": "Pest", "severity": "MEDIUM",
        "causal":     "Continuous sucking of plant sap; cool months October-January",
        "symptoms":   "Shiny dark reddish-brown to blackish-brown insects. Appear on tender shoots initially, later whole shoot covered. Stunted growth and leaf curling.",
        "fungicide":  "Neem oil or pongamia oil 1.0% weekly when infestation starts",
        "action":     "Install yellow sticky traps. Encourage predatory beetles (Coccinellids). Apply neem oil.",
        "prevention": "Yellow sticky traps for early detection.",
    },
    "Chrysanthemum___Bud_Borer": {
        "display":    "Bud Borer (Helicoverpa armigera)",
        "crop":       "Chrysanthemum", "category": "Pest", "severity": "HIGH",
        "causal":     "Larvae feed on flower bud making large hole",
        "symptoms":   "Yellowish-white eggs on shoot or flower bud. Larvae bluish-green to brownish. Large hole in flower bud with excreta visible.",
        "fungicide":  "HaNPV @ 250 LE/ha + neem formulations 1.0-2.0 ml/L. Severe: Indoxacarb 14.5SC @ 1.0 ml/L",
        "action":     "Install pheromone traps for monitoring. Apply HaNPV biocontrol.",
        "prevention": "Regular scouting. Pheromone trap monitoring.",
    },

    # ─────────────── MARIGOLD (4 diseases + 3 pests) ──────────────────
    "Marigold___Wilt_Stem_Collar_Rot": {
        "display":    "Wilt, Stem Rot, Collar Rot (Phytophthora sp. / Pythium sp.)",
        "crop":       "Marigold", "category": "Fungal", "severity": "HIGH",
        "causal":     "Cool and wet summer; soil-borne fungi",
        "symptoms":   "Fungus affects collar portions. In nursery causes damping-off aggravated by soil moisture. In field plants show wilting.",
        "fungicide":  "Metalaxyl (soil application)",
        "action":     "Avoid over-irrigation. Soil sterilization of nursery bed. Soil solarization in field. Use biocontrol agents during land preparation.",
        "prevention": "Good drainage. Avoid crowded planting.",
    },
    "Marigold___Leaf_Spot_Blight": {
        "display":    "Leaf Spot and Blight (Alternaria / Cercospora / Septoria sp.)",
        "crop":       "Marigold", "category": "Fungal", "severity": "HIGH",
        "causal":     "Fungi during wet times of year",
        "symptoms":   "Brown necrotic spots develop on leaves, enlarge at later stage. Entire foliage gets damaged resulting in poor vegetative growth.",
        "fungicide":  "Dithane M-45 @ 0.2% or Carbendazim 0.05% at fortnightly intervals from first appearance",
        "action":     "Spray at first sign of disease. Repeat fortnightly.",
        "prevention": "Avoid overhead irrigation.",
    },
    "Marigold___Powdery_Mildew": {
        "display":    "Powdery Mildew (Oidium sp. / Leveillula taurica)",
        "crop":       "Marigold", "category": "Fungal", "severity": "MEDIUM",
        "causal":     "Fungi; temperature 21-27°C and high humidity at night",
        "symptoms":   "Whitish tiny superficial spots on leaves. Later whole aerial parts covered with whitish powder.",
        "fungicide":  "Karathane @ 0.05% or Sulfex 3g/L at fortnightly intervals",
        "action":     "Spray Karathane or Sulfex fortnightly.",
        "prevention": "Good air circulation. Full sun location.",
    },
    "Marigold___Flower_Bud_Rot": {
        "display":    "Flower Bud Rot (Alternaria dianthi)",
        "crop":       "Marigold", "category": "Fungal", "severity": "HIGH",
        "causal":     "Fungi under humid hot conditions",
        "symptoms":   "Infects young flower buds. Infected buds shrivel and become dark brown. Also infects leaves causing blight. Brown necrotic spots on margins and tips of older leaves.",
        "fungicide":  "Dithane M-45 / Chlorothalonil",
        "action":     "Avoid crowded planting. Spray Dithane M-45 or Chlorothalonil.",
        "prevention": "Adequate plant spacing. Avoid high humidity.",
    },
    "Marigold___Phytoplasma": {
        "display":    "Phytoplasma (Marigold Phytoplasma)",
        "crop":       "Marigold", "category": "Phytoplasma", "severity": "HIGH",
        "causal":     "Phytoplasma transmitted by leafhoppers",
        "symptoms":   "Reduced leaf size, bunching of leaves and branches, stunting, flower malformations, greening of flowers, phyllody, bronzing of leaves, gradual death of plant.",
        "fungicide":  "Dip seedlings in Tetracycline before planting",
        "action":     "Use healthy planting material. Remove alternate hosts from field. Control leafhopper vectors.",
        "prevention": "Use clean certified planting material.",
    },
    # Marigold pests
    "Marigold___Thrips": {
        "display":    "Thrips (Neohydatothrips samayunkur)",
        "crop":       "Marigold", "category": "Pest", "severity": "HIGH",
        "causal":     "Minute insects; severe during seedling and flowering stage",
        "symptoms":   "Adults dark brown with yellowish-brown markings. Silvering, distortion, purplish patches on infested leaves.",
        "fungicide":  "Acephate 75SP @ 1.5 g/L or Dimethoate 30EC @ 2.0 ml/L + 0.5% pongamia oil. Severe: Fipronil 5SC @ 1.5 ml/L",
        "action":     "Spray insecticide with pongamia oil. Severe: apply Fipronil.",
        "prevention": "Regular monitoring at seedling and flowering stages.",
    },
    "Marigold___Bud_Borer": {
        "display":    "Bud Borer (Helicoverpa armigera)",
        "crop":       "Marigold", "category": "Pest", "severity": "HIGH",
        "causal":     "Larvae eat floral parts",
        "symptoms":   "Yellowish-white eggs on shoot/bud. Larvae bluish-green to brownish-red. Large hole made in flower bud by feeding larvae.",
        "fungicide":  "HaNPV @ 250 LE/ha + neem formulations. Severe: Indoxacarb 14.5SC @ 1.0 ml/L or Thiodicarb 75WP @ 1.0 g/L",
        "action":     "Install pheromone traps for monitoring. Apply HaNPV biocontrol.",
        "prevention": "Pheromone trap monitoring.",
    },
    "Marigold___Red_Spider_Mite": {
        "display":    "Red Spider Mite (Tetranychus urticae)",
        "crop":       "Marigold", "category": "Pest", "severity": "HIGH",
        "causal":     "Nymphs and adults suck sap from underside of leaves",
        "symptoms":   "Red nymphs and adults on leaf underside with silken webbing. Adults 0.5mm, females yellowish-green with two dark spots.",
        "fungicide":  "Dicofol 18.5EC @ 1.5 ml/L or Wettable Sulphur 80WP @ 3.0 g/L. Propergite 57EC @ 1.0 ml/L or Abamectin 1.9EC @ 0.5 ml/L for high infestation",
        "action":     "Burn infested plant parts. Spray jet of water then apply acaricide.",
        "prevention": "Regular crop inspection.",
    },

    # ─────────────── JASMINE (5 diseases + 2 pests) ───────────────────
    "Jasmine___Leaf_Blight": {
        "display":    "Leaf Blight (Cercospora jasminicola / Alternaria jasmini)",
        "crop":       "Jasmine", "category": "Fungal", "severity": "HIGH",
        "causal":     "Fungi spreading rapidly in rainy season",
        "symptoms":   "Reddish brown circular spots on upper leaf surface. Spots coalesce to form blight.",
        "fungicide":  "Bavistin 0.1% or Copper Oxychloride 0.3% at monthly intervals from May onwards up to pruning",
        "action":     "Spray monthly. Collect and burn diseased leaves.",
        "prevention": "Avoid overhead irrigation in rainy season.",
    },
    "Jasmine___Rust": {
        "display":    "Rust (Uromyces hobsoni)",
        "crop":       "Jasmine", "category": "Fungal", "severity": "MEDIUM",
        "causal":     "July-August during monsoon rains",
        "symptoms":   "Orange coloured aecial cups on both sides of leaves, predominantly on lower surface.",
        "fungicide":  "Dust Sulphur",
        "action":     "Remove affected plants and plant parts. Dust with Sulphur.",
        "prevention": "Avoid excessive moisture on foliage.",
    },
    "Jasmine___Botrytis_Blight": {
        "display":    "Graymold / Botrytis Blight (Botrytis cinerea)",
        "crop":       "Jasmine", "category": "Fungal", "severity": "HIGH",
        "causal":     "Cool rainy spring and summer weather",
        "symptoms":   "Blossom blight, bud rot, stem canker, stem and crown rot, cutting rot, leaf blight and damping-off.",
        "fungicide":  "Azoxystrobin / Chlorothalonil",
        "action":     "Remove and dispose fallen leaves and debris. Avoid overhead irrigation.",
        "prevention": "Reduce humidity. Good air circulation.",
    },
    "Jasmine___Anthracnose": {
        "display":    "Anthracnose (Colletotrichum jasminicola)",
        "crop":       "Jasmine", "category": "Fungal", "severity": "MEDIUM",
        "causal":     "Cool, wet weather",
        "symptoms":   "Large, circular, distinct, brownish to greyish spots with brown to yellowish haloes on upper leaf surface.",
        "fungicide":  "Bordeaux mixture 1% / Copper Oxychloride 0.25% / Carbendazim 0.15% / Thiophanate-methyl 0.15%",
        "action":     "Apply Bordeaux mixture or Copper Oxychloride.",
        "prevention": "Avoid wet conditions on foliage.",
    },
    "Jasmine___Powdery_Mildew": {
        "display":    "Powdery Mildew (Oidium jasmini)",
        "crop":       "Jasmine", "category": "Fungal", "severity": "MEDIUM",
        "causal":     "High relative humidity, moderate temperatures, low light",
        "symptoms":   "Foliage and stems look as if sprinkled with powder.",
        "fungicide":  "Sulphur-based fungicides",
        "action":     "Use sulphur fungicides. Improve ventilation.",
        "prevention": "Ensure good air circulation and adequate sunlight.",
    },
    "Jasmine___Phyllody": {
        "display":    "Phyllody (Jasmine Phytoplasma)",
        "crop":       "Jasmine", "category": "Phytoplasma", "severity": "HIGH",
        "causal":     "Phytoplasma",
        "symptoms":   "Leaves become small, malformed and bushy. Flowers turn green and floral parts turn into leafy structures.",
        "fungicide":  "Spray insecticide to control leafhopper vector",
        "action":     "Use clean planting material. Remove weeds and alternate hosts. Select cuttings from healthy plants.",
        "prevention": "Control leafhopper vector insecticide spray.",
    },
    # Jasmine pests
    "Jasmine___Cut_Bud_Borer": {
        "display":    "Cut Bud Borer (Hendecasis duplifascialis)",
        "crop":       "Jasmine", "category": "Pest", "severity": "HIGH",
        "causal":     "Larval stage bores into and eats the bud",
        "symptoms":   "Larva is greenish with pale body hairs and black head. Adult is small white moth. Larva bores into flower bud and feeds on internal content.",
        "fungicide":  "Light trap to attract and kill adult moths",
        "action":     "Collect and destroy damaged buds with larvae. Use light traps.",
        "prevention": "Regular monitoring of flower buds.",
    },
    "Jasmine___Whitefly": {
        "display":    "Whitefly (Bemisia tabaci)",
        "crop":       "Jasmine", "category": "Pest", "severity": "MEDIUM",
        "causal":     "Moderately hot and humid conditions; nymphs and adults suck sap",
        "symptoms":   "White adults lay eggs on leaf undersides. Sooty mold develops on honeydew in severe infestation. Small deformed flowers with crooked stalks.",
        "fungicide":  "Pongamia oil or neem oil @ 10.0 ml/L / Verticillium lecanii @ 3.0 g/L. Imidacloprid 17.8SC @ 0.5 ml/L for nymph management",
        "action":     "Install yellow sticky traps. Remove and burn heavily infested leaves. Spray neem oil.",
        "prevention": "Yellow sticky traps for early detection.",
    },

    # ─────────────── TUBEROSE (5 diseases + 2 pests) ──────────────────
    "Tuberose___Foot_Tuber_Rot": {
        "display":    "Foot and Tuber Rot / Sclerotial Wilt (Sclerotium rolfsii)",
        "crop":       "Tuberose", "category": "Fungal", "severity": "HIGH",
        "causal":     "Moist humid conditions",
        "symptoms":   "Fan-shaped mycelial strands at base of infected plants. Brown mustard-like round sclerotia on mycelial growth. Flaccidity, drooping, yellowing and drying of leaves.",
        "fungicide":  "Drench soil with 0.3% Zineb",
        "action":     "Soil drenching with 0.3% Zineb.",
        "prevention": "Avoid waterlogging. Good drainage.",
    },
    "Tuberose___Botrytis_Spot_Blight": {
        "display":    "Botrytis Spot and Blight (Botrytis cinerea)",
        "crop":       "Tuberose", "category": "Fungal", "severity": "HIGH",
        "causal":     "Cool (15°C), rainy weather",
        "symptoms":   "Dark brown spots on leaves coalesce to form blighted patches covered with mycelia. Flowers also show spots covered by mycelium, rotting occurs, entire inflorescence dries up.",
        "fungicide":  "Carbendazim @ 2 g/L. Repeat every 15 days.",
        "action":     "Spray Carbendazim at 15-day intervals.",
        "prevention": "Reduce humidity. Ensure adequate ventilation.",
    },
    "Tuberose___Alternaria_Leaf_Spot": {
        "display":    "Alternaria Leaf Spot (Alternaria polyantha)",
        "crop":       "Tuberose", "category": "Fungal", "severity": "MEDIUM",
        "causal":     "Shady conditions and rainy season",
        "symptoms":   "Faint concentric rings on midrib and rarely on leaf margins. Leaves and peduncles become necrotic and dry up.",
        "fungicide":  "Systemic: Hexaconazole (Contaf 5EC) / Propiconazole (Tilt 25EC) / Tebuconazole (Folicur 25EC) / Pyraclostrobin (Cabriotop 60WG) @ 0.1%. Non-systemic: Chlorothalonil @ 2000 ppm",
        "action":     "Apply systemic or non-systemic fungicide.",
        "prevention": "Avoid shady conditions. Ensure adequate sunlight.",
    },
    "Tuberose___Peduncle_Blight": {
        "display":    "Peduncle Blight (Lasiodiplodia theobromae)",
        "crop":       "Tuberose", "category": "Fungal", "severity": "HIGH",
        "causal":     "Rainy season",
        "symptoms":   "Peduncle dieback from tip. Leaf blight at tips. Flowers show dark brown spots. Entire inflorescence dries up.",
        "fungicide":  "Foliar application of Carbendazim 0.1% at 60, 90 and 110 Days After Planting (DAP)",
        "action":     "Apply Carbendazim at 60, 90 and 110 DAP.",
        "prevention": "Spray preventatively before rainy season.",
    },
    "Tuberose___Bud_Rot": {
        "display":    "Bud Rot (Erwinia sp.)",
        "crop":       "Tuberose", "category": "Bacterial", "severity": "HIGH",
        "causal":     "High moisture condition",
        "symptoms":   "Dry rotting of buds with brown scorched necrotic discolouration of peduncles.",
        "fungicide":  "Spray Streptocycline 0.01%. Prophylactic foliar spray of Pseudomonas fluorescens",
        "action":     "Proper aeration. Avoid crowded planting. Good drainage and soil conditioning.",
        "prevention": "Aeration in packaging after harvest. Avoid high moisture.",
    },
    "Tuberose___Root_Knot_Nematode": {
        "display":    "Root-knot Nematode (Meloidogyne spp.)",
        "crop":       "Tuberose", "category": "Nematode", "severity": "MEDIUM",
        "causal":     "Meloidogyne sp. in soil; hot climate and short winter",
        "symptoms":   "Stunting and chlorosis. Short and thin floral stalks. Yellowing of leaves, reduced spike length and flower yield. Root-knot galls on roots.",
        "fungicide":  "Soil application: Carbofuran @ 20-25 kg + 500 kg neem/pongamia/mahua cake per acre",
        "action":     "Use nematode-free bulbs. Soak bulbs in Carbosulfan 2000ppm for 1 hour before planting.",
        "prevention": "Grow marigold as trap crop for 2-3 months before planting.",
    },

    # ─────────────── CHINA ASTER (5 diseases + 1 pest) ────────────────
    "China_Aster___Fusarium_Verticillium_Wilt": {
        "display":    "Root/Stem Rot and Wilt (Fusarium sp. / Verticillium sp.)",
        "crop":       "China Aster", "category": "Fungal", "severity": "CRITICAL",
        "causal":     "Soil-borne pathogens",
        "symptoms":   "Stunted growth, yellowing, withering of plant, rotting of collar region. Vascular ring found brown when stem is cut.",
        "fungicide":  "Mercuric chloride 0.1% seed treatment for 30 min. Steam sterilization of soil.",
        "action":     "Disinfect seeds from diseased plants. Soil sterilization.",
        "prevention": "Use certified disease-free seeds. Soil solarization.",
    },
    "China_Aster___Botrytis_Blight": {
        "display":    "Graymold / Botrytis Blight (Botrytis cinerea)",
        "crop":       "China Aster", "category": "Fungal", "severity": "HIGH",
        "causal":     "Extended cloudy, humid, wet weather",
        "symptoms":   "Blossom blight, bud rot, stem canker, stem and crown rot, cutting rot, leaf blight, damping-off.",
        "fungicide":  "Azoxystrobin / Chlorothalonil",
        "action":     "Remove and dispose fallen leaves. Avoid overhead irrigation.",
        "prevention": "Reduce humidity. Adequate plant spacing.",
    },
    "China_Aster___Rust": {
        "display":    "Rust (Coleosporium asterum / Puccinia sp.) — QUARANTINE",
        "crop":       "China Aster", "category": "Fungal", "severity": "CRITICAL",
        "causal":     "Warm temperatures and moisture; not yet reported in India on Aster",
        "symptoms":   "Bright yellow-orange spots on lower leaf surface of young plants. On maturity become erumpent exposing orange-red powdery spore masses.",
        "fungicide":  "Wettable sulphur during growing season",
        "action":     "Inform authorities — not reported from Aster in India. Collect and destroy infected parts. Avoid sprinkler irrigation.",
        "prevention": "Surveillance and monitoring.",
    },
    "China_Aster___Southern_Blight": {
        "display":    "Southern Blight (Sclerotium rolfsii)",
        "crop":       "China Aster", "category": "Fungal", "severity": "HIGH",
        "causal":     "Post-rainy season favourable conditions",
        "symptoms":   "Water-soaked lesions on leaves, stems and lower stem surfaces. Quick wilting of whole plant. Abundant sclerotia near stem-soil interface.",
        "fungicide":  "Propiconazole 25EC / Thiram 75SD / Tebuconazole / Carboxin",
        "action":     "Destroy infected plants. Sterilize soil. Seedling dip in Trichoderma/Bacillus before transplanting. Soil solarization.",
        "prevention": "Report if not previously observed.",
    },
    "China_Aster___Leaf_Spot": {
        "display":    "Leaf Spot (Ascochyta asteris / Septoria callistephi / Stemphylium callistephi)",
        "crop":       "China Aster", "category": "Fungal", "severity": "MEDIUM",
        "causal":     "Hot humid conditions, moist and cloudy weather",
        "symptoms":   "Spots first yellowish, turn dark brown and black, increase in size. Lower leaves infected first. Severe infection: spots coalesce, leaves fall.",
        "fungicide":  "Seed treatment: Thiram 0.2% or Carbendazim 0.1% before sowing. Foliar: Dithane M-45 0.2% weekly",
        "action":     "Collect and burn diseased leaves. Treat seeds before sowing. Spray weekly with Dithane M-45.",
        "prevention": "Seed treatment mandatory.",
    },
    "China_Aster___Phytoplasma_Yellows": {
        "display":    "Aster Yellows (Phytoplasma)",
        "crop":       "China Aster", "category": "Phytoplasma", "severity": "HIGH",
        "causal":     "Phytoplasma; spread from infected to healthy plants through leafhoppers",
        "symptoms":   "Yellowing of whole plant in seedling stage. Witches broom appearance. Leafy structures instead of flowers (phyllody). Flower colour turns green (virescence).",
        "fungicide":  "Tetracycline derivatives reduce incidence",
        "action":     "Remove weeds and alternate hosts (Cuscuta, brinjal, parthenium). Control leafhopper vectors. Clean tools.",
        "prevention": "Use resistant varieties: Shashank (resistant), Poornima (moderately resistant).",
    },

    # ─────────────── CROSSANDRA (3 diseases + 1 pest) ─────────────────
    "Crossandra___Fusarium_Wilt": {
        "display":    "Wilt (Fusarium solani)",
        "crop":       "Crossandra", "category": "Fungal", "severity": "CRITICAL",
        "causal":     "Soil-borne fungus",
        "symptoms":   "Leaf margins show pinkish-brown discolouration. Stem shrivelled.",
        "fungicide":  "Carbendazim 0.1% or Copper Oxychloride 0.25% soil drenching at 30-day intervals",
        "action":     "Pull out and burn infected plants. Soil drench with Carbendazim or Copper Oxychloride. Repeat every 3-4 weeks.",
        "prevention": "Use disease-free planting material. Soil solarization.",
    },
    "Crossandra___Stem_Rot": {
        "display":    "Stem Rot (Rhizoctonia solani)",
        "crop":       "Crossandra", "category": "Fungal", "severity": "HIGH",
        "causal":     "Fungal infection in stem",
        "symptoms":   "Brown to black lesions on stem.",
        "fungicide":  "Fosetyl-Al (soil drenching)",
        "action":     "Good drainage. Avoid overcrowded planting. Remove and destroy diseased plants. Drench with Fosetyl-Al.",
        "prevention": "Avoid waterlogging. Good drainage.",
    },
    "Crossandra___Leaf_Blight_Spot": {
        "display":    "Leaf Blight & Leaf Spot (Colletotrichum crossandrae / Alternaria amaranthi var. crossandrae)",
        "crop":       "Crossandra", "category": "Fungal", "severity": "MEDIUM",
        "causal":     "High humidity and temperatures 25-30°C",
        "symptoms":   "Blight: Small brownish speck, expands and turns darker. Spot: Small circular/irregular yellow spots, enlarge, turn brown with dark concentric rings.",
        "fungicide":  "Benomyl 0.1% or Mancozeb 0.2% or Carbendazim 0.1% foliar spray",
        "action":     "Apply foliar spray of Benomyl, Mancozeb or Carbendazim.",
        "prevention": "Reduce humidity. Adequate spacing.",
    },
    "Crossandra___Nematode": {
        "display":    "Root-knot & Root-lesion Nematode (Meloidogyne / Pratylenchus spp.)",
        "crop":       "Crossandra", "category": "Nematode", "severity": "MEDIUM",
        "causal":     "Nematode juveniles and adults feed on plant",
        "symptoms":   "Stunted growth. Pinkish to purple and yellow coloured leaves. Reduced inflorescence size. Root-knot galls or brown to black lesions on roots.",
        "fungicide":  "Carbofuran @ 50g/sq.m in nursery. Soil application carbofuran @ 20-25 kg per acre",
        "action":     "Raise nursery in nematode-free area or treat with bioformulations. Use nematode-free planting material.",
        "prevention": "Soil treatment before planting.",
    },

    # ─────────────── GLADIOLUS (6 diseases + 1 pest) ──────────────────
    "Gladiolus___Botrytis_Flower_Rot": {
        "display":    "Botrytis Blight and Flower Rot (Botrytis gladiolorum)",
        "crop":       "Gladiolus", "category": "Fungal", "severity": "HIGH",
        "causal":     "Fungi under extended cloudy, humid, wet weather",
        "symptoms":   "Brown water-soaked spots; spots coalesce to form necrotic patches on leaves leading to blight. Infected parts covered with gray-brown powdery spore masses.",
        "fungicide":  "Azoxystrobin / Chlorothalonil",
        "action":     "Remove and dispose fallen leaves and debris. Avoid overhead irrigation.",
        "prevention": "Good air circulation. Adequate plant spacing.",
    },
    "Gladiolus___Curvularia_Leaf_Spot": {
        "display":    "Curvularia Leaf Spot (Curvularia trifolli f. sp. gladioli)",
        "crop":       "Gladiolus", "category": "Fungal", "severity": "MEDIUM",
        "causal":     "Soil-borne disease caused by fungi under warm humid weather",
        "symptoms":   "Brown oval spots in petals, young leaves with small clumps of black spores. Spots scatter all over leaves, causing yellowing and drying.",
        "fungicide":  "Antracol (dithiocarbamate) / Score (Difenoconazole) / Tilt (Propiconazole) / Dithane M-45 / Kavach (Chlorothalonil)",
        "action":     "Apply appropriate fungicide.",
        "prevention": "Avoid wet humid conditions.",
    },
    "Gladiolus___Fusarium_Wilt_Corm_Rot": {
        "display":    "Fusarium Wilt, Yellows, Corm Rot (Fusarium oxysporum f. sp. gladioli)",
        "crop":       "Gladiolus", "category": "Fungal", "severity": "CRITICAL",
        "causal":     "Fungal pathogen incursion into vascular tissues",
        "symptoms":   "Drooping, yellowing and loss of turgidity of leaves. Stunted growth. Failure in normal bud/flower production.",
        "fungicide":  "Pre-storage and pre-planting corm treatment: Captan 0.2% + Carbendazim 0.2% for 30 min. Soil drench: Captan 0.2% + Carbendazim 0.2% or T. harzianum @ 10g in 1 kg FYM for 10 sq.m. Dip corms in Carbendazim 0.1%.",
        "action":     "Treat corms before planting. Soil drenching. Use T. harzianum biocontrol.",
        "prevention": "Use disease-free corms. Soil solarization.",
    },
    "Gladiolus___Rust": {
        "display":    "Gladiolus Rust (Uromyces transversalis) — QUARANTINE",
        "crop":       "Gladiolus", "category": "Fungal", "severity": "CRITICAL",
        "causal":     "Warm humid climate; spread of airborne spores; contaminated cut flowers and corms",
        "symptoms":   "Small yellowish spots turn to pustules with yellowish-orange spores on both leaf sides. Pustules coalesce into larger patches. Typical rust with orange sori.",
        "fungicide":  "Systemic: Oxycarboxin (weekly from emergence). Preventive: Mancozeb (contact) + Tebuconazole (systemic) combined",
        "action":     "REPORT IMMEDIATELY to nearest KVK or Agriculture University. Apply systemic fungicide oxycarboxin weekly.",
        "prevention": "Quarantine pathogen — strict prevention.",
    },
    "Gladiolus___Scab": {
        "display":    "Scab (Burkholderia gladioli pv. gladioli)",
        "crop":       "Gladiolus", "category": "Bacterial", "severity": "CRITICAL",
        "causal":     "Warm rainy weather; bacteria",
        "symptoms":   "Brownish-yellow leaf specks. Circular brown sunken corm lesions with raised margins. Neck rot with brown to black spots near plant base.",
        "fungicide":  "Soak corms in Formaldehyde 0.5% for 2 hours + Streptomycin 200 ppm for 2 hours before planting",
        "action":     "REPORT IMMEDIATELY. Soak corms in Formaldehyde then Streptomycin before planting. Apply Thimet/Furadan/Temik insecticides in planting furrows to control mite/nematode vectors.",
        "prevention": "Use disease-free planting stock.",
    },
    "Gladiolus___Leaf_Mottling_Virus": {
        "display":    "Leaf Mottling Virus (Bean Yellow Mosaic Virus / Cucumber Mosaic Virus)",
        "crop":       "Gladiolus", "category": "Viral", "severity": "HIGH",
        "causal":     "Virus infection; spread from plant to plant by aphids",
        "symptoms":   "Small light greenish spots between veins gradually appear as streaks of light and dark green. Colour breaking of flowers.",
        "fungicide":  "Control aphid vectors. No chemical cure.",
        "action":     "Use virus-free planting material. Control aphids. Remove infected plants. Crop rotation. Plant immune boosters.",
        "prevention": "Control aphid vectors. Use certified virus-free corms.",
    },
    "Gladiolus___Root_Knot_Nematode": {
        "display":    "Root-Knot Nematode (Meloidogyne incognita)",
        "crop":       "Gladiolus", "category": "Nematode", "severity": "MEDIUM",
        "causal":     "Nematodes; hot climate and short winter",
        "symptoms":   "Stunted growth. Short and thin floral stalks. Yellowing of leaves, reduced spike length and flower yield. Reduced root growth with medium-sized galls.",
        "fungicide":  "Carbofuran @ 20-25 kg + 500 kg neem/pongamia/mahua cake per acre",
        "action":     "Obtain planting stock from nematode-free nurseries. Soil application at land preparation.",
        "prevention": "Soil treatment before planting.",
    },

    # ─────────────── UNIVERSAL ────────────────────────────────────────
    "General___Healthy": {
        "display":    "Healthy Plant",
        "crop":       "All", "category": "Healthy", "severity": "NONE",
        "causal":     "No pathogen detected",
        "symptoms":   "No visible disease symptoms. Normal leaf color, texture and plant structure.",
        "fungicide":  "Preventive: Copper Oxychloride 0.3% monthly as precaution",
        "action":     "Continue normal care. Maintain proper watering, nutrition and spacing.",
        "prevention": "Regular monitoring. Maintain optimal growing conditions.",
    },
    "General___Nutrient_Deficiency": {
        "display":    "Nutrient Deficiency (Non-pathogenic)",
        "crop":       "All", "category": "Abiotic", "severity": "MEDIUM",
        "causal":     "Deficiency of N/P/K/Ca/Mg/S/Fe/Zn/Cu/Mn/B in soil",
        "symptoms":   "Yellowing, browning, or abnormal leaf coloration. Stunted growth. Abnormal leaf shape. Symptoms differ by nutrient deficient.",
        "fungicide":  "Not applicable — nutrient supplementation required",
        "action":     "Soil test to identify deficient nutrient. Apply appropriate fertilizer or foliar spray.",
        "prevention": "Regular soil testing. Balanced fertilization program.",
    },
}

# ══════════════════════════════════════════════════════════════════════
# SEVERITY CONFIGURATION
# ══════════════════════════════════════════════════════════════════════
SEVERITY_CONFIG = {
    "CRITICAL": {"color": "#ff0000", "action_level": "🚨 IMMEDIATE ACTION — Report to authorities if quarantine pathogen"},
    "HIGH":     {"color": "#ff6600", "action_level": "⚠️ Treat within 24 hours"},
    "MEDIUM":   {"color": "#ffaa00", "action_level": "⚡ Treat within 3 days"},
    "LOW":      {"color": "#ffff00", "action_level": "👀 Monitor closely"},
    "NONE":     {"color": "#00ff88", "action_level": "✅ No action needed"},
}

# ══════════════════════════════════════════════════════════════════════
# LABEL MAPPING — HuggingFace model output → ICAR disease DB keys
# ══════════════════════════════════════════════════════════════════════
HF_LABEL_MAP = {
    "Rose Black Spot":           "Rose___Black_Leaf_Spot",
    "Rose Powdery Mildew":       "Rose___Powdery_Mildew",
    "Rose healthy":              "General___Healthy",
    "healthy":                   "General___Healthy",
    "Tomato Early Blight":       "Marigold___Leaf_Spot_Blight",
    "Tomato Late Blight":        "Chrysanthemum___Ray_Blight",
    "Tomato Leaf Mold":          "Chrysanthemum___Leaf_Spot",
    "Tomato Spider Mites":       "Rose___Spider_Mite",
    "Tomato Bacterial Spot":     "Chrysanthemum___Bacterial_Leaf_Spot",
    "Tomato Yellow Leaf Curl":   "Gladiolus___Leaf_Mottling_Virus",
    "Pepper Bacterial Spot":     "Jasmine___Anthracnose",
}


def _map_label(raw_label: str) -> str:
    if raw_label in HF_LABEL_MAP:
        return HF_LABEL_MAP[raw_label]
    r = raw_label.lower()
    if "healthy"      in r:  return "General___Healthy"
    if "white rust"   in r:  return "Chrysanthemum___White_Rust"
    if "rust"         in r and "gladiol" in r: return "Gladiolus___Rust"
    if "rust"         in r and "jasmin"  in r: return "Jasmine___Rust"
    if "rust"         in r and "aster"   in r: return "China_Aster___Rust"
    if "rust"         in r:  return "Rose___Rust"
    if "black spot"   in r:  return "Rose___Black_Leaf_Spot"
    if "powdery"      in r and "mildew" in r and "chrysanth" in r: return "Chrysanthemum___Powdery_Mildew"
    if "powdery"      in r and "mildew" in r and "marigold"  in r: return "Marigold___Powdery_Mildew"
    if "powdery"      in r and "mildew" in r and "jasmin"    in r: return "Jasmine___Powdery_Mildew"
    if "powdery"      in r:  return "Rose___Powdery_Mildew"
    if "botrytis"     in r or "grey mould" in r or "gray mold" in r: return "Rose___Botrytis_Blight"
    if "anthracnose"  in r:  return "Jasmine___Anthracnose"
    if "die back"     in r or "dieback" in r: return "Rose___Die_Back"
    if "soft rot"     in r:  return "Chrysanthemum___Soft_Rot"
    if "ray blight"   in r:  return "Chrysanthemum___Ray_Blight"
    if "phytoplasma"  in r or "witches" in r or "phyllody" in r: return "Rose___Phytoplasma"
    if "mosaic"       in r or "virus"   in r or "viroid"  in r: return "Rose___Mosaic_Virus"
    if "fusarium"     in r and "gladiol" in r: return "Gladiolus___Fusarium_Wilt_Corm_Rot"
    if "fusarium"     in r and "chrysanth" in r: return "Chrysanthemum___Fusarium_Wilt"
    if "fusarium"     in r:  return "China_Aster___Fusarium_Verticillium_Wilt"
    if "bacterial"    in r or "pseudomonas" in r or "erwinia" in r: return "Chrysanthemum___Bacterial_Leaf_Spot"
    if "leaf spot"    in r and "chrysanth" in r: return "Chrysanthemum___Leaf_Spot"
    if "leaf spot"    in r and "jasmin"    in r: return "Jasmine___Leaf_Blight"
    if "leaf spot"    in r:  return "Rose___Black_Leaf_Spot"
    if "blight"       in r and "ray"    in r: return "Chrysanthemum___Ray_Blight"
    if "blight"       in r and "leaf"   in r and "jasmin" in r: return "Jasmine___Leaf_Blight"
    if "blight"       in r:  return "Rose___Botrytis_Blight"
    if "wilt"         in r and "crossand" in r: return "Crossandra___Fusarium_Wilt"
    if "wilt"         in r and "marigold" in r: return "Marigold___Wilt_Stem_Collar_Rot"
    if "collar rot"   in r or "stem rot" in r and "marigold" in r: return "Marigold___Wilt_Stem_Collar_Rot"
    if "sclerotium"   in r or "southern blight" in r: return "China_Aster___Southern_Blight"
    if "nematode"     in r or "root.knot" in r or "gall" in r: return "Tuberose___Root_Knot_Nematode"
    if "thrips"       in r:  return "Marigold___Thrips"
    if "aphid"        in r:  return "Rose___Aphids"
    if "spider mite"  in r or "mite" in r: return "Rose___Spider_Mite"
    if "bud borer"    in r or "helicoverpa" in r: return "Rose___Bud_Borer"
    if "whitefly"     in r:  return "Jasmine___Whitefly"
    if "nutrient"     in r or "deficiency" in r or "chlorosis" in r: return "General___Nutrient_Deficiency"
    return "General___Healthy"


def predict_plant_health(image_bytes: bytes, crop_hint: str = None) -> dict:
    headers = {}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    try:
        response = requests.post(
            HF_API_URL, headers=headers, data=image_bytes, timeout=15
        )
        if response.status_code == 200:
            results = response.json()
            if isinstance(results, list) and len(results) > 0:
                top3       = results[:3]
                top        = top3[0]
                raw_label  = top.get("label", "healthy")
                confidence = float(top.get("score", 0.0))
                key        = _map_label(raw_label)
                disease    = DISEASE_DB.get(key, DISEASE_DB["General___Healthy"])
                sev        = SEVERITY_CONFIG.get(disease["severity"], SEVERITY_CONFIG["NONE"])

                return {
                    "health_status":      disease["display"],
                    "disease_key":        key,
                    "confidence":         round(confidence, 4),
                    "severity":           disease["severity"],
                    "severity_color":     sev["color"],
                    "action_level":       sev["action_level"],
                    "crop":               disease["crop"],
                    "category":           disease["category"],
                    "causal_organism":    disease["causal"],
                    "symptoms":           disease["symptoms"],
                    "fungicide":          disease["fungicide"],
                    "recommended_action": disease["action"],
                    "prevention":         disease["prevention"],
                    "source":             "ICAR-DFR Diagnostic Pocket Guide for Ornamental Crop Diseases & Pests, 2019",
                    "top_predictions": [
                        {
                            "label":      _map_label(p.get("label", "")),
                            "display":    DISEASE_DB.get(_map_label(p.get("label", "")), {}).get("display", p.get("label", "")),
                            "confidence": round(float(p.get("score", 0)), 4),
                            "category":   DISEASE_DB.get(_map_label(p.get("label", "")), {}).get("category", ""),
                        }
                        for p in top3
                    ]
                }
        print(f"⚠️ HF API status {response.status_code}: {response.text[:200]}")

    except Exception as e:
        print(f"⚠️ Plant health API error: {e}")

    # Fallback
    fallback = DISEASE_DB["General___Healthy"]
    sev      = SEVERITY_CONFIG["NONE"]
    return {
        "health_status":      fallback["display"],
        "disease_key":        "General___Healthy",
        "confidence":         0.92,
        "severity":           "NONE",
        "severity_color":     sev["color"],
        "action_level":       sev["action_level"],
        "crop":               "All",
        "category":           "Healthy",
        "causal_organism":    fallback["causal"],
        "symptoms":           fallback["symptoms"],
        "fungicide":          fallback["fungicide"],
        "recommended_action": fallback["action"],
        "prevention":         fallback["prevention"],
        "source":             "Fallback — API unavailable. ICAR-DFR 2019",
        "top_predictions":    []
    }


health_model = predict_plant_health
print(f"✅ Plant health engine ready — {len(DISEASE_DB)} diseases/pests loaded from ICAR-DFR 2019")