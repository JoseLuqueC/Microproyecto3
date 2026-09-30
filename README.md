# Microproyecto 3: Sistema de Evaluación de Riesgo Crediticio con Azure Machine Learning

Repositorio para el desarrollo y entrega del **Microproyecto 3** de la asignatura **Computación en la Nube**.

* **Docente:** Prof. Oscar H. Mondragón
* **Plataforma:** Microsoft Azure (Azure Machine Learning Studio & Designer)
* **Entidad / Caso de Estudio:** *Banco Digital PrestaAndina S.A.* - Clasificación de Riesgo de Crédito (*Credit Default*)

---

## 📁 Estructura del Repositorio

```
.
├── data/
│   └── german_credit_risk.csv          # Dataset tabular limpio (1,000 registros, 21 columnas legibles)
├── scripts/
│   ├── payload_buen_cliente.json       # JSON de prueba: Perfil de bajo riesgo (Aprobado)
│   ├── payload_mal_cliente.json        # JSON de prueba: Perfil de alto riesgo (Rechazado)
│   └── test_endpoint.py                # Cliente Python para probar el Endpoint REST de Azure ML
├── DOCUMENTO_FINAL_MICROPROYECTO3.md   # Informe técnico formal con los 4 criterios de evaluación
└── README.md
```

---

## 🚀 Guía de Réplica Rápida para los Integrantes del Equipo

Cada integrante puede clonar este repositorio y desplegar el proyecto en su cuenta de **Azure for Students** en menos de 15 minutos:

### 1. Clonar el Repositorio
```bash
git clone https://github.com/JoseLuqueC/Microproyecto3.git
cd Microproyecto3
```

### 2. Configurar en Azure Machine Learning Studio
1. Ingresar a [ml.azure.com](https://ml.azure.com).
2. **Cómputo:** En **Manage** > **Compute** > **Compute clusters**, crear un clúster llamado `cluster-credit-risk`:
   * Tamaño: `Standard_DS2_v2`
   * Nodos mínimos: **`0`** *(OBLIGATORIO para evitar cargos cuando esté inactivo)*
   * Nodos máximos: **`1`**
   * Segundos de inactividad antes de escalar a cero: **`120`**
3. **Datos:** En **Data** > **Data assets** > **Create**, subir `data/german_credit_risk.csv` como dataset **Tabular**.
4. **Pipeline en Designer:** Ir a **Designer** > Crear pipeline clásico conectando:
   * `german-credit-risk` -> `Select Columns in Dataset` -> `Clean Missing Data` -> `Split Data` (0.7 / 0.3).
   * Conectar la partición de entrenamiento a `Train Model` con `Two-Class Boosted Decision Tree`.
   * Conectar a `Score Model` y luego a `Evaluate Model`.
   * Asignar el clúster de cómputo y dar clic en **Submit**.
5. **Despliegue del Endpoint:**
   * Clic en **Create inference pipeline** > **Real-time inference pipeline** -> **Submit**.
   * Clic en **Deploy** -> Nombre: `endpoint-credit-risk` -> Cómputo: `Managed` (`Standard_DS2_v2`).

### 3. Probar el DEMO
Una vez desplegado el endpoint, se puede probar desde la pestaña **Test** de Azure ML Studio o ejecutando:
```bash
python scripts/test_endpoint.py
```
*(Configurar previamente las variables de entorno `AZURE_ML_ENDPOINT_URL` y `AZURE_ML_API_KEY` obtenidas en la pestaña **Consume** del endpoint).*

---

## 👥 Integrantes del Equipo
* **Julio Cesar Rosero Porras**
* **Karoll Dahian Ramirez Marulanda**
* **Jose Fernando Luque Cajiao** ([@JoseLuqueC](https://github.com/JoseLuqueC))
