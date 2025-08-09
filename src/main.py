import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.model import AgenteSimulador
import random
import pandas as pd

def choice_action():
    agente = AgenteSimulador()

    for _ in range(0, 1000):
        acao = agente.escolher_acao()
        recompensa = random.randint(0, 10)
        agente.registrar_recompensa(acao, recompensa)

def kill_agent():
    agente = AgenteSimulador()
    agente.kill_agent()
    print(f'Agente resetado com sucesso!')

def tittle(text):
    print('-'*30)
    print(f'{text:^30}')
    print('-'*30)

def public():
    tittle('Reward Simulator')

def show_model():
    df_data = pd.DataFrame(data = pd.read_json('data/data.json'))
    df_data_invertido = df_data.T
    df_data_invertido["media_recompensa"] = df_data_invertido["media_recompensa"].astype(float).round(2)
    df_data_invertido.columns = ["Vezes", "Soma", "Media", "Esforço"]
    print(df_data_invertido)

def option():
    list_option = ['training basic model', 'reset agente', 'show model']
    for e, _ in enumerate(list_option):
        print(f'{e+1} - {_.title()}')
    option_choice = input('Choice your option: ').lower()

    while option_choice not in list_option:
        option_choice = input('\033[31m(OPTION NOT FOUND, TRY AGAIN)\033[m Choice your option: ').strip().lower()

    match option_choice:
        case "training basic model":
            tittle('Training the model')
            print('The model is trained in a 30-iteration loop.')
            choice_action()

        case "reset agente":
            kill_agent()

        case "show model":
            show_model()

def main():
    public()
    option()

if __name__ == "__main__":
    main()
