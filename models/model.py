import json
import os
import random

class AgenteSimulador():
    def __init__(self):
        self.arquivo_json = "data/data.json"
        self.dopamina = 0
        self.historico = []

        if not os.path.exists(self.arquivo_json):
            raise FileNotFoundError("Arquivo de memória não encontrado.")

        with open(self.arquivo_json, 'r') as f:
            self.memoria = json.load(f)

    def escolher_acao(self):  
        acoes_disponiveis = list(self.memoria.keys())
        acao_escolhida = random.choice(acoes_disponiveis)
        self.historico.append(acao_escolhida)
        return acao_escolhida

    def registrar_recompensa(self, acao, recompensa_real):
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
                
        with open(self.arquivo_json, 'w') as f:
            json.dump(k, f, indent=4)