import pandas as pd 
import json


class Utils():

    BASE_URL = 'files/'
    
    DEFAULT_URL_CONFIG = 'ele2022/{}/dados/'
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

    TP_CARGOS = {
        '1': 'Cargos majoritários',
        '2': 'Cargos proporcionais',
        '3': 'Pergunta de consulta popular'
    }

    CD_FASES = {
        'S': 'Simulado – o arquivo foi gerado durante o simulado.',
        'O': 'Oficial –  o arquivo foi gerado com resultados reais da eleição.'
    } 

    CD_CARGOS = {
        3: 'Governador',
        5: 'Senador',
        11: 'Prefeito', 
        6: 'Deputado Federal'
    }
    
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # FUNÇÕES UTILITÁRIAS # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def load_json(self, filename: str) -> dict:
        try:
            file = open(filename)
            data = json.load(file)
            return data 
        except Exception as e:
            print(f"Erro em load_json: {e}")

    def build_json_municipios(self) -> dict:
        '''
            RETORNA UM OBJETO JSON COM OS MUNICIPIOS CARREGADOS
        '''
        url = self.BASE_URL + 'ele2022/' + str(self.DEFAULT_ELECTION_ID) + '/config/mun-e00' + str(self.DEFAULT_ELECTION_ID) + '-cm.json'
        mun = self.load_json(filename=url)
        return mun 

    def build_resultado_de_eleitos(self, cd_cargo: int, abr: str) -> dict:
        '''
            <br|uf>-c<código do cargo>-e<número da eleição>-e.json

            RETORNA UMA LISTA COM OBJETOS JSON COM O ARQUIVO DOS ELEITOS PRO CARGO DE ACORDO COM O CODIGO DO CARGO
            cd_cargo: num inteiro com o codigo do cargo a ser retornado ou então um asterisco '*'
            para retornar de todos os cargos
            abr: SIGLA da abrangência. 'BR' para brasil
            EM CADA ITEM DA LISTA VÃO TER TODOS OS ELEITOS E DADOS DE VICE/SUPLENTE P AQUELE CARGO
        '''
        data = []

        abr = abr.lower() 

        if cd_cargo != '*':
            url = self.BASE_URL + self.DEFAULT_URL_CONFIG.format(self.DEFAULT_ELECTION_ID) + abr + '/' + abr + '-c' + str(cd_cargo).zfill(4) + '-e' + str(self.DEFAULT_ELECTION_ID).zfill(6) +  '-e.json'
            obj = self.load_json(url)
            data.append(obj)
            
        else: 
            for item in self.CD_CARGOS:
                url = self.BASE_URL + self.DEFAULT_URL_CONFIG.format(self.DEFAULT_ELECTION_ID) + abr + '/' + abr + '-c' + str(item).zfill(4) + '-e' + str(self.DEFAULT_ELECTION_ID).zfill(6) + '-e.json'
                obj = self.load_json(url)
                data.append(obj)
            
        return data 

    def get_all_states(self) -> dict:
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

    def get_state_capital(self, acronym: str) -> dict:
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # FUNÇÕES DE DOCUMENTAÇÃO # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def docs_comum_config_ele_c(self) -> None:
        '''
            Função que lê e descreve com base na documentação oficial disponível em 
            https://www.tse.jus.br/++theme++justica_eleitoral/pdfjs/web/viewer.html?file=https://www.tse.jus.br/eleicoes/eleicoes-2022/arquivos/interessados/ea11-arquivo-de-configuracao-de-eleicoes/@@download/file/TSE-EA11-Arquivo-de-configuracao-de-eleicoes.pdf
            o arquivo ele-c.json
        '''
        # # # # COMMUN / CONFIG -> ele-c.json
        print('-'*30)
        filepath = self.BASE_URL + 'comum/config/'
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
                        print("Tradução: " + str(self.TP_CARGOS[str(data['pl'][i]['e'][j]['abr'][k]['cp'][l]['tp'])]))

                print('*'*30)

    def docs_ele_year_electionID_config_mun_stateId_cm_json(self) -> None:
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
        path =  self.BASE_URL + 'ele2022/9579/config/'
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

    def docs_ele_year_electionID_dados_br(self) -> None:
        '''
            Função de documentação do arquivo br-c0003-e009579-e.json -> <br|uf>-c<código do cargo>-e<número da eleição>-e.json
            EA10 – Arquivo de resultado de eleitos
            Documentação disponível em: 
            https://www.tse.jus.br/++theme++justica_eleitoral/pdfjs/web/viewer.html?file=https://www.tse.jus.br/eleicoes/eleicoes-2022/arquivos/interessados/ea10-arquivo-de-resultado-de-eleitos/@@download/file/TSE-EA10-Arquivo-de-resultado-de-eleitos.pdf
        
            ¹Votos Computados: São os votos que foram destinados ao candidato ou partido pela urna eletrônica, antes de passar pela regras de totalização.

        '''
        path = self.BASE_URL + 'ele2022/' + str(self.DEFAULT_ELECTION_ID) + '/dados/br/'
        filename = 'br-c0003-e00' + str(self.DEFAULT_ELECTION_ID) + '-e.json'
        data = self.load_json(filename=path+filename)
        print("data['ele'] - " + str(data['ele']) + ' - Código da eleição')
        print("data['cdabr'] - " + str(data['cdabr']) + ' - Código da abrangência (onde) ')
        print("data['nmabr'] - " + str(data['nmabr']) + ' - Nome da abrangência (onde) ')
        print("data['t'] - " + str(data['t']) + ' - Turno')
        print("data['f'] - " + str(data['f']) + ' - Fase: ' + str(self.CD_FASES[data['f']]))
        print("data['cdcar'] - " + str(data['cdcar']) + ' - Número identificador do cargo. - ' + self.CD_CARGOS[data['cdcar']])
        print("data['nmcar'] - "+ data['nmcar']  + " - Nome do cargo")
        for i in range(0, len(data['abr'])):
            # DENTRO DE CADA UF DA ABRANGÊNCIA
            print('-'*30)
            print("data['abr'][i]['tpabr'] - " + data['abr'][i]['tpabr']  + " - Abrangência dos cargos do arquivo, UF ou MU ")
            print("data['abr'][i]['cdabr'] - " + data['abr'][i]['cdabr']  + " - Codigo da abrangência, do UF ou MU ")
            print("data['abr'][i]['nmabr'] - " + data['abr'][i]['nmabr']  + " - Nome da abrangência, UF ou MU ")
            print("data['abr'][i]['dt'] - " + data['abr'][i]['dt']  + " - Data da última totalização ")
            print("data['abr'][i]['ht'] - " + data['abr'][i]['ht']  + " - Hora da ultima totalização")
            print("data['abr'][i]['scv'] - " + data['abr'][i]['scv']  + " - Se NÃO existem ou não candidatos para serem votados: S ou N")
            print("data['abr'][i]['tvap'] - " + str(data['abr'][i]['tvap'])  + " - Numero de votos atribuidos a alguem ou alguma legenda")
            # DENTRO DE CADA CANDIDATO ELEITO NA UF 
            for j in range(0, len(data['abr'][i]['cand'])):
                # Descrição: Contém dados referentes aos candidatos eleitos.
                # Conteúdo: 
                # Para os cargos de Governador e Prefeito, um elemento “vs” representando o Vice.
                # Para o cargo de Senador, um ou dois elementos “vs” representando o(s) suplente(s).
                # Para o cargo de Deputado Federal o elemento “vs” é omitido.
                print('CANDIDATOS ELEITOS: ')
                print("data['abr'][i]['cand'][j]['seq'] - " + str(data['abr'][i]['cand'][j]['seq'])  + " - Sequencial da ordem do candidato. Indica a ordem do mesmo na eleição")
                print("data['abr'][i]['cand'][j]['sqcand'] - " + str(data['abr'][i]['cand'][j]['sqcand'])  + " - Identificador único do candidato")
                print("data['abr'][i]['cand'][j]['n'] - " + str(data['abr'][i]['cand'][j]['n'])  + " - Numero do candidato na urnas")
                print("data['abr'][i]['cand'][j]['nm'] - " + str(data['abr'][i]['cand'][j]['nm'])  + " - Nome completo")
                print("data['abr'][i]['cand'][j]['nmu'] - " + str(data['abr'][i]['cand'][j]['nmu'])  + " - Nome urna")
                print("data['abr'][i]['cand'][j]['vap'] - " + str(data['abr'][i]['cand'][j]['vap'])  + " - Votos que o candidato teve")
                print("data['abr'][i]['cand'][j]['sgp'] - " + str(data['abr'][i]['cand'][j]['sgp'])  + " - Sigla do partido")
                print("data['abr'][i]['cand'][j]['com'] - " + str(data['abr'][i]['cand'][j]['com'])  + " - Partidos das coligações (separados por /) ")
                print('VICE / SUPLENTE: ')
                for k in range(0, len(data['abr'][i]['cand'][j]['vs'])):
                    print("data['abr'][i]['cand'][j]['vs'][k]['sqcand'] - " + str(data['abr'][i]['cand'][j]['vs'][k]['sqcand'])  + " - Identificador unico ")
                    print("data['abr'][i]['cand'][j]['vs'][k]['nm'] - " + str(data['abr'][i]['cand'][j]['vs'][k]['nm'])  + " - Nome completo ")
                    print("data['abr'][i]['cand'][j]['vs'][k]['nmu'] - " + str(data['abr'][i]['cand'][j]['vs'][k]['nmu'])  + " - Nome de urna ")
                    print("data['abr'][i]['cand'][j]['vs'][k]['tp'] - " + str(data['abr'][i]['cand'][j]['vs'][k]['tp'])  + " - V ou S: Vice ou suplente ")
                    print("data['abr'][i]['cand'][j]['vs'][k]['sgp'] - " + str(data['abr'][i]['cand'][j]['vs'][k]['sgp'])  + " - sigla do partido ")


                    











            
        





                
if __name__ == '__main__':
    obj = Utils()
    # # # # DOCS
    # obj.docs_comum_config_ele_c()
    # obj.docs_ele_year_electionID_config_mun_stateId_cm_json()
    # obj.docs_ele_year_electionID_dados_br()
    
    # # # UTILS
    # obj.get_state_capital(acronym='df')
    # obj.get_all_states()
    # obj.build_resultado_de_eleitos('*', 'BR')

 