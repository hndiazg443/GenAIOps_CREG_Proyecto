#!/usr/bin/env python
"""
Script de verificación de instalación del proyecto GenAIOps
Verifica que todos los componentes estén correctamente instalados
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.10+")
        return False

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("\n📦 Verificando dependencias...")
    required = [
        'langchain',
        'langchain_classic',
        'langchain_openai',
        'langchain_community',
        'openai',
        'streamlit',
        'mlflow',
        'plotly',
        'faiss',
        'python-dotenv'
    ]
    
    all_installed = True
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NO INSTALADO")
            all_installed = False
    
    return all_installed

def check_env_file():
    """Verifica el archivo .env"""
    print("\n🔐 Verificando archivo .env...")
    env_path = Path('.env')
    
    if not env_path.exists():
        print("   ❌ Archivo .env no existe")
        print("      Copia .env.example a .env y configura tu API Key")
        return False
    
    with open(env_path) as f:
        content = f.read()
    
    if 'OPENAI_API_KEY=' not in content:
        print("   ❌ OPENAI_API_KEY no configurada")
        return False
    
    if 'tu-api-key-aqui' in content or 'your-api-key-here' in content:
        print("   ⚠️  OPENAI_API_KEY no parece estar configurada correctamente")
        return False
    
    print("   ✅ Archivo .env configurado")
    return True

def check_directories():
    """Verifica directorios necesarios"""
    print("\n📁 Verificando estructura de directorios...")
    required_dirs = [
        'app',
        'app/prompts',
        'data/pdfs',
        'tests'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ - NO EXISTE")
            all_exist = False
    
    return all_exist

def check_pdfs():
    """Verifica que existan PDFs"""
    print("\n📄 Verificando documentos PDF...")
    pdf_dir = Path('data/pdfs')
    
    if not pdf_dir.exists():
        print("   ❌ Directorio data/pdfs/ no existe")
        return False
    
    pdfs = list(pdf_dir.glob('*.pdf'))
    if len(pdfs) == 0:
        print("   ❌ No hay PDFs en data/pdfs/")
        return False
    
    print(f"   ✅ {len(pdfs)} documentos PDF encontrados")
    for pdf in pdfs:
        print(f"      • {pdf.name}")
    
    return True

def check_vectorstore():
    """Verifica si el vectorstore existe"""
    print("\n🗃️  Verificando vectorstore...")
    vectorstore_dir = Path('vectorstore')
    
    if not vectorstore_dir.exists():
        print("   ⚠️  Vectorstore no existe - Ejecuta: python -c 'from app.rag_pipeline import save_vectorstore; save_vectorstore()'")
        return False
    
    index_file = vectorstore_dir / 'index.faiss'
    if not index_file.exists():
        print("   ⚠️  index.faiss no encontrado")
        return False
    
    print(f"   ✅ Vectorstore existe ({index_file.stat().st_size / 1024:.1f} KB)")
    return True

def check_prompts():
    """Verifica que existan los prompts"""
    print("\n📝 Verificando prompts...")
    prompts_dir = Path('app/prompts')
    
    if not prompts_dir.exists():
        print("   ❌ Directorio app/prompts/ no existe")
        return False
    
    prompts = list(prompts_dir.glob('*.txt'))
    if len(prompts) == 0:
        print("   ❌ No hay prompts en app/prompts/")
        return False
    
    print(f"   ✅ {len(prompts)} prompts encontrados")
    for prompt in prompts:
        print(f"      • {prompt.name}")
    
    return True

def check_eval_dataset():
    """Verifica el dataset de evaluación"""
    print("\n📊 Verificando dataset de evaluación...")
    dataset_path = Path('tests/eval_dataset_creg.json')
    
    if not dataset_path.exists():
        print("   ❌ tests/eval_dataset_creg.json no existe")
        return False
    
    print(f"   ✅ Dataset de evaluación existe")
    return True

def main():
    """Función principal"""
    print("="*60)
    print("🔍 VERIFICACIÓN DE INSTALACIÓN - GenAIOps CREG")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_env_file(),
        check_directories(),
        check_pdfs(),
        check_prompts(),
        check_eval_dataset(),
        check_vectorstore()
    ]
    
    print("\n" + "="*60)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ VERIFICACIÓN COMPLETA: {passed}/{total} checks pasados")
        print("\n🎉 ¡Todo está listo! Puedes ejecutar:")
        print("   • streamlit run app/ui_streamlit.py")
        print("   • streamlit run app/dashboard_advanced.py")
        print("   • python app/run_eval_advanced.py")
    elif passed >= total - 1 and not checks[-1]:
        print(f"⚠️  CASI LISTO: {passed}/{total} checks pasados")
        print("\n⚡ Genera el vectorstore con:")
        print("   python -c 'from app.rag_pipeline import save_vectorstore; save_vectorstore()'")
    else:
        print(f"❌ VERIFICACIÓN INCOMPLETA: {passed}/{total} checks pasados")
        print("\nRevisa los errores arriba y corrige antes de continuar.")
    
    print("="*60)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
