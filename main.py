import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Example dataset
data = {
    'income': [5000, 6000, 7000, 8000, 9000],
    'expenses': [2000, 2500, 3000, 3500, 4000],
    'investment': [1000, 1200, 1500, 1800, 2000],
    'savings_goal': [500, 600, 700, 800, 900]
}

df = pd.DataFrame(data)

# Preprocessing
X = df[['income', 'expenses', 'investment']]
y = df['savings_goal']

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scaling the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Training the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Save the model and scaler
joblib.dump(model, 'random_forest_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
