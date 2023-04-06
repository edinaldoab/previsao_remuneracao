from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def get_job_info(keyword, location_name, num_pages, file_path):
    
    
    # seta Opitions() para abrir a tela do navegador implicitamente
    options = Options()
    options.add_argument('--headless')
    
    # inicia o driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.glassdoor.co.in/Job/Home/recentActivity.htm")
    
    # insere a palavra chave (ex.: Data Scientist)
    search_input = driver.find_element(By.ID, 'sc.keyword')
    search_input.send_keys(keyword)

    # insere a palavra localização da vaga (ex.: United States)
    location_input = driver.find_element(By.ID, 'sc.location')
    location_input.send_keys(Keys.CONTROL + 'a')
    time.sleep(2)
    location_input.send_keys(location_name)
    time.sleep(5)
    location_input.send_keys(Keys.ENTER)
    time.sleep(2)
    
    # inicializa as listas de atributos das vagas
    company_name = []
    job_title = []
    location = []
    job_description = []
    salary_estimate = []
    company_size = []
    company_type = []
    company_sector = []
    company_industry = []
    company_founded = []
    company_revenue = []

    #atribuindo 1 como índice da primeira página
    current_page = 1     
     
    time.sleep(3)
    
    while current_page <= num_pages:   
        
        done = False
        
        #iterador criado para escrever o xpath do salário
        i = 1

        while not done:
            job_cards = driver.find_elements(By.XPATH, "//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")
            for card in job_cards:
                card.click()
                time.sleep(3)

                # Fecha a janela de requisição de login
                try:
                    driver.find_element(By.XPATH, ".//span[@class='SVGInline modal_closeIcon']").click()
                    time.sleep(1)
                except NoSuchElementException:
                    time.sleep(2)
                    pass

                #Expande as descrições em "Show More"
                opened=False
                tries=0

                while not opened and tries!=5:
                    try:
                        driver.find_element(By.XPATH,"//div[@class='css-t3xrds e856ufb4']").click()
                        time.sleep(1)
                        opened=True
                    except NoSuchElementException:
                        card.click()
                        print(str(current_page) + '#ERROR: no such element')
                        tries+=1
                        time.sleep(2)
                
                #Raspagem dos dados 
                try:
                    # company_name.append(driver.find_element(By.XPATH, "//div[@class='css-87uc0g e1tk4kwz1']").text)
                    parent_name = driver.find_element(By.XPATH,"//div[@class='css-87uc0g e1tk4kwz1']")
                    company_name.append(driver.execute_script('return arguments[0].childNodes[0].textContent;', parent_name).strip())
                except:
                    company_name.append("#N/A")
                    pass

                try:
                    job_title.append(driver.find_element(By.XPATH, "//div[@class='css-1vg6q84 e1tk4kwz4']").text)
                except:
                    job_title.append("#N/A")
                    pass

                try:
                    location.append(driver.find_element(By.XPATH, "//div[@class='css-56kyx5 e1tk4kwz5']").text)
                except:
                    location.append("#N/A")
                    pass

                try:
                    job_description.append(driver.find_element(By.XPATH, "//div[@id='JobDescriptionContainer']").text)
                except:
                    job_description.append("#N/A")
                    pass

                try:
                    parent_salary = driver\
                        .find_element(By.XPATH, f"/html/body/div[2]/div/div/div/div/div[2]/section/article/div[1]/ul/li[{i}]/div[2]/div[3]/div[1]/span")
                    salary_estimate.append(driver.execute_script('return arguments[0].childNodes[0].textContent;', parent_salary).strip())

                except:
                    salary_estimate.append("#N/A")
                    pass
                
                try:
                    company_size.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Size']//following-sibling::*").text)
                except:
                    company_size.append("#N/A")
                    pass
                
                try:
                    company_type.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*").text)
                except:
                    company_type.append("#N/A")
                    pass
                    
                try:
                    company_sector.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*").text)
                except:
                    company_sector.append("#N/A")
                    pass
                    
                try:
                    company_industry.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*").text)
                except:
                    company_industry.append("#N/A")
                    pass
                    
                try:
                    company_founded.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*").text)
                except:
                    company_founded.append("#N/A")
                    pass
                    
                try:
                    company_revenue.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Revenue']//following-sibling::*").text)
                except:
                    company_revenue.append("#N/A")
                    pass
                                
                i += 1    
                    
                done = True
                
       # Para a próxima página:        
        if done:
            driver.find_element(By.XPATH, "//span[@alt='next-icon']").click()   
            current_page += 1
            time.sleep(4)

    driver.close()

    #criação do data frame
    df = pd.DataFrame({'company': company_name, 
    'job title': job_title,
    'location': location,
    'job description': job_description,
    'salary estimate': salary_estimate,
    'company_size': company_size,
    'company_type': company_type,
    'company_sector': company_sector,
    'company_industry' : company_industry,
    'company_founded' : company_founded,
    'company_revenue': company_revenue})
    
    df.to_csv(f'{file_path}/{keyword.replace(" ", "_")}_{location_name.replace(" ", "_")}.csv', index=False, mode='w+')
