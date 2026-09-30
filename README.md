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

### 2. Configurar en Azure Machine Learning Studio (Interfaz en Español)

#### Paso 0: Crear la primera "Área de trabajo" (Workspace)
Si al ingresar a [ml.azure.com](https://ml.azure.com) ves la pantalla de bienvenida solicitando crear una nueva área de trabajo:
1. **Nombre:** `mlw-prestaandina` (o `mlw-credit-risk`)
2. **Nombre descriptivo:** `Riesgo Crediticio PrestaAndina`
3. **Configuración avanzada:**
   * **Suscripción:** `Azure for Students`
   * **Grupo de recursos:** `rg-credit-risk-ia` (puedes hacer clic en *Crear nuevo*)
   * **Región:** `East US 2` (o `East US`)
4. Hacer clic en **Crear** (tarda ~1 a 2 minutos). Al terminar, entrarás al área de trabajo y se desbloqueará el menú completo de la izquierda (**Creación**, **Recursos** y **Administrar**).

#### Paso 1: Configurar el Cómputo Económico
En el menú lateral izquierdo:
1. Ir a **Administrar** > **Cómputo** (o *Compute*) > pestaña **Clústeres de proceso** (o *Compute clusters*).
2. Hacer clic en **Nuevo** (o *+ Crear*):
   * **Nombre del proceso:** `cluster-credit-risk`
   * **Tamaño de máquina virtual:** `Standard_DS2_v2` (o `Standard_DS11_v2`, 2 núcleos)
   * **Número mínimo de nodos:** **`0`** *(OBLIGATORIO: para que cueste $0 cuando esté inactivo)*
   * **Número máximo de nodos:** **`1`**
   * **Segundos de inactividad antes de reducir verticalmente:** **`120`**
3. Clic en **Crear**.

#### Paso 2: Cargar el Dataset (Datos)
1. En el menú lateral izquierdo, ir a **Recursos** > **Datos** (o *Data*).
2. Pestaña **Recursos de datos** > clic en **+ Crear**:
   * **Nombre:** `german-credit-risk`
   * **Tipo:** **Tabular**
   * **Origen:** *De archivos locales* > Subir `data/german_credit_risk.csv`.
   * Verificar que la columna `CreditRisk` tenga valores `Good` y `Bad`.

#### Paso 3: Construcción del Pipeline en el Diseñador (Designer)
1. En el menú izquierdo, ir a **Creación** > **Diseñador** (o *Designer*).
2. Seleccionar **Crear una nueva canalización con componentes clásicos compilados previamente**.
3. Arrastrar y conectar los módulos:
   * `german-credit-risk` -> `Select Columns in Dataset` -> `Clean Missing Data` -> `Split Data` (0.7 / 0.3).
   * Conectar la partición 1 (70%) a `Train Model` junto con `Two-Class Boosted Decision Tree`.
   * Conectar `Train Model` a `Score Model` junto con la partición 2 (30%).
   * Conectar `Score Model` a `Evaluate Model`.
4. En la configuración de la canalización, asignar como destino de cómputo `cluster-credit-risk` y hacer clic en **Enviar** (*Submit*).

#### Paso 4: Despliegue del Punto de Conexión (Endpoint)
1. En la parte superior de la canalización completada, hacer clic en **Crear canalización de inferencia** > **Canalización de inferencia en tiempo real** -> **Enviar**.
2. Al finalizar, hacer clic en **Implementar** (*Deploy*):
   * **Nombre:** `endpoint-credit-risk`
   * **Tipo de proceso:** `Administrado` (*Managed*) con VM `Standard_DS2_v2`.

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
