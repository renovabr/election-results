import json



class Utils():

    BASE_URL = 'files/'
    DEFAULT_URL_CONFIG = 'ele2022/{}/dados/'
    SIMPLIFICADOS_URL_CONFIG = 'ele2022/{}/dados-simplificados/'
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
        1: 'Presidente',
        3: 'Governador',
        5: 'Senador',
        11: 'Prefeito', 
        6: 'Deputado Federal',
        7: 'Deputado Estadual',
        8: 'Deputado Distrital',
        13: 'Vereador'
    }
    
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # FUNÇÕES UTILITÁRIAS # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def load_json(self, filename: str) -> json:
        try:
            file = open(filename)
            data = json.load(file)
        except:
            data = {}
        return data 

    def build_municipios(self) -> json:
        '''
            RETORNA UM OBJETO JSON COM OS MUNICIPIOS CARREGADOS
            
            EA12 – Arquivo de configuração de municípios
            e<número da eleição>: Número de controle identificador da eleição a que ser refere o arquivo. 
            Compostopor seis dígitos. É o um número fixo para todos os arquivos de uma mesma eleição
    
        '''
        url = self.BASE_URL + 'ele2022/' + str(self.DEFAULT_ELECTION_ID) + '/config/mun-e' + str(self.DEFAULT_ELECTION_ID).zfill(6) + '-cm.json'
        mun = self.load_json(filename=url)
        return mun 

    def build_resultado_de_eleitos(self, cd_cargo, abr: str) -> list:
        '''
            <br|uf>-c<código do cargo>-e<número da eleição>-e.json

            EA10 – Arquivo de resultado de eleitos
            Documentação disponível em: 
            https://www.tse.jus.br/++theme++justica_eleitoral/pdfjs/web/viewer.html?file=https://www.tse.jus.br/eleicoes/eleicoes-2022/arquivos/interessados/ea10-arquivo-de-resultado-de-eleitos/@@download/file/TSE-EA10-Arquivo-de-resultado-de-eleitos.pdf
        

            RETORNA UMA LISTA COM OBJETOS JSON COM O ARQUIVO DOS ELEITOS PRO CARGO DE ACORDO COM O CODIGO DO CARGO
            
            cd_cargo: num inteiro com o codigo do cargo a ser retornado ou então um asterisco '*'
            para retornar de todos os cargos
            
            abr: SIGLA da abrangência. 'BR' para brasil
            CADA ITEM DA LISTA CONTÉM TODOS OS ELEITOS E DADOS DE VICE/SUPLENTE P AQUELE ->CARGO<-
        '''
        data = []

        abr = abr.lower() 

        if cd_cargo != '*':
            url = self.BASE_URL + self.DEFAULT_URL_CONFIG.format(self.DEFAULT_ELECTION_ID) + abr + '/' + abr + '-c' + str(cd_cargo).zfill(4) + '-e' + str(self.DEFAULT_ELECTION_ID).zfill(6) +  '-e.json'
            obj = self.load_json(url)
            if len(obj) is not 0:
                data.append(obj)
            
        else: 
            for item in self.CD_CARGOS:
                url = self.BASE_URL + self.DEFAULT_URL_CONFIG.format(self.DEFAULT_ELECTION_ID) + abr + '/' + abr + '-c' + str(item).zfill(4) + '-e' + str(self.DEFAULT_ELECTION_ID).zfill(6) + '-e.json'
                obj = self.load_json(url)
                if len(obj) is not 0:
                    data.append(obj)
            
        return data 

    def build_totalizacao(self, abr: str) -> list:
        '''
            Constrói o arquivo 
            EA15 – Arquivo de acompanhamento UF
            Documentação completa disponível em https://www.tse.jus.br/++theme++justica_eleitoral/pdfjs/web/viewer.html?file=https://www.tse.jus.br/eleicoes/eleicoes-2022/arquivos/interessados/ea15-arquivo-de-acompanhamento-uf-1653934878111/@@download/file/TSE-EA15-Arquivo-de-acompanhamento-UF.pdf
        '''
        
        abr = abr.lower() 
        url = self.BASE_URL + self.DEFAULT_URL_CONFIG.format(self.DEFAULT_ELECTION_ID) + str(abr) + '/' + str(abr) + '-e' + str(self.DEFAULT_ELECTION_ID).zfill(6) + '-ab.json'
        data = self.load_json(url)
        return data 

    def build_dados_simplificados(self, abr: str, cd_cargo) -> list:
        '''
            EA04 – Arquivo de resultado consolidado
            Documentação completa disponível em:
            https://www.tse.jus.br/++theme++justica_eleitoral/pdfjs/web/viewer.html?file=https://www.tse.jus.br/eleicoes/eleicoes-2022/arquivos/interessados/ea04-arquivo-de-resultado-consolidado/@@download/file/TSE-EA04-Arquivo-de-resultado-consolidado.pdf
        '''
        datalist = []
        abr = abr.lower()
        if cd_cargo != '*':
            if abr == 'br':
                states = self.get_all_states()
                for st in states:
                    abr = st.get('cd').lower()
                    path = self.BASE_URL + self.SIMPLIFICADOS_URL_CONFIG.format(str(self.DEFAULT_ELECTION_ID)) + str(abr) + '/' + str(abr) + '-c' + str(cd_cargo).zfill(4) + '-e' + str(self.DEFAULT_ELECTION_ID).zfill(6) + '-r.json'
                    data = self.load_json(path)
                    if len(data) is not 0:
                        datalist.append(data)
            else:
                path = self.BASE_URL + self.SIMPLIFICADOS_URL_CONFIG.format(str(self.DEFAULT_ELECTION_ID)) + str(abr) + '/' + str(abr) + '-c' + str(cd_cargo).zfill(4) + '-e' + str(self.DEFAULT_ELECTION_ID).zfill(6) + '-r.json'
                data = self.load_json(path)
                if len(data) is not 0:
                    datalist.append(data)
        else:
            for cargo in self.CD_CARGOS:
                if abr.lower() == 'br':
                    states = self.get_all_states()
                    for st in states:
                        br_abr = st.get('cd').lower()
                        path = self.BASE_URL + self.SIMPLIFICADOS_URL_CONFIG.format(str(self.DEFAULT_ELECTION_ID)) + str(br_abr) + '/' + str(br_abr) + '-c' + str(cargo).zfill(4) + '-e' + str(self.DEFAULT_ELECTION_ID).zfill(6) + '-r.json'
                        data = self.load_json(path)
                        if len(data) is not 0:
                            data['cargo'] = self.CD_CARGOS[int(cargo)]
                            datalist.append(data)
                else:
                    path = self.BASE_URL + self.SIMPLIFICADOS_URL_CONFIG.format(str(self.DEFAULT_ELECTION_ID)) + str(abr) + '/' + str(abr) + '-c' + str(cargo).zfill(4) + '-e' + str(self.DEFAULT_ELECTION_ID).zfill(6) + '-r.json'
                    data = self.load_json(path)
                    if len(data) is not 0:
                        datalist.append(data)
        return datalist

    def get_all_states(self) -> dict:
        '''
            Retorna uma lista contendo informaçõeschaves sobre o estado

            <INT>, {'cd' : '<STR>', 'nome' : '<STR>', 'capital_nome': <STR>, 'capital_cd': <INT>, 'count_mun': <INT>,}

        '''
        states = [] 
        mun = self.build_municipios()
        for i in range(0, len(mun['abr'])):
            state = {} 
            state['cd'] = mun['abr'][i]['cd']
            state['ds'] = mun['abr'][i]['ds']
            capital_data = self.get_state_capital(sigla=state['cd'])
            state['capital_nome'] = capital_data['nome']
            state['capital_cd'] = capital_data['cd']
            states.append(state)

        return states

    def get_state_capital(self, sigla: str) -> dict:
        '''
            RETORNA o nome e o código do municipio no formato 
            {'cd' : '<INT>', 'nome' : '<STR>'}
            RECEBE o atributo state, uma string de 2 digitos com a sigla do estado

        '''
        # build URL 
        capital = {}
        mun = self.build_municipios()

        # FIND sigla:
        for i in range(0, len(mun['abr'])):
           if mun['abr'][i]['cd'] == sigla.upper():
                for j in range(0, len(mun['abr'][i]['mu'])):
                    if mun['abr'][i]['mu'][j]['c'] == 'S':
                        capital['cd'] = mun['abr'][i]['mu'][j]['cdi']
                        capital['nome'] = mun['abr'][i]['mu'][j]['nm']

        return capital

    def get_todos_eleitos(self, vices = False) -> list:
        '''
            Retorna uma lista com informações críticas e facilitadas sobre todos os eleitos, em todos os cargos do brasil
            TODO: fazer a vice = True
        '''
        data = self.build_resultado_de_eleitos(cd_cargo='*', abr='br')
        todos_eleitos = [] 
        if not vices:
            for item in data:
                eleito = {} 
                eleito['cargo'] = item.get('nmcar')
                for abr in item.get("abr"):
                    eleito['estado'] = abr.get('cdabr')
                    eleito['total_votos_estado'] = abr.get('tvap')
                    for cand in abr.get("cand"):
                        eleito['nome'] = cand.get('nm')
                        eleito['sqcand'] = cand.get('sqcand')
                        eleito['partido'] = cand.get("sgp")
                        eleito['votos'] = cand.get('vap')
                        eleito['numero_urna'] = cand.get('n')
                        eleito['nome_de_urna'] = cand.get('nmu')
                        todos_eleitos.append(eleito)      
        return todos_eleitos

    def check_eleito(self, sqcand: int) -> bool:
        todos_eleitos = self.get_todos_eleitos() 
        for eleito in todos_eleitos:
            if eleito.get('sqcand') == sqcand:
                return True
        return False 

    def get_infos_totalizacao(self, sigla: str) -> list: 
        '''
            Retorna informações facilitadas sobre a totaliazação de uma abrancência
            recebe 'br' como sigla se for retornar informações sobre todo o brasil 
            ou então recebe a sigla do estado alvo
        ''' 
        data = self.build_totalizacao(abr='br')
        lista = [] 
        
        for abr in data.get('abr'):
            infos = {} 
            infos['estado'] = abr.get('cdabr')
            infos['dg'] = data.get('dg')
            infos['hg'] = data.get('hg')
            if abr.get('and') == 'N':
                infos['andamento'] = '#'
            elif abr.get('and') == 'P':
                infos['andamento'] = 'Iniciada'
            elif abr.get('and') == 'F':
                infos['andamento'] = 'Finalizada'
            infos['percentual_seções_totalizadas'] = abr.get("pst")
            infos['percentual_comparecimento'] = abr.get('pc')
            infos['percentual_abstenções'] = abr.get('pa')
            if sigla != 'br':
                if infos['estado'] == sigla.upper():
                    lista.append(infos)
            else:
                lista.append(infos)
        return lista

    def get_situacao_candidato(self, sqcand: int) -> dict: 
        '''
            Retorna um dicionário contendo informações compiladas com nome, votos partido e resultado do candidato, bem como percentuais
            de votação naquele estado.
        '''
        data = self.build_dados_simplificados(abr='br', cd_cargo='*')
        for dataset in data:
            infos = {}
            infos['estado'] = dataset.get('cdabr')
            infos['cargo'] = dataset.get('cargo')
            infos['status_totalização'] = self.get_infos_totalizacao(sigla=infos['estado'])[0].get('andamento')
            infos['num_vagas_disputadas'] = dataset.get('v')
            infos['percentual_secoes_totalizadas'] = dataset.get("pst")
            infos['percentual_comparecimento'] = dataset.get("pc")
            infos['percentual_abstencias'] = dataset.get("pa")
            infos['percentual_votos_brancos'] = dataset.get("pvb")
            infos['percentual_votos_nulos'] = dataset.get("pvn")
            infos['percentual_votos_anulados'] = dataset.get("pvan")
            for cand in dataset.get('cand'):
                infos['numero'] = cand.get('n')
                infos['sqcand'] = cand.get('sqcand')
                infos['nome_de_urna'] = cand.get('nm')
                infos['destinação_de_votos'] = cand.get('dvt')
                infos['resultado'] = cand.get('st')
                infos['votos_computados'] = cand.get('vap')
                infos['percentual_votos'] = cand.get("pvap")
                infos['eleito'] = cand.get('e')

                if cand.get('sqcand') == sqcand:
                    return infos

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
    # obj.get_state_capital(sigla='df')
    # print(obj.get_all_states())
    # obj.build_resultado_de_eleitos('*', 'BR')
    # obj.get_todos_eleitos()
    # obj.build_totalizacao(abr='df')
    # obj.get_infos_totalizacao(sigla='br')
    # print(obj.build_dados_simplificados(abr='df', cd_cargo='*'))
    # print(obj.get_situacao_candidato(sqcand=70007787505))

    
    # a = obj.check_eleito(sqcand=70007787505)
    # print(a)

 