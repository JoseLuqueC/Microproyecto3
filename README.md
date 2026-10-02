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
   * **Grupo de recursos:** `rg-credit-risk-westus` (dar clic en *Crear nuevo*)
   * **Región:** **`West US`** (o **`North Central US`**) *(OBLIGATORIO: la política de Azure for Students restringe la creación únicamente a estas regiones en EE. UU.)*
4. Hacer clic en **Crear** (tarda ~1 a 2 minutos). Al terminar, entrarás al área de trabajo y se desbloqueará el menú completo de la izquierda (**Creación**, **Recursos** y **Administrar**).

#### Paso 1: Configurar el Cómputo Económico
En el menú lateral izquierdo:
1. Ir a **Administrar** > **Proceso** > pestaña **Clústeres de proceso**.
2. Hacer clic en **+ Nuevo** (o *Crear*):
   * **Paso 1 (Máquina virtual):**
     * Ubicación: `West US`
     * Nivel de máquina virtual: `Dedicado`
     * Tipo de máquina virtual: `CPU`
     * Tamaño: Seleccionar `Standard_DS11_v2` (2 núcleos, 14 GB RAM, 0.18 USD/h)
     * Clic en **Siguiente**.
   * **Paso 2 (Configuración avanzada):**
     * Nombre del proceso: `cluster-credit-risk`
     * Número mínimo de nodos: **`0`** *(OBLIGATORIO: para que el costo sea $0.00 cuando esté inactivo)*
     * Número máximo de nodos: **`1`**
     * Segundos de inactividad antes de la reducción vertical: **`120`**
3. Clic en **Crear**.

#### Paso 2: Cargar el Dataset (Datos)
1. En el menú lateral izquierdo, ir a **Recursos** > **Datos**.
2. Pestaña **Recursos de datos** > clic en el botón azul **+ Crear**:
   * **1. Tipo de datos:** Nombre: `german-credit-risk`, Tipo: **Tabular** -> *Siguiente*.
   * **2. Origen de datos:** Seleccionar **De archivos locales** -> *Siguiente*.
   * **3. Tipo de almacenamiento de destino:** Dejar seleccionado `workspaceblobstore` -> *Siguiente*.
   * **4. Selección de archivos:** Clic en **Examinar** > **Cargar archivos** > seleccionar `data/german_credit_risk.csv` -> *Siguiente*.
   * **5. Configuración:** Delimitador: Coma (`,`), Encabezados: **Solo el primer archivo tiene encabezados** -> *Siguiente*.
   * **6. Esquema:** Verificar columnas detectadas (CheckingAccount, DurationMonths, ..., CreditRisk) -> *Siguiente*.
   * **7. Revisar:** Clic en **Crear**.

#### Paso 3: Construcción del Pipeline en el Diseñador (Designer)
1. En el menú izquierdo (**Creación**), hacer clic en **Diseñador**.
2. Seleccionar **Crear una nueva canalización con componentes clásicos compilados previamente**.
3. En la barra izquierda del lienzo, ir a la pestaña **Datos** y arrastrar **`german-credit-risk`** al centro del lienzo.
4. Cambiar a la pestaña **Componente** (al lado de Datos) y arrastrar y conectar los siguientes 6 módulos:
   * **Select Columns in Dataset:**
     * Conectar la salida de `german-credit-risk` a su entrada.
     * En el panel derecho > *Editar columna* > Incluir todas las columnas.
   * **Clean Missing Data:**
     * Conectar la salida de `Select Columns in Dataset` a su entrada.
     * Cleaning mode: *Replace with mean* (o sustitución personalizada).
   * **Split Data:**
     * Conectar la salida izquierda (Dataset limpio) de `Clean Missing Data` a su entrada.
     * En el panel derecho: *Fraction of rows*: `0.7`, *Random seed*: `42`.
   * **Two-Class Boosted Decision Tree:**
     * Arrastrar al lienzo (a la izquierda de Train Model).
   * **Train Model:**
     * Entrada izquierda (Untrained model): Conectar la salida de `Two-Class Boosted Decision Tree`.
     * Entrada derecha (Dataset): Conectar la salida izquierda (70% Train) de `Split Data`.
     * En el panel derecho > *Editar columna* (Label column) > Seleccionar **`CreditRisk`**.
   * **Score Model:**
     * Entrada izquierda: Conectar la salida de `Train Model`.
     * Entrada derecha: Conectar la salida derecha (30% Test) de `Split Data`.
   * **Evaluate Model:**
     * Entrada izquierda: Conectar la salida de `Score Model`.
5. **Configuración y Envío (Botón 'Configurar y enviar'):**
   * Cambiar el nombre del pipeline arriba a la izquierda a: `Pipeline-Credit-Risk-Evaluation`.
   * Clic en el botón azul superior **Configurar y enviar** (*Configure & submit*).
   * **Paso 1 (Datos básicos):** Seleccionar *Crear nuevo* -> Nombre: `exp-credit-risk` -> *Siguiente*.
   * **Paso 2 (Entradas y salidas):** Dejar por defecto -> *Siguiente*.
   * **Paso 3 (Parámetros de ejecución):** En *Proceso predeterminado*, seleccionar el clúster: `cluster-credit-risk` -> *Siguiente*.
   * **Paso 4 (Revisar y enviar):** Verificar el resumen y hacer clic en el botón azul **Enviar** (*Submit*).
   * El entrenamiento tomará entre 3 y 5 minutos. El clúster encenderá 1 nodo, ejecutará todos los pasos y al finalizar volverá a 0 nodos automáticamente.

#### Paso 4: Despliegue del Punto de Conexión (Pipeline Endpoint)
1. En la canalización de entrenamiento completada, hacer clic en **Crear canalización de inferencia** > **Canalización de inferencia en tiempo real**.
2. Azure genera automáticamente el borrador con `Trained model`, `Apply Transformation` y `Web Service Output`.
3. Hacer clic en **Configurar y enviar**:
   * Usar el experimento existente: `exp-credit-risk` y clúster: `cluster-credit-risk` -> Clic en **Enviar**.
4. Al finalizar la ejecución con estado **✔️ Completado**:
   * En la barra superior de herramientas, hacer clic en el botón con ícono de nube: **`Publicar`** (*Publish*).
   * En la ventana emergente *Configuración de una canalización publicada*:
     * Seleccionar: **Crear nuevo**.
     * **Nombre de nuevo PipelineEndpoint:** `endpoint-credit-risk`.
     * **Descripción:** `Servicio REST de inferencia en tiempo real para evaluación de riesgo crediticio.`
     * Mantener marcadas las casillas de canalización predeterminada.
     * Hacer clic en el botón azul **Publicar** (*Publish*).
5. El punto de conexión quedará activo y visible en el menú lateral izquierdo bajo **Recursos** > **Puntos de conexión** > pestaña **Puntos de conexión de canalización** (*Pipeline endpoints*), listo con su **Dirección URL de REST** para ser consumido.

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
