import streamlit as st
import json
import os
from datetime import date

ARCHIVO = "datos.json"

# -----------------------------
# CARGAR DATOS
# -----------------------------
if os.path.exists(ARCHIVO):
    with open(ARCHIVO, "r") as f:
        datos = json.load(f)
else:
    datos = {}

# -----------------------------
# USUARIO ÚNICO
# -----------------------------
usuarios = {
    "pato": "1234"
}

# -----------------------------
# INIT APP
# -----------------------------
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

            if user not in datos:
                datos[user] = {
                    "trabajos": [],
                    "examenes": [],
                    "materias": {
                        "politica": {"peso": 8},
                        "literatura": {"peso": 6},
                        "economia": {"peso": 9},
                        "matematica": {"peso": 6}
                    }
                }

                with open(ARCHIVO, "w") as f:
                    json.dump(datos, f)

            st.rerun()

        else:
            st.error("Usuario o contraseña incorrectos")

# -----------------------------
# APP PRINCIPAL
# -----------------------------
else:

    user = st.session_state.user

    if user not in datos:
        datos[user] = {"trabajos": [], "examenes": [], "materias": {}}

    user_data = datos[user]

    # -------------------------
    # FUNCION SCORE
    # -------------------------
    def calcular_score(peso, avance, longitud, dias):
        if dias <= 1:
            return 100
        return (peso * longitud * (6 - avance)) / dias

    # -------------------------
    # MENU
    # -------------------------
    menu = st.sidebar.radio(
        "Menú",
        ["📚 Trabajos", "📝 Exámenes", "⚙️ Materias", "✅ Cumplidos", "🚪 Salir"]
    )

    # =====================================================
    # TRABAJOS
    # =====================================================
    if menu == "📚 Trabajos":

        st.subheader("📚 Trabajos")

        materias = list(user_data["materias"].keys())

        if materias:

            materia = st.selectbox("Materia", materias)
            titulo = st.text_input("Título del trabajo")

            col1, col2 = st.columns(2)

            with col1:
                fecha = st.date_input("Fecha de entrega")

            with col2:
                longitud = st.slider("Longitud", 1, 5)

            avance = st.slider("Avance", 1, 5)

            if st.button("Agregar trabajo"):

                hoy = date.today()
                dias = (fecha - hoy).days

                peso = user_data["materias"][materia]["peso"]

                score = calcular_score(peso, avance, longitud, dias)

                user_data["trabajos"].append({
                    "titulo": titulo,
                    "materia": materia,
                    "fecha": str(fecha),
                    "dias": dias,
                    "score": score,
                    "estado": "pendiente"
                })

                with open(ARCHIVO, "w") as f:
                    json.dump(datos, f)

        st.divider()

        st.subheader("📊 Pendientes")

        trabajos = [t for t in user_data["trabajos"] if t["estado"] == "pendiente"]
        ordenados = sorted(trabajos, key=lambda x: x["score"], reverse=True)

        for i, t in enumerate(ordenados):

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"🏷️ {t['titulo']} | 📚 {t['materia']} | 📅 {t['fecha']} | ⭐ {round(t['score'],2)}")

            with col2:
                if st.button("✔️", key=f"done_{i}"):

                    for x in user_data["trabajos"]:
                        if x == t:
                            x["estado"] = "hecho"

                    with open(ARCHIVO, "w") as f:
                        json.dump(datos, f)

                    st.rerun()

    # =====================================================
    # EXÁMENES
    # =====================================================
    elif menu == "📝 Exámenes":

        st.subheader("📝 Exámenes")

        materias = list(user_data["materias"].keys())

        if materias:

            materia = st.selectbox("Materia", materias)
            fecha = st.date_input("Fecha examen")
            temas = st.text_area("Temas (coma separada)")

            if st.button("Agregar examen"):

                user_data["examenes"].append({
                    "materia": materia,
                    "fecha": str(fecha),
                    "temas": [t.strip() for t in temas.split(",")]
                })

                with open(ARCHIVO, "w") as f:
                    json.dump(datos, f)

        st.divider()

        for i, e in enumerate(user_data["examenes"]):

            with st.expander(f"📝 {e['materia']} - {e['fecha']}"):

                for t in e["temas"]:
                    st.write("• " + t)

    # =====================================================
    # MATERIAS
    # =====================================================
    elif menu == "⚙️ Materias":

        st.subheader("⚙️ Materias")

        nueva = st.text_input("Nueva materia")
        peso = st.slider("Dificultad", 1, 10)

        if st.button("Agregar materia") and nueva:

            user_data["materias"][nueva.lower()] = {
                "peso": peso
            }

            with open(ARCHIVO, "w") as f:
                json.dump(datos, f)

        st.divider()

        for m, v in user_data["materias"].items():

            st.markdown(f"📘 **{m}** - peso: {v['peso']}")

    # =====================================================
    # CUMPLIDOS
    # =====================================================
    elif menu == "✅ Cumplidos":

        st.subheader("✅ Cumplidos / Vencidos")

        hoy = date.today()

        for t in user_data["trabajos"]:

            fecha = date.fromisoformat(t["fecha"])

            if t["estado"] == "hecho":

                st.success(f"✔️ {t['titulo']} - {t['materia']}")

            elif fecha < hoy:

                st.error(f"⚠️ VENCIDO: {t['titulo']} - {t['materia']}")

    # =====================================================
    # SALIR
    # =====================================================
    elif menu == "🚪 Salir":
        del st.session_state.user
        st.rerun()
