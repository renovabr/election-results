import pandas as pd 
import json

class FilesExploration():
    
    def load_json(self, filename: str) -> dict:
        try:
            file = open(filename)
            data = json.load(file)
            return data 
        except Exception as e:
            print(f"Erro em load_json: {e}")
    
    def ele_c(self):
        # # # # COMMUN / CONFIG -> ele-c.json
        print('-'*30)
        filepath = 'files/comum/config/'
        filename = 'ele-c.json'
        print(filepath + filename)
        print("Esse arquivo contém informações acerca de todas as eleições disponíveis para divulgação. Os arquivos JSONserão consumidos pelo aplicativo Resultados")
        data = self.load_json(filename=filepath+filename)
            # # # # print(data)
            # # {'dg': '08/07/2022', 'hg': '13:49:50', 'f': 'S', 'c': 'ele2022', 
            # 'pl': [{'cd': '8417', 'cdpr': '7296', 'dt': '01/10/2022', 'dtlim': '01/01/2024', 
            # 'e': [{'cd': '9579', 'cdt2': '9580', 'nm': 'Eleição Ordinária Estadual - 2022 - 8417 1&#186; Turno', 't': '1', 'tp': '1', 
            # 'abr': [{'cd': 'BR', 'cp': [{'cd': '3', 'ds': 'Governador', 'tp': '1'}, {'cd': '5', 'ds': 'Senador', 'tp': '1'}, 
            # {'cd': '6', 'ds': 'Deputado Federal', 'tp': '2'}, {'cd': '7', 'ds': 'Deputado Estadual', 'tp': '2'}, 
            # {'cd': '8', 'ds': 'Deputado Distrital', 'tp': '2'}]}]}, {'cd': '9577', 'cdt2': '9578', 
            # 'nm': 'Eleição Ordinária Federal - 2022 - 8417 1&#186; Turno', 't': '1', 'tp': '8', '
            # abr': [{'cd': 'BR', 'cp': [{'cd': '1', 'ds': 'Presidente', 'tp': '1'}]}]}]}]}
        
        print('-'*30)
        print('Atributos raiz \n')
        print("data['dg'] - " + data['dg'] + ' - Data da geração do arquivo')
        print("data['hg'] - " + data['hg'] + ' - Hora da geração do arquivo')
        print("data['f'] - " + data['f'] + ' - Fase em que foi gerado o arquivo.')
        if data['f'] == 'S':
            print('\t\t “S”: Simulado – se o arquivo foi gerado durante o simulado.')
        elif data['f'] == 'O':
            print('\t\t“O”: Oficial – se o arquivo foi gerado com resultados reais da eleição.')
        print("data['c'] - " + data['c'] + ' - Ciclo eleitoral dos softwares que foram usados para geração do arquivo')
        
        print('-'*30)
        print('Elemento pl (pleito) - Conteúdo: Um elemento “e” para cada eleição do pleito. \n')
        for i in range(0, len(data['pl'])):
            print("data['pl'][i]['cd'] - " + str(data['pl'][i]['cd']) + ' - Código do pleito, utilizado para identificar os códigos de eleições que participam do mesmoprocesso eleitoral.')
            print("data['pl'][i]['cdpr'] - " + str(data['pl'][i]['cdpr']) + ' - Código do processo eleitoral, utilizado para identificar os códigos de pleitos que participamdo mesmo processo eleitoral.')
            print("data['pl'][i]['dt'] - " + str(data['pl'][i]['dt']) + ' - Data de ocorrência das eleições do pleito no formato dd/mm/aaaa')
            print("data['pl'][i]['dtlim'] - " + str(data['pl'][i]['dtlim']) + ' - Data limite para a divulgação dos resultados no formato dd/mm/aaaa')

            
        
        

if __name__ == '__main__':
    obj = FilesExploration()
    obj.ele_c()
