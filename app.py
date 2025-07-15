import streamlit as st
import pandas as pd
import requests
import json

# Fonction pour interroger Ollama Llama3.2
def ollama_llama32_humanize(analysis_text, model="llama3.2"):
    url = "http://localhost:11434/api/generate"
    prompt = (
        "Traduis cette analyse technique de tableau en langage humain, accessible à un non-expert, en français :\n\n"
        f"{analysis_text}\n"
    )
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except Exception as e:
        return f"Erreur lors de l'appel à Ollama : {e}"

st.title("Analyse Automatisée d'un Tableur Excel avec IA")

uploaded_file = st.file_uploader("Déposez votre fichier Excel (.xlsx)", type=['xlsx'])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("Aperçu du tableau importé :")
        st.dataframe(df)

        # Analyse automatique du tableau
        analysis = []
        analysis.append(f"Nombre de lignes : {df.shape[0]}")
        analysis.append(f"Nombre de colonnes : {df.shape[1]}")
        analysis.append("Colonnes et types :")
        for col in df.columns:
            analysis.append(f"- {col}: {df[col].dtype}")

        analysis.append("\nStatistiques descriptives :")
        analysis.append(str(df.describe(include='all')))

        # Facultatif : détection de valeurs manquantes
        missing = df.isnull().sum()
        if missing.sum() > 0:
            analysis.append("\nValeurs manquantes par colonne :")
            analysis.append(str(missing[missing > 0]))

        # Préparation du texte à envoyer à Ollama
        analysis_text = "\n".join(analysis)

        st.subheader("Analyse technique:")
        st.code(analysis_text)

        st.subheader("Analyse en langage humain (par Llama3.2):")
        with st.spinner("Demande à l'IA en cours..."):
            human_analysis = ollama_llama32_humanize(analysis_text)
            st.write(human_analysis)
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Uploadez un fichier Excel pour commencer l’analyse.")
