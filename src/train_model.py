import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from preprocessing import LoanPreprocessor # Importing our class from Step 2

def train():
    # 1. Load Data
    df = pd.read_csv('data/raw/loan_prediction.csv')
    
    # 2. Preprocess using our custom Engine
    pp = LoanPreprocessor()
    df_cleaned = pp.fit_and_clean(df)
    
    # 3. Label Encoding for Categorical Columns
    # We must save these encoders to use them in the Web App later
    cat_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
    encoders = {}
    
    for col in cat_cols:
        le = LabelEncoder()
        df_cleaned[col] = le.fit_transform(df_cleaned[col].astype(str))
        encoders[col] = le
        
    # Target Encoding
    target_le = LabelEncoder()
    y = target_le.fit_transform(df_cleaned['Loan_Status'])
    X = df_cleaned.drop('Loan_Status', axis=1)
    
    # 4. Train XGBoost
    # Hyperparameters tuned for better generalization
    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    model.fit(X, y)
    
    # 5. Save Artifacts (The "Master" Step)
    joblib.dump(model, 'models/loan_model.pkl')
    joblib.dump(encoders, 'models/encoders.pkl')
    joblib.dump(target_le, 'models/target_encoder.pkl')
    joblib.dump(X.columns.tolist(), 'models/features_list.pkl')
    joblib.dump(pp, 'models/preprocessor_object.pkl') # Save the stats for the web app
    
    print("✅ Training Complete!")
    print(f"✅ Model saved to models/loan_model.pkl")
    print(f"✅ Feature order: {X.columns.tolist()}")

if __name__ == "__main__":
    train()