import os
import sys
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request

# --- 1. SETUP SYSTEM PATHS ---
# Ensures Flask can find 'preprocessing.py' inside the 'src' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # app/
ROOT_DIR = os.path.dirname(BASE_DIR)                # Project root
sys.path.append(os.path.join(ROOT_DIR, 'src'))

try:
    from preprocessing import LoanPreprocessor
    print("✅ Preprocessing module linked successfully.")
except ImportError:
    print("❌ Critical: Could not find preprocessing.py in src folder!")

app = Flask(__name__)

# --- 2. LOAD ML ARTIFACTS ---
MODEL_PATH = os.path.join(ROOT_DIR, 'models')

try:
    model = joblib.load(os.path.join(MODEL_PATH, 'loan_model.pkl'))
    encoders = joblib.load(os.path.join(MODEL_PATH, 'encoders.pkl'))
    features_list = joblib.load(os.path.join(MODEL_PATH, 'features_list.pkl'))
    pp = joblib.load(os.path.join(MODEL_PATH, 'preprocessor_object.pkl'))
    print("✅ MASTER LEVEL READY: All models and encoders loaded.")
except Exception as e:
    print(f"❌ Error loading models: {e}")

# --- 3. ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Capture Data
        raw_data = request.form.to_dict()
        input_df = pd.DataFrame([raw_data])
        
        # Add defaults for Wizard UI missing fields
        defaults = {'Education': 'Graduate', 'Property_Area': 'Semiurban', 'Self_Employed': 'No'}
        for key, value in defaults.items():
            if key not in input_df.columns:
                input_df[key] = value

        # Convert numerics
        numeric_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History']
        for col in numeric_cols:
            input_df[col] = pd.to_numeric(input_df[col], errors='coerce').fillna(0)

        # 1. SMART LOGIC: Debt-to-Income (DTI) Calculation
        # LoanAmount is usually in thousands in this dataset
        income = float(raw_data.get('ApplicantIncome', 1))
        loan_amt_raw = float(raw_data.get('LoanAmount', 0)) * 1000
        # Monthly DTI calculation (assuming 30-year term for logic)
        dti_ratio = (loan_amt_raw / 360) / (income if income > 0 else 1)

        # 2. ML PREDICTION PIPELINE
        processed_df = pp.transform(input_df)
        
        for col, le in encoders.items():
            if col in processed_df.columns:
                try:
                    processed_df[col] = le.transform(processed_df[col].astype(str))
                except:
                    processed_df[col] = 0
            
        final_input = processed_df[features_list]
        prediction = model.predict(final_input)[0]
        prob = model.predict_proba(final_input)[0][1]
        
        # 3. SET STATUS & CONFIDENCE
        result = "APPROVED" if prediction == 1 else "DECLINED"
        confidence = round(prob * 100, 2) if prediction == 1 else round((1 - prob) * 100, 2)
        
        # 4. SMART ADVISOR FEEDBACK
        advice = ""
        if prediction == 0:
            if float(raw_data.get('Credit_History', 1)) == 0:
                advice = "Focus on clearing existing debts to improve your Credit History score."
            elif dti_ratio > 0.4:
                suggested_income = (float(raw_data['LoanAmount']) * 1000) / 0.3 / 12
                advice = f"DTI ratio is high. Consider an income of roughly ${round(suggested_income)} or a lower loan amount."
            else:
                advice = "Your profile is on the edge. Try applying with a co-applicant to reduce risk."
        else:
            advice = "Your financial profile is strong. You qualify for our 'Premier' interest rates."

        return render_template('result.html', 
                               status=result, 
                               score=confidence, 
                               advice=advice, 
                               dti=round(dti_ratio*100, 1))

    except Exception as e:
        print(f"Prediction Error: {e}")
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)