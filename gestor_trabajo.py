import streamlit as st
import json
import os
from datetime import date

# ---------------- CONFIG ----------------
USUARIOS = {"pato": "1234"}
DATA_FILE = "datos.json"

# ---------------- FUNCIONES ----------------
def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_datos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- SESSION ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- APP ----------------
st.title("📚 Organizador Escolar PRO")

data = cargar_datos()

# ---------------- LOGIN ----------------
if not st.session_state.login:
    st.subheader("Login")
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if user in USUARIOS and USUARIOS[user] == password:
            st.session_state.login = True
            st.session_state.user = user

            if user not in data:
                data[user] = {
                    "tareas": [],
                    "examenes": []
                }
                guardar_datos(data)

            st.rerun()
        else:
            st.error("Datos incorrectos")

# ---------------- PANEL ----------------
else:
    usuario = st.session_state.user

    # -------- SIDEBAR --------
    st.sidebar.title("📌 Menú")
    opcion = st.sidebar.selectbox(
        "Secciones",
        ["Dashboard", "Tareas", "Exámenes", "Cumplidos"]
    )

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.login = False
        st.session_state.user = None
        st.rerun()

    st.write(f"👤 Usuario: {usuario}")

    # -------- CALENDARIO (minimizable) --------
    with st.expander("📅 Calendario"):
        st.date_input("Seleccionar fecha", date.today())

    # -------- DASHBOARD --------
    if opcion == "Dashboard":
        st.subheader("📊 Resumen")

        tareas = data[usuario]["tareas"]
        examenes = data[usuario]["examenes"]

        pendientes = sum(not t["hecho"] for t in tareas) + sum(not e["hecho"] for e in examenes)
        completados = sum(t["hecho"] for t in tareas) + sum(e["hecho"] for e in examenes)

        st.write(f"🟡 Pendientes: {pendientes}")
        st.write(f"🟢 Completados: {completados}")

    # -------- TAREAS --------
    elif opcion == "Tareas":
        st.subheader("📝 Tareas")

        nueva = st.text_input("Nueva tarea")

        if st.button("Agregar tarea"):
            if nueva:
                data[usuario]["tareas"].append({
                    "texto": nueva,
                    "hecho": False
                })
                guardar_datos(data)
                st.rerun()

        for i, t in enumerate(data[usuario]["tareas"]):
            if not t["hecho"]:
                col1, col2 = st.columns([4,1])

                with col1:
                    st.write(f"⬜ {t['texto']}")

                with col2:
                    if st.button("✔", key=f"t{i}"):
                        data[usuario]["tareas"][i]["hecho"] = True
                        guardar_datos(data)
                        st.rerun()

    # -------- EXAMENES --------
    elif opcion == "Exámenes":
        st.subheader("📚 Exámenes")

        nuevo = st.text_input("Nuevo examen")

        if st.button("Agregar examen"):
            if nuevo:
                data[usuario]["examenes"].append({
                    "texto": nuevo,
                    "hecho": False
                })
                guardar_datos(data)
                st.rerun()

        for i, e in enumerate(data[usuario]["examenes"]):
            if not e["hecho"]:
                col1, col2 = st.columns([4,1])

                with col1:
                    st.write(f"⬜ {e['texto']}")

                with col2:
                    if st.button("✔", key=f"e{i}"):
                        data[usuario]["examenes"][i]["hecho"] = True
                        guardar_datos(data)
                        st.rerun()

    # -------- CUMPLIDOS --------
    elif opcion == "Cumplidos":
        st.subheader("✅ Completados")

        for t in data[usuario]["tareas"]:
            if t["hecho"]:
                st.write(f"📝 {t['texto']}")

        for e in data[usuario]["examenes"]:
            if e["hecho"]:
                st.write(f"📚 {e['texto']}")
