import telebot, json, requests 
import pandas as pd
from time import sleep
from datetime import datetime

#Carregando o JSON com algumas informações 
with open("creds.json", "r") as file:
    creds = json.load(file)

#Atribuindo as informações do JSON a variáveis
bot = telebot.TeleBot(creds['telegram']['bot_token'])
sheet_url = creds['planilha']
shortner_url = creds['encurtador']
chat_id = creds['telegram']['chat_id_prod']

df = pd.read_csv(sheet_url)

print(f"[FROGGY-LOG] Iniciando as atividades! - {datetime.now()}")
print('-=' * 30)

#Lembrar de enviar alguns exemplos de frase nos primeiros posts de cada dia. Ou também 
#Algumas frases de efeito antes do primeiro post em cada TURNO do dia.
bot.send_message(chat_id, "Fala pessoal! Promoções novas hoje!")

#Lembrando, a mensagem acompanha a identação, ou seja, caso deixe a mensagem indentada em python,
#irá aplicar os "espaços vazios" também na exibição.
def envioUnico():
    product = df.iloc[3].to_dict()
    body = {
        "url": product['LINK']
    }
    product_url = requests.post(shortner_url, json=body)
    product_url = product_url.json()
    print(product_url["urlEncurtada"])
    print(f"[FROGGY-LOG] PRODUTO ENVIADO! ID: {df.index} | NOME: {product['NOME']} | - {datetime.now()}")
    mensagem = f""" 
{product['FRASE']} 🐸

<b>{product['NOME']}</b>

De: <s>{product['VALOR_ANTIGO']}</s>            

<b>Por: {product['VALOR_PROMO']} 😍</b>
<i>CUPOM: {product['CUPOM']} ✨</i>​

Compre aqui:
🛍️ {product["LINK"]}
"""
#🛍️ {product_url["urlEncurtada"]}
    #Enviando mensagem com IMAGEM em anexo
    bot.send_photo(chat_id,photo=product["IMAGEM"],caption=mensagem, parse_mode="HTML")
    print('-=' * 30)
    
def envioEmLote():
    for i in range(len(df)):
        product = df.iloc[i].to_dict()
        print(f'Produto: {product['NOME']} | Preço: {product['VALOR_PROMO']}')
        print(f'Produto: {product['NOME']} | Preço: {product['VALOR_PROMO']}')
        
        bot.send_message(
            chat_id, 
            f"""
            OFERTAS DO SAPO LOUCO 🐸
            {product['FRASE']}

            {product['NOME']}

            De: ~~{product['VALOR_ANTIGO']}~~            
            Por: {product['VALOR_PROMO']} 😍
            CUPOM: {product['CUPOM']} ✨​

            Compre aqui:
            🛍️ {product['LINK']}

            """, parse_mode="HTML")
        print('-=' * 30)

#Executando o código de acordo com o fluxo
envioUnico()
print(f"[FROGGY-LOG] Finalizando envio! - {datetime.now()}")
print(f"[FROGGY-LOG] Aguardando horário...")
