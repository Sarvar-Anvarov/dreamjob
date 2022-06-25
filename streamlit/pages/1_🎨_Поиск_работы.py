import streamlit as st
import requests

st.set_page_config(
    page_title="Поиск работы", page_icon="🎨", initial_sidebar_state="expanded"
)


st.header("Поиск работы")
st.markdown("#### Мы поможем тебе найти работу мечты!")

with st.sidebar:
    with st.form(key="job search"):
        st.subheader("Фильтр параметров")
        city = st.multiselect("Город(а)", ["Москва", "Санкт-Петербург"], default="Москва")
        salary = st.slider("Диапазон зарплат, ₽", 0, 500000, (50000, 250000), step=5000)
        submit_button = st.form_submit_button(label="Принять")

st.write(
    """
    Опиши свои навыки, увлечения, интересы и наш алгоритм на основе предоставленной информации подберет
    для тебя подходящие вакансии.
    """
)
text = st.text_area("Только не скромничай!", value="Умею собирать кубир Рубика! Возьмите меня на работу...")
