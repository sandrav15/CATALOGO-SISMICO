import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CATALOGO SISMICO PERÚ 1960-2021 (IGP)",
    page_icon="🗺️",
    # initial_sidebar_state="collapsed"
)

st.write("""
    La información contenida en esta página web permite acceder 
    al dataset “CATALOGO SISMICO 1960-2021 (IGP)”. 
    Se presentan los epicentros de los sismos en mapas 
    de acuerdo al año, la magnitud y la profundidad del 
    sismo. Así como también se presentan gráficos en base a la 
    magnitud, profundidad y la fecha del mismo. También se 
    permite el filtrado de datos en base a la magnitud, la 
    profundidad o la fecha.
""")

st.title("CATALOGO SISMICO EN EL PERÚ (1960-2021) (IGP)")

st.write("""El Perú es un país sísmico debido a que en su geografía se encuentran las
         placas de Nazca y Sudamericana. Por otro lado, el país ha registrado sismos
         de gran magnitud que le han ocasionado múltiples daños, tanto en infraestructura
         como en pérdida de vidas humanas. Es por ello, que es importante conocer la información
         de los sismos ocurridos en el país durante los últimos años, y así estar preparados
         para lo que pueda suceder en un futuro. Por tal motivo, se ha decidido realizar un
         catálogo sísmico.
         """)

st.write(
    """
    Un catálogo sísmico es una base de datos que contiene todos los 
    parámetros que caracterizan a un sismo, calculados en las mismas 
    condiciones, con el objetivo de constituirse como una base 
    homogénea útil para la realización de estudios en sismología. 
    El presente catálogo ha sido elaborado por el Instituto 
    Geofísico del Perú (IGP), institución responsable del 
    monitoreo de la actividad sísmica en el país, y contiene 
    todos aquellos sismos percibidos por la población y registrados 
    por la Red Sísmica Nacional desde 1960, fecha en la que 
    se inicia la vigilancia instrumental de la sismicidad 
    en el Perú.
    """
)

st.header("Conjunto de datos")


@st.cache
def load_data():
    url = "https://www.datosabiertos.gob.pe/sites/default/files/Catalogo1960_2021.xlsx"
    data_raw = pd.read_excel(url)
    data = data_raw.set_index("ID")
    return data


loading = st.text("Cargando datos ...")
data = load_data()
st.dataframe(data)
loading.empty()

st.write("El dataset del catálogo sísmico se encuentra en el siguiente [link](https://www.datosabiertos.gob.pe/sites/default/files/Catalogo1960_2021.xlsx)")

st.subheader("Columnas")
st.write(
    """
    - **FECHA_UTC**: Hora universal coordinado (UTC), es la fecha con cinco horas 
        adelantadas con respecto a la hora local debido a que Peru 
        se encuentra en una zona horaria UTC -5. 
    - **HORA_UTC**: Hora universal coordinada (UTC), cinco horas adelantadas 
        con respecto a la hora local debido a que Peru se encuentra 
        en una zona horaria UTC -5.
    - **LATITUD**: Es la distancia en grados, minutos y segundos que hay con 
        respecto al paralelo principal, que es el ecuador (0º). 
        La latitud puede ser norte y sur.
    - **LONGITUD**: Es la distancia en grados, minutos y segundos que hay 
        con respecto al meridiano principal, que es el meridiano de Greenwich (0º).
    - **PROFUNDIDAD**: Profundidad del foco sísmico por debajo de la superficie.
    - **MAGNITUD**: Corresponde a la cantidad de energía liberada por el sismo 
        y esta expresada en la escala de magnitud momento Mw.
    - **FECHA_CORTE**: Fecha de corte de información.
"""
)


def get_new_data(data):
    FECHA_CORTE = data.at[0, "FECHA_CORTE"]
    data = data.drop(columns=["FECHA_CORTE"], axis=1)
    data["FECHA_UTC"] = pd.to_datetime(data["FECHA_UTC"], format="%Y%m%d")
    data.rename(columns={"LATITUD": "Latitud", "LONGITUD": "Longitud"}, inplace=True)

    if "FECHA_CORTE" not in st.session_state:
        st.session_state["FECHA_CORTE"] = FECHA_CORTE

    new_data = data.copy(deep=True)
    new_data["Año"] = new_data["FECHA_UTC"].dt.year
    new_data["Mes"] = new_data["FECHA_UTC"].dt.month
    new_data["Dia"] = new_data["FECHA_UTC"].dt.day
    new_data["HORA_UTC"] = new_data["HORA_UTC"].astype(str)
    dic_hora = {
        "Hora": [],
        "Minutos": [],
        "Segundos": [],
    }
    for i in new_data["HORA_UTC"]:
        dic_hora["Hora"].append(i[:-4])
        dic_hora["Minutos"].append(i[-4:-2])
        dic_hora["Segundos"].append(i[-2:])
    new_data.drop(["FECHA_UTC"], axis=1, inplace=True)
    new_data.drop(["HORA_UTC"], axis=1, inplace=True)
    new_data = pd.concat([new_data, pd.DataFrame(dic_hora)], axis=1)
    new_data.rename(
        {"MAGNITUD": "Magnitud", "PROFUNDIDAD": "Profundidad"}, axis=1, inplace=True
    )
    new_data = new_data[
        [
            "Año",
            "Mes",
            "Dia",
            "Hora",
            "Minutos",
            "Segundos",
            "Latitud",
            "Longitud",
            "Magnitud",
            "Profundidad",
        ]
    ]
    return new_data


new_data = get_new_data(data)
if "data" not in st.session_state:
    st.session_state["data"] = new_data

st.subheader("Cambios en los datos")
st.write("Se hizo cambios al conjunto de datos para un mejor análisis.")
st.subheader("Columnas")
st.write(
    """
    - **Año**: Año cuando ocurrió el sismo.
    - **Mes**: Mes cuando ocurrió el sismo.
    - **Día**: Día cuando ocurrió el sismo.
    - **Hora**: Hora cuando ocurrió el sismo.
    - **Minutos**: Minutos cuando ocurrió el sismo.
    - **Segundos**: Segundos cuando ocurrió el del sismo.
    - **Latitud**: Es la distancia en grados, minutos y segundos que hay con 
        respecto al paralelo principal, que es el ecuador (0º). 
        La latitud puede ser norte y sur.
    - **Longitud**: Es la distancia en grados, minutos y segundos que hay 
        con respecto al meridiano principal, que es el meridiano de Greenwich (0º).
    - **Profundidad**: Profundidad del foco sísmico por debajo de la superficie.
    - **Magnitud**: Corresponde a la cantidad de energía liberada por el sismo 
        y esta expresada en la escala de magnitud momento Mw.
"""
)
st.write(new_data)


with st.sidebar:
    st.write(f"Authores : ")
    name = "- AYDEE ZENAIDA "
    last_name = "QUISPE RIMACHI"
    st.write(f"  {name} {last_name}")
    name = "- DIANA MARYSABELL "
    last_name = "LLAMOCA ZARATE"
    st.write(f"  {name} {last_name}")
    name = "- JOSUE EDUARDO"
    last_name = "HUARAUYA FABIAN"
    st.write(f"  {name} {last_name}")
    name = "- SANDRA"
    last_name = "VILLEGAS HUAMAN"
    st.write(f"  {name} {last_name}")
