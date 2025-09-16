# app_consulta.py (VERSÃO COM MAIS INFORMAÇÕES)

import os
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep



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
        # try:
        #     voltar_pesquisa = navegador.find_element(By.XPATH, '//*[@id="searchPanel"]/div/div/div[1]/div[1]/div/span/span/span')
        #     voltar_pesquisa.click()
        #     sleep(0.5)
        # except:
        #     pass

        # # Realiza a busca
        # clicar_pesquisa = navegador.find_element(By.XPATH, '//*[@id="legendPanel"]/div/div/div[1]/div[4]/div')
        # clicar_pesquisa.click()
        # sleep(0.8)
        wait = WebDriverWait(navegador, 30)
        campo_busca = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'searchInput')))
        campo_busca.clear()
        sleep(1)
        campo_busca.send_keys(endereco)
        sleep(1)
        campo_busca.send_keys(Keys.ENTER)
        sleep(2)

        ponteiro_mapa = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'circle[r="4"]')))
        ponteiro_mapa.click()
        # ActionChains(navegador).move_to_element(ponteiro_mapa).move_by_offset(5, 0).click().perform()
        # sleep(0.5)
        # ponteiro_mapa.click()
        # sleep(3)

        # Extrai o nome da unidade
        unidade = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'attrValue'))).text
        print(f"Unidade encontrada: {unidade}")
        if unidade:
            dados_encontrados['unidade'] = unidade

        # TENTA EXTRAIR O DISTRITO
        # try:
        #     distrito = navegador.find_element(By.CLASS_NAME, 'contentPane').text
        #     print(f"Distrito encontrado: {distrito}")
        #     if distrito:
        #         dados_encontrados['distrito'] = distrito
        # except Exception:
        #     # Se não encontrar, mantém o valor padrão "Não informado"
        #     pass

        # TENTA EXTRAIR AS INFORMAÇÕES ADICIONAIS
        try:
            info_adicional = navegador.find_element(By.CLASS_NAME, 'contentPane').text
            if info_adicional:
                dados_encontrados['info'] = info_adicional
        except Exception:
            # Se não encontrar, mantém o valor padrão "Não informada"
            pass

        # # Clica para voltar da tela de detalhes
        # voltar_detalhes = navegador.find_element(By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[3]/div[1]/div/span/span/span')
        # voltar_detalhes.click()
        # sleep(0.5)

    except Exception as e:
        st.error(f"Ocorreu um erro durante a automação verifique endereço e adicione Joinville.")
        print(f"Erro na automação: {e}")
        # try:
        #     navegador.find_element(By.XPATH, '//*[@id="searchPanel"]/div/div/div[1]/div[1]/div/span/span/span').click()
        # except:
        #     pass
            
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
        navegador.get('https://geo.joinville.sc.gov.br/portal/apps/simgeo/index.html?id=0e2ffa64f4254dda952757813efb6565')
        sleep(5)
        wait = WebDriverWait(navegador, 60)
        st.info("Configurando mapa...")
        lista_de_camadas = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="themes_PlateauTheme_widgets_HeaderController_Widget_20"]/div[2]/div[5]')))
        sleep(1)
        lista_de_camadas.click()
        st.info("lista de camadas encontrada...")
        checkbox_desabilitar = wait.until(EC.presence_of_element_located((By.ID, 'jimu_dijit_CheckBox_0')))
        sleep(1)
        checkbox_desabilitar.click()
        st.info("desabilitado combobox")
        checkbox_desabilitar = wait.until(EC.presence_of_element_located((By.ID, 'jimu_dijit_CheckBox_12')))
        sleep(1)
        checkbox_desabilitar.click()
        st.info("desabilitado combobox")
        checkbox_desabilitar = wait.until(EC.presence_of_element_located((By.ID, 'jimu_dijit_CheckBox_21')))
        sleep(1)
        checkbox_desabilitar.click()
        st.info("desabilitado combobox")
        checkbox_ubsf = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="jimu_dijit_CheckBox_103"]/div[1]')))
        sleep(1)
        checkbox_ubsf.click()
        st.info("abilitar ubsf")
        checkbox_expand = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dijit__TemplatedMixin_2"]/table/tbody[1]/tr[17]/td[1]/div[1]')))
        sleep(1)
        checkbox_expand.click()
        st.info("abilitar ubsf")
        tres_pontos = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dijit__TemplatedMixin_2"]/table/tbody[1]/tr[18]/td/table/tr[3]/td[3]/div')))
        sleep(1)
        tres_pontos.click()
        st.info("3 pontos")
        sleep(2)
        habilitar_poupup = navegador.find_element(By.XPATH, '//div[text()="Habilitar pop-up"]')
        if habilitar_poupup:
            habilitar_poupup.click()
            st.info("clicou poupup")
        else:
            pass
        sleep(1)
        fechar_confg = navegador.find_element(By.CSS_SELECTOR, 'div[aria-label="Pesquisa"]')
        fechar_confg.click()
        st.info("clicou pesquisa")

        return navegador
    except Exception as e:
        st.error(f"Não foi possível iniciar o navegador. recarregue a página e tente novamente//.")
        print(f"Erro ao iniciar o navegador: {e}")
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
                    # st.metric(label="Distrito", value=dados_ubsf['distrito'])
                    
                    st.markdown("**Mais Informações:**")
                    st.info(dados_ubsf['info'])


st.markdown("---")
st.write("© 2025 SES - Inova - Todos os direitos reservados")