import streamlit as st
import requests

from dreamjob.db.utils.data_manipulation import select
from dreamjob.db.utils.engine import DBConfig

st.set_page_config(
    page_title="Поиск работы", page_icon="🎨", initial_sidebar_state="expanded"
)


@st.cache()
def load_data():
    engine = DBConfig.get().db_engine
    df = select(engine, columns="id, name, description")
    return df


def prepare_recs(df):
    return (
        df
        .iloc[(map(lambda x: x["id"], reversed(response["recommendations"])))]
        .assign(description=lambda df: df["description"].apply(lambda x: x[:100] + "..."))
    )


st.header("Поиск работы")
st.markdown("#### Мы поможем тебе найти работу мечты!")

with st.sidebar:
    with st.form(key="job search"):
        st.subheader("Фильтр параметров")
        city = st.multiselect("Город(а)", ["Санкт-Петербург"], default="Санкт-Петербург")
        salary = st.slider("Диапазон зарплат, ₽", 0, 500000, (50000, 250000), step=5000)
        submit_button = st.form_submit_button(label="Принять")

st.write(
    """
    Опиши свои навыки, увлечения, интересы и наш алгоритм на основе предоставленной информации подберет
    для тебя подходящие вакансии.
    """
)

# Send request to backend
text = st.text_area("Только не скромничай!", value="Умею собирать кубик Рубика! Возьмите меня на работу...")
response = requests.post("http://127.0.0.1:8080/recommend", json={"user_input": text}).json()

# Prepare recommendations from response
vacancies = load_data()
recommendations = prepare_recs(vacancies)

st.table(recommendations)
