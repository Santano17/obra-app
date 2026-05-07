import streamlit as st
import pandas as pd
from datetime import date
import smtplib
from email.message import EmailMessage

# =========================================
# CONFIGURACIÓN DE LA APP
# =========================================

st.set_page_config(
    page_title="Seguimiento de Obra",
    page_icon="⚡",
    layout="centered"
)

# =========================================
# LOGO EMPRESA
# =========================================

st.image("logo.png", width=250)

st.title("📊 Seguimiento de Obra")
st.subheader("SANTANO S.L. - OBRA ELÉCTRICA")

st.divider()

# =========================================
# MEMORIA DE REGISTROS
# =========================================

if "registros" not in st.session_state:
    st.session_state.registros = []

# =========================================
# CAMPOS DEL FORMULARIO
# =========================================

trabajador = st.text_input(
    "👷 Nombre del trabajador"
)

fecha_envio = st.date_input(
    "📅 Fecha del informe",
    value=date.today()
)

# =========================================
# LISTA DE TAREAS
# =========================================

tareas = [
    "Trazado y marcado de cajas, tubos y cuadros",
    "Ejecución rozas en paredes y techos",
    "Montaje de soportes",
    "Colocación tubos y conductos",
    "Tendido de cables",
    "Identificación y etiquetado",
    "Conexionado de cables en bornes o regletas",
    "Instalación y conexionado de mecanismos",
    "Fijación de carril DIN y mecanismos en cuadro eléctrico",
    "Cableado interno del cuadro eléctrico",
    "Configuración de equipos domóticos y/o automáticos",
    "Conexionado de sensores/actuadores de equipos domóticos/automáticos",
    "Pruebas de continuidad",
    "Pruebas de aislamiento",
    "Verificación de tierras",
    "Programación del automatismo",
    "Pruebas de funcionamiento"
]

tarea = st.selectbox(
    "🛠️ Selecciona la tarea",
    tareas
)

# =========================================
# ESTADO DE LA TAREA
# =========================================

estados = [
    "Avance de la tarea en torno al 25%",
    "Avance de la tarea en torno al 50%",
    "Avance de la tarea en torno al 75%",
    "OK, finalizado sin errores",
    "Finalizado, pero con errores pendientes",
    "Finalizado y corregidos los errores"
]

estado = st.selectbox(
    "📊 Estado de la tarea",
    estados
)

# =========================================
# BOTÓN AÑADIR REGISTRO
# =========================================

if st.button("➕ Añadir registro"):

    if trabajador == "":
        st.warning("Introduce el nombre del trabajador")

    else:

        nuevo_registro = {
            "Trabajador": trabajador,
            "Fecha": fecha_envio,
            "Tarea": tarea,
            "Estado": estado
        }

        st.session_state.registros.append(
            nuevo_registro
        )

        st.success("✅ Registro añadido correctamente")

# =========================================
# MOSTRAR REGISTROS
# =========================================

st.divider()

st.subheader("📋 Registros guardados")

df = pd.DataFrame(
    st.session_state.registros
)

st.dataframe(
    df,
    use_container_width=True
)

# =========================================
# EXPORTAR A EXCEL
# =========================================

if len(df) > 0:

    nombre_excel = "seguimiento_obra.xlsx"

    df.to_excel(
        nombre_excel,
        index=False
    )

    # =====================================
    # DESCARGAR EXCEL
    # =====================================

    with open(nombre_excel, "rb") as file:

        st.download_button(
            label="📥 Descargar Excel",
            data=file,
            file_name=nombre_excel,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# =========================================
# CONFIGURACIÓN EMAIL
# =========================================

EMAIL_REMITENTE = "tuempresa@gmail.com"

# IMPORTANTE:
# Usa contraseña de aplicación Google
# SIN espacios
# SIN ñ
# SIN símbolos raros

PASSWORD_EMAIL = "abcdefghijklmnop"

EMAIL_DESTINO = "empresa@correo.com"

# =========================================
# FUNCIÓN ENVIAR EMAIL
# =========================================

def enviar_email(destino, archivo_excel):

    msg = EmailMessage()

    msg["Subject"] = "📊 Parte de obra"
    msg["From"] = EMAIL_REMITENTE
    msg["To"] = destino

    msg.set_content(
        "Adjunto Excel de seguimiento de obra."
    )

    # Adjuntar Excel
    with open(archivo_excel, "rb") as f:

        contenido = f.read()

        msg.add_attachment(
            contenido,
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=archivo_excel
        )

    # Enviar correo
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            EMAIL_REMITENTE,
            PASSWORD_EMAIL
        )

        smtp.send_message(msg)

# =========================================
# BOTÓN ENVIAR EMAIL
# =========================================

if len(df) > 0:

    if st.button("📧 Enviar Excel por correo"):

        try:

            enviar_email(
                EMAIL_DESTINO,
                nombre_excel
            )

            st.success(
                "✅ Excel enviado correctamente"
            )

        except Exception as e:

            st.error(
                f"❌ Error enviando email: {e}"
            )
