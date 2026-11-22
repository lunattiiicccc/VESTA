# VESTA

### A smarter way to get dressed.

**An intelligent digital wardrobe and personal styling assistant.**

VESTA is a digital wardrobe application designed to help users make more intentional use of the clothes they already own. By combining wardrobe management, weather-aware outfit recommendations, outfit planning and visualisation, VESTA makes getting dressed a more organised, personalised and enjoyable experience.

Inspired by Vesta, the Roman goddess of the hearth, VESTA represents independence, identity, warmth and inner strength.

---

## ✦ Features

### Digital Wardrobe
Build and manage a personal digital clothing collection.

- Add garments with photographs and detailed descriptions.
- Organise clothing by category and subcategory.
- Record colours, materials, fit, seasons and weather suitability.
- Edit and delete wardrobe items.
- Search, filter and sort your collection.
- View wardrobe statistics and colour distribution.

### Intelligent Outfit Generator
Discover outfit combinations using garments already in your wardrobe.

- Generate up to three outfit recommendations.
- Consider current temperature and weather conditions.
- Select a season and dressing occasion.
- Receive ranked recommendations with style match scores.
- View explanations of why each outfit was recommended.
- Explore individual scoring categories.

VESTA uses a deterministic, rule-based recommendation engine rather than an external generative AI service.

### Weather Integration
Make more informed clothing choices using current weather conditions.

- Retrieve weather information through Open-Meteo.
- Display temperature, conditions and wind speed.
- Automatically suggest relevant weather settings.
- Allow users to override conditions manually.

### Outfit Visualisation
Bring outfit combinations together visually.

- Create flat-lay compositions using photographs from your wardrobe.
- Preview complete outfit combinations.
- Download generated outfit mockups.

### Outfit Calendar
Plan outfits ahead of time.

- Schedule outfits for specific dates.
- Record the intended occasion.
- View planned outfits in a monthly calendar.
- Review and remove existing plans.

### Saved Outfits
Keep track of favourite outfit combinations and revisit them.

---

## ✦ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and recommendation engine |
| Streamlit | User interface |
| SQLite | Local database |
| SQLAlchemy | Database management and ORM |
| Pillow | Image processing and outfit visualisation |
| Requests | Weather API communication |
| Open-Meteo | Weather data |
| Pytest | Automated testing |

VESTA is designed to run locally through a web browser.

No external AI API or paid AI service is required.

---

## ✦ Project Structure

```text
VESTA/
│
├── app.py
│
├── pages/
│   ├── dashboard.py
│   ├── wardrobe.py
│   ├── outfit_generator.py
│   ├── mockup_studio.py
│   ├── calendar.py
│   ├── saved_outfits.py
│   └── outfit_details.py
│
├── engine/
│   ├── generator.py
│   ├── filtering.py
│   ├── scoring.py
│   ├── compatibility.py
│   └── explanations.py
│
├── services/
│   ├── clothing_service.py
│   ├── weather.py
│   ├── calendar_service.py
│   └── image_composer.py
│
├── database/
│   ├── connection.py
│   ├── models.py
│   ├── seed.py
│   └── vesta.db
│
├── tests/
│   ├── test_db.py
│   └── test_engine.py
│
├── assets/
│   └── clothing/
│
├── init_db.py
│
└── README.md
```

---

## ✦ Getting Started

### Requirements

- Python 3.12 or later
- pip
- A modern web browser
- An internet connection for live weather information

### 1. Clone the repository

```bash
git clone REPOSITORY_URL
cd VESTA
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

Linux and macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install streamlit sqlalchemy pillow requests pytest
```

### 5. Initialise the database

```bash
python init_db.py
```

### 6. Launch VESTA

```bash
python -m streamlit run app.py --client.showSidebarNavigation=false
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

---

## ✦ How the Recommendation Engine Works

VESTA uses a structured recommendation process to identify suitable outfit combinations.

**1. Wardrobe retrieval**

The engine retrieves available garments from the user's digital wardrobe.

**2. Contextual filtering**

Garments are filtered according to relevant conditions, including:

- Temperature suitability
- Weather compatibility
- Seasonal suitability
- Dressing occasion

**3. Outfit construction**

The engine builds complete combinations using supported outfit structures:

- Top + Bottom + Footwear
- Dress + Footwear
- Jumpsuit + Footwear

Optional garments, such as outerwear and accessories, can also be incorporated.

**4. Outfit scoring**

Valid combinations receive a weighted score based on several criteria.

| Scoring category | Weight |
|---|---:|
| Weather suitability | 30% |
| Garment compatibility | 25% |
| Occasion suitability | 20% |
| Colour coordination | 15% |
| Style compatibility | 10% |

**5. Recommendations and explanations**

The highest-ranked combinations are selected, with diversity considered to avoid presenting near-identical outfits.

Each recommendation includes an overall score and an explanation of its suitability.

---

## ✦ Design Philosophy

VESTA takes inspiration from classical Roman architecture, Renaissance manuscripts and traditional luxury fashion houses.

Its visual identity combines:

- Oxblood and burgundy
- Warm parchment
- Antique gold
- Charcoal
- Dusty rose

The interface aims to balance classical elegance with modern functionality.

**Brand colours**

| Colour | Hexadecimal |
|---|---|
| Vesta Oxblood | `#641F30` |
| Sacred Burgundy | `#873B4C` |
| Parchment | `#F1E9DC` |
| Antique Gold | `#B39460` |
| Hearth Charcoal | `#292629` |
| Dusty Rose | `#C69B9D` |

---

## ✦ Project Goals

VESTA explores how intelligent wardrobe management can encourage more intentional clothing choices.

Its central goals are to:

- Help users rediscover and use existing garments.
- Reduce the effort involved in choosing outfits.
- Make outfit planning more practical.
- Encourage individual style and self-expression.
- Demonstrate how rule-based recommendation systems can solve everyday problems.

Rather than encouraging users to constantly purchase new clothing, VESTA focuses on making more of what they already own.

---

## ✦ Future Development

Potential future improvements include:

- More advanced outfit compatibility rules.
- Expanded outfit visualisation options.
- Improved personal style preferences.
- Outfit feedback and recommendation refinement.
- More detailed wardrobe analytics.
- Enhanced saved outfit management.
- Additional weather and occasion-based recommendations.

---

## ✦ Project Information

**Project:** VESTA  
**Category:** Fashion Technology / Personal Productivity  
**Application type:** Local web application  
**Primary language:** Python  
**Development environment:** VSCodium  

*A smarter way to get dressed.*

**Vesti. Vidi. Vici.**
