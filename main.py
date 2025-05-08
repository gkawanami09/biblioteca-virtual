from flask import Flask, render_template, request, redirect, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'biblioteca_virtual'

livros = []

@app.route('/')
def index():
    return render_template('index.html', livros=livros)

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html', livros=livros)

@app.route('/emprestimos')
def emprestimos():
    emprestados = []
    for livro in livros:
        if livro['emprestado']:
            emprestados.append(livro)
    return render_template('emprestimos.html', livros=emprestados)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            autor = request.form['autor']
            ano = int(request.form['ano'])
            if ano < 0 or ano > 2025:
                raise ValueError('Ano inválido. Informe um ano entre 0 e 2025.')
            codigo = len(livros)
            novo_livro = {
                'codigo': codigo,
                'titulo': titulo,
                'autor': autor,
                'ano': ano,
                'emprestado': False,
                'data_emprestimo': None,
                'data_devolucao': None
            }
            livros.append(novo_livro)
            flash('Livro "{}" adicionado com sucesso!'.format(titulo))
            return redirect('/')
        except Exception as e:
            return render_template('erro.html', mensagem='Erro ao adicionar livro: {}'.format(e))
    return render_template('form.html', titulo='Adicionar Livro', livro=None)

@app.route('/editar/<int:codigo>', methods=['GET', 'POST'])
def editar(codigo):
    try:
        livro = livros[codigo]
        if request.method == 'POST':
            livro['titulo'] = request.form['titulo']
            livro['autor'] = request.form['autor']
            ano = int(request.form['ano'])
            if ano < 0 or ano > 2025:
                raise ValueError('Ano inválido. Informe um ano entre 0 e 2025.')
            livro['ano'] = ano
            flash('Livro "{}" editado com sucesso!'.format(livro['titulo']))
            return redirect('/')
        return render_template('form.html', titulo='Editar Livro', livro=livro)
    except Exception as e:
        return render_template('erro.html', mensagem='Erro ao editar livro: {}'.format(e))

@app.route('/excluir/<int:codigo>')
def excluir(codigo):
    try:
        titulo = livros[codigo]['titulo']
        livros.pop(codigo)
        flash('Livro "{}" excluído com sucesso!'.format(titulo))
    except Exception as e:
        return render_template('erro.html', mensagem='Erro ao excluir livro: {}'.format(e))
    return redirect('/')

@app.route('/emprestar/<int:codigo>')
def emprestar(codigo):
    try:
        livro = livros[codigo]
        agora = datetime.now()
        livro['emprestado'] = True
        livro['data_emprestimo'] = agora
        livro['data_devolucao'] = agora + timedelta(days=7)
        data_str = livro['data_devolucao'].strftime('%d/%m/%Y')
        flash('Livro "{}" emprestado até {}.'.format(livro['titulo'], data_str))
    except Exception as e:
        return render_template('erro.html', mensagem='Erro ao emprestar livro: {}'.format(e))
    return redirect('/')

@app.route('/devolver/<int:codigo>')
def devolver(codigo):
    try:
        livro = livros[codigo]
        hoje = datetime(2025, 5, 1)
        atraso = (hoje - livro['data_devolucao']).days
        if atraso > 0:
            multa = 10 + (10 * 0.01 * atraso)
            flash('Livro devolvido com {} dias de atraso. Multa: R$ {:.2f}'.format(atraso, multa))
        else:
            flash('Livro "{}" devolvido sem atraso.'.format(livro['titulo']))
        livro['emprestado'] = False
        livro['data_emprestimo'] = None
        livro['data_devolucao'] = None
    except Exception as e:
        return render_template('erro.html', mensagem='Erro ao devolver livro: {}'.format(e))
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)