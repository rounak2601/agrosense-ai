# 🌿 AgroSense AI — Smart Crop Intelligence for Indian Farmers

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.x-orange?style=flat-square&logo=scikit-learn)
![Random Forest](https://img.shields.io/badge/Model-Random%20Forest-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> An end-to-end Machine Learning web application that recommends the best crop to plant and predicts expected yield — built on 20+ years of Indian government farming data.

🔗 **Live Web App:** [🚀 Click Here](https://agrosenseai-rt.streamlit.app/)
---

## 📌 Table of Contents
- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Dataset](#-dataset)
- [Model Performance](#-model-performance)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [How to Use](#-how-to-use)
- [Author](#-author)

---

## 🌾 Overview

**AgroSense AI** is a full-stack data science project that solves two real-world agriculture problems:

| Problem | Solution | Accuracy |
|---|---|---|
| Which crop should I plant on my soil? | 🌱 Crop Recommendation (Classification) | **99.32%** |
| How much yield will my farm produce? | 📈 Yield Prediction (Regression) | **R² = 0.9936** |

The application is built using **Random Forest** models trained on 2 real datasets — one covering soil and climate conditions for 22 crops, and one covering **293,744 farming records** across **28 Indian states and 8 Union Territories** from **1997 to 2020**.

---

## 🚀 Live Demo

Run locally with:
```bash
streamlit run app.py
```

---

## ✨ Features

- **🌱 Crop Advisor** — Enter soil nutrients (N, P, K) and climate data to get instant AI-powered crop recommendation with confidence score and farming tips
- **📈 Yield Predictor** — Select state, crop, season and farm area to get predicted yield in tonnes/hectare with comparison to national average
- **📊 Data Insights** — Full EDA with 10+ interactive charts — histograms, heatmaps, box plots, pie charts, trend lines
- **🗺️ Crop Map** — State-wise crop analysis with average yield, total production and area metrics
- **📱 Professional Dashboard** — Clean green farming theme, radar chart soil profile, gauge chart yield meter

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Web Framework | Streamlit |
| ML Models | Scikit-learn (Random Forest) |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly Express, Plotly Graph Objects |
| Model Serialization | Pickle |
| IDE | Jupyter Notebook |

---

## 📊 Dataset

### Dataset 1 — Crop Recommendation
| Property | Value |
|---|---|
| Source | Kaggle — Crop Recommendation Dataset |
| Rows | 2,200 |
| Features | N, P, K, Temperature, Humidity, pH, Rainfall |
| Target | Crop Label (22 classes) |
| Missing Values | 0 (perfectly clean) |

### Dataset 2 — APY (Area Production Yield)
| Property | Value |
|---|---|
| Source | Indian Government Agriculture Data (1997–2020) |
| Rows | 345,336 |
| Features | State, District, Crop, Year, Season, Area, Production |
| Target | Yield (tonnes/ha) |
| Coverage | 28 States + 8 Union Territories |

---

## 📈 Model Performance

### 🌱 Crop Recommendation — Random Forest Classifier
```
Accuracy          : 99.32%
Training Accuracy : 100.00%
Testing Accuracy  : 99.32%
Overfitting Gap   : 0.68%  ✅ Not overfitting
Trees             : 100
Classes           : 22 crops
```

### 📈 Yield Prediction — Random Forest Regressor
```
R² Score  (Test) : 0.9936
RMSE      (Test) : 0.0819 t/ha
R² Score (Train) : 0.9991
RMSE     (Train) : 0.0303 t/ha
Overfitting Gap  : 0.0055  ✅ Not overfitting
Trees            : 100
```

### Top Feature Importances
**Crop Model:** Rainfall (22%) > Humidity (21%) > K (16%) > P (15%) > N (11%)

**Yield Model:** Production (42%) > Area (38%) > Crop Type (10%) > Season (6%)

---

## 📁 Project Structure

```
Crop Recommendation/
│
├── app.py                      # Streamlit dashboard (main file)
├── Untitled.ipynb              # Jupyter notebook (full analysis)
│
├── Crop_recommendation.csv     # Dataset 1 — soil & climate data
├── APY.csv                     # Dataset 2 — government farming data
│
├── crop_model.pkl              # Trained crop classification model
├── yield_model.pkl             # Trained yield regression model
├── label_encoder.pkl           # Label encoder for crop names
│
└── README.md                   # This file
```

---

## ⚙️ Installation & Setup

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/agrosense-ai.git
cd agrosense-ai
```

### Step 2 — Install required libraries
```bash
pip install streamlit pandas numpy scikit-learn plotly
```

### Step 3 — Run the dashboard
```bash
streamlit run app.py
```

### Step 4 — Open in browser
The app will automatically open at `http://localhost:8501`

---

## 📖 How to Use

### Crop Advisor
1. Navigate to **🌱 Crop Advisor** in the sidebar
2. Enter your soil nutrients — **Nitrogen (N)**, **Phosphorus (P)**, **Potassium (K)** from a soil test report
3. Enter climate data — temperature, humidity, rainfall, pH
4. Click **"Recommend Best Crop"**
5. View your recommended crop with confidence score and farming tips

### Yield Predictor
1. Navigate to **📈 Yield Predictor** in the sidebar
2. Select your **State**, **Crop**, **Season**, and **District**
3. Enter your **farm area** in hectares (1 acre ≈ 0.4 ha)
4. Enter expected production and crop year
5. Click **"Predict Yield"** to see predicted tonnes/hectare

---

## 🔬 ML Pipeline Summary

```
Raw Data
    ↓
Exploratory Data Analysis (6 chart types)
    ↓
Data Cleaning
  • Dropped 9 rows with missing Crop names
  • Filled 4,948 missing Production values with median
  • Per-crop 5th–95th percentile outlier removal
    ↓
Feature Engineering
  • Label Encoding for categorical columns
  • Train/Test Split (80/20)
    ↓
Model Training
  • Random Forest Classifier (Crop Recommendation)
  • Random Forest Regressor  (Yield Prediction)
    ↓
Evaluation
  • Accuracy, Confusion Matrix, Classification Report
  • R² Score, RMSE, Actual vs Predicted Plot
    ↓
Deployment
  • Streamlit Web Dashboard
```

---

## 👤 Author

**Rounak**
- GitHub: [@rounak2601](https://github.com/rounak2601)
- LinkedIn: [Rounak Tilante](https://linkedin.com/in/rounak-tilante)

---

## 📄 License

This project is licensed under the MIT License.

---

⭐ **If you found this project helpful, please give it a star!**
