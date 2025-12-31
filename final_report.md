# Fraud Detection Final Report

## A. Understanding & Defining the Business Objective

### 1. The Challenge in Fintech
Fraud detection is a critical capability for e-commerce and banking platforms. As transaction volumes scale, manual review becomes impossible. The objective is to build an automated system that identifies fraudulent transactions in real-time, protecting revenue without blocking legitimate customers.

### 2. The Trade-off: Security vs. User Experience
This project centers on the balance between **False Positives** and **False Negatives**:
*   **False Negatives (Missed Fraud):** Direct financial loss (chargebacks, stolen goods).
*   **False Positives (False Alarm):** Customer friction, cart abandonment, and reputational damage.
Our goal is to maximize fraud capture (Recall) while maintaining a reasonable precision to avoid alienating good users.

### 3. Class Imbalance & Explainability
*   **Imbalance:** Fraud is rare (often < 1%). Standard accuracy is a misleading metric (a model predicting "all legit" would be 99% accurate but useless). We use **AUC-PR** and **F1-score** to validly measure performance.
*   **Explainability (XAI):** A "black box" model is risky in finance. We use **SHAP** to explain *why* a transaction was blocked, enabling compliance and trust.

---

## B. Discussion of Completed Work & Analysis

### 1. Data Analysis & Features
We processed user transaction data combined with geolocation info.
*   **Geolocation:** Fraud rates varied significantly by country.
*   **Feature Engineering:**
    *   `time_since_signup`: Calculated as `purchase_time - signup_time`. This proved critical—bots often buy instantly.
    *   `velocity`: Transaction frequency per user per hour.
    *   `day/hour`: Temporal patterns of fraud.
*   **Imbance Handling:** Applied **SMOTE** (Synthetic Minority Over-sampling Technique) to the training set to prevent the model from ignoring the minority fraud class.

### 2. Model Building & Selection
We compared a linear baseline against a non-linear ensemble.

| Model | Test F1 | Test AUC-PR | CV AUC-PR (Mean ± Std) | decision |
| :--- | :---: | :---: | :---: | :--- |
| **Random Forest** | **0.704** | **0.637** | **0.899 ± 0.00** | **Selected** |
| Logistic Regression | 0.294 | 0.304 | 0.760 ± 0.00 | Discarded |

**Justification:** The Random Forest's ability to model complex, non-linear interactions (e.g., a specific combination of "new account" + "high value") allowed it to achieve double the precision-recall performance of the logistic regression.

### 3. Model Explainability (SHAP)
Using SHAP, we examined the model's decision-making logic.

#### Global Importance (Summary Plot)
*   **Top Driver:** `time_since_signup` is universally the most impactful feature.
*   **Directionality:** The Summary Plot (Fig 2 in notebooks) shows that **low** values (blue dots, meaning short time) push SHAP values **positive** (higher fraud risk). This aligns perfectly with domain intuition about bot attacks.

#### Local Interpretation (Force Plots)
*   **True Positive:** For confirmed fraud cases, the model successfully identifies the combination of *high velocity* and *low account age*.
*   **False Positive:** In edge cases, legitimate users with "unusual" behaviors (e.g., buying quickly) were flagged. This highlights the need for a secondary verification step (recommendation #2) rather than an outright ban.

---

## C. Business Recommendations & Strategic Insights

Based on our model's findings, we propose three strategic actions:

1.  **Velocity-Based Circuit Breakers (Operational):**
    *   **Insight:** `user_tx_count` is a top predictor.
    *   **Action:** Implement a hard rule blocking any user attempting >10 transactions/hour, or trigger a CAPTCHA at >5/hour. This stops high-frequency bot attacks immediately.

2.  **Dynamic Friction for New Accounts (Strategic):**
    *   **Insight:** `time_since_signup` is the #1 risk factor.
    *   **Action:** Do not block new users (to preserve growth). Instead, enforce **3D-Secure / 2FA** for any purchase made within **10 minutes** of registration. This balances security with UX.

3.  **Risk-Based Manual Review Queue:**
    *   **Insight:** High-value transactions (`purchase_value`) are risky but legitimate users also spend high amounts.
    *   **Action:** Route top 5% risk scores (from the model) to a manual review team if the transaction value > $200. This ensures human oversight for expensive decisions.

---

## D. Limitations & Future Work

While robust, the current system has constraints:

1.  **Data Limitations:** We rely heavily on IP-based geolocation, which is easily spoofed by VPNs/Proxies. The processed dataset does not contain device fingerprints which would be more robust.
2.  **Model Limitations:** The Random Forest is a static batch model. It does not learn from new fraud patterns in real-time (Concept Drift).
3.  **Future Improvements:**
    *   **Real-time Serving:** Deploy model as an API endpoint.
    *   **Drift Monitoring:** Implement dashboard to track if `time_since_signup` distribution shifts.
    *   **Graph Features:** Build a network graph to detect "fraud rings" (shared IPs/devices across accounts).

---

## E. Conclusion
The implementation of the Random Forest model, supported by SMOTE and SHAP analysis, provides a high-precision, explainable fraud detection system. It moves beyond simple rules to capture complex risk patterns, offering a scalable solution for modern fintech security.
