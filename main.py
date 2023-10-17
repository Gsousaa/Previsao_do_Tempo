from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager 
import tkinter as tk
from PIL import Image,ImageTk
import base64, io, time

cidade_in = "Curitiba"
#Configuração do WebDriver do Firefox
firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True #Se você quiser executar sem interface Gráfica

#Inicializa o navegador Firefox 
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=firefox_options)
#Abrir a página do google
driver.get("https://www.google.com.br")

#Realizar a busca no google
buscar = driver.find_element(By.XPATH,'//*[@class="gLFyf"]')
buscar.send_keys("Previsão do tempo "+cidade_in+Keys.ENTER)

#Tempo para garantir o carregamento
time.sleep(5)

#Capturar as informações da página
temp = driver.find_element(By.XPATH,'//*[@class="wob_t q8U8x"]').text 
cidade = driver.find_element(By.XPATH,'//*[@class="BBwThe"]').text 
percentual_chuva = driver.find_element(By.XPATH,'//*[@id="wob_pp"]').text 
percentual_uumidade = driver.find_element(By.XPATH,'//*[@id="wob_hm"]').text 
velocidade_vento = driver.find_element(By.XPATH, '//*[@id="wob_ws"]').text 
imagem = driver.find_element(By.XPATH, '//*[@id="wob_tci"]').screenshot_as_base64

#Texto a ser exibido no popup de saída
mensagem = f"Cidade: {cidade}\nTemperatura: {temp}º\nChuva: {percentual_chuva}\nUmidade: {percentual_uumidade}\nVento: {velocidade_vento}"

#Cria a janela principal
root = tk.Tk()
root.withdraw()

#Cria uma nova janela personalizada
janela_personalizada = tk.Toplevel(root)

#Configura a imagem Base64
imagem_bytes = base64.b64decode(imagem)
imagem = Image.open(io.BytesIO(imagem_bytes))
imagem_tk = ImageTk.PhotoImage(imagem)

#Cria um rotulo para exibir a imagem
label_imagem = tk.Label(janela_personalizada,image=imagem_tk)
label_imagem.pack(side="left")

#Configura a imagem para que não seja coletada pelo garbage collector
label_imagem.imagem_tk = imagem_tk

#Cria o texto ao lado
label_texto = tk.Label(janela_personalizada,text=mensagem)
label_texto.pack(side="right")

#Executa a janela personalizada
janela_personalizada.mainloop()

root.mainloop()
