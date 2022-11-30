import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="Graficas", page_icon="📈")

MAG = None  # MAGNITUD
DEEP = None  # PROFUNDIDAD

st.title("Datos")

data = st.session_state["data"]

st.subheader("Filtrar información según magnitud y profundidad.")

col1, col2 = st.columns(2)

with col1:
    opt = ["Todos"] + list(pd.unique(data["Magnitud"].sort_values()))
    MAG = st.selectbox(label="Magnitud", options=opt)

with col2:
    opt = ["Todos"] + list(
        pd.unique(data[data["Magnitud"] == MAG]["Profundidad"].sort_values())
    )
    # opt = ["Todos"] +  list(pd.unique(data["PROFUNDIDAD"].sort_values()))
    DEEP = st.selectbox(label="Profundidad", options=opt)


def get_filtered_data(data, mag, deep):
    filtered_data = data.copy(deep=True)
    if mag != "Todos":
        filtered_data = filtered_data[filtered_data["Magnitud"] == mag]
    if deep != "Todos":
        filtered_data = filtered_data[filtered_data["Profundidad"] == deep]
    return filtered_data


filtered_data = get_filtered_data(data, MAG, DEEP)
if filtered_data.size == 0:
    st.write("No se encontraron sismos")
st.write(filtered_data)


st.subheader("Filtrar según año, mes y día.")


days = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo")
months = (
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
)
years = [i for i in range(1960, 2022)]

col1_year, col_month, cold_day = st.columns(3)

with col1_year:
    select_year = st.selectbox(label="Año", options=years)


with col_month:
    select_month = st.selectbox(label="Mes", options=months)
    select_month = months.index(select_month) + 1


with cold_day:
    select_day = st.selectbox(label="Día", options=days)
    select_day = days.index(select_day)  + 1


def get_data_filer_date(data, year, month, day):
    filtered_data = data.copy(deep=True)
    filtered_data = filtered_data[
        (filtered_data["Año"] == year)
        & (filtered_data["Mes"] == month) # & (filtered_data["Dia"] == day)
    ]
    filtered_data["Dia"] = filtered_data["Dia"].astype(int)
    filtered_data = filtered_data[filtered_data["Dia"]%7 == day]
    return filtered_data


date_data = get_data_filer_date(data, select_year, select_month, select_day)

if date_data.size == 0:
    st.write("No se encontraron sismos")
st.write(date_data)
