from interface import *
import backend as core

app = None

# Função para exibir todos os registros no Listbox da interface
def view_command():
    """
    Obtém todos os registros do banco de dados e exibe no Listbox da interface.
    Usa a função 'view()' do backend para buscar os dados.
    """
    rows = core.view()  # Recupera os registros do banco
    app.listClientes.delete(0, END)  # Limpa os itens atuais do Listbox
    for r in rows:  # Itera sobre os registros e os adiciona ao Listbox
        app.listClientes.insert(END, r)

# Função para buscar registros no banco com base nos dados inseridos nos campos de entrada
def search_command():
    """
    Busca registros no banco de dados com base nos critérios informados.
    Atualiza o Listbox com os resultados da busca.
    """
    app.listClientes.delete(0, END)  # Limpa o Listbox
    # Busca no banco usando os valores dos campos de entrada da interface
    rows = core.search(app.txtNome.get(), app.txtSobrenome.get(), app.txtEmail.get(), app.txtCPF.get())
    for r in rows:  # Exibe os resultados no Listbox
        app.listClientes.insert(END, r)

# Função para inserir novos registros no banco
def insert_command():
    """
    Insere um novo registro no banco de dados com os dados fornecidos.
    Após a inserção, atualiza o Listbox para exibir os novos dados.
    """
    core.insert(app.txtNome.get(), app.txtSobrenome.get(), app.txtEmail.get(), app.txtCPF.get())
    view_command()  # Atualiza o Listbox com todos os registros

# Função para atualizar um registro existente no banco
def update_command():
    """
    Atualiza o registro selecionado no banco com os novos dados inseridos nos campos.
    Após a atualização, atualiza o Listbox.
    """
    core.update(selected[0], app.txtNome.get(), app.txtSobrenome.get(), app.txtEmail.get(), app.txtCPF.get())
    view_command()  # Atualiza o Listbox com todos os registros

# Função para excluir um registro selecionado
def del_command():
    """
    Exclui o registro selecionado no Listbox.
    Após a exclusão, atualiza o Listbox.
    """
    id = selected[0]  # Obtém o ID do registro selecionado
    core.delete(id)  # Remove o registro do banco
    view_command()  # Atualiza o Listbox com todos os registros

# Função que lida com a seleção de um registro no Listbox
def getSelectedRow(event):
    """
    Obtém os dados do registro selecionado no Listbox e os exibe nos campos de entrada.
    Também armazena o registro selecionado em uma variável global.
    """
    global selected  # Declara a variável como global para armazenar o registro selecionado
    index = app.listClientes.curselection()[0]  # Obtém o índice do item selecionado no Listbox
    selected = app.listClientes.get(index)  # Recupera os dados do registro selecionado
    # Atualiza os campos de entrada com os dados do registro selecionado
    app.entNome.delete(0, END)
    app.entNome.insert(END, selected[1])  # Nome
    app.entSobrenome.delete(0, END)
    app.entSobrenome.insert(END, selected[2])  # Sobrenome
    app.entEmail.delete(0, END)
    app.entEmail.insert(END, selected[3])  # Email
    app.entCPF.delete(0, END)
    app.entCPF.insert(END, selected[4])  # CPF
    return selected  # Retorna o registro selecionado

# Código principal para inicializar a interface e vincular os eventos
if __name__ == "__main__":
    app = Gui()  # Cria a interface gráfica
    app.listClientes.bind('<<ListboxSelect>>', getSelectedRow)  # Vincula a seleção do Listbox à função getSelectedRow

    # Configura os botões da interface com as funções correspondentes
    app.btnViewAll.configure(command=view_command)
    app.btnBuscar.configure(command=search_command)
    app.btnInserir.configure(command=insert_command)
    app.btnUpdate.configure(command=update_command)
    app.btnDel.configure(command=del_command)
    app.btnClose.configure(command=app.window.destroy)  # Fecha a aplicação ao clicar no botão "Fechar"

    app.run()  # Inicia o loop principal da interface gráfica