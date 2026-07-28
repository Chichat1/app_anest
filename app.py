import streamlit as st
import math

st.set_page_config(page_title='Calculadoras de anestesia', page_icon='💉', layout='centered')

st.title('Calculadora de sonda endotraqueal')
st.markdown('Cálculo preditivo do tamanho de sonda endotraqueal com base no peso do paciente')

with st.container():
    st.subheader('Dados do paciente')
    peso = st.number_input('Peso (kg)', min_value=0.1, max_value=70.0, step=0.1, format='%.1f')

if st.button('Calcular', type='primary'):
    if peso > 0:
        numero_sonda = math.sqrt(peso * 4)

        st.success(f'Tamanho estimado da sonda endotraqueal: **{numero_sonda:.1f} mm**')
        st.info('Lembre-se: as variações intra e interespécies pode fazer com que o cálculo não seja exato')