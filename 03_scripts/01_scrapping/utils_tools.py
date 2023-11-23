## Imports
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep

## Configs
driver_path = r"..\..\04_utils\driver\chromedriver.exe"
url_base = r"https://dados.ons.org.br/"
url_ccee = r"https://www.ccee.org.br/web/guest/busca-ccee?q=infohor%C3%A1rio&dtIni=01/01/2000&dtFim=28/04/2023&structure="
url_aneel = r"https://www2.aneel.gov.br/scg/Consulta_Empreendimento.asp"

# Define os recursos desejados para ignorar erros de SSL
capabilities = DesiredCapabilities().CHROME.copy()
capabilities["acceptInsecureCerts"] = True

## Funções
def set_options():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")

    return options

def get_ons_dataset_links():
    """ 
    Função que abre o site da ONS, captura os links onde os arquivos de interesse estão
    e retorna a página pronta para iteração pelos links e a lista de links.

    Returns:
        Uma tupla contendo a lista de links e o objeto do navegador.
    """
    
    # Mensagem para o usuário saber que os links de download estão sendo gerados
    print("\nGerando os links de Download\n")
    
    # Inicializa o webdriver do Chrome com as opções especificadas
    browser = webdriver.Chrome(options=set_options(), executable_path=driver_path, desired_capabilities=capabilities)
    
    # Acessa o URL desejado
    browser.get(url_base)

    # Encontra o elemento ul que contém os links para os dados
    ul = browser.find_element(
        By.XPATH, "/html/body/div[3]/div[4]/div/div/div/div/div/ul[1]"
    )

    # Encontra todos os elementos li dentro do elemento ul
    li_list = ul.find_elements(By.TAG_NAME, "li")

    # Inicializa uma lista vazia para armazenar os links
    link_list = []

    # Para cada elemento li, encontra o elemento a, extrai o link e adiciona à lista de links
    for li in li_list:
        # Encontra o elemento a dentro do elemento li
        a = li.find_element(By.TAG_NAME, "a")
        
        # Obtém o valor do atributo href que contém o link
        href = a.get_attribute("href")
        
        # Adiciona o link à lista de links
        link_list.append(href)

    # Retorna a lista de links e o objeto do navegador
    return link_list, browser

def get_ccee_dataset_links():
    """ 
    Função que abre o site da CCEE, captura os links onde os arquivos de interesse estão
    e retorna a página pronta para iteração pelos links e a lista de links.

    Returns:
        Uma tupla contendo a lista de links e o objeto do navegador.
    """
    
    # Mensagem para o usuário saber que a página de download está sendo aberta
    print("\nAbrindo a Página de Download\n")
    
    # Inicializa o webdriver do Chrome com as opções especificadas
    browser = webdriver.Chrome(options=set_options(), executable_path=driver_path, desired_capabilities=capabilities)
    
    # Acessa o URL desejado
    browser.get(url_ccee)

    # Configura uma espera implícita de até 10 segundos
    wait = WebDriverWait(browser, 10)

    # Espera até que o primeiro elemento seja clicável e executa o script de clique
    element = wait.until(EC.element_to_be_clickable((By.XPATH, 
                                                     "/html/body/div[1]/div[2]/section[1]/div/div[1]/div/div/div/section/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[3]/button/i")))
    browser.execute_script("arguments[0].click();", element)

    # Espera até que o segundo elemento seja clicável e executa o script de clique
    element = wait.until(EC.element_to_be_clickable((By.XPATH, 
                                                     "/html/body/div[1]/div[2]/section[1]/div/div[1]/div/div/div/section/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[3]/ul/li[3]/span")))
    browser.execute_script("arguments[0].click();", element)

    # Aguarda 5 segundos para garantir que a página tenha tempo suficiente para carregar
    sleep(5)
    
    # Encontra todos os elementos que correspondem ao seletor CSS e obtém o link de cada elemento
    elements = browser.find_elements(By.CSS_SELECTOR, 'a.d-flex.ms-2.card-link')
    
    # Cria uma lista de links dos elementos encontrados
    link_list = [element.get_attribute('href') for element in elements]

    # Retorna a lista de links e o objeto do navegador
    return link_list, browser

def get_aneel_page():
    """ 
    Função que abre o site da ANEEL utilizando o WebDriver do Chrome e retorna o objeto do navegador.

    Returns:
        O objeto WebDriver do Chrome para a página aberta.
    """
    
    # Mensagem para o usuário saber que a página da ANEEL está sendo aberta
    print("\nAbrindo Página da Aneel\n")
    
    # Inicializa o webdriver do Chrome com as opções especificadas
    browser = webdriver.Chrome(options=set_options(), executable_path=driver_path, desired_capabilities=capabilities)
    
    # Acessa o URL desejado
    browser.get(url_aneel)
    
    # Aguarda 5 segundos para garantir que a página tenha tempo suficiente para carregar
    sleep(5)
    
    # Retorna o objeto do navegador
    return browser

def extract_aneel_table_data(browser):
    """ 
    Função que extrai dados de uma tabela na página da ANEEL.

    Args:
        browser: objeto WebDriver do Chrome para a página aberta.

    Returns:
        DataFrame do pandas contendo os dados extraídos da tabela.
    """
    
    # Inicializa um dicionário vazio para armazenar os dados
    data = {}

    # Encontra o elemento da tabela na página da web pelo seu XPath
    table = browser.find_element(By.XPATH, 
                                "/html/body/div/div/table/tbody/tr[2]/td/table[3]")

    # Encontra os cabeçalhos da tabela (elementos td dentro de tr com a classe 'linhaAzul')
    headers = table.find_elements(By.CSS_SELECTOR, "tr.linhaAzul td")

    # Inicializa uma lista vazia para cada cabeçalho no dicionário de dados
    for header in headers:
        data[header.text] = []

    # Encontra todas as linhas da tabela (elementos tr com a classe 'linhaBranca')
    rows = table.find_elements(By.CSS_SELECTOR, "tr.linhaBranca")

    # Para cada linha, encontra todas as colunas (elementos td) e adiciona o texto de cada coluna à lista correspondente no dicionário de dados
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        for header, col in zip(headers, cols):
            data[header.text].append(col.text)

    # Converte o dicionário de dados em um DataFrame do pandas
    df = pd.DataFrame(data)
    
    # Retorna o DataFrame
    return df