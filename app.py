import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Inicializa o cliente OpenAI
api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=api_key) if api_key else None

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "projeto": "Transparência Cidadã API",
        "status": "online"
    })

@app.route('/api/simplificar', methods=['POST'])
def simplificar():
    try:
        data = request.get_json()
        texto = data.get('texto', '')

        if not texto:
            return jsonify({'error': 'Nenhum texto fornecido'}), 400

        if not client:
            return jsonify({
                'resumo_cidadao': 'Erro: Chave OPENAI_API_KEY não configurada no Render.',
                'impacto_social': 'Configure a variável no painel do Render.',
                'recomendacao_fiscalizacao': 'Verifique as configurações.'
            }), 500

        prompt = f"""
        Você é um especialista em Transparência Pública.
        Analise o documento abaixo e extraia as informações essenciais de forma clara para um cidadão comum.

        DOCUMENTO:
        \"\"\"{texto}\"\"\"

        Responda ESTRITAMENTE um formato JSON válido com estas 3 chaves exatas:
        {{
            "resumo_cidadao": "Explique o que é este documento em linguagem simples, citando nomes de contratados/órgãos, valores exatos e datas do texto se houver.",
            "impacto_social": "Explique para que serve essa contratação/ação e o impacto dela na rotina da população.",
            "recomendacao_fiscalizacao": "Dê orientações práticas de como o cidadão pode fiscalizar se este contrato/processo está correto."
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        resultado = json.loads(response.choices[0].message.content)
        return jsonify(resultado)

    except Exception as e:
        return jsonify({
            'resumo_cidadao': f'Erro no processamento da IA: {str(e)}',
            'impacto_social': 'Tente novamente.',
            'recomendacao_fiscalizacao': 'Verifique se o texto enviado é válido.'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
