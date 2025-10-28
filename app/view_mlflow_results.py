"""
Script para visualizar resultados de evaluación desde MLflow
"""

import mlflow
import pandas as pd

# Conectar al experimento
experiment_name = "eval_advanced_v1_asistente_creg_didactico"
experiment = mlflow.get_experiment_by_name(experiment_name)

if experiment is None:
    print(f"❌ Experimento '{experiment_name}' no encontrado")
    exit(1)

print(f"📊 Analizando experimento: {experiment_name}")
print(f"🆔 Experiment ID: {experiment.experiment_id}")
print("="*80)

# Obtener todas las runs del experimento
runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])

if runs.empty:
    print("⚠️  No se encontraron runs en este experimento")
    exit(0)

print(f"\n✅ Total de runs encontradas: {len(runs)}")

# Mostrar métricas clave
print("\n📈 RESUMEN DE MÉTRICAS POR PREGUNTA:")
print("="*80)

metrics_of_interest = [
    'metrics.qa_is_correct',
    'metrics.correctness_score',
    'metrics.relevance_score',
    'metrics.coherence_score',
    'metrics.toxicity_score',
    'metrics.harmfulness_score',
    'metrics.helpfulness_score',
    'metrics.conciseness_score',
    'metrics.avg_criteria_score'
]

# Filtrar columnas que existen
available_metrics = [col for col in metrics_of_interest if col in runs.columns]

if available_metrics:
    results = runs[['tags.mlflow.runName'] + available_metrics].copy()
    
    # Renombrar columnas para mejor visualización
    results.columns = [col.replace('metrics.', '').replace('tags.mlflow.', '') 
                       for col in results.columns]
    
    # Ordenar por nombre de run
    results = results.sort_values('runName')
    
    print(results.to_string(index=False))
    
    # Calcular estadísticas generales
    print("\n" + "="*80)
    print("📊 ESTADÍSTICAS GENERALES:")
    print("="*80)
    
    for metric in available_metrics:
        metric_name = metric.replace('metrics.', '')
        if metric in runs.columns:
            mean_val = runs[metric].mean()
            print(f"{metric_name:30s}: {mean_val:.2f} (promedio)")
    
    # Contar correctas
    if 'metrics.qa_is_correct' in runs.columns:
        correctas = runs['metrics.qa_is_correct'].sum()
        total = len(runs)
        print(f"\n✅ Preguntas correctas (QA básico): {correctas}/{total} ({correctas/total*100:.1f}%)")
    
    if 'metrics.avg_criteria_score' in runs.columns:
        avg_criteria = runs['metrics.avg_criteria_score'].mean()
        print(f"📊 Score promedio de criterios: {avg_criteria:.2f}")
    
else:
    print("⚠️  No se encontraron métricas en las runs")

print("\n" + "="*80)
print("💡 Para ver más detalles, ejecuta: mlflow ui")
print("   Luego abre http://localhost:5000 en tu navegador")
print("="*80)
