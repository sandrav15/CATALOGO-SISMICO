import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Graficas", page_icon="📈")

st.title("Gráficos")

data = st.session_state["data"]

options = st.multiselect(
    'Seleccione la información que desea observar para que sea mostrada en un histograma:',
    ['Magnitud', "Profundidad"],
    ['Magnitud'])

if "Magnitud" in options:
    st.header("Histograma de Magnitudes")

    mag_chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            alt.X("Magnitud:Q", bin=alt.BinParams(maxbins=30), title="Magnitud"),
            alt.Y("count()", title="Frecuencia de Magnitudes"),
        )
    )
    mag_chart.title = "Histograma de Magnitud"
    # chart.encoding.x.title = "Magnitud"
    # chart.encoding.y.title = "Frecuencia de Magnitudes"

    st.altair_chart(mag_chart, use_container_width=True)
    st.write("""Este gráfico muestra las magnitudes de los
             sismos registrados.
             La mayor cantidad de sismos registrados tiene una magnitud promedio
             de 4.4 - 5.
             """)

data = st.session_state["data"]

if "Profundidad" in options:
    st.header("Histograma de Profundidad")

    deep_chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            alt.X("Profundidad:Q", bin=alt.BinParams(maxbins=30), title="Profundidad"),
            alt.Y("count()", title="Frecuencia de Profundidades"),
        )
    )
    deep_chart.title = "Histograma de Profundidad"
    st.altair_chart(deep_chart, use_container_width=True)
    st.write("""Este gráfico muestra la frecuencia de las profundidades
             en los sismos registrados.
             La mayor cantidad de sismos registrados presenta una
             profundidad de 0 - 50.""")


options_2 = st.multiselect(
    'Seleccione la información que desea observar para que sea mostrada en el gráfico de barras: ',
    ['Mes', "Día", "Año"],
    ['Día'])


list_month = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junior",
    "Julio",
    "Agosto",
    "Setiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]

list_days = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

if "Mes" in options_2:
    st.header("Sismos por mes")
    data_mes = data.groupby(["Mes"])["Mes"].count()
    data_mes = pd.DataFrame({"Mes": list_month,
                             "Sismos": list(data_mes)})
    chart_mes = (
        alt.Chart(data_mes)
        .mark_bar()
        .encode(
            alt.X("Mes", sort=None, title="Mes"),
            alt.Y("Sismos", title="Cantidad de sismos"),
        )
    )
    chart_mes.title = "Sismos por mes"
    st.altair_chart(chart_mes, use_container_width=True)


if "Día" in options_2:
    st.header("Sismos por día")
    ddata = data.copy(deep=True)
    ddata["Dia"] = ddata["Dia"].astype(int)
    ddata["Dia"]= ddata["Dia"]%7
    data_day = ddata.groupby(["Dia"])["Dia"].count()
    data_day = pd.DataFrame({"Dia": list_days,
                             "Sismos": list(data_day)})
    chart_day = (
        alt.Chart(data_day)
        .mark_bar()
        .encode(
            alt.X("Dia", title="Dia", sort=None),
            alt.Y("Sismos", title="Cantidad de sismos"),
        )
    )
    chart_day.title = "Sismos por día"
    st.altair_chart(chart_day, use_container_width=True)

if "Año" in options_2:
    st.header("Sismos por Año")
    data_year = data.groupby(["Año"])["Año"].count()
    data_year = pd.DataFrame({"Año": [i for i in range(1960, 2022)],
                             "Sismos": list(data_year)})
    chart_year = (
        alt.Chart(data_year)
        .mark_bar()
        .encode(
            alt.X("Año", sort=None, title="Año"),
            alt.Y("Sismos", title="Cantidad de sismos"),
        )
    )
    chart_year.title = "Sismos por Año"
    st.altair_chart(chart_year, use_container_width=True)
