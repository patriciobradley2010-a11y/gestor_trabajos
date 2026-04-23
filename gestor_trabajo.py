import streamlit as st
import json
import os

# -----------------------------
# CONFIG
# -----------------------------
USUARIOS = {
    "pato": "1234"
}

DATA_FILE = "datos.json"

# -----------------------------
# FUNCIONES
# -----------------------------
def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_datos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------------
# SESSION
# -----------------------------
if "login" not in st.session_state:
    st.session_state.login = False

if "user" not in st.session_state:
    st.session_state.user = None

# -----------------------------
# APP
# -----------------------------
st.title("📚 Organizador Escolar")

data = cargar_datos()

# -----------------------------
# LOGIN
# -----------------------------
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

            st.success("Bienvenido Pato 😎")
        else:
            st.error("Datos incorrectos")

# -----------------------------
# PANEL
# -----------------------------
else:
    usuario = st.session_state.user

    st.sidebar.title("Menú")
    opcion = st.sidebar.radio("Ir a:", ["Tareas", "Exámenes"])

    st.write(f"👤 Usuario: {usuario}")

    # ---------------- TAREAS ----------------
    if opcion == "Tareas":
        st.subheader("📝 Tareas")

        nueva = st.text_input("Nueva tarea")

        if st.button("Agregar tarea"):
            if nueva:
                data[usuario]["tareas"].append({
                    "texto": nueva,
                    "hecho": False
                })
                guardar_datos(data)

        for i, tarea in enumerate(data[usuario]["tareas"]):
            col1, col2 = st.columns([4,1])

            with col1:
                if tarea["hecho"]:
                    st.write(f"✅ ~~{tarea['texto']}~~")
                else:
                    st.write(f"⬜ {tarea['texto']}")

            with col2:
                if not tarea["hecho"]:
                    if st.button("✔", key=f"t{i}"):
                        data[usuario]["tareas"][i]["hecho"] = True
                        guardar_datos(data)
                        st.rerun()

    # ---------------- EXAMENES ----------------
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

        for i, examen in enumerate(data[usuario]["examenes"]):
            col1, col2 = st.columns([4,1])

            with col1:
                if examen["hecho"]:
                    st.write(f"✅ ~~{examen['texto']}~~")
                else:
                    st.write(f"⬜ {examen['texto']}")

            with col2:
                if not examen["hecho"]:
                    if st.button("✔", key=f"e{i}"):
                        data[usuario]["examenes"][i]["hecho"] = True
                        guardar_datos(data)
                        st.rerun()

    # ---------------- LOGOUT ----------------
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.login = False
        st.session_state.user = None
        st.rerun()
   
