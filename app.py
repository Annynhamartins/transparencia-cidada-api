import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Inicializa o cliente Groq
api_key = os.environ.get('GROQ_API_KEY')
client = Groq(api_key=api_key) if api_key else None

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
                'resumo_cidadao': 'Erro: Chave GROQ_API_KEY não configurada no Render.',
                'impacto_social': 'Configure a variável no painel do Render.',
                'recomendacao_fiscalizacao': 'Verifique as configurações.'
            }), 500

        prompt = f"""
        Você é um especialista em Transparência Pública.
        Analise o documento público abaixo e extraia as informações essenciais de forma clara para um cidadão comum.

        DOCUMENTO:
        \"\"\"{texto}\"\"\"

        Responda ESTRITAMENTE em formato JSON válido (sem textos antes ou depois) usando exatamente estas 3 chaves:
        {{
            "resumo_cidadao": "Explique o que é este documento em linguagem simples, citando nomes de pessoas/órgãos, cargos, valores e datas encontradas no texto.",
            "impacto_social": "Explique o objetivo dessa medida e como ela afeta a população ou o serviço público.",
            "recomendacao_fiscalizacao": "Dê dicas práticas e específicas de como o cidadão pode acompanhar ou fiscalizar essa publicação."
        }}
        """

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )

        resultado = json.loads(response.choices[0].message.content)
        return jsonify(resultado)

    except Exception as e:
        return jsonify({
            'resumo_cidadao': f'Erro no processamento da IA: {str(e)}',
            'impacto_social': 'Tente novamente em instantes.',
            'recomendacao_fiscalizacao': 'Verifique se o texto enviado é um documento válido.'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
