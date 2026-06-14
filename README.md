# DSGP-GROUP-9: UK Road Accident Analysis & Prediction

A Data Science Group Project (DSGP) that analyzes historical UK road accident
data and serves machine-learning predictions through a Flask web application.
The system helps identify accident hotspots, predicts accident severity, and
visualizes accident trends for several UK cities.

## Features

- **Accident count / hotspot prediction** — predicts expected accident counts
  for a given month, hour, day of week, district, weather, and lighting
  condition, and highlights the location on a map.
- **Road surface condition prediction** — predicts the likely road surface
  condition (dry, wet/damp, frost/ice, snow, flood) based on weather, light,
  and road type.
- **Accident severity prediction** — predicts severity (Fatal / Serious /
  Slight) based on number of vehicles, number of casualties, weather, road
  surface, and lighting conditions.
- **Analysis dashboard** — interactive charts (road type distribution, speed
  limit distribution, accidents by day of week) for cities such as Liverpool,
  Knowsley, Manchester, Leeds, Birmingham, Westminster, Bradford, Kirklees,
  Sheffield, and Leicester.
- **Login / sign-up page** as the entry point to the application.

## Repository Structure

```
DSGP-GROUP-9/
├── connecting model/          # Flask web application
│   ├── main.py                # Flask app: routes, model loading, mappings
│   ├── *.pkl / *.pkl.gz       # Trained ML models (pickled)
│   ├── templates/             # Jinja2 HTML templates
│   │   ├── loginpage.html
│   │   ├── homepage.html
│   │   ├── aaa.html           # Accident count / hotspot prediction page
│   │   ├── bbb.html           # Severity prediction page
│   │   └── analystpage.html   # Analysis dashboard
│   └── static/                # CSS, JS, images, map templates
├── *.ipynb                    # Jupyter notebooks for data cleaning, EDA,
│                               # and model training
├── Birmingham_road_surface_dataset.csv
├── newDataset.csv
└── Local_Authority_Districts_December_2022_UK_BGC_V2_.../  # UK district
                                                              # boundary shapefiles
```

## Tech Stack

- **Backend**: Python, Flask
- **Machine Learning**: scikit-learn (Random Forest models), pandas, numpy
- **Data Analysis**: Jupyter Notebook, pandas, numpy, matplotlib, seaborn
- **Frontend**: HTML, CSS, JavaScript, Google Charts, Leaflet/Folium (maps)
- **Data**: UK road accident datasets (Accidents/Vehicles 2005–2014, Birmingham
  road surface dataset, custom processed datasets), tracked with Git LFS

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
pip install flask numpy pandas scikit-learn
```

### Running the Web App

```bash
cd "connecting model"
python main.py
```

The app starts on `http://localhost:8000/`. Navigate to the login page, then
use the **PREDICTION**, **SEVERITY**, and **ANALYSIS** links in the
navigation bar to access each feature.

### Notebooks

The root-level `.ipynb` files contain the data cleaning, exploratory data
analysis, and model training steps used to produce the pickled models in
`connecting model/`. Open them with Jupyter Notebook or JupyterLab to review
the analysis.

## Models

| File | Purpose |
|---|---|
| `best_random_forest_model_zip.pkl.gz` | Accident count / hotspot prediction |
| `road_surface_model.pkl` | Road surface condition prediction |
| `random_forest_model.pkl` | Accident severity prediction |
| `accident_severity_model.pkl` | Severity model (alternate) |

## Data

Large datasets (`Accidents0514.csv`, `Vehicles0514.csv`, etc.) are tracked
using Git LFS — make sure `git lfs install` has been run before cloning to
retrieve these files.
