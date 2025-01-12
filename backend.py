import sqlite3 as sql

# Classe para gerenciar transações com o banco de dados SQLite
class TransactionObject:
    # Atributos estáticos para a conexão ao banco de dados
    database = "clientes.db"  # Nome do banco de dados SQLite
    conn = None               # Armazena a conexão com o banco
    cursor = None             # Armazena o cursor para executar comandos SQL
    connected = False         # Indica se a conexão com o banco está ativa ou não
    
    # Função para conectar ao banco de dados
    def connect(self):
        """
        Estabelece a conexão com o banco de dados 'clientes.db',
        inicializando 'conn' e 'cursor', e define 'connected' como True.
        """
        TransactionObject.conn = sql.connect(TransactionObject.database)
        TransactionObject.cursor = TransactionObject.conn.cursor()
        TransactionObject.connected = True

    # Função para desconectar do banco de dados
    def disconnect(self):
        """
        Fecha a conexão com o banco de dados e define 'connected' como False.
        """
        TransactionObject.conn.close()
        TransactionObject.connected = False

    # Função para executar comandos SQL no banco
    def execute(self, sql, parms=None):
        """
        Executa um comando SQL no banco de dados.
        Parâmetros:
        - sql: string com o comando SQL a ser executado.
        - parms: parâmetros opcionais para comandos SQL parametrizados.
        
        Retorna:
        - True se a execução foi bem-sucedida.
        - False se a conexão com o banco não estiver ativa.
        """
        if TransactionObject.connected:  # Verifica se há uma conexão ativa
            if parms is None:            # Se não há parâmetros, executa o SQL direto
                TransactionObject.cursor.execute(sql)
            else:                        # Executa o SQL com parâmetros
                TransactionObject.cursor.execute(sql, parms)
            return True
        else:
            return False
        
    # Função para buscar todos os resultados de um comando SQL
    def fetchall(self):
        """
        Retorna todos os resultados da última consulta SQL executada.
        Utiliza o cursor do banco de dados.
        """
        return TransactionObject.cursor.fetchall()
    
    # Função para salvar alterações no banco
    def persist(self):
        """
        Confirma (commit) as alterações realizadas no banco de dados.
        Retorna:
        - True se a conexão está ativa e o commit foi realizado.
        - False se não há conexão ativa.
        """
        if TransactionObject.connected:
            TransactionObject.conn.commit()
            return True
        else:
            return False

# Função para inicializar o banco de dados
def initDB():
    """
    Inicializa o banco de dados criando uma tabela chamada 'clientes', caso ela ainda não exista.
    Essa tabela possui as colunas:
    - id: Identificador único (PRIMARY KEY) do tipo INTEGER.
    - nome: Nome do cliente (TEXT).
    - sobrenome: Sobrenome do cliente (TEXT).
    - email: E-mail do cliente (TEXT).
    - cpf: CPF do cliente (TEXT).
    
    Após criar a tabela, a conexão é fechada.
    """
    trans = TransactionObject()  # Cria uma instância da classe
    trans.connect()              # Estabelece conexão com o banco

    trans.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY, nome TEXT, sobrenome TEXT, email TEXT, CPF text)")
    trans.persist()
    trans.disconnect()

def insert(nome, sobrenome, email, cpf):
    """
    Insere um novo cliente na tabela 'clientes'.
    Parâmetros:
    - nome: Nome do cliente.
    - sobrenome: Sobrenome do cliente.
    - email: E-mail do cliente.
    - cpf: CPF do cliente.
    
    O ID é gerado automaticamente (NULL).
    A conexão é aberta antes da execução e fechada após a inserção.
    """
    trans = TransactionObject()
    trans.connect()
    trans.execute("INSERT INTO clientes VALUES(NULL, ?,?,?,?)",(nome, sobrenome,email,cpf))
    trans.persist()
    trans.disconnect()

def view():
    """
    Retorna todos os registros da tabela 'clientes'.
    A conexão com o banco de dados é aberta para executar o comando
    'SELECT * FROM clientes' e fechada após a execução.
    
    Retorna:
    - Uma lista de tuplas contendo todos os registros da tabela.
    """
    trans = TransactionObject()
    trans.connect()
    trans.execute("SELECT * FROM clientes")
    rows = trans.fetchall()
    trans.disconnect()
    return rows

def search(nome="",sobrenome="",email="",cpf=""):
    """
    Pesquisa clientes na tabela 'clientes' com base nos critérios fornecidos.
    Qualquer parâmetro pode ser deixado vazio, sendo considerado como um critério opcional.
    Parâmetros:
    - nome: Nome do cliente (opcional).
    - sobrenome: Sobrenome do cliente (opcional).
    - email: E-mail do cliente (opcional).
    - cpf: CPF do cliente (opcional).
    
    Retorna:
    - Uma lista de tuplas com os registros que atendem aos critérios de pesquisa.
    """
    trans = TransactionObject()
    trans.connect()
    trans.execute("SELECT * FROM clientes WHERE nome=? or sobrenome=? or email=? or cpf=?", (nome,sobrenome,email,cpf))
    rows = trans.fetchall()
    trans.disconnect()
    return rows

def delete(id):
    """
    Exclui um registro da tabela 'clientes' com base no ID.
    Parâmetros:
    - id: Identificador único do cliente a ser excluído.
    
    A conexão é aberta antes da execução do comando 'DELETE' e fechada após a persistência.
    """
    trans = TransactionObject()
    trans.connect()
    trans.execute("DELETE FROM clientes WHERE id = ?", (id,))
    trans.persist()
    trans.disconnect()

def update(id, nome,sobrenome,email,cpf):
    """
    Atualiza os dados de um cliente na tabela 'clientes' com base no ID.
    Parâmetros:
    - id: Identificador único do cliente a ser atualizado.
    - nome: Novo nome do cliente.
    - sobrenome: Novo sobrenome do cliente.
    - email: Novo e-mail do cliente.
    - cpf: Novo CPF do cliente.
    
    A conexão é aberta antes da execução do comando 'UPDATE' e fechada após a persistência.
    """
    trans = TransactionObject()
    trans.connect()
    trans.execute("UPDATE clientes set nome =?, sobrenome =?, email =?, cpf=? WHERE id = ?", (nome,sobrenome,email,cpf,id))
    trans.persist()
    trans.disconnect()

initDB()


