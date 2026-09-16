import streamlit as st
import math
import pandas as pd

# Configuração inicial da página
st.set_page_config(page_title='Calculadoras de anestesia', page_icon='💉', layout='centered')

# ==========================================
# ESTRUTURA PRINCIPAL E BARRA LATERAL
# ==========================================
def main():
    st.sidebar.title('Menu de navegação')
    opcoes_menu = [
        'Preparo anestésico-cirúrgico', # Adicionado o 'r'
        'Bulário',
        'Parâmetros fisiológicos e laboratoriais',
        'Anestesia locorregional',
        'Calculadora de infusão contínua',
        'Calculadora de doses',
        'Escalas de dor (Glasgow, APPLE)'
    ]
    escolha = st.sidebar.selectbox('Selecione a ferramenta:', opcoes_menu)

    # O texto aqui agora é EXATAMENTE igual ao da lista acima
    if escolha == 'Preparo anestésico-cirúrgico':
        tela_preparo()
    
    elif escolha == 'Bulário':
        tela_bulario()

    elif escolha == 'Parâmetros fisiológicos e laboratoriais':
        tela_parametros()

# ==========================================
# FUNÇÕES DAS TELAS (Módulos do aplicativo)
# PREPARO ANESTÉSICO-CIRÚRGICO
# ==========================================
def tela_preparo():
    st.title('Preparo anestésico-cirúrgico')
    st.markdown('Cálculo preditivo do tamanho de sonda endotraqueal com base no peso do paciente')
    
    # CONTAINER DE DADOS DO PACIENTE
    with st.container(border=True):
        st.subheader('Dados do paciente')
        col_peso, col_ecc = st.columns(2)
        with col_peso:
            peso = st.number_input('Peso (kg)', min_value=0.1, max_value=70.0, format='%.1f')
        with col_ecc:
            ecc = st.number_input('Escore de condição corporal (ECC)', min_value=1, max_value=9, step=1)

    if st.button('Calcular', type='primary', use_container_width=True):
        if peso > 0:
            # CÁLCULO DE SONDA ENDOTRAQUEAL
            numero_sonda = math.sqrt(peso * 4)
            
            # CÁLCULO DE BALÃO RESERVATÓRIO
            volume_min_ml = peso * 60
            volume_max_ml = peso * 90
            volume_medio_l = ((volume_min_ml + volume_max_ml) / 2) / 1000
            
            # LÓGICA PARA SUGERIR O BALÃO COMERCIAL
            if volume_medio_l <= 0.5:
                balao_comercial = '0,5 L'
            elif volume_medio_l <= 1.0:
                balao_comercial = '1 L'
            elif volume_medio_l <= 2.0:
                balao_comercial = '2 L'
            elif volume_medio_l <= 3.0:
                balao_comercial = '3 L'
            else:
                balao_comercial = '5 L'
            
            # CÁLCULO DE FLUIDOTERAPIA
            manutencao = peso * 4  # ml/h
            reposicao = peso * 10  # ml/h

            # CÁLCULO DE VOLUME CORRENTE
            vt_min = peso * 10 # mL
            vt_max = peso * 15 # mL

            st.divider() # Linha de separação
            st.subheader('Cálculos')
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                with st.container(border=True):
                    st.metric(label='Sonda endotraqueal', value=f'{numero_sonda:.1f} mm')
                    st.caption('Lembre-se: variações intra e interespécies podem fazer com que o cálculo não seja exato, separe tamanhos ±0.5 mm')

            with col_res2:
                with st.container(border=True):
                    st.metric(label='Balão reservatório', value=f'{balao_comercial}')
                    st.caption(f'Calculado: {volume_min_ml:.1f} a {volume_max_ml:.1f} L')

            st.subheader('Fluidoterapia intravenosa')
            col_flu1, col_flu2 = st.columns(2)
            
            with col_flu1:
                with st.container(border=True):
                    st.metric(label="Manutenção", value=f"{manutencao:.1f} mL/h")
                    
            with col_flu2:
                with st.container(border=True):
                    st.metric(label="Reposição", value=f"{reposicao:.1f} mL/h")


# BULÁRIO 
# ==========================================

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


# PARÂMETROS FISIOLÓGICOS E LABORATORIAIS
# ==========================================
def formatar_ranges(df):
    cols_to_drop = []
    # Analisa as colunas dinamicamente
    for col in list(df.columns):
        if '_min' in col:
            # Tenta prever o nome da coluna de valor máximo correspondente
            col_max = col.replace('min', 'max')
            if col_max in df.columns:
                # O nome da nova coluna é o nome original sem o sufixo '_min' ou '_max'
                base_name = col.replace('min', '')

                def combine(row, c_min, c_max):
                    val_min = row[c_min]
                    val_max = row[c_max]
                    if pd.isna(val_min) and pd.isna(val_max):
                        return ""
                    if pd.isna(val_max):
                        return str(val_min)
                    if pd.isna(val_min):
                        return str(val_max)

                    # Limpa os números com zero desnecessário
                    v_min = str(int(val_min)) if isinstance(val_min, float) and val_min.is_integer() else str(val_min)
                    v_max = str(int(val_max)) if isinstance(val_max, float) and val_max.is_integer() else str(val_max)

                    return f"{v_min} a {v_max}"

                # Aplica a combinação linha por linha
                df[base_name] = df.apply(lambda row: combine(row, col, col_max), axis=1)
                cols_to_drop.extend([col, col_max])

    # Remove as colunas originais
    if cols_to_drop:
        df = df.drop(columns=list(set(cols_to_drop)))
    return df

def tela_parametros():
    st.title('Parâmetros fisiológicos e laboratoriais')
    st.markdown('Confira os valores normais de monitoração e exames laboratoriais')

    pesquisa = st.text_input('🔍 Buscar parâmetro por nome:',  '')

    arquivos = {
        'Monitoração': 'dados/bruto/prmt_monit.csv',
        'Hemograma e Bioquímica': 'dados/bruto/prmt_hc_bq.csv',
        'Hemogasometria e eletrólitos': 'dados/bruto/prmt_hemogaso_eletrolitos.csv',
        'Gases e Ecocardiograma': 'dados/bruto/prmt_gases_eco.csv'
    }

    # Loop que cria um card/aba para cada categoria da lista de parâmetros
    for categoria, arquivo in arquivos.items():
        with st.expander(f'📊 {categoria}', expanded=True):
            try:
                # Tenta ler o arquivo CSV correspondente à categoria
                df = pd.read_csv(arquivo)

                # Passa a tabela pela função que junta os valores min e max
                df = formatar_ranges(df)

                # Se o usuário pesquisou, filtra a tabela
                if pesquisa:
                    mask = pd.Series(False, index=df.index) # CORRIGIDO AQUI: pd.Series com S maiúsculo
                    # Procura o termo digitado em TODAS as colunas ao mesmo tempo
                    for col in df.columns:
                        mask = mask | df[col].astype(str).str.contains(pesquisa, case=False, na=False)
                    df = df[mask]

                # Mostra o resultado na tela
                if df.empty:
                    st.warning(f'Nenhum resultado encontrado em {categoria}.')
                else:
                    st.dataframe(df, use_container_width=True, hide_index=True)
            except FileNotFoundError:
                st.error(f'Arquivo não encontrado nessa pasta: {arquivo}')


# Comando que inicia o aplicativo
if __name__ == '__main__':
    main()