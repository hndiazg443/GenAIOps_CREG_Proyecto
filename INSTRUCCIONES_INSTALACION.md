# 🚀 Instrucciones de Instalación - Proyecto GenAIOps CREG

## 📋 Requisitos Previos

- Python 3.10 o superior
- Git
- Cuenta de OpenAI con API Key

---

## 🔧 Instalación Paso a Paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/darkanita/GenAIOps_Pycon2025.git
cd GenAIOps_Pycon2025
```

### 2. Crear entorno virtual (Recomendado)

**Opción A: Con conda**
```bash
conda create -n genaiops python=3.10 -y
conda activate genaiops
```

**Opción B: Con venv**
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` y agrega tu API Key de OpenAI:
```
OPENAI_API_KEY=tu-api-key-aqui
```

### 5. Generar el vectorstore

**IMPORTANTE:** Este paso procesa los PDFs y crea el índice vectorial.

```bash
python -c "from app.rag_pipeline import save_vectorstore; save_vectorstore()"
```

Esto tomará unos minutos y creará la carpeta `vectorstore/`.

---

## 🎯 Uso del Sistema

### Chatbot Interactivo

```bash
streamlit run app/ui_streamlit.py
```

Abre tu navegador en: http://localhost:8501

### Dashboard de Evaluación Avanzado

```bash
streamlit run app/dashboard_advanced.py
```

Abre tu navegador en: http://localhost:8501

### Ejecutar Evaluación Básica

```bash
python app/run_eval.py
```

### Ejecutar Evaluación Avanzada (Con 7 criterios)

```bash
python app/run_eval_advanced.py
```

**Tiempo estimado:** 5-10 minutos (8 preguntas × 7 criterios)

### Ver Resultados en MLflow

```bash
mlflow ui
```

Abre tu navegador en: http://localhost:5000

---

## 📊 Estructura del Proyecto

```
GenAIOps_Pycon2025/
├── app/
│   ├── ui_streamlit.py              # Chatbot simple
│   ├── main_interface.py            # Interfaz combinada
│   ├── rag_pipeline.py              # Pipeline RAG
│   ├── run_eval.py                  # Evaluación básica
│   ├── run_eval_advanced.py         # Evaluación avanzada ⭐
│   ├── dashboard_advanced.py        # Dashboard con criterios ⭐
│   ├── view_mlflow_results.py       # Visualizador de resultados
│   ├── resumen_final.py             # Resumen del proyecto
│   └── prompts/
│       ├── v1_asistente_creg_didactico.txt
│       └── v2_creg_conciso.txt
├── data/
│   └── pdfs/                        # PDFs de resoluciones CREG
├── tests/
│   ├── eval_dataset_creg.json       # Dataset de evaluación CREG
│   └── test_run_eval.py
├── vectorstore/                     # Índice vectorial (se genera)
├── mlruns/                          # Experimentos MLflow (se genera)
├── requirements.txt
├── .env.example
├── README.md
├── PROGRESO_DESAFIO.md             # Documentación del desafío
└── INSTRUCCIONES_INSTALACION.md    # Este archivo
```

---

## 🎓 Componentes del Sistema

### 1. Pipeline RAG
- **Documentos:** 3 Resoluciones CREG 2025 (50 páginas)
- **Embeddings:** OpenAI
- **Vectorstore:** FAISS
- **LLM:** GPT-4o

### 2. Evaluación Avanzada
- **QAEvalChain:** Evaluación básica (correcto/incorrecto)
- **LabeledCriteriaEvalChain:** 7 criterios detallados
  - ✅ Corrección (Correctness)
  - ✅ Relevancia (Relevance)
  - ✅ Coherencia (Coherence)
  - ✅ Toxicidad (Toxicity)
  - ✅ Daño Potencial (Harmfulness)
  - ✅ Utilidad (Helpfulness)
  - ✅ Concisión (Conciseness)

### 3. Visualización
- **Dashboard interactivo** con Streamlit + Plotly
- **Razonamientos en español** guardados en MLflow
- **Gráficos:** Barras, Radar Chart, Tablas

---

## 🔍 Verificación de la Instalación

Para verificar que todo funciona correctamente:

```bash
# 1. Ver resumen del proyecto
python app/resumen_final.py

# 2. Ver resultados de MLflow
python app/view_mlflow_results.py
```

---

## ⚠️ Solución de Problemas Comunes

### Error: "No module named 'langchain_classic'"

```bash
pip install langchain-classic
```

### Error: "Port already in use"

```bash
# Detener procesos de Streamlit
pkill -f streamlit

# O usar un puerto diferente
streamlit run app/ui_streamlit.py --server.port 8503
```

### Error: "OpenAI API Key not found"

Verifica que el archivo `.env` tenga la API Key correcta:
```bash
cat .env
```

### Vectorstore vacío o no funciona

Regenera el vectorstore:
```bash
rm -rf vectorstore/
python -c "from app.rag_pipeline import save_vectorstore; save_vectorstore()"
```

---

## 📚 Recursos Adicionales

- **README.md:** Descripción general del proyecto
- **PROGRESO_DESAFIO.md:** Documentación completa del desafío
- **Documentación LangChain:** https://python.langchain.com/
- **MLflow Docs:** https://mlflow.org/docs/latest/index.html

---

## 🤝 Contribuir

Si encuentras problemas o tienes sugerencias:
1. Crea un issue en GitHub
2. Envía un pull request con mejoras

---

## 📧 Contacto

**Proyecto:** GenAIOps PyCon 2025  
**Repositorio:** https://github.com/darkanita/GenAIOps_Pycon2025  
**Dominio:** Regulación Energética Colombiana (CREG)

---

## ✅ Checklist de Instalación

- [ ] Python 3.10+ instalado
- [ ] Repositorio clonado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] Archivo `.env` configurado con API Key
- [ ] Vectorstore generado
- [ ] Chatbot funciona
- [ ] Dashboard funciona
- [ ] Evaluación ejecutada
- [ ] MLflow UI accesible

¡Listo para usar! 🎉
