from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import time
from bs4 import BeautifulSoup

def extrair_informacoes(localizacao):
    driver = webdriver.Firefox() 
    driver.get("https://www.google.com/maps")

    search_box = driver.find_element("name", "q")
    search_box.send_keys(localizacao)
    search_box.send_keys(Keys.ENTER)

    time.sleep(10)

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        nome_element = soup.find('div', class_='qBF1Pd')
        nome = nome_element.text.strip() if nome_element else None
        endereco_element = soup.find('div', class_='section-info-text')
        endereco = endereco_element.text.strip() if endereco_element else None
        telefone_element = soup.find('span', class_='UsdlK')
        telefone = telefone_element.text.strip() if telefone_element else None
        
    except Exception as e:
        print("Erro ao extrair informações:", e)
        nome, endereco, telefone = None, None, None

    driver.quit()
    return nome, endereco, telefone

def salvar_csv(nome, endereco, telefone, nome_arquivo):
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerow(['Nome', 'Endereço', 'Telefone'])
        escritor_csv.writerow([nome, endereco, telefone])

if __name__ == "__main__":
    localizacao = input("Digite o nome da escola que deseja pesquisar: ")
    nome, endereco, telefone = extrair_informacoes(localizacao)

    if nome:
        salvar_csv(nome, endereco, telefone, f'informacoes_{localizacao}.csv')
        print(f"Informações da escola '{nome}' salvas com sucesso.")
    else:
        print(f"Não foi possível extrair informações da escola '{localizacao}'.")
