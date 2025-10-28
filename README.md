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

## ✨ Características Implementadas

Este proyecto implementa un sistema RAG completo con evaluación avanzada:

### 🎯 **1. Dominio Personalizado: Regulación Energética CREG**

- ✅ 3 Resoluciones CREG 2025 (076, 078, 079) - 50 páginas
- ✅ 2 Prompts especializados (didáctico y conciso)
- ✅ Dataset de evaluación con 8 preguntas específicas de CREG

### 📊 **2. Sistema de Evaluación Dual**

**Evaluación Básica (`run_eval.py`):**
- ⚡ Rápida y simple
- 🎯 Usa `QAEvalChain` de LangChain
- 📈 Métrica binaria: correcto/incorrecto
- 🔧 Ideal para: debugging rápido y verificación

**Evaluación Avanzada (`run_eval_advanced.py`):**
- 🔬 Sistema completo con `LabeledCriteriaEvalChain`
- 📊 7 criterios de evaluación:
  - ✅ **Correctness** – Precisión de la respuesta
  - ✅ **Relevance** – Pertinencia a la pregunta
  - ✅ **Coherence** – Estructura y fluidez
  - ✅ **Toxicity** – Detección de lenguaje ofensivo
  - ✅ **Harmfulness** – Identificación de contenido dañino
  - ✅ **Helpfulness** – Utilidad para el usuario
  - ✅ **Conciseness** – Brevedad y claridad
- 💾 Cada criterio registra score (0-1) y razonamiento en MLflow
- 🇪🇸 Razonamientos generados en español

### � **3. Dashboard Avanzado Interactivo**

Dashboard completo en `app/dashboard_advanced.py`:
- 📊 **6 secciones de visualización:**
  1. Resumen general con KPIs principales
  2. Gráfico de barras comparativo por criterio
  3. Radar chart multidimensional
  4. Tabla detallada con todos los scores
  5. Análisis de preguntas problemáticas
  6. Razonamientos completos en español
- 🎨 Visualizaciones con Plotly
- 🔍 Filtrado por experimento MLflow

### 📊 **4. Resultados del Proyecto CREG**

Métricas obtenidas:
- 📈 **87.5%** de precisión en QA básica (7/8 correctas)
- 📊 **71.2%** promedio en criterios avanzados
- ✅ **100%** en coherence (estructura perfecta)
- ✅ **100%** sin toxicity (lenguaje apropiado)
- ✅ **100%** sin harmfulness (contenido seguro)
- 🔧 Áreas de mejora: relevancia (62.5%) y concisión (50%)

### �️ **5. Herramientas Adicionales**

- 📝 `QUICKSTART.md` – Instalación en 5 minutos
- 📚 `INSTRUCCIONES_INSTALACION.md` – Guía completa paso a paso
- 🔄 `COMPARTIR.md` – Cómo compartir el proyecto
- 📊 `PROGRESO_DESAFIO.md` – Documentación detallada del desarrollo
- ✅ `verify_installation.py` – Script de verificación automática

---

## 🎓 Adaptación a Otros Dominios

¿Quieres adaptar este proyecto a tu dominio? Sigue estos pasos:

1. **Reemplaza los documentos:** Coloca tus PDFs en `data/pdfs/`
2. **Crea tus prompts:** Edita archivos en `app/prompts/`
3. **Define tu dataset:** Crea preguntas/respuestas en `tests/`
4. **Regenera vectorstore:** `python -c "from app.rag_pipeline import save_vectorstore; save_vectorstore()"`
5. **Ejecuta evaluación avanzada:** `python app/run_eval_advanced.py`
6. **Visualiza resultados:** `streamlit run app/dashboard_advanced.py`

Dominios sugeridos: salud, educación, legal, financiero, ambiental, tecnológico.

---

¡Sistema completo de GenAIOps listo para producción o investigación! 🚀
