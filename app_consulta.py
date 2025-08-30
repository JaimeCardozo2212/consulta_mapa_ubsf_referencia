# app_consulta.py (VERSÃO COM MAIS INFORMAÇÕES)

import os
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

# --- LÓGICA DO SELENIUM (MODIFICADA PARA RETORNAR MAIS DADOS) ---

### ALTERAÇÃO 1: A função agora busca mais campos e retorna um dicionário ###
def buscar_unidade(navegador, endereco):
    """
    Função que realiza a busca do endereço no mapa e retorna um dicionário
    com os dados da unidade de saúde (unidade, distrito, informações).
    """
    # Inicializa um dicionário com os valores padrão
    dados_encontrados = {
        'unidade': "Não foi possível encontrar a unidade.",
        'distrito': "Não informado",
        'info': "Não informada"
    }

    try:
        # Tenta voltar para a tela inicial de pesquisa
        try:
            voltar_pesquisa = navegador.find_element(By.XPATH, '//*[@id="searchPanel"]/div/div/div[1]/div[1]/div/span/span/span')
            voltar_pesquisa.click()
            sleep(0.5)
        except:
            pass

        # Realiza a busca
        clicar_pesquisa = navegador.find_element(By.XPATH, '//*[@id="legendPanel"]/div/div/div[1]/div[4]/div')
        clicar_pesquisa.click()
        sleep(0.8)

        campo_busca = navegador.find_element(By.XPATH, '//*[@id="searchPanel"]/div/div/div[1]/div[2]/div[1]/div/div[1]/input')
        campo_busca.clear()
        campo_busca.send_keys(endereco)
        sleep(1)
        campo_busca.send_keys(Keys.ENTER)
        sleep(2)

        ponteiro_mapa = navegador.find_element(By.XPATH, '//*[@id="map-canvas"]/div[1]/div[3]/div[1]/div[2]/div/div[3]/div')
        ActionChains(navegador).move_to_element(ponteiro_mapa).move_by_offset(5, 0).click().perform()
        sleep(1.5)

        # Extrai o nome da unidade
        unidade = navegador.find_element(By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[1]/div[2]').text
        if unidade:
            dados_encontrados['unidade'] = unidade

        # TENTA EXTRAIR O DISTRITO
        try:
            distrito = navegador.find_element(By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[2]/div[2]').text
            if distrito:
                dados_encontrados['distrito'] = distrito
        except Exception:
            # Se não encontrar, mantém o valor padrão "Não informado"
            pass

        # TENTA EXTRAIR AS INFORMAÇÕES ADICIONAIS
        try:
            info_adicional = navegador.find_element(By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[3]/div[2]').text
            if info_adicional:
                dados_encontrados['info'] = info_adicional
        except Exception:
            # Se não encontrar, mantém o valor padrão "Não informada"
            pass

        # Clica para voltar da tela de detalhes
        voltar_detalhes = navegador.find_element(By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[3]/div[1]/div/span/span/span')
        voltar_detalhes.click()
        sleep(0.5)

    except Exception as e:
        st.error(f"Ocorreu um erro durante a automação: {e}")
        try:
            navegador.find_element(By.XPATH, '//*[@id="searchPanel"]/div/div/div[1]/div[1]/div/span/span/span').click()
        except:
            pass
            
    # Retorna o dicionário completo com os dados
    return dados_encontrados


# --- CONFIGURAÇÃO DO NAVEGADOR (NÃO PRECISA MUDAR) ---

@st.cache_resource
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service()
    
    try:
        navegador = webdriver.Chrome(service=service, options=chrome_options)
        navegador.get('https://www.google.com/maps/d/u/0/viewer?mid=1NgDrl6I4Alzy1DAjM3WBDTuELO0r1YI&ll=-26.271590317094045%2C-48.931617999999986&z=11')
        sleep(5)
        return navegador
    except Exception as e:
        st.error(f"Não foi possível iniciar o navegador. Verifique os logs. Erro: {e}")
        return None

# --- INTERFACE DO APLICATIVO STREAMLIT ---

st.set_page_config(page_title="Consulta de Unidades", layout="centered")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    try:
        st.image("inova_saude.png", width=300)
    except:
        st.title("Inova Saúde")

st.header("Consulta de Unidades de Saúde")
st.write("Digite um endereço abaixo para encontrar a unidade de saúde de referência.")

endereco_usuario = st.text_input("Para uma localização mais precisa após o endereço adicione Joinville", placeholder="Ex: Rua das Flores 123 Joinville")

if st.button("Buscar Unidade"):
    if not endereco_usuario:
        st.warning("Por favor, digite um endereço.")
    else:
        with st.spinner("Inicializando o navegador e realizando a busca... Isso pode levar um momento."):
            navegador = get_driver()
            if navegador:
                ### ALTERAÇÃO 2: A interface agora recebe o dicionário e exibe os novos campos ###
                dados_ubsf = buscar_unidade(navegador, endereco_usuario)
                
                # Verifica se a busca principal falhou
                if "Não foi possível" in dados_ubsf['unidade']:
                    st.error(f"**Resultado:** {dados_ubsf['unidade']}")
                else:
                    st.success("Busca concluída com sucesso!")
                    st.subheader("Informações da Unidade de Referência:")
                    
                    # Exibe os resultados de forma organizada
                    st.metric(label="Nome da Unidade", value=dados_ubsf['unidade'])
                    st.metric(label="Distrito", value=dados_ubsf['distrito'])
                    
                    st.markdown("**Mais Informações:**")
                    st.info(dados_ubsf['info'])


st.markdown("---")
st.write("© 2025 SES - Inova - Todos os direitos reservados")