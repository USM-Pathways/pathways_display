import streamlit as st
from utility import parse_DRP, course_options, advisment_prompt

import google.generativeai as genai

# establish AI agent 
genai.configure(api_key=st.secrets['GEMINI_KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")

if 'previous_advisement' not in st.session_state:
    st.session_state['current_advisement'] = None

# streamlit UI
st.title('USM - Pathways Advisement')

uploaded_file = st.file_uploader("Provide your degree progress report (DPR)", type="pdf")

if uploaded_file is not None:
    DPR = parse_DRP(uploaded_file)  # read student DPR
    OFFERINGS = course_options()    # pull next semester course offerings

    if st.button("Run Advisement"):
        st.session_state['previous_advisement'] = None

        with st.status("Your Advisement", expanded=True):
            response = model.generate_content([advisment_prompt, DPR, OFFERINGS], stream=True)

            response_field = st.empty()
            advisement_text = ""

            for chunk in response:
                advisement_text += chunk.text
                response_field.markdown(advisement_text)

            st.session_state['current_advisement'] = advisement_text

    if 'previous_advisement' in st.session_state:
        if st.session_state['previous_advisement'] is not None:
            with st.status("Your Advisement", expanded=True):

                response_field = st.empty()
                response_field.markdown(st.session_state['previous_advisement'])

def save_advisement():
    #with open('reference.txt', 'w') as f:
        #f.write(str(st.session_state['current_advisement']))
    
    st.session_state['previous_advisement'] = st.session_state['current_advisement']
    st.session_state['current_advisement'] = None

    st.session_state['save_state'] = True

if 'current_advisement' in st.session_state:
    if st.session_state['current_advisement'] is not None:
        save_button = st.button("Save Your Advisement", on_click=save_advisement)

if 'save_state' in st.session_state:
    if st.session_state['save_state']:
        st.write('Advisement Saved')
        st.session_state['save_state'] = False
