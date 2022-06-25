import streamlit as st
import requests

from PIL import Image
from dreamjob.config import settings

st.set_page_config(
    page_title="DreamJob", initial_sidebar_state="expanded"
)


st.header("DreamJob")
st.markdown("#### Пусть работа приносит удовольствие")

st.write(
    """
    Привет, мы рады тебя видеть! Наш алгоритм поможет тебе найти вакансии, соответствующие твоим навыкам и интересам. 
    Просто расскажи о себе, своих увлечениях, способностях и получи подходящий список вакансий.
    """
)

image = Image.open(settings.PICTURE)
st.image(image, caption="Good boy")
