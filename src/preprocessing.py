import pandas as pd
import numpy as np

class LoanPreprocessor:
    def __init__(self):
        # We store modes/medians to use them later in the live Web App
        self.stats = {}
    
    def fit_and_clean(self, df):
        # Identify missing value fillers
        self.stats['Gender_mode'] = df['Gender'].mode()[0]
        self.stats['Married_mode'] = df['Married'].mode()[0]
        self.stats['LoanAmount_median'] = df['LoanAmount'].median()
        self.stats['Credit_History_mode'] = df['Credit_History'].mode()[0]
        
        return self.transform(df)

    def transform(self, df):
        df = df.copy()
        # 1. Handle Missing Values using stored stats
        df['Gender'] = df['Gender'].fillna(self.stats.get('Gender_mode', 'Male'))
        df['Married'] = df['Married'].fillna(self.stats.get('Married_mode', 'Yes'))
        df['LoanAmount'] = df['LoanAmount'].fillna(self.stats.get('LoanAmount_median', 120))
        df['Credit_History'] = df['Credit_History'].fillna(self.stats.get('Credit_History_mode', 1.0))
        
        # 2. Advanced Feature Engineering (The Master Level Difference)
        # Combine Incomes
        df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
        
        # Calculate EMI (Equated Monthly Installment)
        # Term is often in months, LoanAmount in thousands
        df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(360)
        df['EMI'] = df['LoanAmount'] / df['Loan_Amount_Term']
        
        # Log Transforms to normalize skewed data
        df['Total_Income_Log'] = np.log(df['Total_Income'] + 1)
        
        # 3. Drop ID if exists
        if 'Loan_ID' in df.columns:
            df = df.drop('Loan_ID', axis=1)
            
        return df