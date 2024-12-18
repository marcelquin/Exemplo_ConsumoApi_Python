import requests
import time
from tinydb import TinyDB
from datetime import datetime

def get_papiline_data():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    data = response.json()
    print(data)
    return data

def transform_dados_bitcoin(dados):
    valor = dados["data"]["amount"]
    criptomoeda = dados["data"]["base"]
    moeda = dados["data"]["currency"]
    timestamp = datetime.now().timestamp()

    dados_transformados = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }

    return dados_transformados

def salvar_dados_tinydb(dados, db_name="bitcoin.json"):
    db = TinyDB(db_name)
    db.insert(dados)
    print("Dados salvos com sucesso!")


if __name__ == "__main__":
    # Extração dos dados
    while True:
        dados_json = get_papiline_data()
        dados_tratados = transform_dados_bitcoin(dados_json)
        salvar_dados_tinydb(dados_tratados)
        time.sleep(60)

