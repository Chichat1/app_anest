import streamlit as st
import math
import pandas as pd

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

def tela_bulario():
    st.title('Bulário')
    st.markdown('Consulte informações rápidas sobre fármacos')

    try:
        df = pd.read_csv('bulario.csv')
    except FileNotFoundError:
        st.warning("Arquivo 'bulario.csv' não encontrado. Mostrando dados de exemplo")
        dados_exemplo = {
            'Fármaco': ['Propofol', 'Cetamina', 'Midazolam', 'Dexmedetomidina'],
            'Categoria': ['Indutor', 'Anestésico dissociativo', 'Benzodiazepínico', 'Alfa-2 Agonista'],
            'Faixa de dose': ['2 - 6 mg/kg', '5 - 10 mg/kg', '0.1 - 0.5 mg/kg', '1 - 10 mcg/kg']
        }
        df = pd.DataFrame(dados_exemplo)
    # Barra de pesquisa
    pesquisa = st.text_input('🔍 Buscar fármaco por nome:', '')

    # Filtrando a tabela baseada na pesquisa
    if pesquisa:
        df = df[df['Fármaco'].str.contains(pesquisa, case=False, na=False)]
    # Exibindo a tabela no streamlit
    st.dataframe(df, use_container_width=True, hide_index=True)

def tela_em_construcao(titulo):
    st.title(titulo)
    st.warning('🚧 Esta ferramenta está em desenvolvimento. Em breve estará disponível!')

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
        tela_calculadora_sonda()
    
    elif escolha == 'Bulário':
        tela_bulario()

# Comando que inicia o aplicativo
if __name__ == '__main__':
    main()