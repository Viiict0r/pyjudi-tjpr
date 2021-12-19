from bs4 import BeautifulSoup
from requests.sessions import Session

import onetimepass as otp
import re
import requests


class Authenticator:
    def __init__(self, username: str, password: str, twofactor_secret: str) -> None:
        """Cria uma sessão logada no projudi-tjpr

        username : str
            Nome de usuário / cpf ou cnpj

        password : str
            Senha de acesso

        twofactor_secret : str
            Código secreto do Google Authenticator
            Ex: ABCDE1FGHIJKLMNOPQ2RS3TUVXWYZA4B
        """

        self.__username = username
        self.__password = password
        self.__secret_key = str(twofactor_secret).replace(' ', '')

        self.__base_url = 'https://projudi.tjpr.jus.br'
        self.__home_url = 'https://projudi.tjpr.jus.br/projudi/home.do'

        self.html_final = ''

    def get_logged_session(self) -> Session:
        """Retorna uma sessão válida no
        sistema do projudi
        """

        # Create new session
        crawler_session = requests.session()

        crawler_session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }

        # Open home page
        request_home = crawler_session.get(url=self.__home_url)

        # Get _tj token to make login
        request_home_html = BeautifulSoup(
            str(request_home.text), features='html.parser')

        access_elements = request_home_html.select('ul[class="acessos"]')[0]

        # Find auth url with _tj token
        path_tj = re.compile(
            '(\/projudi\/autenticacao.do?.*_tj=.*\w)').search(str(access_elements))

        if not path_tj:
            raise Exception('Não foi possível encontrar o path de login')

        path_tj = path_tj.group()

        # Go to login page
        request_login = crawler_session.get(url=f'{self.__base_url}{path_tj}')

        # Get form action url
        request_login_html = BeautifulSoup(
            str(request_login.text), features='html.parser')
        request_login_form = request_login_html.find(
            'form', {'id': 'kc-form-login'})

        session_url = request_login_form.get('action')

        # Make post form request
        session_response = crawler_session.post(
            url=session_url,
            data={
                'username': self.__username,
                'password': self.__password
            }
        )

        # Get 2fa form action url
        request_2fa_html = BeautifulSoup(
            str(session_response.text), features='html.parser')

        request_2fa_form = request_2fa_html.find(
            'form', {'id': 'kc-otp-login-form'})

        # Check if 2fa form exists
        if not request_2fa_form:
            raise Exception('Falha ao efetuar login')

        session_2fa_url = request_2fa_form.get('action')

        # Generate authenticator 6 digit code
        secret_code = otp.get_totp(self.__secret_key)

        # Make twofactor login
        final_response = crawler_session.post(
            url=session_2fa_url,
            data={'otp': str(secret_code)}
        )

        # Check if is logged
        final_response_html = BeautifulSoup(
            str(final_response.text), features='html.parser')

        self.html_final = final_response.text

        if not final_response_html.find('iframe', attrs={'name': 'userMainFrame'}):
            raise Exception('Falha ao realizar login 2fa',
                            ' response: ', final_response_html)

        return crawler_session

    def get_session_cookies(self, session: Session) -> dict:
        cookie_dict = {}

        for cookie in session.cookies:
            cookie_dict[cookie.name] = cookie.value

        return cookie_dict

    def get_link_consulta_processo(self):
        if self.html_final:
            links = re.findall(
                "\/processo\/buscaProcessosQualquerInstancia.do\?_tj=[a-z0-9A-Z]*",
                self.html_final)
            return "https://projudi.tjpr.jus.br/projudi" + links[0]
        else:
            raise Exception("Fazer login no projudi")

    def get_link_assessores(self):
        if self.html_final:
            links = re.findall(
                "\/projudi\/usuario\/advogado.do\?_tj=[a-z0-9]+",
                self.html_final)
            return "https://projudi.tjpr.jus.br" + links[0]
        else:
            raise Exception("Fazer login no projudi")
