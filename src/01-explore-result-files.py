import pandas as pd 
import json

class FilesExploration():

    TP_ELECTIONS = {
        '1': 'Estadual ordinária',
        '2': 'Estadual suplementar',
        '3': 'Municipal ordinária',
        '4': 'Municipal suplementar',
        '5': 'Consulta popular nacional',
        '6': 'Consulta popular estadual',
        '7': 'Consulta popular municipal',
        '8': 'Federal ordinária',
        '9': 'Federal suplementar'
    } 

    TP_CARGO = {
        '1': 'Cargos majoritários',
        '2': 'Cargos proporcionais',
        '3': 'Pergunta de consulta popular'
    }

    CD_FASES = {
        'S': 'Simulado – se o arquivo foi gerado durante o simulado.',
        'O': 'Oficial – se o arquivo foi gerado com resultados reais da eleição.'
    } 
    
    def load_json(self, filename: str) -> dict:
        try:
            file = open(filename)
            data = json.load(file)
            return data 
        except Exception as e:
            print(f"Erro em load_json: {e}")

    
    def ele_c(self):
        '''
            Função que lê e descreve com base na documentação oficial disponível em 
            https://www.tse.jus.br/++theme++justica_eleitoral/pdfjs/web/viewer.html?file=https://www.tse.jus.br/eleicoes/eleicoes-2022/arquivos/interessados/ea11-arquivo-de-configuracao-de-eleicoes/@@download/file/TSE-EA11-Arquivo-de-configuracao-de-eleicoes.pdf
            o arquivo ele-c.json
        '''
        # # # # COMMUN / CONFIG -> ele-c.json
        print('-'*30)
        filepath = 'files/comum/config/'
        filename = 'ele-c.json'
        print(filepath + filename)
        print("Esse arquivo contém informações acerca de todas as eleições disponíveis para divulgação. Os arquivos JSONserão consumidos pelo aplicativo Resultados")
        data = self.load_json(filename=filepath+filename)
        
        print('-'*30)
        print('Atributos raiz \n')
        print("data['dg'] - " + data['dg'] + ' - Data da geração do arquivo')
        print("data['hg'] - " + data['hg'] + ' - Hora da geração do arquivo')
        print("data['f'] - " + data['f'] + ' - Fase em que foi gerado o arquivo.')
        print("data['c'] - " + data['c'] + ' - Ciclo eleitoral dos softwares que foram usados para geração do arquivo')
        
        print('-'*30)
        print('Elemento pl (pleito) - Conteúdo: Um elemento “e” para cada eleição do pleito. \n')
        for i in range(0, len(data['pl'])):
            print("data['pl'][i]['cd'] - " + str(data['pl'][i]['cd']) + ' - Código do pleito, utilizado para identificar os códigos de eleições que participam do mesmoprocesso eleitoral.')
            print("data['pl'][i]['cdpr'] - " + str(data['pl'][i]['cdpr']) + ' - Código do processo eleitoral, utilizado para identificar os códigos de pleitos que participamdo mesmo processo eleitoral.')
            print("data['pl'][i]['dt'] - " + str(data['pl'][i]['dt']) + ' - Data de ocorrência das eleições do pleito no formato dd/mm/aaaa')
            print("data['pl'][i]['dtlim'] - " + str(data['pl'][i]['dtlim']) + ' - Data limite para a divulgação dos resultados no formato dd/mm/aaaa')

            print('\nSubelemento de pl: "e" (eleição) - Um elemento “abr” para cada UF que participa da eleição.\n')
            for j in range(0, len(data['pl'][i]['e'])):
                print("data['pl'][i]['e'][j]['cd'] - " + str(data['pl'][i]['e'][j]['cd']) + ' - Código da eleição')
                print("data['pl'][i]['e'][j]['cdt2'] - " + str(data['pl'][i]['e'][j]['cdt2']) + ' - Código da eleição para o segundo turno.')
                print("data['pl'][i]['e'][j]['nm'] - " + str(data['pl'][i]['e'][j]['nm']) + ' - Nome da Eleição')
                print("data['pl'][i]['e'][j]['t'] - " + str(data['pl'][i]['e'][j]['t']) + ' - Turno da Eleição')
                print("data['pl'][i]['e'][j]['tp'] - " + str(data['pl'][i]['e'][j]['tp']) + ' - Número identificador do tipo da eleição.')
                print('Tradução: ' + self.TP_ELECTIONS[data['pl'][i]['e'][j]['tp']])

                print('\nSubelemento de e: "abr" - Abrangência onde ocorrerá a eleição em questão.')
                for k in range(0, len(data['pl'][i]['e'][j]['abr'])):
                    print()
                    print("data['pl'][i]['e'][j]['abr'][k]['cd'] - " + str(data['pl'][i]['e'][j]['abr'][k]['cd']) + ' - Código da abrangência')
                    for l in range(0, len(data['pl'][i]['e'][j]['abr'][k]['cp'])):
                        print('\nSubemenento de abr: "cp" -  Elemento: cp (Cargo ou Pergunta)')
                        print("data['pl'][i]['e'][j]['abr'][k]['cp'][l]['cd'] - " + str(data['pl'][i]['e'][j]['abr'][k]['cp'][l]['cd']) + ' - Código do cargo ou da pergunta.')
                        print("data['pl'][i]['e'][j]['abr'][k]['cp'][l]['ds'] - " + str(data['pl'][i]['e'][j]['abr'][k]['cp'][l]['ds']) + ' - Descrição do cargo ou da pergunta.')
                        print("data['pl'][i]['e'][j]['abr'][k]['cp'][l]['tp'] - " + str(data['pl'][i]['e'][j]['abr'][k]['cp'][l]['tp']) + ' - Número identificado do tipo de cargo.')
                        print("Tradução: " + str(self.TP_CARGO[str(data['pl'][i]['e'][j]['abr'][k]['cp'][l]['tp'])]))

                print('*'*30)
            
if __name__ == '__main__':
    obj = FilesExploration()
    obj.ele_c()
