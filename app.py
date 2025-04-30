import gradio as gr
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Load the models
dt_model = joblib.load('dt_clf.pkl')
rf_model = joblib.load('rf_clf.pkl')



# Feature names
feature_names = [
    'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)',
    'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP',
    'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5',
    'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA',
    'spread1', 'spread2', 'D2', 'PPE'
]

# Prediction function
def predict(model_name, *inputs):
    input_data = pd.DataFrame([inputs], columns=feature_names)

    if model_name == "Decision Tree Classifier":
        model = dt_model
    else:
        model = rf_model

    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0]

    # Prepare prediction result
    if prediction == 1:
        pred_text = f"⚠️ Likely to have Parkinson's Disease. (Confidence: {prediction_proba[1]:.2f})"
    else:
        pred_text = f"✅ Unlikely to have Parkinson's Disease. (Confidence: {prediction_proba[0]:.2f})"

    # Create probability bar chart
    fig1, ax1 = plt.subplots()
    classes = ['Healthy', 'Parkinsons']
    colors = ['#4CAF50', '#F44336']
    ax1.bar(classes, prediction_proba, color=colors)
    ax1.set_ylim(0, 1)
    ax1.set_ylabel('Probability')
    ax1.set_title('Prediction Confidence')
    plt.close(fig1)

    # Create feature importance chart (only if Random Forest)
    fig2 = None
    if model_name == "Random Forest Classifier":
        importances = model.feature_importances_
        indices = np.argsort(importances)[-10:]  # Top 10 important features

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.barh(np.array(feature_names)[indices], importances[indices], color="#2196F3")
        ax2.set_xlabel('Importance')
        ax2.set_title('Top 10 Feature Importances')
        plt.tight_layout()
        plt.close(fig2)

    return pred_text, fig1, fig2

# Inputs
inputs = [
    gr.Dropdown(choices=["Decision Tree Classifier", "Random Forest Classifier"], label="🛠️ Select Model")
]

for feature in feature_names:
    inputs.append(gr.Number(label=f"🔹 {feature}"))

# Outputs
outputs = [
    gr.Textbox(label="📄 Prediction Result"),
    gr.Plot(label="📊 Prediction Probability"),
    gr.Plot(label="📈 Feature Importance (only for Random Forest)")
]

# App Layout
demo = gr.Interface(
    fn=predict,
    inputs=inputs,
    outputs=outputs,
    title="Parkinson's Disease Prediction App",
    description="""
    Upload patient's voice measurements to predict Parkinson's Disease.
    Choose between Decision Tree and Random Forest models.
    
    🔎 The model will predict and show probability graphs!
    """,
    theme="soft"
)

# # Launch
# if __name__ == "__main__":
#     app.launch(share=True)
