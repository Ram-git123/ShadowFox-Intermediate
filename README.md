# ShadowFox-Intermediate
"LendWise AI is an intelligent loan eligibility platform powered by XGBoost, featuring a sleek glassmorphism multi-step wizard. It goes beyond approve/decline decisions by offering smart, actionable insights based on DTI and credit history."

# LendWise AI: Advanced Loan Approval System 🚀

An end-to-end Machine Learning web application that predicts loan eligibility using **XGBoost** and provides real-time financial advice.

## 🌟 Key Features
- **Predictive Engine:** Powered by XGBoost for high-accuracy credit scoring.
- **Smart Advisor:** Provides actionable feedback (e.g., DTI analysis) for declined applications.
- **Modern UI:** Immersive Glassmorphism wizard interface with real-time progress tracking.
- **Robust Pipeline:** Custom preprocessing class for handling missing data and feature engineering.

## 🛠️ Tech Stack
- **Backend:** Python (Flask)
- **Machine Learning:** Scikit-Learn, XGBoost, Joblib
- **Frontend:** HTML5, CSS3 (Glassmorphism), JavaScript, Bootstrap 5, Animate.css

## 🚀 How to Run
1. **Clone the repo:**
   ```bash
   gh repo clone Ram-git123/ShadowFox-Intermediate
   cd Loan-Approval-Master
   ```

2. **Install Dependencies:**

```bash
pip install -r requirements.txt

```


3. **Run the App:**
```bash
python app/main.py

```


4. **Access:** Open `http://127.0.0.1:5000` in your browser.


## 📁 Project Structure

* `app/`: Flask application logic and templates.
* `src/`: Data preprocessing and training scripts.
* `models/`: Pickled ML models and encoders.
* `data/`: Dataset used for training.

###  3. Final Folder Clean-up
Before running `git push`, make sure your folder structure is clean:
1.  **Delete any `__pycache__` folders** (they just clutter the repo).
2.  **Ensure all 5 `.pkl` files** are inside the `models/` folder.
3.  **Ensure `preprocessing.py`** is inside the `src/` folder.

### 4. GitHub Commands
Open your terminal in the root folder and run these:

```bash
git init
git add .
git commit -m "Initial Commit: Master Level Loan Approval System with Smart Advisor"
git branch -M main
git remote add origin https://github.com/Ram-git123/ShadowFox-Intermediate.git
git push -u origin main

```

