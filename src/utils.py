import pandas as pd 
import json


class Utils():

    BASE_URL = ''

    DEFAULT_ELECTION_ID = 9579
    PRESIDENTIAL_ELECTION_ID = 9577

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

    def build_json_municipios(self):
        '''
            RETORNA UM OBJETO JSON COM OS MUNICIPIOS CARREGADOS
        '''
        url = 'files/ele2022/' + str(self.DEFAULT_ELECTION_ID) + '/config/mun-e00' + str(self.DEFAULT_ELECTION_ID) + '-cm.json'
        mun = self.load_json(filename=url)
        return mun 

    def get_all_states(self):
        '''
            RETORNA DUAS VARIÁVEIS: UM NUMERO INTEIRO COM A QUANTIDADE DE ESTADOS E UMA LISTA CONTENDO TODOS ELES

            <INT>, {'cd' : '<STR>', 'name' : '<STR>', 'capital_name': <STR>, 'capital_cd': <INT>, 'count_mun': <INT>,}

        '''
        states = [] 
        mun = self.build_json_municipios()
        for i in range(0, len(mun['abr'])):
            state = {} 
            state['cd'] = mun['abr'][i]['cd']
            state['ds'] = mun['abr'][i]['ds']
            capital_data = self.get_state_capital(acronym=state['cd'])
            state['capital_name'] = capital_data['name']
            state['capital_cd'] = capital_data['cd']
            states.append(state)

        print(len(states), states)
        return len(states), states


    def get_state_capital(self, acronym: str):
        '''
            RETORNA o nome e o código do municipio no formato 
            {'cd' : '<INT>', 'name' : '<STR>'}
            RECEBE o atributo state, uma string de 2 digitos com a sigla do estado

        '''
        # build URL 
        capital = {}
        mun = self.build_json_municipios()

        # FIND ACRONYM:
        for i in range(0, len(mun['abr'])):
           if mun['abr'][i]['cd'] == acronym.upper():
                for j in range(0, len(mun['abr'][i]['mu'])):
                    if mun['abr'][i]['mu'][j]['c'] == 'S':
                        capital['cd'] = mun['abr'][i]['mu'][j]['cdi']
                        capital['name'] = mun['abr'][i]['mu'][j]['nm']

        print(capital)
        return capital


    def load_json(self, filename: str) -> dict:
        try:
            file = open(filename)
            data = json.load(file)
            return data 
        except Exception as e:
            print(f"Erro em load_json: {e}")

    def docs_comum_config_ele_c(self):
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
        # LISTA DOS PLEITOS
        for i in range(0, len(data['pl'])):
            print("data['pl'][i]['cd'] - " + str(data['pl'][i]['cd']) + ' - Código do pleito, utilizado para identificar os códigos de eleições que participam do mesmoprocesso eleitoral.')
            print("data['pl'][i]['cdpr'] - " + str(data['pl'][i]['cdpr']) + ' - Código do processo eleitoral, utilizado para identificar os códigos de pleitos que participamdo mesmo processo eleitoral.')
            print("data['pl'][i]['dt'] - " + str(data['pl'][i]['dt']) + ' - Data de ocorrência das eleições do pleito no formato dd/mm/aaaa')
            print("data['pl'][i]['dtlim'] - " + str(data['pl'][i]['dtlim']) + ' - Data limite para a divulgação dos resultados no formato dd/mm/aaaa')

            print('\nSubelemento de pl: "e" (eleição) - Um elemento “abr” para cada UF que participa da eleição.\n')
            # ELEIÇÃO EM QUESTÃO DE CADA PLEITO
            for j in range(0, len(data['pl'][i]['e'])):
                print("data['pl'][i]['e'][j]['cd'] - " + str(data['pl'][i]['e'][j]['cd']) + ' - Código da eleição')
                print("data['pl'][i]['e'][j]['cdt2'] - " + str(data['pl'][i]['e'][j]['cdt2']) + ' - Código da eleição para o segundo turno.')
                print("data['pl'][i]['e'][j]['nm'] - " + str(data['pl'][i]['e'][j]['nm']) + ' - Nome da Eleição')
                print("data['pl'][i]['e'][j]['t'] - " + str(data['pl'][i]['e'][j]['t']) + ' - Turno da Eleição')
                print("data['pl'][i]['e'][j]['tp'] - " + str(data['pl'][i]['e'][j]['tp']) + ' - Número identificador do tipo da eleição.')
                print('Tradução: ' + self.TP_ELECTIONS[data['pl'][i]['e'][j]['tp']])

                print('\nSubelemento de e: "abr" - Abrangência onde ocorrerá a eleição em questão.')
                # ABRANGÊNICA DA ELEIÇÃO (ESTADUAL/FEDERAL)
                for k in range(0, len(data['pl'][i]['e'][j]['abr'])):
                    print()
                    print("data['pl'][i]['e'][j]['abr'][k]['cd'] - " + str(data['pl'][i]['e'][j]['abr'][k]['cd']) + ' - Código da abrangência')
                    # CARGOS EM JOGO NA ABRANGÊNCIA
                    for l in range(0, len(data['pl'][i]['e'][j]['abr'][k]['cp'])):
                        print('\nSubemenento de abr: "cp" -  Elemento: cp (Cargo ou Pergunta)')
                        print("data['pl'][i]['e'][j]['abr'][k]['cp'][l]['cd'] - " + str(data['pl'][i]['e'][j]['abr'][k]['cp'][l]['cd']) + ' - Código do cargo ou da pergunta.')
                        print("data['pl'][i]['e'][j]['abr'][k]['cp'][l]['ds'] - " + str(data['pl'][i]['e'][j]['abr'][k]['cp'][l]['ds']) + ' - Descrição do cargo ou da pergunta.')
                        print("data['pl'][i]['e'][j]['abr'][k]['cp'][l]['tp'] - " + str(data['pl'][i]['e'][j]['abr'][k]['cp'][l]['tp']) + ' - Número identificado do tipo de cargo.')
                        print("Tradução: " + str(self.TP_CARGO[str(data['pl'][i]['e'][j]['abr'][k]['cp'][l]['tp'])]))

                print('*'*30)

    def docs_ele_year_electionID_condig_mun_stateId_cm_json(self):
        '''
            Função dedicada para documentar arquivos dentro da pasta ele2022/9579/config, referente as Eleições estaduais ordinárias.
            Tem um único arquivo nessa pasta, o mun-e009579-cm.json, o arquivo de configuração de municípios. 
            A documentação desse arquivo está disponivel no link https://www.tse.jus.br/++theme++justica_eleitoral/pdfjs/web/viewer.html?file=https://www.tse.jus.br/eleicoes/eleicoes-2022/arquivos/interessados/ea12-arquivo-de-configuracao-de-municipios/@@download/file/TSE-EA12-Arquivo-de-configuracao-de-municipios.pdf
        
            1. Descrição
                Esse arquivo contém informações acerca dos municípios das eleições disponíveis para divulgação. 
                Os arquivos JSON serão consumidos pelo aplicativo Resultados.
            2. Formato do nome do arquivo
                O nome do arquivo é formado conforme o padrão a seguir:
                    mun-e<número da eleição>-cm.json
                Exemplo: mun-e012345-cm.json
                Onde:
                    e<número da eleição>: Número de controle identificador da eleição a que ser refere o arquivo. 
                Compostopor seis dígitos. É o um número fixo para todos os arquivos de uma mesma eleição.

            TODO: verificar similaridade desse arquivo com o da pasta 9577, que contém os arquivos referentes as eleições federais ordinárias

        '''
        path = 'files/ele2022/9579/config/'
        filename = 'mun-e009579-cm.json'

        data = self.load_json(filename=path+filename)
        print("Atributos raiz: ")
        print("data['dg'] - " + str(data['dg']) + ' - Data de geração do arquivo')
        print("data['hg'] - " + str(data['hg']) + ' - Hora de geração do arquivo')
        print("data['f'] - " + str(data['f']) + ' - Fase em que foi gerado o arquivo')
        print('Tradução: ' + self.CD_FASES[str(data['f'])])
        
        print('-'*30)
        print('Elemento: abrangência: "abr"')
        print('Lista com as UF’s - Unidades Federativas - que participam da eleição. Para Exterior, a siglaserá “ZZ”') 
        print(f'Conteúdo: Contém um elemento “mu” para cada município ou localidade do exterior que faz parte da UF em questão.')
        # LISTA DOS ESTADOS
        for i in range(0, len(data['abr'])):
            print('\n')
            print("data['abr'][i]['cd'] - " + data['abr'][i]['cd'] + ' - Sigla da UF em maiúsculo.')
            print("data['abr'][i]['ds'] - " + data['abr'][i]['ds'] + ' - Nome descritivo da abrangência. Nesse caso, o nome da UF')
            # LISTA DOS MUNICIPIOS
            for j in range(0, len(data['abr'][i]['mu'])):
                print("data['abr'][i]['mu'][j]['cd'] - " + data['abr'][i]['mu'][j]['cd'] + ' - Número do Município com cinco dígitos, preenchidos com zero à esquerda, de acordo com ocadastro da Justiça Eleitoral')
                print("data['abr'][i]['mu'][j]['cdi'] - " + data['abr'][i]['mu'][j]['cdi'] + ' - Código identificador do Município com cinco dígitos, preenchidos com zero à esquerda, deacordo com o cadastro IBGE')
                print("data['abr'][i]['mu'][j]['nm'] - " + data['abr'][i]['mu'][j]['nm'] + ' - Nome do município')
                print("data['abr'][i]['mu'][j]['c'] - " + data['abr'][i]['mu'][j]['c'] + ' - Indica se o Município é a capital da UF (S) ou não é a capital da UF (N).')
                # LISTA DAS ZONAS ELEITORAIS 
                for k in range(0, len(data['abr'][i]['mu'][j]['z'])):
                    print("data['abr'][i]['mu'][j]['z'][k] - " + data['abr'][i]['mu'][j]['c'] + ' - Indica se o Município é a capital da UF (S) ou não é a capital da UF (N).')


                
if __name__ == '__main__':
    obj = Utils()
    # obj.docs_comum_config_ele_c()
    # obj.docs_ele_year_electionID_condig_mun_stateId_cm_json()
    # obj.get_state_capital(acronym='df')
    obj.get_all_states()

