# 🤖 Chatbot GenAI - Regulación Energética CREG

Este proyecto demuestra cómo construir, evaluar y automatizar un chatbot de tipo RAG (Retrieval Augmented Generation) con buenas prácticas de **GenAIOps**.

---

## 🧠 Caso de Estudio

El chatbot responde preguntas sobre regulación energética colombiana basándose en documentos oficiales de la **CREG (Comisión de Regulación de Energía y Gas)**. Utiliza Resoluciones CREG 2025 como fuente de conocimiento.

---

## 📂 Estructura del Proyecto

```
├── app/
│   ├── ui_streamlit.py           ← interfaz simple del chatbot
│   ├── main_interface.py         ← interfaz combinada con métricas
│   ├── run_eval.py               ← evaluación automática básica
│   ├── run_eval_advanced.py      ← evaluación con 7 criterios
│   ├── dashboard_advanced.py     ← dashboard con visualizaciones
│   ├── rag_pipeline.py           ← lógica de ingestión y RAG
│   └── prompts/
│       ├── v1_asistente_creg_didactico.txt
│       └── v2_creg_conciso.txt
├── data/pdfs/                    ← documentos CREG (Resoluciones 076, 078, 079)
├── tests/
│   ├── test_run_eval.py
│   └── eval_dataset_creg.json    ← dataset de evaluación CREG
├── .env.example
├── Dockerfile
├── QUICKSTART.md                 ← guía rápida de instalación
├── INSTRUCCIONES_INSTALACION.md ← guía completa
├── COMPARTIR.md                  ← cómo compartir el proyecto
├── PROGRESO_DESAFIO.md          ← documentación del desafío
└── verify_installation.py        ← script de verificación
```

---

## 🚦 Ciclo de vida GenAIOps aplicado

### 1. 🧱 Preparación del entorno

```bash
git clone https://github.com/hndiazg443/GenAIOps_CREG_Proyecto.git
cd GenAIOps_CREG_Proyecto
conda create -n genaiops-creg python=3.10 -y
conda activate genaiops-creg
pip install -r requirements.txt
cp .env.example .env  # Agrega tu API KEY de OpenAI
```

---

### 2. 🔍 Ingesta y vectorización de documentos

Procesa los PDFs y genera el índice vectorial:

```bash
python -c "from app.rag_pipeline import save_vectorstore; save_vectorstore()"
```

Esto:
- Divide los documentos en chunks (por defecto `chunk_size=512`, `chunk_overlap=50`)
- Genera embeddings con OpenAI
- Guarda el índice vectorial en `vectorstore/`
- Registra los parámetros en **MLflow**

🔧 Para personalizar:
```python
save_vectorstore(chunk_size=1024, chunk_overlap=100)
```

♻️ Para reutilizarlo directamente:
```python
vectordb = load_vectorstore_from_disk()
```

---

### 3. 🧠 Construcción del pipeline RAG

```python
from app.rag_pipeline import build_chain
chain = build_chain(vectordb, prompt_version="v1_asistente_creg_didactico")
```

- Soporta múltiples versiones de prompt
- Usa `ConversationalRetrievalChain` con `LangChain` + `OpenAI`

---

### 4. 💬 Interacción vía Streamlit

Versión básica:
```bash
streamlit run app/ui_streamlit.py
```

Versión combinada con métricas:
```bash
streamlit run app/main_interface.py
```

---

### 5. 🧪 Evaluación automática de calidad

Ejecuta:

```bash
python app/run_eval.py
```

Esto:
- Usa `tests/eval_dataset_creg.json` como ground truth
- Genera respuestas usando el RAG actual
- Evalúa con `LangChain Eval (QAEvalChain)`
- Registra resultados en **MLflow**

Para evaluación avanzada con 7 criterios:

```bash
python app/run_eval_advanced.py
```

Evalúa: correctness, relevance, coherence, toxicity, harmfulness, helpfulness, conciseness

---

### 6. 📈 Visualización de resultados

Dashboard completo:

```bash
streamlit run app/dashboard_advanced.py
```

- Tabla con todas las preguntas evaluadas
- Gráficos de barras por criterio
- Radar chart multidimensional
- Análisis de preguntas problemáticas
- Razonamientos de evaluación en español
- Filtrado por experimento MLflow

---

### 7. 🔁 Automatización con GitHub Actions (Opcional)

⚠️ Los workflows de GitHub Actions han sido removidos temporalmente. Puedes recrearlos si necesitas CI/CD.

---

### 8. 🧪 Validación automatizada

```bash
pytest tests/test_run_eval.py
```

- Evalúa que el sistema tenga al menos 80% de precisión con el dataset base

---

## 🔍 ¿Qué puedes hacer?

- 💬 Hacer preguntas al chatbot
- 🔁 Evaluar diferentes estrategias de chunking y prompts
- 📊 Comparar desempeño con métricas semánticas avanzadas
- 🧪 Trazar todo en MLflow
- � Visualizar resultados con dashboards interactivos
- �🔄 Adaptar a otros dominios (legal, salud, educación, financiero…)

---

## ⚙️ Stack Tecnológico

- **OpenAI + LangChain** – LLM + RAG
- **FAISS** – Vectorstore
- **Streamlit** – UI
- **MLflow** – Registro de experimentos
- **LangChain Eval** – Evaluación semántica (QA + Criteria)
- **Plotly** – Visualizaciones interactivas
- **GitHub** – Control de versiones

---

## 🎓 Desafío para estudiantes

🧩 Parte 1: Personalización

1. Elige un nuevo dominio
Ejemplos: salud, educación, legal, bancario, ambiental, etc.

2. Reemplaza los documentos PDF
Ubícalos en data/pdfs/.

3. Modifica o crea tus prompts
Edita los archivos en app/prompts/.

4. Crea un conjunto de pruebas
En tests/eval_dataset_creg.json (o tu propio archivo), define preguntas y respuestas esperadas para evaluar a tu chatbot.

✅ Parte 2: Evaluación Automática

1. Ejecuta run_eval.py para probar tu sistema actual.
La evaluación básica usa QAEvalChain de LangChain, que devuelve una métrica binaria: correcto / incorrecto.

🔧 Parte 3: Evaluación Avanzada (✅ Implementado en este proyecto)

1. Sistema de evaluación mejorado con LabeledCriteriaEvalChain:

    * ✅ "correctness" – ¿Es correcta la respuesta?
    * ✅ "relevance" – ¿Es relevante respecto a la pregunta?
    * ✅ "coherence" – ¿Está bien estructurada la respuesta?
    * ✅ "toxicity" – ¿Contiene lenguaje ofensivo o riesgoso?
    * ✅ "harmfulness" – ¿Podría causar daño la información?
    * ✅ "helpfulness" – ¿Es útil para el usuario?
    * ✅ "conciseness" – ¿Es concisa y directa?

    * Cada criterio registra:
        * Una métrica en MLflow (score)
        * Un razonamiento como artefacto en español

    Ver: `app/run_eval_advanced.py`

📊 Parte 4: Dashboard Avanzado (✅ Implementado)

1. Dashboard completo en `app/dashboard_advanced.py` con:

    * ✅ Métricas por criterio (scores de 0-1)
    * ✅ Gráfico de barras comparativo
    * ✅ Radar chart multidimensional
    * ✅ Tabla detallada con todos los scores
    * ✅ Análisis de preguntas problemáticas
    * ✅ Razonamientos del modelo en español

🧪 Parte 5: Análisis y Reflexión (Ver PROGRESO_DESAFIO.md)

1. Resultados del proyecto CREG:
    * 87.5% de precisión en QA básica
    * 71.2% promedio en criterios avanzados
    * 100% en coherencia, sin toxicidad, sin contenido dañino
    * Áreas de mejora: relevancia (62.5%) y concisión (50%)

🚀 Bonus (✅ Implementado)

- ✅ 7 criterios implementados (más allá de los 5 requeridos)
- ✅ Razonamientos en español
- ✅ Visualizaciones interactivas con Plotly
- ✅ Documentación completa para instalación y compartir
- ✅ Script de verificación automática

---

¡Listo para ser usado en clase, investigación o producción educativa! 🚀
