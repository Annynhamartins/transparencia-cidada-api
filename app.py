import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(_name_)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "projeto": "Transparência Cidadã API"
    })

@app.route('/api/simplificar', methods=['POST', 'OPTIONS'])
def simplificar():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    data = request.get_json() or {}
    return jsonify({
        "resumo_cidadao": "Este documento trata de aquisição/contratação pública referente ao texto inserido. Os termos principais indicam a destinação de recursos para atender às demandas administrativas da gestão.",
        "impacto_social": "Garante a continuidade dos serviços prestados à população e a correta aplicação das verbas destinadas a esta categoria.",
        "recomendacao_fiscalizacao": "Verifique o número do processo, as datas de publicação no Diário Oficial e se o valor total está de acordo com o orçamento previsto."
    })

if _name_ == '_main_':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
