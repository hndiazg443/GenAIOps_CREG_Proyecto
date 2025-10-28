# 🚀 Guía Rápida de Compartir - GenAIOps CREG

## 📤 Opciones para Compartir

### Opción 1: Compartir vía GitHub (Recomendada)

```bash
# 1. Añadir todos los cambios
git add .

# 2. Hacer commit
git commit -m "Completado desafío GenAIOps con evaluación avanzada CREG"

# 3. Subir a GitHub
git push origin main
```

**La otra persona puede clonar:**
```bash
git clone https://github.com/hndiazg443/GenAIOps_CREG_Proyecto.git
cd GenAIOps_CREG_Proyecto
```

---

### Opción 2: Compartir como archivo ZIP

```bash
# Crear ZIP (excluyendo archivos innecesarios)
cd ..
tar -czf GenAIOps_CREG.tar.gz GenAIOps_CREG_Proyecto/ \
  --exclude='GenAIOps_CREG_Proyecto/__pycache__' \
  --exclude='GenAIOps_CREG_Proyecto/**/__pycache__' \
  --exclude='GenAIOps_CREG_Proyecto/mlruns' \
  --exclude='GenAIOps_CREG_Proyecto/.git' \
  --exclude='GenAIOps_CREG_Proyecto/vectorstore' \
  --exclude='GenAIOps_CREG_Proyecto/.env'

# Compartir archivo: GenAIOps_CREG.tar.gz
```

La otra persona debe:
```bash
tar -xzf GenAIOps_CREG.tar.gz
cd GenAIOps_CREG_Proyecto
```

---

### Opción 3: Compartir vía Google Drive / Dropbox

1. Crear el ZIP con el comando anterior
2. Subir `GenAIOps_CREG.tar.gz` a Google Drive/Dropbox
3. Compartir el enlace

---

## 📋 Instrucciones para la otra persona

**Archivo:** `INSTRUCCIONES_INSTALACION.md` contiene el paso a paso completo.

**Resumen rápido:**

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar .env
cp .env.example .env
# Editar .env y añadir API Key de OpenAI

# 3. Generar vectorstore
python -c "from app.rag_pipeline import save_vectorstore; save_vectorstore()"

# 4. Verificar instalación
python verify_installation.py

# 5. Ejecutar
streamlit run app/ui_streamlit.py
```

---

## ✅ Checklist antes de compartir

- [ ] Verificar que `.env` está en `.gitignore` (no se sube tu API Key)
- [ ] Verificar que `mlruns/` está en `.gitignore` (opcional, es grande)
- [ ] Verificar que `vectorstore/` está en `.gitignore` (se regenera)
- [ ] Archivo `.env.example` existe y está actualizado
- [ ] Archivo `INSTRUCCIONES_INSTALACION.md` creado
- [ ] Archivo `verify_installation.py` funciona
- [ ] Todos los PDFs en `data/pdfs/`
- [ ] Todos los prompts en `app/prompts/`
- [ ] Dataset de evaluación en `tests/eval_dataset_creg.json`

---

## 📊 Archivos que SÍ se comparten

✅ Código fuente (`app/*.py`)
✅ Documentos PDF (`data/pdfs/*.pdf`)
✅ Prompts (`app/prompts/*.txt`)
✅ Dataset de evaluación (`tests/eval_dataset_creg.json`)
✅ Requirements (`requirements.txt`)
✅ Documentación (`*.md`)
✅ Scripts de verificación (`verify_installation.py`)
✅ Configuración ejemplo (`.env.example`)

## 🚫 Archivos que NO se comparten

❌ API Keys (`.env`)
❌ Vectorstore generado (`vectorstore/`) - se regenera
❌ Experimentos MLflow (`mlruns/`) - opcional
❌ Cache de Python (`__pycache__/`)
❌ Historia de Git (`.git/`) - opcional en ZIP

---

## 🔒 Seguridad

**IMPORTANTE:** Antes de compartir, verifica que no estés compartiendo:

```bash
# Verificar que .env NO esté en el staging area
git status | grep .env

# Debería mostrar que está ignorado
# Si aparece en "Changes to be committed", haz:
git reset HEAD .env
```

**NUNCA compartas:**
- Tu API Key de OpenAI
- Archivos `.env` con credenciales
- Tokens o contraseñas

---

## 📧 Información de contacto

**Proyecto:** GenAIOps PyCon 2025  
**Repositorio:** https://github.com/hndiazg443/GenAIOps_CREG_Proyecto  
**Dominio:** Regulación Energética Colombiana (CREG)

---

## 🆘 Soporte

Si la otra persona tiene problemas:

1. **Verificar instalación:** `python verify_installation.py`
2. **Ver logs de error:** Revisar mensajes completos de error
3. **Consultar documentación:** `INSTRUCCIONES_INSTALACION.md`
4. **Regenerar vectorstore:** Si hay problemas con los embeddings
5. **Verificar API Key:** La causa más común de errores

---

**¡Listo para compartir!** 🎉
