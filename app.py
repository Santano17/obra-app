import streamlit as st
import pandas as pd
from datetime import date
import smtplib
from email.message import EmailMessage

# =====================================================
# CONFIGURACIÓN DE LA APP
# =====================================================

st.set_page_config(
    page_title="Seguimiento de Obra",
    page_icon="⚡",
    layout="centered"
)

# =====================================================
# LOGO EMPRESA
# =====================================================

try:
    st.image("logo.png", width=250)
except:
    st.warning("⚠️ No se encontró el archivo logo.png")

st.title("📊 Seguimiento de Obra")
st.subheader("SANTANO S.L. - OBRA ELÉCTRICA")

st.divider()

# =====================================================
# MEMORIA TEMPORAL DE REGISTROS
# =====================================================

if "registros" not in st.session_state:
    st.session_state.registros = []

# =====================================================
# DATOS DEL FORMULARIO
# =====================================================

trabajador = st.text_input(
    "👷 Nombre del trabajador"
)

fecha_envio = st.date_input(
    "📅 Fecha del informe",
    value=date.today()
)

# =====================================================
# LISTADO DE TAREAS
# =====================================================

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

# =====================================================
# ESTADOS DE LA TAREA
# =====================================================

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

# =====================================================
# BOTÓN PARA AÑADIR REGISTRO
# =====================================================

if st.button("➕ Añadir registro"):

    if trabajador.strip() == "":
        st.warning("⚠️ Introduce el nombre del trabajador")

    else:

        nuevo_registro = {
            "Trabajador": trabajador.strip(),
            "Fecha": fecha_envio,
            "Tarea": tarea,
            "Estado": estado
        }

        st.session_state.registros.append(
            nuevo_registro
        )

        st.success("✅ Registro añadido correctamente")

# =====================================================
# MOSTRAR REGISTROS
# =====================================================

st.divider()

st.subheader("📋 Registros guardados")

df = pd.DataFrame(
    st.session_state.registros
)

if len(df) > 0:
    st.dataframe(
        df,
        use_container_width=True
    )
else:
    st.info("Todavía no hay registros")

# =====================================================
# EXPORTAR A EXCEL
# =====================================================

nombre_excel = "seguimiento_obra.xlsx"

if len(df) > 0:

    df.to_excel(
        nombre_excel,
        index=False
    )

    with open(nombre_excel, "rb") as archivo:

        st.download_button(
            label="📥 Descargar Excel",
            data=archivo,
            file_name=nombre_excel,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# =====================================================
# CONFIGURACIÓN EMAIL
# =====================================================

# CORREO GMAIL REMITENTE
EMAIL_REMITENTE = "nunezs.daniel@alumnos25.fundacionmasaveu.com"

# CONTRASEÑA DE APLICACIÓN GOOGLE
PASSWORD_EMAIL = "zvbhfagykqjpjubo"

# DESTINATARIO
EMAIL_DESTINO = "ana@fundacionmasaveu.com"

# =====================================================
# FUNCIÓN ENVIAR EMAIL
# =====================================================

def enviar_email():

    # Asegurar que todo sea string
    remitente = str(EMAIL_REMITENTE).strip()
    password = str(PASSWORD_EMAIL).strip()

    # Permitir uno o varios destinatarios
    if isinstance(EMAIL_DESTINO, list):
        destinatarios = [str(x).strip() for x in EMAIL_DESTINO]
        destino_header = ", ".join(destinatarios)
    else:
        destinatarios = [str(EMAIL_DESTINO).strip()]
        destino_header = destinatarios[0]

    # Crear mensaje
    msg = EmailMessage()

    msg["Subject"] = "Parte de obra"
    msg["From"] = remitente
    msg["To"] = destino_header

    msg.set_content(
        "Adjunto Excel generado desde la app de seguimiento de obra."
    )

    # Adjuntar Excel
    with open(nombre_excel, "rb") as f:

        contenido = f.read()

        msg.add_attachment(
            contenido,
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=nombre_excel
        )

    # Conexión Gmail
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            remitente,
            password
        )

        smtp.send_message(msg)

# =====================================================
# BOTÓN ENVIAR EMAIL
# =====================================================

if len(df) > 0:

    if st.button("📧 Enviar Excel por correo"):

        try:

            enviar_email()

            st.success(
                "✅ Excel enviado correctamente"
            )

        except Exception as e:

            st.error(
                f"❌ Error enviando correo: {e}"
            )

# =====================================================
# INFORMACIÓN FINAL
# =====================================================

st.divider()

st.info(
    "📱 App desarrollada en Streamlit para seguimiento de obra."
)
