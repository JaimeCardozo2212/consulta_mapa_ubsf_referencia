
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep



def get_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service()
    
    try:
        navegador = webdriver.Chrome(service=service, options=chrome_options)
        navegador.get('https://geo.joinville.sc.gov.br/portal/apps/simgeo/index.html?id=0e2ffa64f4254dda952757813efb6565')
        sleep(10)
        try:
            print("Configurando mapa...")
            lista_de_camadas = navegador.find_element(By.XPATH, '//*[@id="themes_PlateauTheme_widgets_HeaderController_Widget_20"]/div[2]/div[5]/div[1]')
            lista_de_camadas.click()
            sleep(1)
            checkbox_ubsf = navegador.find_element(By.XPATH, '//*[@id="jimu_dijit_CheckBox_103"]/div[1]')
            checkbox_ubsf.click()
            sleep(1)
            tres_pontos = navegador.find_element(By.XPATH, '//*[@id="dijit__TemplatedMixin_2"]/table/tbody[1]/tr[17]/td[3]/div')
            tres_pontos.click()
            sleep(1)
            habilitar_poupup = navegador.find_element(By.XPATH, '//*[@id="dijit__TemplatedMixin_3"]/div[5]/div[4]')
            habilitar_poupup.click()
            sleep(1)
            fechar_confg = navegador.find_element(By.CSS_SELECTOR, 'div[aria-label="Pesquisa"]')
            fechar_confg.click()
            sleep(10)
        except Exception as e:
            print(f"Erro ao configurar mapa: {e}")
            # st.error(f"Erro ao configurar mapa: {e}")
            return
    except Exception as e:
        # st.error(f"Não foi possível iniciar o navegador. Verifique os logs. Erro: {e}")
        return None
    
get_driver()