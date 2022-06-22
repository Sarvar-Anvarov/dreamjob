import streamlit as st

st.set_page_config(
    page_title="Поиск работы", page_icon="🎨", initial_sidebar_state="expanded"
)


st.header("Поиск работы")
st.subheader("Мы поможем тебе найти работу мечты!")


with st.sidebar:
    with st.form(key="job search"):
        st.subheader("Фильтр параметров")
        city = st.multiselect("Город(а)", ["Москва", "Санкт-Петербург"], default="Москва")
        salary = st.slider("Диапазон зарплат, ₽", 0, 150000, (25000, 125000), step=5000)
        submit_button = st.form_submit_button(label="Принять")


st.write(
    """
    Опиши свои навыки, увлечения, интересы и наш алгоритм на основе этой информации подберет
    для тебя подходящую вакансию.
    """
)
text = st.text_area("Только не скромничай!", value="fdsf")
