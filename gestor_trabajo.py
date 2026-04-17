import streamlit as st
import json
import os

ARCHIVO = "datos.json"

# -----------------------------
# CARGA DE DATOS
# -----------------------------
if os.path.exists(ARCHIVO):
    with open(ARCHIVO, "r") as f:
        datos = json.load(f)
else:
    datos = {}

# -----------------------------
# LOGIN SIMPLE
# -----------------------------
usuarios = {
    "juan": "1234",
    "maria": "abcd"
}

st.title("📚 Organizador de Estudio")

if "user" not in st.session_state:

    st.subheader("🔐 Login")

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):

        if user in usuarios and usuarios[user] == password:

            st.session_state.user = user

            if user not in datos:
                datos[user] = {
                    "trabajos": [],
                    "examenes": [],
                    "materias": {
                        "politica": 8,
                        "literatura": 6,
                        "economia": 9,
                        "matematica": 6
                    }
                }

        else:
            st.error("Usuario o contraseña incorrectos")

# -----------------------------
# APP PRINCIPAL
# -----------------------------
else:

    user = st.session_state.user
    st.sidebar.title(f"👤 {user}")

    if user not in datos:
        datos[user] = {"trabajos": [], "examenes": [], "materias": {}}

    user_data = datos[user]

    # -------------------------
    # FUNCION SCORE
    # -------------------------
    def calcular_score(peso, longitud, avance, dias):
        if dias <= 1:
            return 100
        return (peso * longitud * (6 - avance)) / dias

    # -------------------------
    # MENU
    # -------------------------
    menu = st.sidebar.radio("Menú", ["📚 Trabajos", "📝 Exámenes", "⚙️ Materias", "🚪 Cerrar sesión"])

    # =====================================================
    # TRABAJOS
    # =====================================================
    if menu == "📚 Trabajos":

        st.subheader("📚 Trabajos")

        materia = st.selectbox("Materia", list(user_data["materias"].keys()))
        longitud = st.slider("Longitud", 1, 5)
        avance = st.slider("Avance", 1, 5)
        dias = st.number_input("Días restantes", min_value=0)

        if st.button("Agregar trabajo"):

            peso = user_data["materias"][materia]
            score = calcular_score(peso, longitud, avance, dias)

            user_data["trabajos"].append({
                "materia": materia,
                "score": score,
                "dias": dias
            })

            with open(ARCHIVO, "w") as f:
                json.dump(datos, f)

        st.divider()

        st.subheader("📊 Prioridad")

        ordenados = sorted(user_data["trabajos"], key=lambda x: x["score"], reverse=True)

        for i, t in enumerate(ordenados):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"{t['materia']} → {round(t['score'],2)} (días: {t['dias']})")

            with col2:
                if st.button("✔️", key=f"t_{i}"):
                    user_data["trabajos"].remove(t)
                    with open(ARCHIVO, "w") as f:
                        json.dump(datos, f)
                    st.rerun()

    # =====================================================
    # EXÁMENES
    # =====================================================
    elif menu == "📝 Exámenes":

        st.subheader("📝 Exámenes")

        exam_materia = st.selectbox("Materia examen", list(user_data["materias"].keys()))
        fecha = st.text_input("Fecha (YYYY-MM-DD)")
        temas = st.text_area("Temas (separados por coma)")

        if st.button("Agregar examen"):

            user_data["examenes"].append({
                "materia": exam_materia,
                "fecha": fecha,
                "temas": [t.strip() for t in temas.split(",")]
            })

            with open(ARCHIVO, "w") as f:
                json.dump(datos, f)

        st.divider()

        for i, e in enumerate(user_data["examenes"]):

            with st.expander(f"{e['materia']} - {e['fecha']}"):

                st.write("📌 Temas:")
                for t in e["temas"]:
                    st.write("- " + t)

                if st.button("Eliminar examen", key=f"e_{i}"):
                    user_data["examenes"].remove(e)
                    with open(ARCHIVO, "w") as f:
                        json.dump(datos, f)
                    st.rerun()

    # =====================================================
    # MATERIAS (EDITABLES)
    # =====================================================
    elif menu == "⚙️ Materias":

        st.subheader("⚙️ Materias y dificultad")

        nueva = st.text_input("Agregar nueva materia")
        peso_nuevo = st.slider("Dificultad (1-10)", 1, 10)

        if st.button("Agregar materia") and nueva:

            user_data["materias"][nueva.lower()] = peso_nuevo

            with open(ARCHIVO, "w") as f:
                json.dump(datos, f)

        st.divider()

        st.write("📊 Editar existentes:")

        for m in list(user_data["materias"].keys()):

            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.write(m)

            with col2:
                nuevo_valor = st.number_input(
                    f"peso_{m}",
                    min_value=1,
                    max_value=10,
                    value=user_data["materias"][m],
                    key=m
                )

                user_data["materias"][m] = nuevo_valor

            with col3:
                if st.button("🗑️", key=f"del_{m}"):
                    del user_data["materias"][m]
                    st.rerun()

        with open(ARCHIVO, "w") as f:
            json.dump(datos, f)

    # =====================================================
    # LOGOUT
    # =====================================================
    elif menu == "🚪 Cerrar sesión":
        del st.session_state.user
        st.rerun()
