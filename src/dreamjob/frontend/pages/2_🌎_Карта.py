import streamlit as st

st.set_page_config(
    page_title="Карта", page_icon="🌎", initial_sidebar_state="expanded"
)


st.header("Карта")

with st.sidebar:
    with st.form(key="map"):
        st.subheader("Фильтр параметров")
        city = st.selectbox("Город", ["Санкт-Петербург"])
        param = st.selectbox("Параметр", ["Зарплата", "Количество вакансий", "Вакансии"])
        submit_button = st.form_submit_button(label="Принять")

st.write("Hello World")