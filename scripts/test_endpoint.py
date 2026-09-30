# ==============================================================================
# Script de Prueba para Endpoint de Inferencia en Tiempo Real (Azure ML)
# Microproyecto 3: Evaluación de Riesgo Crediticio con Azure Machine Learning
# ==============================================================================
import urllib.request
import json
import os
import sys

# INSTRUCCIONES:
# 1. En Azure ML Studio (ml.azure.com), ve a 'Endpoints' > Selecciona tu endpoint.
# 2. Ve a la pestaña 'Consume'.
# 3. Copia el 'REST endpoint' y pegalo en ENDPOINT_URL.
# 4. Copia la 'Primary key' y pegala en API_KEY.

ENDPOINT_URL = os.environ.get('AZURE_ML_ENDPOINT_URL', 'https://<TU-ENDPOINT>.<REGION>.inference.ml.azure.com/score')
API_KEY = os.environ.get('AZURE_ML_API_KEY', '<TU-API-KEY>')

def consultar_modelo(nombre_caso, ruta_json):
    print(f'\n============================================================')
    print(f' Enviando solicitud de inferencia: {nombre_caso}')
    print(f'============================================================')
    
    if not os.path.exists(ruta_json):
        print(f'Error: No se encuentra el archivo {ruta_json}')
        return

    with open(ruta_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    body = str.encode(json.dumps(data))
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
        'azureml-model-deployment': 'default'
    }

    req = urllib.request.Request(ENDPOINT_URL, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        parsed = json.loads(result)
        print('Respuesta exitosa de Azure ML:')
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except urllib.error.HTTPError as error:
        print(f'La solicitud fallo con codigo de estado: {error.code}')
        print(error.read().decode('utf8', 'ignore'))
    except Exception as e:
        print(f'Error de conexion: {e}')

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    buen_cliente = os.path.join(script_dir, 'payload_buen_cliente.json')
    mal_cliente = os.path.join(script_dir, 'payload_mal_cliente.json')

    print('Probando cliente de bajo riesgo (Buen pagador)...')
    consultar_modelo('Perfil de Bajo Riesgo (Aprobado)', buen_cliente)

    print('\nProbando cliente de alto riesgo (Default)...')
    consultar_modelo('Perfil de Alto Riesgo (Rechazado)', mal_cliente)
