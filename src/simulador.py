import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.carrega_data import CarregaData
import random
import pandas as pd

def choice_action():
    agente = CarregaData()

    for _ in range(0, 1000):
        acao = agente.escolher_acao()
        recompensa = random.randint(0, 10)
        agente.registrar_recompensa(acao, recompensa)

def kill_agent():
    temp_pass = 0000
    o = str(input('Deseja realmente apagar todos os dados do dataset? [S/N]: ')).lower()
    pass_w = int(input('Password: '))
    if pass_w == temp_pass:
        match o[0]:
            case "s":
                agente = CarregaData()
                agente.kill_agent()
                print(f'Agente resetado com sucesso!')
            case "n":
                main()
    else:
        print('\033[31m(Incorret Password, try again)\033[m')
        main()

def tittle(text):
    print('-'*30)
    print(f'{text:^30}')
    print('-'*30)

def public():
    tittle('Reward Simulator')
    list_option = ['training basic model', 'reset agente', 'show model', 'exit']
    for e, _ in enumerate(list_option):
        print(f'{e+1} - {_.title()}')
    return list_option

def show_model():
    df_data = pd.DataFrame(data = pd.read_json('data/data.json'))
    df_data_invertido = df_data.T
    df_data_invertido["media_recompensa"] = df_data_invertido["media_recompensa"].astype(float).round(2)
    df_data_invertido.columns = ["Vezes", "Soma", "Media", "Esforço"]
    print(df_data_invertido)

def option(list_option, option_choice):
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

        case "exit":
            exit

def main():
    lista = public()
    option_choice = input('Choice your option: ').lower()
    option(lista, option_choice)

if __name__ == "__main__":
    main()
