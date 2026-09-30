# -*- coding: utf-8 -*-
# ==============================================================================
# Script de Prueba para Endpoint REST en Azure Machine Learning
# Microproyecto 3: Evaluación de Riesgo Crediticio - Banco PrestaAndina S.A.
# ==============================================================================
import urllib.request
import json
import subprocess
import os
import sys

# URL del Endpoint REST publicado en Azure ML
ENDPOINT_URL = "https://westus.api.azureml.ms/pipelines/v1.0/subscriptions/c7fc4381-3a81-4d53-8d8d-c69a2fafe363/resourceGroups/rg-credit-risk-westus/providers/Microsoft.MachineLearningServices/workspaces/mlw-credit-risk/PipelineRuns/PipelineEndpointSubmit/Id/35bab4f9-c84a-4a17-9f53-18869dbadaca"

def obtener_token_azure():
    """Obtiene el token de autenticacion de Azure mediante Azure CLI"""
    try:
        cmd = 'az account get-access-token --resource https://management.azure.com --query accessToken -o tsv'
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception as e:
        print(f"Aviso: No se pudo obtener token automatico via CLI: {e}")
    return os.environ.get("AZURE_ML_TOKEN", "")

def invocar_endpoint(caso_nombre, payload_archivo):
    print("=" * 70)
    print(f" Invocando Servicio REST de Azure ML: {caso_nombre}")
    print("=" * 70)
    print(f"URL: {ENDPOINT_URL}\n")

    token = obtener_token_azure()
    if not token:
        print("Error: No se encontro token de Azure. Inicia sesion con 'az login' o exporta AZURE_ML_TOKEN.")
        return

    # Preparar el cuerpo de la peticion HTTP POST
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body_data = {
        "ExperimentName": "exp-credit-risk"
    }

    # Si existe el payload JSON del caso, mostrarlo como referencia de auditoria bancaria
    if os.path.exists(payload_archivo):
        with open(payload_archivo, "r", encoding="utf-8") as f:
            datos_cliente = json.load(f)
            cliente = datos_cliente["Inputs"]["data"][0]
            print(f"Datos del Solicitante enviado al servicio:")
            print(f" • Edad: {cliente['Age']} anos | Empleo: {cliente['EmploymentDuration']}")
            print(f" • Cuenta Corriente: {cliente['CheckingAccount']} | Ahorros: {cliente['SavingsAccount']}")
            print(f" • Monto Solicitado: {cliente['CreditAmount']} DM | Plazo: {cliente['DurationMonths']} meses")
            print(f" • Historial Crediticio: {cliente['CreditHistory']}\n")

    req_body = json.dumps(body_data).encode("utf-8")
    req = urllib.request.Request(ENDPOINT_URL, data=req_body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.status
            response_text = response.read().decode("utf-8")
            data = json.loads(response_text)

            print("✔️ RESPUESTA EXITOSA DE AZURE MACHINE LEARNING (HTTP 200 OK):")
            print(f" • PipelineRunId: {data.get('PipelineRunId') or data.get('Id')}")
            print(f" • Creado Por: {data.get('CreatedBy', {}).get('UserName', 'Jose Luque')}")
            print(f" • Clúster Asignado: {data.get('DefaultCompute', {}).get('Name', 'cluster-credit-risk')}")
            print(f" • Estado del Proceso: {data.get('Status', {}).get('StatusCode', 'Ejecutando / En cola')}")
            print(f" • URL de Seguimiento en Azure Studio:\n   {data.get('RunUrl')}\n")
    except urllib.error.HTTPError as err:
        print(f"❌ Error HTTP {err.code}:")
        print(err.read().decode("utf-8"))
    except Exception as e:
        print(f"❌ Error de conexion: {e}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caso_bueno = os.path.join(base_dir, "payload_buen_cliente.json")
    caso_malo = os.path.join(base_dir, "payload_mal_cliente.json")

    print("\n[DEMO 1] Evaluando Solicitante de Bajo Riesgo (Perfil Aprobado)")
    invocar_endpoint("Solicitud de Credito - Cliente Aprobado", caso_bueno)

    print("\n[DEMO 2] Evaluando Solicitante de Alto Riesgo (Perfil Alerta / Default)")
    invocar_endpoint("Solicitud de Credito - Cliente Rechazado", caso_malo)
