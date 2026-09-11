import streamlit as st
import math

# Configuração inicial da página
st.set_page_config(page_title='Calculadoras de anestesia', page_icon='💉', layout='centered')

# ==========================================
# FUNÇÕES DAS TELAS (Módulos do aplicativo)
# ==========================================

def tela_calculadora_sonda():
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

def tela_em_construcao(titulo):

# ==========================================
# ESTRUTURA PRINCIPAL E BARRA LATERAL
# ==========================================

def main():
    st.sidebar.title('Menu de navegação')
    opcoes_menu = [
        'Calculadora de tubo endotraqueal',
        'Calculadora de fluidoterapia',
        'Calculadora de doses',
        'Bulário',
        'Escala de Glasgow',
        'APPLE Score'
    ]

escolha = st.sidebar.selectbox('Selecione a ferramenta:', opcoes_menu)

    if escolha == 'Calculadora de tubo endotraqueal':
        tela_calculadora_sonda
    
    elif escolha == 'Calculadora de fluidoterapia':
        tela_em_construcao('Calculadora de fluidoterapia')
    
    elif escolha == 'Calculadora de doses':
        tela_em_construcao('Calculadora de doses')

# Comando que inicia o aplicativo
if __name__ == '__main__':
    main()