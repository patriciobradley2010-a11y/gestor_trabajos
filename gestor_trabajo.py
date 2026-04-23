import streamlit as st
import json
import os
from datetime import date

ARCHIVO = "datos.json"

# -----------------------------
# MATERIAS FIJAS
# -----------------------------
MATERIAS_BASE = {
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

# -----------------------------
# FUNCIONES SEGURAS
# -----------------------------
def cargar_datos():
    if not os.path.exists(ARCHIVO):
        return {}
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except:
        return {}

def guardar_datos(data):
    with open(ARCHIVO, "w") as f:
        json.dump(data, f, indent=4)

# 🔥 VALIDADOR TOTAL (clave)
def validar_usuario(data, user):
    if user not in data:
        data[user] = {}

    user_data = data[user]

    if "trabajos" not in user_data or not isinstance(user_data["trabajos"], list):
        user_data["trabajos"] = []

    if "examenes" not in user_data or not isinstance(user_data["examenes"], list):
        user_data["examenes"] = []

    if "materias" not in user_data or not isinstance(user_data["materias"], dict):
        user_data["materias"] = {m: {"peso": p} for m, p in MATERIAS_BASE.items()}

    return user_data

# -----------------------------
# INIT
# -----------------------------
datos = cargar_datos()
usuarios = {"pato": "1234"}

st.title("📚 Organizador de Estudio")

# -----------------------------
# LOGIN
# -----------------------------
if "user" not in st.session_state:

    st.subheader("🔐 Login")

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        if user in usuarios and usuarios[user] == password:

            st.session_state.user = user

            user_data = validar_usuario(datos, user)
            guardar_datos(datos)

            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

# -----------------------------
# APP
# -----------------------------
else:

    user = st.session_state.user
    user_data = validar_usuario(datos, user)
    guardar_datos(datos)

    def calcular_score(peso, avance, longitud, dias):
        if dias <= 1:
            return 100
        return (peso * longitud * (6 - avance)) / max(dias, 1)

    menu = st.sidebar.radio(
        "Menú",
        ["📚 Trabajos", "📝 Exámenes", "⚙️ Materias", "✅ Cumplidos", "🚪 Salir"]
    )

    # ---------------- TRABAJOS ----------------
    if menu == "📚 Trabajos":

        st.subheader("📚 Trabajos")

        materias = list(user_data["materias"].keys())

        materia = st.selectbox("Materia", materias)
        titulo = st.text_input("Título")

        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Entrega")
        with col2:
            longitud = st.slider("Longitud", 1, 5)

        avance = st.slider("Avance", 1, 5)

        if st.button("Agregar trabajo"):
            dias = (fecha - date.today()).days
            peso = user_data["materias"][materia]["peso"]

            user_data["trabajos"].append({
                "titulo": titulo,
                "materia": materia,
                "fecha": str(fecha),
                "score": calcular_score(peso, avance, longitud, dias),
                "estado": "pendiente"
            })

            guardar_datos(datos)
            st.rerun()

        st.divider()

        trabajos = [t for t in user_data["trabajos"] if t["estado"] == "pendiente"]
        ordenados = sorted(trabajos, key=lambda x: x["score"], reverse=True)

        for i, t in enumerate(ordenados):

            col1, col2 = st.columns([4,1])

            with col1:
                st.write(f"{t['titulo']} | {t['materia']} | {t['fecha']} | ⭐ {round(t['score'],2)}")

            with col2:
                if st.button("✔️", key=f"done_{i}_{t['titulo']}"):
                    t["estado"] = "hecho"
                    guardar_datos(datos)
                    st.rerun()

    # ---------------- EXAMENES ----------------
    elif menu == "📝 Exámenes":

        st.subheader("📝 Exámenes")

        materia = st.selectbox("Materia", list(user_data["materias"].keys()))
        fecha = st.date_input("Fecha")
        temas = st.text_area("Temas")

        if st.button("Agregar examen"):
            user_data["examenes"].append({
                "materia": materia,
                "fecha": str(fecha),
                "temas": [t.strip() for t in temas.split(",")]
            })

            guardar_datos(datos)
            st.rerun()

        st.divider()

        for i, e in enumerate(user_data["examenes"]):
            with st.expander(f"{e['materia']} - {e['fecha']}"):
                for t in e["temas"]:
                    st.write("• " + t)

    # ---------------- MATERIAS ----------------
    elif menu == "⚙️ Materias":

        st.subheader("⚙️ Materias")

        for m, v in user_data["materias"].items():
            st.write(f"{m} - peso: {v['peso']}")

    # ---------------- CUMPLIDOS ----------------
    elif menu == "✅ Cumplidos":

        st.subheader("✅ Cumplidos / Vencidos")

        hoy = date.today()

        for t in user_data["trabajos"]:
            fecha = date.fromisoformat(t["fecha"])

            if t["estado"] == "hecho":
                st.success(f"{t['titulo']} - {t['materia']}")
            elif fecha < hoy:
                st.error(f"VENCIDO: {t['titulo']} - {t['materia']}")

    # ---------------- SALIR ----------------
    elif menu == "🚪 Salir":
        del st.session_state.user
        st.rerun()
