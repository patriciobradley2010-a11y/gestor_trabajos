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

            # 🔥 GARANTIZA QUE EL USUARIO EXISTA SIEMPRE
            if user not in datos:
                datos[user] = {
                    "trabajos": [],
                    "examenes": [],
                    "materias": {m: {"peso": p} for m, p in MATERIAS_BASE.items()}
                }
                guardar_datos(datos)

            st.rerun()

        else:
            st.error("Usuario o contraseña incorrectos")

# -----------------------------
# APP
# -----------------------------
else:

    user = st.session_state.user

    # 🔥 GARANTIZA ESTRUCTURA SIEMPRE (clave del fix)
    if user not in datos:
        datos[user] = {
            "trabajos": [],
            "examenes": [],
            "materias": {m: {"peso": p} for m, p in MATERIAS_BASE.items()}
        }
        guardar_datos(datos)

    user_data = datos[user]

    # -------------------------
    def calcular_score(peso, avance, longitud, dias):
        if dias <= 1:
            return 100
        return (peso * longitud * (6 - avance)) / max(dias, 1)

    # -------------------------
    menu = st.sidebar.radio(
        "Menú",
        ["📚 Trabajos", "📝 Exámenes", "⚙️ Materias", "✅ Cumplidos", "🚪 Salir"]
    )

    # =========================
    # TRABAJOS
    # =========================
    if menu == "📚 Trabajos":

        st.subheader("📚 Trabajos")

        materias = list(user_data["materias"].keys())

        if not materias:
            st.warning("No hay materias cargadas")
        else:
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

        for i, t in enumerate(trabajos):
            col1, col2 = st.columns([4,1])

            with col1:
                st.write(f"{t['titulo']} | {t['materia']} | {t['fecha']}")

            with col2:
                if st.button("✔️", key=f"done_{i}_{t['titulo']}"):
                    t["estado"] = "hecho"
                    guardar_datos(datos)
                    st.rerun()

    # =========================
    # EXAMENES
    # =========================
    elif menu == "📝 Exámenes":

        st.subheader("📝 Exámenes")

        materias = list(user_data["materias"].keys())

        if materias:
            materia = st.selectbox("Materia", materias)
            fecha = st.date_input("Fecha")
            temas = st.text_area("Temas")

            if st.button("Agregar examen"):
                user_data["examenes"].append({
                    "materia": materia,
                    "fecha": str(fecha),
                    "temas": temas.split(",")
                })
                guardar_datos(datos)
                st.rerun()

        for i, e in enumerate(user_data["examenes"]):
            with st.expander(f"{e['materia']} - {e['fecha']}"):
                for t in e["temas"]:
                    st.write("• " + t.strip())

    # =========================
    # MATERIAS
    # =========================
    elif menu == "⚙️ Materias":

        st.subheader("⚙️ Materias")

        for m, v in user_data["materias"].items():
            st.write(f"{m} - peso: {v['peso']}")

    # =========================
    # CUMPLIDOS
    # =========================
    elif menu == "✅ Cumplidos":

        st.subheader("✅ Cumplidos")

        for t in user_data["trabajos"]:
            if t["estado"] == "hecho":
                st.success(f"{t['titulo']} - {t['materia']}")

    # =========================
    # SALIR
    # =========================
    elif menu == "🚪 Salir":
        del st.session_state.user
        st.rerun()
