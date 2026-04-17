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
# USUARIOS BASE (demo)
# -----------------------------
usuarios = {
    "juan": "1234",
    "maria": "abcd"
}

# -----------------------------
# INIT APP
# -----------------------------
st.title("📚 Organizador de Estudio")

# -----------------------------
# LOGIN / REGISTRO
# -----------------------------
if "user" not in st.session_state:

    st.subheader("🔐 Login / Registro")

    modo = st.radio("Modo", ["Login", "Registro"])

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Continuar"):

        # LOGIN
        if modo == "Login":

            if user in usuarios and usuarios[user] == password:

                st.session_state.user = user

                if user not in datos:
                    datos[user] = {
                        "trabajos": [],
                        "examenes": [],
                        "materias": {
                            "politica": {"peso": 8, "color": "#ef4444"},
                            "literatura": {"peso": 6, "color": "#22c55e"},
                            "economia": {"peso": 9, "color": "#3b82f6"},
                            "matematica": {"peso": 6, "color": "#f59e0b"}
                        }
                    }

            else:
                st.error("Usuario o contraseña incorrectos")

        # REGISTRO
        else:

            if user in usuarios:
                st.error("El usuario ya existe")
            else:
                usuarios[user] = password

                datos[user] = {
                    "trabajos": [],
                    "examenes": [],
                    "materias": {}
                }

                st.session_state.user = user
                st.success("Usuario creado")

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
        color = st.color_picker("Color")

        if st.button("Agregar materia") and nueva:

            user_data["materias"][nueva.lower()] = {
                "peso": peso,
                "color": color
            }

            with open(ARCHIVO, "w") as f:
                json.dump(datos, f)

        st.divider()

        for m, v in user_data["materias"].items():

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"🟦 **{m}** - peso: {v['peso']}")

            with col2:
                st.write(v["color"])

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

   
