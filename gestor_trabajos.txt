import streamlit as st
import json
import os

# --- Pesos ---
pesos = {
    "politica": 8,
    "literatura": 6,
    "economia": 9,
    "matematica": 6,
    "geografia": 5,
    "ingles": 4,
    "taller de ingles": 7,
    "espiritualidad betharramita": 6,
    "historia": 7,
    "taller de programacion": 3,
    "quimica": 6,
    "sociologia": 7,
    "comunicacion, cultura y sociedad": 6
}

ARCHIVO = "trabajos.json"

# --- cargar datos ---
if os.path.exists(ARCHIVO):
    with open(ARCHIVO, "r") as f:
        trabajos = json.load(f)
else:
    trabajos = []

# --- función ---
def calcular_score(peso, longitud, avance, dias):
    if dias <= 1:
        return 100
    return (peso * longitud * (6 - avance)) / dias

# --- UI ---
st.title("📚 Gestor de Trabajos")

materia = st.selectbox("Materia", list(pesos.keys()))
longitud = st.slider("Longitud", 1, 5)
avance = st.slider("Avance", 1, 5)
dias = st.number_input("Días restantes", min_value=0)

if st.button("Agregar trabajo"):
    score = calcular_score(pesos[materia], longitud, avance, dias)

    trabajos.append({
        "materia": materia,
        "dias": dias,
        "score": score
    })

    with open(ARCHIVO, "w") as f:
        json.dump(trabajos, f)

# --- mostrar ---
st.subheader("📊 Prioridades")

ordenados = sorted(trabajos, key=lambda x: x["score"], reverse=True)

for i, t in enumerate(ordenados):
    col1, col2 = st.columns([4, 1])

    with col1:
        st.write(f"{t['materia']} → {round(t['score'],2)} (faltan {t['dias']} días)")

    with col2:
        if st.button("✔️", key=i):
            trabajos.remove(t)

            with open(ARCHIVO, "w") as f:
                json.dump(trabajos, f)

            st.rerun()
