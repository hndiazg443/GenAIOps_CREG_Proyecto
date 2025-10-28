# app/dashboard_advanced.py
"""
Dashboard Avanzado de Evaluación - Parte 4 del Desafío
Visualiza métricas por criterio: correctness, relevance, coherence, toxicity, harmfulness, etc.
"""

import mlflow
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="📊 Dashboard Avanzado - GenAIOps", layout="wide")

# Header
st.title("🎯 Dashboard Avanzado de Evaluación GenAIOps")
st.markdown("---")

# ✅ Buscar experimentos que comienzan con "eval_"
client = mlflow.tracking.MlflowClient()
experiments = [exp for exp in client.search_experiments() if exp.name.startswith("eval_")]

if not experiments:
    st.warning("⚠️ No se encontraron experimentos de evaluación.")
    st.stop()

# Sidebar para selección
st.sidebar.header("🔧 Configuración")
exp_names = [exp.name for exp in experiments]
selected_exp_name = st.sidebar.selectbox("📊 Selecciona un experimento:", exp_names)

experiment = client.get_experiment_by_name(selected_exp_name)
runs = client.search_runs(experiment_ids=[experiment.experiment_id], order_by=["start_time DESC"])

if not runs:
    st.warning("⚠️ No hay ejecuciones registradas en este experimento.")
    st.stop()

# Convertir runs a DataFrame con todas las métricas
data = []
for run in runs:
    params = run.data.params
    metrics = run.data.metrics
    tags = run.data.tags
    
    row = {
        "run_id": run.info.run_id,
        "run_name": tags.get("mlflow.runName", "unknown"),
        "pregunta": params.get("question", "N/A"),
        "prompt_version": params.get("prompt_version", "N/A"),
        "chunk_size": int(params.get("chunk_size", 0)),
        "chunk_overlap": int(params.get("chunk_overlap", 0)),
    }
    
    # Agregar todas las métricas disponibles
    metric_names = [
        "qa_is_correct",
        "correctness_score",
        "relevance_score", 
        "coherence_score",
        "toxicity_score",
        "harmfulness_score",
        "helpfulness_score",
        "conciseness_score",
        "avg_criteria_score",
        "lc_is_correct"  # Para compatibilidad con evaluación básica
    ]
    
    for metric_name in metric_names:
        row[metric_name] = metrics.get(metric_name, None)
    
    data.append(row)

df = pd.DataFrame(data)

# Filtrar columnas con datos
available_metrics = [col for col in df.columns if col.endswith('_score') or col in ['qa_is_correct', 'lc_is_correct']]
available_metrics = [col for col in available_metrics if df[col].notna().any()]

# =====================================================
# 1. RESUMEN GENERAL
# =====================================================
st.header("📊 Resumen General")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_questions = len(df)
    st.metric("📝 Total Preguntas", total_questions)

with col2:
    if 'qa_is_correct' in df.columns:
        qa_accuracy = df['qa_is_correct'].mean() * 100
        st.metric("✅ Precisión QA Básica", f"{qa_accuracy:.1f}%")
    elif 'lc_is_correct' in df.columns:
        qa_accuracy = df['lc_is_correct'].mean() * 100
        st.metric("✅ Precisión QA Básica", f"{qa_accuracy:.1f}%")

with col3:
    if 'avg_criteria_score' in df.columns:
        avg_score = df['avg_criteria_score'].mean() * 100
        st.metric("🎯 Score Promedio Criterios", f"{avg_score:.1f}%")

with col4:
    if 'coherence_score' in df.columns:
        coherence = df['coherence_score'].mean() * 100
        st.metric("📝 Coherencia Promedio", f"{coherence:.1f}%")

st.markdown("---")

# =====================================================
# 2. MÉTRICAS POR CRITERIO
# =====================================================
st.header("📈 Análisis por Criterio")

# Calcular promedios por criterio
criteria_metrics = {
    "Corrección": "correctness_score",
    "Relevancia": "relevance_score",
    "Coherencia": "coherence_score",
    "Toxicidad": "toxicity_score",
    "Daño Potencial": "harmfulness_score",
    "Utilidad": "helpfulness_score",
    "Concisión": "conciseness_score"
}

# Filtrar solo los disponibles
available_criteria = {k: v for k, v in criteria_metrics.items() if v in df.columns and df[v].notna().any()}

if available_criteria:
    # Gráfico de barras con promedios
    criteria_data = []
    for name, col in available_criteria.items():
        avg_value = df[col].mean()
        criteria_data.append({"Criterio": name, "Score Promedio": avg_value, "Porcentaje": avg_value * 100})
    
    criteria_df = pd.DataFrame(criteria_data)
    
    # Gráfico de barras horizontal
    fig = px.bar(
        criteria_df, 
        x="Porcentaje", 
        y="Criterio", 
        orientation='h',
        title="🎯 Score Promedio por Criterio de Evaluación",
        color="Porcentaje",
        color_continuous_scale="RdYlGn",
        range_color=[0, 100]
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Métricas individuales
    st.subheader("📊 Detalle de Criterios")
    cols = st.columns(len(available_criteria))
    for idx, (name, col) in enumerate(available_criteria.items()):
        with cols[idx]:
            avg_value = df[col].mean() * 100
            # Determinar color según el valor
            delta_color = "normal" if avg_value >= 70 else "inverse"
            st.metric(name, f"{avg_value:.1f}%", delta=f"{avg_value - 50:.1f}%", delta_color=delta_color)

st.markdown("---")

# =====================================================
# 3. COMPARACIÓN ENTRE CRITERIOS (Radar Chart)
# =====================================================
if len(available_criteria) >= 3:
    st.header("🕸️ Análisis Multidimensional")
    
    # Preparar datos para radar chart
    categories = list(available_criteria.keys())
    values = [df[col].mean() * 100 for col in available_criteria.values()]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Score Promedio',
        line_color='rgb(31, 119, 180)',
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Evaluación Multidimensional del Sistema"
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 4. TABLA DETALLADA POR PREGUNTA
# =====================================================
st.header("📋 Resultados Detallados por Pregunta")

# Selector de criterios a mostrar
selected_criteria = st.multiselect(
    "Selecciona criterios a visualizar:",
    options=list(available_criteria.keys()),
    default=list(available_criteria.keys())[:4]  # Mostrar primeros 4 por defecto
)

# Preparar DataFrame para mostrar
display_cols = ["run_name", "pregunta"]
for criterion in selected_criteria:
    col_name = available_criteria[criterion]
    if col_name in df.columns:
        display_cols.append(col_name)

df_display = df[display_cols].copy()

# Renombrar columnas para mejor visualización
rename_dict = {
    "run_name": "Run",
    "pregunta": "Pregunta",
}
for criterion, col in available_criteria.items():
    if col in df_display.columns:
        rename_dict[col] = criterion

df_display = df_display.rename(columns=rename_dict)

# Formatear scores como porcentajes
for criterion in selected_criteria:
    if criterion in df_display.columns:
        df_display[criterion] = df_display[criterion].apply(lambda x: f"{x*100:.0f}%" if pd.notna(x) else "N/A")

st.dataframe(df_display, use_container_width=True, height=400)

st.markdown("---")

# =====================================================
# 5. ANÁLISIS DE PREGUNTAS PROBLEMÁTICAS
# =====================================================
st.header("⚠️ Análisis de Preguntas Problemáticas")

if 'avg_criteria_score' in df.columns:
    # Encontrar preguntas con score bajo
    threshold = st.slider("Umbral de score problemático:", 0.0, 1.0, 0.6, 0.05)
    problematic = df[df['avg_criteria_score'] < threshold].copy()
    
    if not problematic.empty:
        st.warning(f"⚠️ Se encontraron {len(problematic)} preguntas con score inferior a {threshold*100:.0f}%")
        
        # Mostrar las preguntas problemáticas
        prob_display = problematic[['run_name', 'pregunta', 'avg_criteria_score'] + 
                                   [col for col in available_criteria.values() if col in df.columns]].copy()
        
        # Renombrar columnas
        rename_dict = {"run_name": "Run", "pregunta": "Pregunta", "avg_criteria_score": "Score Promedio"}
        for criterion, col in available_criteria.items():
            if col in prob_display.columns:
                rename_dict[col] = criterion
        
        prob_display = prob_display.rename(columns=rename_dict)
        
        # Formatear
        for col in prob_display.columns:
            if col not in ["Run", "Pregunta"]:
                prob_display[col] = prob_display[col].apply(lambda x: f"{x*100:.0f}%" if pd.notna(x) else "N/A")
        
        st.dataframe(prob_display, use_container_width=True)
    else:
        st.success("✅ ¡Todas las preguntas superan el umbral establecido!")

st.markdown("---")

# =====================================================
# 6. VISUALIZACIÓN DE RAZONAMIENTOS
# =====================================================
st.header("💭 Razonamientos del Evaluador")

# Selector de pregunta
selected_run = st.selectbox(
    "Selecciona una pregunta para ver razonamientos:",
    options=df['run_name'].tolist(),
    format_func=lambda x: f"{x} - {df[df['run_name']==x]['pregunta'].iloc[0][:50]}..."
)

if selected_run:
    run_id = df[df['run_name'] == selected_run]['run_id'].iloc[0]
    
    # Obtener artefactos
    artifacts = client.list_artifacts(run_id)
    
    # Buscar directorio de reasoning
    reasoning_dir = [a for a in artifacts if a.path == 'reasoning' and a.is_dir]
    
    reasoning_artifacts = []
    if reasoning_dir:
        # Listar archivos dentro del directorio reasoning
        reasoning_artifacts = client.list_artifacts(run_id, 'reasoning')
        reasoning_artifacts = [a for a in reasoning_artifacts if a.path.endswith('.txt')]
    
    if reasoning_artifacts:
        st.subheader("📝 Pregunta y Respuestas")
        
        # Mostrar pregunta, respuesta esperada y generada
        try:
            question_artifact = [a for a in artifacts if 'question.txt' in a.path]
            if question_artifact:
                question_path = client.download_artifacts(run_id, question_artifact[0].path)
                with open(question_path, 'r', encoding='utf-8') as f:
                    st.info(f"❓ **Pregunta:** {f.read()}")
        except:
            pass
        
        try:
            expected_artifact = [a for a in artifacts if 'expected_answer.txt' in a.path]
            if expected_artifact:
                expected_path = client.download_artifacts(run_id, expected_artifact[0].path)
                with open(expected_path, 'r', encoding='utf-8') as f:
                    st.success(f"✅ **Respuesta Esperada:** {f.read()}")
        except:
            pass
        
        try:
            generated_artifact = [a for a in artifacts if 'generated_answer.txt' in a.path]
            if generated_artifact:
                generated_path = client.download_artifacts(run_id, generated_artifact[0].path)
                with open(generated_path, 'r', encoding='utf-8') as f:
                    st.warning(f"🤖 **Respuesta Generada:** {f.read()}")
        except:
            pass
        
        st.markdown("---")
        st.subheader("💭 Razonamientos por Criterio")
        
        # Diccionario de traducción de criterios
        criterion_translations = {
            "coherence": "Coherencia",
            "conciseness": "Concisión",
            "correctness": "Corrección",
            "harmfulness": "Daño Potencial",
            "helpfulness": "Utilidad",
            "relevance": "Relevancia",
            "toxicity": "Toxicidad"
        }
        
        # Mostrar razonamientos
        for artifact in reasoning_artifacts:
            try:
                reasoning_path = client.download_artifacts(run_id, artifact.path)
                # Extraer nombre del criterio del path
                criterion_key = artifact.path.split('/')[-1].replace('_reasoning.txt', '').lower()
                criterion_name = criterion_translations.get(criterion_key, criterion_key.title())
                
                with open(reasoning_path, 'r', encoding='utf-8') as f:
                    reasoning_text = f.read()
                
                with st.expander(f"🔍 {criterion_name}"):
                    st.write(reasoning_text)
            except Exception as e:
                st.error(f"Error leyendo {artifact.path}: {e}")
    else:
        st.info("ℹ️ No hay razonamientos disponibles para esta pregunta")

st.markdown("---")

# Footer
st.markdown("### 🎯 Dashboard creado para GenAIOps - PyCon 2025")
st.markdown("**Parte 4 del Desafío Estudiante** - Evaluación Multidimensional con LabeledCriteriaEvalChain")
