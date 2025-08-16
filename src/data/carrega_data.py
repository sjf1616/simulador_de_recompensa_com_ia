import json
import os
import random
import csv

class CarregaData():
    def __init__(self):
        self.arquivo_json = "data/data.json"
        self.dopamina = 0
        self.historico = []

        if not os.path.exists(self.arquivo_json):
            raise FileNotFoundError("Arquivo de memória não encontrado.")

        with open(self.arquivo_json, 'r') as f:
            self.memoria = json.load(f)

    def escolher_acao(self):
        '''
        # Random choices an action that into path data.json

        **Param**:\n
        No parameters

        **Return**:\n
        A value action choice
        '''  
        acoes_disponiveis = list(self.memoria.keys())
        self.acao_escolhida = random.choice(acoes_disponiveis)
        self.historico.append(self.acao_escolhida)
        return self.acao_escolhida

    def registrar_recompensa(self, acao, recompensa_real):
        '''
        # Register action in .json 

        **Param**:\n
            acao (str): Action 
            recompensa_real (int): Real values reward

        **Return**:\n
            None
        '''

        dados = self.memoria[acao]

        dados["vezes"] += 1
        dados["soma_recompensa"] += recompensa_real
        dados["media_recompensa"] = (dados["soma_recompensa"] / dados["vezes"])
        self.memoria[acao] = dados

        expectativa = dados["media_recompensa"]

        if recompensa_real > expectativa:
            self.dopamina += (recompensa_real - expectativa)
        else:
            self.dopamina -= (expectativa - recompensa_real)

        self.dopamina = round(self.dopamina, 2)

        self.salvar_memoria()
        self.register_logs(recompensa_real, self.dopamina, acao)

    def salvar_memoria(self):
        with open(self.arquivo_json, 'w') as f:
            json.dump(self.memoria, f, indent=4)  

    def kill_agent(self):
        with open(self.arquivo_json, 'r') as f:
            k = json.load(f)
            for a in k.keys():
                k[a]['vezes'] = 0
                k[a]['soma_recompensa'] = 0
                k[a]['media_recompensa'] = 0

        with open("data/dataset.csv", 'w', newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["dopamina", "acao", "recompensa_real"])

                
        with open(self.arquivo_json, 'w') as f:
            json.dump(k, f, indent=4)

    def register_logs(self, recompensa_real, dopamina, acao):
        fieldname = ['dopamina', 'acao', 'recompensa_real']
        with open('data/dataset.csv', 'a', newline='', encoding='utf-8') as f:
            dataset = csv.DictWriter(f, fieldnames=fieldname)
            dataset.writerow({'dopamina':dopamina, 'acao': acao, 'recompensa_real':recompensa_real})