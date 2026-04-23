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
    st.subheader("Iniciar sesión")

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if user in USUARIOS and USUARIOS[user] == password:
            st.session_state.login = True
            st.session_state.user = user

            # Crear usuario en JSON si no existe
            if user not in data:
                data[user] = {
                    "materias": [],
                    "tareas": []
                }
                guardar_datos(data)

            st.success("Bienvenido Pato 😎")
        else:
            st.error("Usuario o contraseña incorrectos")

# -----------------------------
# PANEL PRINCIPAL
# -----------------------------
else:
    st.write(f"👤 Usuario: {st.session_state.user}")

    usuario = st.session_state.user

    # -------- MATERIAS --------
    st.subheader("Materias")
    nueva_materia = st.text_input("Agregar materia")

    if st.button("Agregar materia"):
        if nueva_materia:
            data[usuario]["materias"].append(nueva_materia)
            guardar_datos(data)

    for m in data[usuario]["materias"]:
        st.write("📘", m)

    # -------- TAREAS --------
    st.subheader("Tareas")
    nueva_tarea = st.text_input("Agregar tarea")

    if st.button("Agregar tarea"):
        if nueva_tarea:
            data[usuario]["tareas"].append(nueva_tarea)
            guardar_datos(data)

    for t in data[usuario]["tareas"]:
        st.write("📝", t)

    # -------- LOGOUT --------
    if st.button("Cerrar sesión"):
        st.session_state.login = False
        st.session_state.user = None
   
