import streamlit as st
import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# 🔹 Azure API деректерін енгіз (бұларды Azure-дан аласың)
AZURE_AI_KEY = "5k96MSu2fN6fBVk8tWz9ijkteXyhaD7GrOWr3AZVM94ce5ZkPLVOJQQJ99BCACYeBjFXJ3w3AAAAACOGy7RA"
AZURE_AI_ENDPOINT = "https://teacherai.openai.azure.com/"

def authenticate_client():
    return TextAnalyticsClient(endpoint=AZURE_AI_ENDPOINT, credential=AzureKeyCredential(AZURE_AI_KEY))

client = authenticate_client()

# 🔹 Оқушылардың үлгерімін талдау
def analyze_performance(data):
    data['Орташа балл'] = data.iloc[:, 1:].mean(axis=1)

    recommendations = []
    for score in data['Орташа балл']:
        if score >= 4.5:
            rec = "Жақсы жұмыс! Осылай жалғастыр!"
        elif score >= 3.5:
            rec = "Қосымша тәжірибе қажет."
        else:
            rec = "Ойын элементтерімен оқыту ұсынылады."
        recommendations.append(rec)

    data['Ұсыныстар'] = recommendations
    return data

# 🔹 Streamlit интерфейсі
st.title("📚 Мұғалімге арналған виртуалды көмекші")
st.write("Оқушылардың бағалары бар CSV файлын жүктеңіз")

uploaded_file = st.file_uploader("CSV файлын таңдаңыз", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    result = analyze_performance(df)
    st.write("🔍 Үлгерімді талдау нәтижесі:")
    st.dataframe(result)

    st.download_button("Ұсыныстарды жүктеу", result.to_csv(index=False).encode('utf-8'), "recommendations.csv", "text/csv")
