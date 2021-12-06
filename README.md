# competencias_cgpe

### Instalar o virtualenv

sudo apt install python3-venv
python3 -m venv myvenv
source myvenv/bin/activate

### Rodar o comando para instalar as dependências:

pip install requirements.py

### Rodar o comando para criar as tabelas no banco de dados:

python manage.py migrate

### Rodar o comando para popular o banco de dados a partir da planilha(Depois tem que atualizar a planilha):

python script_xlsx_to_db.py

### Para criar um superusuario(Posteriormente você poderá acessar pelo navegador e ver todas os registros que existem no bd de forma mais simples):

python manage.py createsuperuser

### Para rodar a aplicação:

python manage.py runserver

### Link de acesso:

http://localhost:8000/

### Link de acesso admin(Usar superusuario cadastrado):

http://localhost:8000/admin
