import streamlit as st
import requests

# Test

st.subheader('Greetings')
st.markdown("I'm glad to see ya'll")

if st.button("Add new vacancies"):
    response = requests.get("http://127.0.0.1:8080/data/add_new_vacancies")
    st.write("I've got some response")
    st.write(response.text)
