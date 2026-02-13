from flask import Flask, render_template, redirect, request, flash, send_file
import requests
from io import BytesIO
import re

ENDPOINT_API = "https://api.thecatapi.com/v1/images/search"

app = Flask(__name__)
app.secret_key = "gato"


def nome_seguro(nome):
    # remove caracteres estranhos do nome para virar nome de arquivo
    nome = nome.strip().lower()
    nome = re.sub(r'[^a-z0-9_-]', '_', nome)
    return nome or "meu_gato"


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/cat', methods=['GET', 'POST'])
def cat():
    if request.method == 'GET':
        return redirect('/')

    nome = request.form.get('nome', None)

    if not nome:
        flash("Informe seu nome ow!")
        return redirect('/')

    resposta = requests.get(ENDPOINT_API)

    if resposta.status_code == 200:
        dados = resposta.json()
        url_imagem = dados[0]['url']
    else:
        flash("Os gatos estão a roncar alto! Volte miaus tarde!")
        return redirect('/')

    return render_template('index.html', nome=nome, url_imagem=url_imagem)


@app.route('/download')
def download():
    url = request.args.get("url")
    nome = request.args.get("nome")

    if not url or not nome:
        flash("Não foi possível baixar o gatinho 😿")
        return redirect('/')

    resp = requests.get(url)
    if resp.status_code != 200:
        flash("Erro ao baixar a imagem do gato 😿")
        return redirect('/')

    nome_arquivo = nome_seguro(nome) + ".jpg"

    return send_file(
        BytesIO(resp.content),
        mimetype="image/jpeg",
        as_attachment=True,
        download_name=nome_arquivo
    )


if __name__ == '__main__':
    app.run(debug=True)
