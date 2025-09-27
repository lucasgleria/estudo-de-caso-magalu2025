import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
import re
from urllib.parse import urljoin
import os
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Gerador de user agents aleatórios
ua = UserAgent()

def get_random_headers():
    """Gera headers aleatórios para evitar bloqueio."""
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/'
    }

def debug_page_html(driver, source_name, page_num, city):
    """Salva o HTML da página para depuração."""
    os.makedirs('debug', exist_ok=True)
    html_path = f'debug/{source_name}_{city}_page_{page_num}.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    logging.info(f"HTML salvo para depuração em {html_path}")

def analyze_card_with_bs4(card_html, source_name, city):
    """Analisa um card usando BeautifulSoup para extrair informações."""
    soup = BeautifulSoup(card_html, 'html.parser')
    
    # Dicionário para armazenar os dados extraídos
    data = {
        'price': 'N/A',
        'area': 'N/A',
        'address': 'N/A'
    }
    
    # Estratégia 1: Procurar por padrões de texto com regex em todo o card
    card_text = soup.get_text()
    
    # Procurar por padrão de preço (R$ X.XXX,XX)
    price_match = re.search(r'R\$ [\d.,]+', card_text)
    if price_match:
        data['price'] = price_match.group(0)
    
    # Procurar por padrão de área (XXX m²)
    area_match = re.search(r'[\d.,]+ m²', card_text)
    if area_match:
        data['area'] = area_match.group(0)
    
    # Procurar por padrão de CEP (XXXXX-XXX)
    cep_match = re.search(r'(\d{5}-\d{3})', card_text)
    if cep_match:
        data['address'] = cep_match.group(0)
    
    # Estratégia 2: Procurar por elementos com atributos específicos
    # Para Zap Imóveis
    if source_name == 'ZapImoveis':
        # Procurar por preço em diferentes elementos
        price_selectors = [
            '[data-testid="price"]',
            '.simple-card__price',
            '.property-card__price',
            '[class*="price"]',
            'p',
            'span'
        ]
        
        for selector in price_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if re.search(r'R\$ [\d.,]+', text):
                    data['price'] = text
                    break
            if data['price'] != 'N/A':
                break
        
        # Procurar por área em diferentes elementos
        area_selectors = [
            '[data-testid="area"]',
            '.simple-card__main-infos__item--area',
            '.property-card__detail-area',
            '[class*="area"]',
            'li',
            'span'
        ]
        
        for selector in area_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if re.search(r'[\d.,]+ m²', text):
                    data['area'] = text
                    break
            if data['area'] != 'N/A':
                break
        
        # Procurar por endereço em diferentes elementos
        address_selectors = [
            '[data-testid="address"]',
            '.simple-card__address',
            '.property-card__address',
            '[class*="address"]',
            'h2',
            'h3',
            'p'
        ]
        
        for selector in address_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if city.lower() in text.lower() or re.search(r'\d{5}-\d{3}', text):
                    data['address'] = text
                    break
            if data['address'] != 'N/A':
                break
    
    # Para Viva Real
    elif source_name == 'VivaReal':
        # Procurar por preço em diferentes elementos
        price_selectors = [
            '[data-testid="price"]',
            '.property-card__price',
            '[class*="price"]',
            'p',
            'span'
        ]
        
        for selector in price_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if re.search(r'R\$ [\d.,]+', text):
                    data['price'] = text
                    break
            if data['price'] != 'N/A':
                break
        
        # Procurar por área em diferentes elementos
        area_selectors = [
            '[data-testid="area"]',
            '.property-card__detail-area',
            '[class*="area"]',
            'li',
            'span'
        ]
        
        for selector in area_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if re.search(r'[\d.,]+ m²', text):
                    data['area'] = text
                    break
            if data['area'] != 'N/A':
                break
        
        # Procurar por endereço em diferentes elementos
        address_selectors = [
            '[data-testid="address"]',
            '.property-card__address',
            '[class*="address"]',
            'h2',
            'h3',
            'p'
        ]
        
        for selector in address_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if city.lower() in text.lower() or re.search(r'\d{5}-\d{3}', text):
                    data['address'] = text
                    break
            if data['address'] != 'N/A':
                break
    
    # Para OLX
    elif source_name == 'OLX':
        # Procurar por preço em diferentes elementos
        price_selectors = [
            '[data-testid="price"]',
            '.sc-1jw7o9w-0',
            '[class*="price"]',
            'h2',
            'span'
        ]
        
        for selector in price_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if re.search(r'R\$ [\d.,]+', text):
                    data['price'] = text
                    break
            if data['price'] != 'N/A':
                break
        
        # Procurar por área em diferentes elementos
        area_selectors = [
            '[data-testid="area"]',
            '.sc-ifAKCX',
            '[class*="area"]',
            'span',
            'div'
        ]
        
        for selector in area_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if re.search(r'[\d.,]+ m²', text):
                    data['area'] = text
                    break
            if data['area'] != 'N/A':
                break
        
        # Procurar por endereço em diferentes elementos
        address_selectors = [
            '[data-testid="address"]',
            '.sc-1jw7o9w-1',
            '[class*="address"]',
            'p',
            'div'
        ]
        
        for selector in address_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if city.lower() in text.lower() or re.search(r'\d{5}-\d{3}', text):
                    data['address'] = text
                    break
            if data['address'] != 'N/A':
                break
    
    # Se ainda não encontrou, tenta uma abordagem mais genérica
    if data['price'] == 'N/A':
        # Procura por qualquer elemento que contenha 'R$' e números
        for element in soup.find_all(string=True):
            text = element.strip()
            if re.search(r'R\$ [\d.,]+', text):
                data['price'] = text
                break
    
    if data['area'] == 'N/A':
        # Procura por qualquer elemento que contenha números seguidos de 'm²'
        for element in soup.find_all(string=True):
            text = element.strip()
            if re.search(r'[\d.,]+ m²', text):
                data['area'] = text
                break
    
    if data['address'] == 'N/A':
        # Procura por qualquer elemento que contenha um CEP ou o nome da cidade
        for element in soup.find_all(string=True):
            text = element.strip()
            if re.search(r'\d{5}-\d{3}', text) or city.lower() in text.lower():
                data['address'] = text
                break
    
    return data

def scrape_with_selenium(url, source_name, city, max_pages=3):
    """
    Usa Selenium para scraping quando requests é bloqueado.
    """
    logging.info(f"Iniciando scraping com Selenium para {source_name} em {city}: {url}")
    data = []
    
    # Configurações do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar sem abrir navegador
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--user-agent={ua.random}")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-extensions")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        for page in range(1, max_pages + 1):
            if 'zap' in url:
                page_url = f"{url}?pagina={page}"
            elif 'vivareal' in url:
                page_url = f"{url}?pagina={page}"
            elif 'olx' in url:
                page_url = f"{url}?o={page}"
            else:
                page_url = url
                
            logging.info(f"Processando página {page} de {max_pages}: {page_url}")
            
            driver.get(page_url)
            time.sleep(5)  # Espera a página carregar completamente
            
            # Verificar se a página carregou corretamente
            if city.lower() not in driver.current_url.lower():
                logging.warning(f"A URL foi redirecionada. Esperado: {city}, Atual: {driver.current_url}")
            
            # Salvar HTML para depuração
            debug_page_html(driver, source_name, page, city)
            
            # Tenta diferentes seletores para cada site
            listings = []
            
            if 'zap' in url:
                # Tenta diferentes seletores para o Zap
                selectors = [
                    'div[data-testid="property-card"]',
                    'div.simple-card__container',
                    'div[data-analytics="listing-card"]',
                    'div[data-testid="card-container"]',
                    'div[class*="card"]'
                ]
                for selector in selectors:
                    try:
                        listings = driver.find_elements(By.CSS_SELECTOR, selector)
                        if listings:
                            logging.info(f"Encontrados {len(listings)} elementos com seletor: {selector}")
                            break
                    except Exception as e:
                        logging.warning(f"Erro com seletor {selector}: {e}")
                        
            elif 'vivareal' in url:
                # Tenta diferentes seletores para o Viva Real
                selectors = [
                    'div[data-testid="property-card"]',
                    'div.property-card__container',
                    'div[data-analytics="listing-card"]',
                    'div[class*="card"]'
                ]
                for selector in selectors:
                    try:
                        listings = driver.find_elements(By.CSS_SELECTOR, selector)
                        if listings:
                            logging.info(f"Encontrados {len(listings)} elementos com seletor: {selector}")
                            break
                    except Exception as e:
                        logging.warning(f"Erro com seletor {selector}: {e}")
                        
            elif 'olx' in url:
                # Tenta diferentes seletores para o OLX
                selectors = [
                    'li[data-aut-id="itemBox"]',
                    'li.sc-1fcmfeb-2',
                    'li[data-testid="listing-card"]',
                    'li[class*="item"]'
                ]
                for selector in selectors:
                    try:
                        listings = driver.find_elements(By.CSS_SELECTOR, selector)
                        if listings:
                            logging.info(f"Encontrados {len(listings)} elementos com seletor: {selector}")
                            break
                    except Exception as e:
                        logging.warning(f"Erro com seletor {selector}: {e}")
            
            if not listings:
                logging.warning(f"Nenhum imóvel encontrado na página {page}")
                continue
                
            logging.info(f"Analisando {len(listings)} cards da página {page}")
            
            # Analisa o primeiro card para entender a estrutura
            if listings and not os.path.exists(f'debug/{source_name}_{city}_card_analysis.html'):
                os.makedirs('debug', exist_ok=True)
                card_path = f'debug/{source_name}_{city}_card_analysis.html'
                with open(card_path, 'w', encoding='utf-8') as f:
                    f.write(listings[0].get_attribute('outerHTML'))
                logging.info(f"Estrutura do card salva para análise em {card_path}")
            
            valid_cards = 0
            for i, listing in enumerate(listings):
                try:
                    # Obtém o HTML do card
                    card_html = listing.get_attribute('outerHTML')
                    
                    # Analisa o card com BeautifulSoup
                    card_data = analyze_card_with_bs4(card_html, source_name, city)
                    
                    # Log para depuração
                    if i < 3:  # Apenas para os primeiros 3 cards
                        logging.info(f"Card {i+1}: Preço: {card_data['price']}, Área: {card_data['area']}, Endereço: {card_data['address']}")
                    
                    # Verifica se o card tem dados válidos
                    if card_data['price'] != 'N/A' and card_data['area'] != 'N/A':
                        valid_cards += 1
                    
                    property_type = 'venda' if '/venda/' in url else 'aluguel'
                    
                    data.append({
                        'source': source_name,
                        'price_raw': card_data['price'],
                        'area_raw': card_data['area'],
                        'address_raw': card_data['address'],
                        'type': property_type,
                        'city': city
                    })
                except Exception as e:
                    logging.warning(f"Erro ao processar imóvel {i+1}: {e}")
                    continue
            
            logging.info(f"Cards válidos na página {page}: {valid_cards} de {len(listings)}")
                    
            time.sleep(3)  # Respeita o site
            
    except Exception as e:
        logging.error(f"Erro durante o scraping com Selenium: {e}")
    finally:
        if driver:
            driver.quit()
    
    logging.info(f"{len(data)} itens coletados de {source_name} em {city}.")
    return pd.DataFrame(data)

def scrape_zapimoveis(url: str, city: str, max_pages: int = 3) -> pd.DataFrame:
    """
    Coleta dados imobiliários do Zap Imóveis.
    """
    return scrape_with_selenium(url, 'ZapImoveis', city, max_pages)

def scrape_vivareal(url: str, city: str, max_pages: int = 3) -> pd.DataFrame:
    """
    Coleta dados imobiliários do Viva Real.
    """
    return scrape_with_selenium(url, 'VivaReal', city, max_pages)

def scrape_olx(url: str, city: str, max_pages: int = 3) -> pd.DataFrame:
    """
    Coleta dados imobiliários do OLX Imóveis.
    """
    return scrape_with_selenium(url, 'OLX', city, max_pages)

def collect_real_estate_data(zap_url: str, vivareal_url: str, olx_url: str, city: str) -> pd.DataFrame:
    """
    Função principal para coletar dados imobiliários de diversas fontes.
    """
    df_zap = scrape_zapimoveis(zap_url, city)
    df_vivareal = scrape_vivareal(vivareal_url, city)
    df_olx = scrape_olx(olx_url, city)
    
    # Concatenar e retornar os dados coletados
    return pd.concat([df_zap, df_vivareal, df_olx], ignore_index=True)

if __name__ == "__main__":
    # URLs de exemplo (precisam ser atualizadas com URLs reais para Recife e Salvador)
    zap_recife_url = "https://www.zapimoveis.com.br/aluguel/galpoes/pe+recife/"
    vivareal_recife_url = "https://www.vivareal.com.br/aluguel/galpoes/pe+recife/"
    olx_recife_url = "https://pe.olx.com.br/grande-recife/imoveis/galpoes-aluguel"
    
    # Para Salvador, URLs similares
    zap_salvador_url = "https://www.zapimoveis.com.br/aluguel/galpoes/ba+salvador/"
    vivareal_salvador_url = "https://www.vivareal.com.br/aluguel/galpoes/ba+salvador/"
    olx_salvador_url = "https://ba.olx.com.br/salvador-e-regiao/imoveis/galpoes-aluguel"
    
    # Coleta para Recife
    logging.info("Iniciando coleta de dados para Recife...")
    df_recife = collect_real_estate_data(zap_recife_url, vivareal_recife_url, olx_recife_url, "Recife")
    logging.info(f"Dados coletados para Recife: {len(df_recife)} registros")
    
    # Coleta para Salvador
    logging.info("Iniciando coleta de dados para Salvador...")
    df_salvador = collect_real_estate_data(zap_salvador_url, vivareal_salvador_url, olx_salvador_url, "Salvador")
    logging.info(f"Dados coletados para Salvador: {len(df_salvador)} registros")
    
    # Combinar dados de ambas as cidades
    all_real_estate_data = pd.concat([df_recife, df_salvador], ignore_index=True)
    logging.info(f"Total de registros combinados: {len(all_real_estate_data)}")
    
    print("\nDados imobiliários brutos (amostra):")
    print(all_real_estate_data.head())
    
    # Criar diretório para dados brutos se não existir
    os.makedirs('data/raw', exist_ok=True)
    
    # Salvar para processamento posterior (ex: CSV ou JSON)
    output_path = 'data/raw/Etapa2_1_1_collect_real_estate_raw_data.csv'
    all_real_estate_data.to_csv(output_path, index=False)
    logging.info(f"Dados imobiliários brutos salvos em '{output_path}'")
    
    # Salvar também em JSON para preservar tipos de dados
    json_path = 'data/raw/Etapa2_1_1_collect_real_estate_raw_data.json'
    all_real_estate_data.to_json(json_path, orient='records', indent=2)
    logging.info(f"Dados imobiliários brutos salvos em JSON em '{json_path}'")
    
    # Exibir estatísticas básicas
    print("\nEstatísticas básicas:")
    print(f"Total de registros: {len(all_real_estate_data)}")
    print(f"Registros por cidade: {all_real_estate_data['city'].value_counts().to_dict()}")
    print(f"Registros por fonte: {all_real_estate_data['source'].value_counts().to_dict()}")