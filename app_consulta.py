# app_consulta.py (VERSÃO PARA DEPLOY)

import os
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

# --- LÓGICA DO SELENIUM (IGUAL A ANTERIOR) ---

def buscar_unidade(navegador, endereco):
    # ... (Esta função continua exatamente a mesma do código anterior)
    unidade_encontrada = "Não foi possível encontrar a unidade."
    
    try:
        try:
            voltar_pesquisa = navegador.find_element(By.XPATH, '//*[@id="searchPanel"]/div/div/div[1]/div[1]/div/span/span/span')
            voltar_pesquisa.click()
            sleep(0.5)
        except:
            pass

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

        unidade = navegador.find_element(By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[1]/div[2]').text
        if unidade:
            unidade_encontrada = unidade

        voltar_detalhes = navegador.find_element(By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[3]/div[1]/div/span/span/span')
        voltar_detalhes.click()
        sleep(0.5)

    except Exception as e:
        st.error(f"Ocorreu um erro durante a automação: {e}")
        try:
            navegador.find_element(By.XPATH, '//*[@id="searchPanel"]/div/div/div[1]/div[1]/div/span/span/span').click()
        except:
            pass
            
    return unidade_encontrada

# --- CONFIGURAÇÃO DO NAVEGADOR (MODIFICADA PARA DEPLOY) ---

@st.cache_resource
def get_driver():
    """
    Inicia o WebDriver do Selenium para o ambiente do Streamlit Cloud.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # OBRIGATÓRIO para rodar no Streamlit Cloud
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # O Selenium já encontra o chromedriver instalado via packages.txt
    service = Service()
    
    try:
        navegador = webdriver.Chrome(service=service, options=chrome_options)
        navegador.get('https://www.google.com/maps/d/u/0/viewer?mid=1NgDrl6I4Alzy1DAjM3WBDTuELO0r1YI&ll=-26.271590317094045%2C-48.931617999999986&z=11')
        sleep(5)  # Espera a página carregar
        return navegador
    except Exception as e:
        st.error(f"Não foi possível iniciar o navegador. Verifique os logs. Erro: {e}")
        return None

# --- INTERFACE DO APLICATIVO STREAMLIT (IGUAL A ANTERIOR) ---

st.set_page_config(page_title="Consulta de Unidades", layout="centered")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    try:
        st.image("inova_saude.png", width=300)
    except:
        st.title("Inova Saúde")

st.header("Consulta de Unidades de Saúde")
st.write("Digite um endereço abaixo para encontrar a unidade de saúde de referência.")

endereco_usuario = st.text_input("Digite o endereço completo:", placeholder="Ex: Rua das Flores, 123, Joinville - SC")

if st.button("Buscar Unidade"):
    if not endereco_usuario:
        st.warning("Por favor, digite um endereço.")
    else:
        with st.spinner("Inicializando o navegador e realizando a busca... Isso pode levar um momento."):
            navegador = get_driver()
            if navegador:
                resultado = buscar_unidade(navegador, endereco_usuario)
                
                if "Não foi possível" in resultado:
                    st.error(f"**Resultado:** {resultado}")
                else:
                    st.success("Busca concluída com sucesso!")
                    st.subheader("Unidade de Referência Encontrada:")
                    st.metric(label="Nome da Unidade", value=resultado)

st.markdown("---")
st.write("© 2025 Inova Saúde - Todos os direitos reservados")