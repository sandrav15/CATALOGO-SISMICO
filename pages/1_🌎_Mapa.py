import streamlit as st

st.set_page_config(page_title="Mapa", page_icon="🌎")

st.title("Mapas")

data = st.session_state["data"]
data_map = data.rename(columns={"Latitud": "lat", "Longitud": "lon"})

year_to_filter = st.slider("Seleccione la información según el año:", 1960, 2021, 2000)

filtered_data_year = data_map[data_map["Año"] == year_to_filter]

st.subheader(f"Mapa de los sismos en el año {year_to_filter}" )
st.write(f"En el mapa, los puntos rojos señalan la latitud y longitud de los sismos ocurridos en el año {year_to_filter}.")
st.map(filtered_data_year)



magnitude_to_filter = st.select_slider(
    "Seleccione la información según la magnitud:",
    data_map.groupby(["Magnitud"]).count().index
    )
filtered_data_mag = data_map[data_map["Magnitud"] == magnitude_to_filter]

st.subheader(f"Mapa de los sismos de magnitud {magnitude_to_filter}")
st.write(f"En el mapa, los puntos rojos señalan la latitud y longitud de los sismos con magnitud {magnitude_to_filter}.")
st.map(filtered_data_mag)



deep_to_filter = st.select_slider(
    "Seleccione la información según la profundidad:",
    data_map.groupby(["Profundidad"]).count().index
    )
filtered_data_deep = data_map[data_map["Profundidad"] == deep_to_filter]

st.subheader(f"Mapa de los sismos de profundidad {deep_to_filter}")
st.write(f"En el mapa, los puntos rojos señalan la latitud y longitud de los sismos con profundidad {deep_to_filter}.")
st.map(filtered_data_deep)
