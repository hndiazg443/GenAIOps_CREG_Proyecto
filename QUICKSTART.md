# 🎯 Quick Start - GenAIOps CREG

## Para quien recibe este proyecto:

### ⚡ Instalación Rápida (5 minutos)

```bash
# 1. Instalar
pip install -r requirements.txt

# 2. Configurar API Key
cp .env.example .env
nano .env  # Añade tu OPENAI_API_KEY

# 3. Generar vectorstore
python -c "from app.rag_pipeline import save_vectorstore; save_vectorstore()"

# 4. Verificar
python verify_installation.py
```

### 🚀 Usar el Sistema

**Chatbot:**
```bash
streamlit run app/ui_streamlit.py
```

**Dashboard de Evaluación:**
```bash
streamlit run app/dashboard_advanced.py
```

**Ejecutar Evaluación Completa:**
```bash
python app/run_eval_advanced.py  # 5-10 minutos
```

---

### 📚 Documentación Completa

- **`INSTRUCCIONES_INSTALACION.md`** - Instalación paso a paso detallada
- **`COMPARTIR.md`** - Guía de cómo compartir el proyecto
- **`README.md`** - Descripción del proyecto
- **`PROGRESO_DESAFIO.md`** - Documentación del desafío completo

---

### ⚠️ Requisitos

- Python 3.10+
- API Key de OpenAI ([obtener aquí](https://platform.openai.com/api-keys))
- 2 GB RAM mínimo

---

### 🆘 Problemas?

```bash
python verify_installation.py
```

Este script te dirá exactamente qué falta o está mal configurado.

---

**¡Listo en 5 minutos!** ⚡
