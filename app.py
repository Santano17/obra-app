import streamlit as st
import pandas as pd
from datetime import date
import smtplib
from email.message import EmailMessage
import os

st.title("📊 Seguimiento de Obra")

# 🧠 Estado en memoria
if "registros" not in st.session_state:
    st.session_state.registros = []

# 👷 Datos
trabajador = st.text_input("👷 Trabajador")
fecha_envio = st.date_input("📅 Fecha", value=date.today())

tareas = ["Trazado y marcado", "Ejecución rozas", "Montaje soportes"]
estados = ["25%", "50%", "75%", "Finalizado"]

tarea = st.selectbox("Tarea", tareas)
estado = st.selectbox("Estado", estados)

# ➕ Añadir registro
if st.button("Añadir"):
    st.session_state.registros.append({
        "Trabajador": trabajador,
        "Fecha": fecha_envio,
        "Tarea": tarea,
        "Estado": estado
    })
    st.success("Registro añadido")

st.divider()

# 📋 DataFrame
df = pd.DataFrame(st.session_state.registros)
st.dataframe(df)

# 📁 Generar Excel temporal
excel_file = "obra.xlsx"
df.to_excel(excel_file, index=False)

# 📧 Función enviar correo
def enviar_email(destino, archivo):

    remitente = "tuempresa@gmail.com"
    password = "CONTRASEÑA_DE_APP"  # importante: no usar contraseña normal

    msg = EmailMessage()
    msg["Subject"] = "📊 Parte de obra"
    msg["From"] = remitente
    msg["To"] = destino
    msg.set_content("Adjunto el parte de obra en Excel.")

    with open(archivo, "rb") as f:
        file_data = f.read()

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="parte_obra.xlsx"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, password)
        smtp.send_message(msg)

# 📩 Email destino fijo empresa
email_empresa = "empresa@correo.com"

# 🚀 Botón enviar
if st.button("📧 Enviar Excel por correo"):

    if len(df) == 0:
        st.warning("No hay datos para enviar")
    else:
        enviar_email(email_empresa, excel_file)
        st.success("Excel enviado correctamente")
