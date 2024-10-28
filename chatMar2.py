import openai
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import pandas as pd
import requests

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Configurar la clave API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# URL del archivo Excel en Supabase
excel_file_url = os.getenv("EXCEL_FILE_URL")


# Descargar el archivo Excel desde la URL y cargarlo en un DataFrame
try:
    response = requests.get(excel_file_url)
    response.raise_for_status()  # Verificar si hubo un error al descargar

    # Guardar el contenido en un archivo temporal y cargarlo con pandas
    with open("DatosBD3_temp.xlsx", "wb") as temp_file:
        temp_file.write(response.content)

    # Cargar el archivo Excel descargado en un DataFrame
    df = pd.read_excel("DatosBD3_temp.xlsx")

except Exception as e:
    st.error(f"Error al cargar el archivo desde Supabase: {e}")

# Configurar la página de Streamlit
st.set_page_config(page_title="IMARPE Chatbot y Excel Analyzer")

# Mostrar la imagen con el ajuste del tamaño
st.sidebar.image(
    "images/logo777.jpeg",  # Ajusta la ruta si es necesario
    use_column_width=False, 
    width=200,  # Ajusta el tamaño de la imagen según lo que desees
)

# Crear una barra de navegación en la barra lateral
seccion = st.sidebar.selectbox("Navegar a:", ["Chat IMARPE", "Consultas sobre Excel"])

# Funcionalidad del Chatbot especializado en IMARPE
if seccion == "Chat IMARPE":
    st.markdown(
        """
        <style>
        .imarpe-title {
            font-size: 30px;
            font-weight: bold;
            color: #0073e6;
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Título estilizado con ícono
    st.markdown('<div class="imarpe-title">🤖 E.M.A.i-iMAR-1 Bot - Análisis y Consultas Especializadas 🌊</div>', unsafe_allow_html=True)

    # Inicializar la sesión de mensajes
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "👋 ¡Hola! Soy **E.M.A.i-iMAR-1 Bot**, un asistente experto en **análisis científico y tecnológico del mar** para IMARPE 🌊. Estoy aquí para ofrecerte **información precisa, educativa y basada en datos relevantes** sobre temas relacionados con los estudios marinos y acuícolas. ¿En qué puedo ayudarte hoy?"
            }
        ]

    # Mostrar historial de mensajes
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    # Capturar entrada del usuario
    if user_input := st.chat_input("Escribe tu consulta sobre los estudios de IMARPE..."):
        # Añadir el mensaje del usuario al historial de la sesión
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # Crear un prompt personalizado según los requisitos, incluyendo información del Excel
        prompt = f"""
        Eres **E.M.A.i-iMAR-1 Bot**, un asistente virtual experto en análisis de datos marinos y acuícolas para IMARPE. 
        Cumples con los siguientes requisitos:
        1. Modo especialista experto en la información de datos adjuntos y análisis minucioso y detallado.
        2. Objetivo de IMARPE: realizar investigaciones científicas y tecnológicas del mar, aguas continentales y recursos acuícolas para su aprovechamiento racional.
        3. Usar NLP para elaborar respuestas en diferentes idiomas.
        4. Respuestas empáticas, asertivas, informativas y educativas.
        5. Análisis profundo basado en documentación e información relacionada, con palabras clave en **negrita**.
        6. Comprender el valor de la respuesta para el consultante.
        7. Enfocarse en la pregunta y comprender las necesidades del consultante.
        8. Lenguaje claro y conciso.
        9. Utilizar ejemplos aplicables con metáforas.
        10. Presentación bien estructurada y emocionalmente conectada.
        11. Transmitir confianza y autoridad.
        12. Lenguaje y tono respetuosos y empáticos.
        13. Ser la voz informada de los hechos.
        14. Dividir el contenido en secciones bien estructuradas y visualmente separadas.
        15. Comenzar con frases llamativas y emojis apropiados.
        16. Incluir datos y estadísticas relevantes.
        17. Elaborar estudios detallados con títulos, subtítulos, y desarrollo tecnológico en *cursiva* con palabras clave en **negrita**.
        18. Listar con emojis de números y mensajes en **negrita**.
        19. Resaltar mensajes principales en negrita.
        20. Usar métodos de precisión y veracidad.
        21. Asegurar precisión y veracidad sin ocultar contenido relevante.
        22. Si tienes dudas, preguntar antes de actualizar.
        23. Sugerir 3 preguntas para continuar el estudio al final de la respuesta.
        24. Respuestas en castellano.
        25. Usar información de internet hasta en un 35% del contenido si es necesario.

        Además, aquí tienes algunos datos clave del archivo Excel relacionado con embarcaciones:
        {df.head(10).to_string(index=False)}

        Basado en esta información y en la consulta del usuario:
        {user_input}
        """

        # Llamada a la API de OpenAI para obtener la respuesta
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres E.M.A.i-iMAR-1 Bot, un asistente experto en análisis de datos marinos y acuícolas para IMARPE."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extraer la respuesta del modelo
        response_message = response.choices[0].message["content"]

        # Añadir la respuesta del asistente al historial de la sesión
        st.session_state["messages"].append({"role": "assistant", "content": response_message})
        st.chat_message("assistant").write(response_message)

# Funcionalidad para realizar consultas sobre el archivo Excel
elif seccion == "Consultas sobre Excel":
    st.markdown(
        """
        <style>
        .excel-title {
            font-size: 30px;
            font-weight: bold;
            color: #0073e6;
            text-align: center;
            margin-bottom: 20px;
        }
        .excel-subtitle {
            font-size: 24px;
            font-weight: bold;
            color: #43526d;
            text-align: center;
            margin-bottom: 15px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Título estilizado en la sección "Consultas sobre Excel"
    st.markdown('<div class="excel-title">📊 Consultas sobre Excel - Análisis de Datos</div>', unsafe_allow_html=True)

    # Agregar una opción para subir un archivo Excel
    uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Cargar el archivo Excel en un DataFrame
        df_uploaded = pd.read_excel(uploaded_file)

        # Mostrar los primeros registros del archivo para que el usuario lo vea
        st.write("📄 **Vista previa de los datos cargados:**")
        st.write(df_uploaded.head())

        # Configurar el modelo de lenguaje de OpenAI
        llm = OpenAI(temperature=0.7, openai_api_key=openai.api_key)

        # Crear el agente utilizando el DataFrame
        agent = create_pandas_dataframe_agent(llm, df_uploaded, verbose=True, allow_dangerous_code=True)

        # Entrada del usuario para la pregunta
        user_question = st.text_input("Haz una pregunta sobre tu archivo Excel:")

        # Ejecutar la consulta cuando el usuario haga la pregunta
        if user_question:
            with st.spinner("Procesando..."):
                # Incluir el contexto del idioma en la pregunta
                prompt = f"Por favor, responde en español a esta pregunta: {user_question}"
                response = agent.run(prompt)
                st.write("💡 **Respuesta:**")
                st.write(response)
    else:
        st.write("Por favor, sube un archivo Excel para comenzar el análisis.")
