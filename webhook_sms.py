from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import urllib.parse
from waitress import serve

app = Flask(__name__)
CORS(app)

@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.json

    try:
        # Dados recebidos
        cpf = dados.get("cpf", "Não informado")
        nome = dados.get("nome", "Não informado")
        telefone = dados.get("telefone", "Não informado")
        parceiro = dados.get("parceiro", "Não informado")

        # Mensagem formatada
        mensagem = f"""📋 *Solicitação de Cashback*

- CPF: {cpf}
- Nome: {nome}
- Telefone: {telefone}
- Parceiro: {parceiro}
"""

        # URL encode da mensagem
        mensagem_encoded = urllib.parse.quote(mensagem)

        # Configuração da API CallMeBot
        phone = "5511917112598"  # Número configurado na API
        apikey = "2998637"       # Sua chave API

        api_url = (
            f"https://api.callmebot.com/whatsapp.php?"
            f"phone={phone}&apikey={apikey}"
            f"&text={mensagem_encoded}"
        )

        # Fazendo o envio
        response = requests.get(api_url)

        return jsonify({
            "status": response.status_code,
            "response": response.text,
            "mensagem_enviada": mensagem
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
