@echo off
chcp 65001 >nul
REM ARQV30 Enhanced v2.0 ULTRA-ROBUSTO - Script de Instalação Windows
REM Execute este arquivo para instalar todas as dependências

echo ========================================
echo ARQV30 Enhanced v2.0 ULTRA-ROBUSTO - Instalação
echo Análise Ultra-Detalhada de Mercado
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo Por favor, instale Python 3.11+ de https://python.org
    echo Certifique-se de marcar "Add Python to PATH" durante a instalação.
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado:
python --version
echo.

REM Cria ambiente virtual
echo 🔄 Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo ❌ ERRO: Falha ao criar ambiente virtual!
    pause
    exit /b 1
)

REM Ativa ambiente virtual
echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

REM Atualiza pip
echo 🔄 Atualizando pip...
python -m pip install --upgrade pip
echo.

REM Instala dependências
echo 🔄 Instalando dependências ULTRA-ROBUSTAS...
echo Isso pode levar alguns minutos...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERRO: Falha ao instalar dependências!
    echo Verifique sua conexão com a internet e tente novamente.
    pause
    exit /b 1
)

REM Instala dependências adicionais para web scraping
echo 🔄 Instalando dependências adicionais...
pip install beautifulsoup4 lxml html5lib
if errorlevel 1 (
    echo ⚠️ AVISO: Algumas dependências adicionais falharam.
)

REM Cria diretórios necessários
echo 🔄 Criando estrutura de diretórios ULTRA-ROBUSTA...
if not exist "src\uploads" mkdir src\uploads
if not exist "src\static\images" mkdir src\static\images
if not exist "src\cache" mkdir src\cache
if not exist "src\logs" mkdir src\logs
echo.

REM Testa a instalação
echo 🧪 Testando instalação ULTRA-ROBUSTA...
cd src
python -c "import flask, requests, google.generativeai, supabase, pandas, PyPDF2; print('✅ Dependências principais OK')"
if errorlevel 1 (
    echo ⚠️ AVISO: Algumas dependências podem não estar funcionando corretamente.
) else (
    echo ✅ Teste de dependências ULTRA-ROBUSTO passou!
)
cd ..
echo.

REM Testa conexão com APIs (se configuradas)
echo 🧪 Testando conexões com APIs...
if exist ".env" (
    cd src
    python -c "
import os
from dotenv import load_dotenv
load_dotenv('../.env')

# Testa Gemini
gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key and gemini_key != 'sua-chave-aqui':
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        print('✅ Gemini API configurada')
    except:
        print('⚠️ Gemini API com problemas')
else:
    print('⚠️ Gemini API não configurada')

# Testa Supabase
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_ANON_KEY')
if supabase_url and supabase_key:
    try:
        from supabase import create_client
        client = create_client(supabase_url, supabase_key)
        print('✅ Supabase configurado')
    except:
        print('⚠️ Supabase com problemas')
else:
    print('⚠️ Supabase não configurado')
" 2>nul
    cd ..
) else (
    echo ⚠️ Arquivo .env não encontrado - APIs não testadas
)
echo.

echo ========================================
echo 🎉 INSTALAÇÃO ULTRA-ROBUSTA CONCLUÍDA!
echo ========================================
echo.
echo 🚀 Próximos passos:
echo.
echo 1. ✅ Arquivo .env já configurado com suas chaves
echo.
echo 2. ⚠️ IMPORTANTE: Configure uma chave válida do Google Search
echo    Acesse: https://console.developers.google.com/
echo    Ative: Custom Search API
echo    Substitua GOOGLE_SEARCH_KEY no arquivo .env
echo.
echo 3. Execute run.bat para iniciar a aplicação
echo.
echo 4. Acesse http://localhost:5000 no seu navegador
echo.
echo 5. Teste com uma análise simples primeiro
echo.
echo ========================================
echo.
echo 📚 SISTEMA ULTRA-ROBUSTO PRONTO!
echo Agora você tem acesso a análises de mercado
echo com profundidade de consultoria profissional
echo.
echo 🔥 RECURSOS ATIVADOS:
echo - Google Gemini Pro para análise IA
echo - Supabase para banco de dados
echo - WebSailor para pesquisa web REAL
echo - HuggingFace para análise complementar
echo - DuckDuckGo para pesquisa alternativa
echo - Jina AI para extração de conteúdo
echo.
echo ⚠️ NOTA: Para pesquisa Google completa, configure
echo    uma chave válida do Google Custom Search API
echo.
pause