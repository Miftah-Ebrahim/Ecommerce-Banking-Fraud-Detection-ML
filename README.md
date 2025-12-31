# Fraud Detection System (E-commerce & Banking)

**Business Objective:**  
Develop a robust machine learning pipeline to detect fraudulent transactions in an e-commerce and banking dataset. The goal is to minimize financial loss (minimize False Negatives) while maintaining a seamless user experience (minimize False Positives) by analyzing transaction velocity, geolocation, and user behavior.

---

## 📂 Repository Structure

```
├── data/                  # Processed datasets (gitignored)
├── images/                # Visualizations (EDA, SHAP plots)
├── models/                # Saved models (Random Forest)
├── notebooks/
│   ├── feature-engineering.ipynb # Data processing & velocity features
│   ├── modeling.ipynb            # Model comparison (LR vs RF)
│   ├── shap-explainability.ipynb # Model interpretation
│   └── ...
├── src/                   # Helper scripts (preprocessing.py)
├── final_report.md        # DETAILED SUBMISSION REPORT
├── requirements.txt       # Dependencies
└── README.md              # Project overview
```

---

## 📊 Approach & Methodology

1.  **Data Processing:** 
    *   Merged identity and transaction data.
    *   Converted raw timestamps into actionable features (`hour_of_day`, `day_of_week`).
    *   Engineered **velocity features** (transaction frequency).
    *   Handled class imbalance using **SMOTE**.

2.  **Modeling Strategy:**
    *   **Baseline:** Logistic Regression (Class Weighted).
    *   **Ensemble:** Random Forest (Class Weighted).
    *   **Validation:** Stratified 5-Fold Cross-Validation.

3.  **Explainability:**
    *   Used **SHAP (SHapley Additive exPlanations)** to interpret the "black box" model.
    *   Analyzed potential fraud drivers globally and locally.

---

## 🏆 Model Performance

Random Forest significantly outperformed the baseline, capturing non-linear fraud patterns effectively.

| Model | Test AUC-PR | CV AUC-PR (Mean) | Key Strength |
| :--- | :---: | :---: | :--- |
| **Random Forest** | **0.637** | **0.899** | **Robustness, High Precision-Recall Balance** |
| Logistic Regression | 0.304 | 0.760 | Interpretability (Linear), Fast Training |

*Metric Chosen: AUC-PR is prioritized over ROC-AUC due to the heavy class imbalance (Fraud is rare).*

---

## 🔍 Key Insights (SHAP)

*   **Time Since Signup:** Immediate transactions after account creation are arguably the strongest indicator of bot/fraud activity, pushing risk scores up significantly.
*   **Transaction Velocity:** Users with unusually high transaction counts per hour are flagged by the model.
*   **Browser/Device:** Certain browser configurations are correlated with fraudulent IP addresses.

*(See `final_report.md` for full Force Plots and analysis)*

---

## 🛠️ Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Miftah-Ebrahim/Ecommerce-Banking-Fraud-Detection-ML.git
    cd Ecommerce-Banking-Fraud-Detection-ML
    ```

2.  **Create Environment:**
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\Activate
    # Mac/Linux:
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Notebooks:**
    Launch Jupyter Lab/Notebook and execute `notebooks/modeling.ipynb` or `notebooks/shap-explainability.ipynb`.

---

## 📝 Business Recommendations
1.  **Velocity Triggers:** Auto-block accounts exceeding 5 transactions/hour.
2.  **Cooling Period:** Enforce 2FA for high-value orders on accounts < 24 hours old.
3.  **Browser Fingerprinting:** Enhance detection for headless/anomalous browsers.

**[View Full Analysis & Final Report](final_report.md)**
