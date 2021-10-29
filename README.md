# Pyjudi TJPR
Um helper para efetuar login no sistema do projudi do paraná (projudi.tjpr.jus.br) utilizando autenticação de dois fatores com um usuários do tipo "Advogados e partes" que possuem acesso com CPF/CNPJ.


### Install
```bash
pip3 install pyjudi-tjpr
```

### Example
```python
from pyjudi_tjpr import Authenticator

projudi_auth = Authenticator(
    # Nome de usuário do projudi (cpf)
    username='1234567891',
    # Senha de acesso
    password='demo1234',
    # Token secreto do Google autenticator para geração do token baseado em tempo
    twofactor_secret='ABCDE1FGHIJKLMNOPQ2RS3TUVXWYZA4B'
)

# Retorna uma sessão autenticada no projudi
session = projudi_auth.get_logged_session()

# Retorna um dicionário com os cookies da sessão
cookies = projudi_auth.get_session_cookies(session)
```

### License
[MIT License](LICENSE)


