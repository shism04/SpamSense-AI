# 📧 SpamSense AI

![SpamSense AI Banner](images/spamsense_banner.jpg)

## 🎯 Descripción

**SpamSense AI** es una aplicación web moderna de detección de spam en correos electrónicos utilizando Machine Learning avanzado. La aplicación combina análisis de características de encabezados de correo con embeddings semánticos del contenido para proporcionar una clasificación precisa y confiable de emails SPAM vs HAM (legítimos).

### ✨ Características Principales

- 🤖 **Machine Learning Avanzado**: Modelo entrenado con scikit-learn
- 🧠 **Embeddings Semánticos**: Utiliza Sentence Transformers (all-mpnet-base-v2) para análisis profundo del contenido
- 📊 **Dashboard Interactivo**: Visualizaciones en tiempo real con Plotly
- 🔍 **Análisis Forense**: Métricas detalladas de confianza, IPs, enlaces y dominio del remitente
- 📁 **Procesamiento por Lotes**: Carga y analiza múltiples emails desde archivos `.eml` o `.txt`
- 🎨 **Interfaz Moderna**: UI elegante con componentes personalizados y diseño responsive
- 🐳 **Docker Ready**: Containerización completa para despliegue fácil

---

## 📁 Estructura del Proyecto

```
SpamSense-AI/
│
├── streamlit_app.py          # Aplicación principal de Streamlit
├── emailProcessor.py         # Procesador de emails y feature engineering
├── components.py             # Componentes UI reutilizables
├── styles.py                 # Estilos CSS y configuración de tema
│
├── requirements.txt          # Dependencias de Python
├── Dockerfile               # Configuración Docker
├── docker-compose.yml       # Orquestación de contenedores
│
├── model/                   # Modelos ML entrenados
│   └── spam_model.pkl      # Modelo de clasificación serializado
│
├── model_cache/            # Cache de modelos Transformer
│   └── models--sentence-transformers--all-mpnet-base-v2/
│
├── images/                 # Recursos visuales
│   └── spamsense_banner.jpg
│
└── __pycache__/           # Archivos compilados de Python
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.12+
- Docker y Docker Compose (opcional, para despliegue containerizado)
- 3GB de RAM mínimo (para el modelo de embeddings)

### Opción 1: Instalación Local

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd SpamSense-AI
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
streamlit run streamlit_app.py
```

La aplicación estará disponible en `http://localhost:8501`

### Opción 2: Docker (Recomendado)

1. **Construir y ejecutar con Docker Compose**
```bash
docker compose up --build
```

2. **Acceder a la aplicación**
```
http://localhost:8501
```

3. **Reiniciar servicios** (si es necesario)
```bash
docker-compose restart
```

---

## 📊 Uso de la Aplicación

### 1. Análisis Individual

1. Navega a la pestaña **"🔍 Single Email Analysis"**
2. Pega el contenido completo del email (incluyendo headers)
3. Haz clic en **"Analyze Email"**
4. Revisa el resultado (SPAM/HAM) y la confianza del modelo

### 2. Análisis por Lotes

1. Ve a la pestaña **"📊 Batch Analysis"**
2. Sube múltiples archivos **`.eml`** o **`.txt`**
3. Haz clic en **"📊 Generate Report"**
4. Explora el dashboard forense con:
  - Distribución de SPAM vs HAM
  - Análisis de confianza
  - Mapas de origen por IP y enlaces detectados
  - Pasaporte de dominio (RDAP)
5. Descarga el reporte con **"Download Full Forensic CSV"**

---

## 🧠 Arquitectura Técnica

### Componentes Principales

#### 1. **emailProcessor.py**
Clase `EmailProcessor` que realiza:
- **Extracción de headers y body** del email raw
- **Feature Engineering**: 14+ características extraídas:
  - Número de headers "Received"
  - Validación de IPs privadas
  - Coincidencia From/Return-Path
  - Análisis de Message-ID
  - Longitud y formato del Subject
  - Detección de HTML/Multipart
  - Headers de listas de correo
- **Generación de Embeddings**: Vector de 768 dimensiones del contenido usando Sentence Transformers

#### 2. **streamlit_app.py**
Aplicación principal con:
- Carga de modelos (con caché)
- Interfaz de tabs para análisis individual y batch
- Dashboard forense con Plotly
- Sección forense: IPs, enlaces y pasaporte de dominio (RDAP)
- Exportación de evidencia en CSV

#### 3. **components.py**
Componentes UI reutilizables:
- `metric_card()`: Tarjetas de métricas KPI
- `result_card_html()`: Tarjeta de resultado del análisis
- `hero_banner()`: Banner principal de la app
- `sidebar_info()`: Información en la barra lateral

#### 4. **styles.py**
Sistema de diseño:
- Paleta de colores definida
- CSS customizado para Streamlit
- Estilos para cards, gradientes, animaciones
- Tema consistente en toda la app

### Pipeline de Predicción

```
Email Raw → EmailProcessor → Features (782 cols) → Model → Probability → SPAM/HAM
                    ↓
         [Headers Analysis + Body Embeddings]
```

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Propósito |
|-----------|-----------|
| **Streamlit** | Framework web interactivo |
| **scikit-learn** | Modelo de clasificación ML |
| **Sentence Transformers** | Embeddings semánticos (all-mpnet-base-v2) |
| **PyTorch** | Backend para transformers |
| **Plotly** | Visualizaciones interactivas |
| **Pandas** | Manipulación de datos |
| **Docker** | Containerización y despliegue |
| **joblib** | Serialización de modelos |

---

## 📈 Métricas del Modelo

El dashboard muestra métricas clave:
- **Accuracy**: Precisión general del modelo
- **Precision**: Tasa de verdaderos positivos
- **Recall**: Capacidad de detectar SPAM
- **F1-Score**: Media armónica de precision y recall
- **Confidence Score**: Nivel de confianza de cada predicción (0-100%)

---

## 🔒 Consideraciones de Seguridad

- ⚠️ No envíes información sensible o credenciales en los emails de prueba
- 🔐 El contenido del email se procesa localmente para la clasificación
- 🌐 Para análisis forense, se consultan servicios externos (RDAP y geolocalización IP)
- 📊 Los datos del modelo están cacheados localmente en `model_cache/`
