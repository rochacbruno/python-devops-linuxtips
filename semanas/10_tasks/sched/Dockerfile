FROM python:3.11-slim

# Instalar dependências mínimas
RUN pip install --no-cache-dir flask

# Criar diretório de trabalho
WORKDIR /app

# Criar a aplicação diretamente no Dockerfile
RUN echo 'from flask import Flask, jsonify\n\
import os\n\
\n\
app = Flask(__name__)\n\
\n\
# Contador de requests para simular falha\n\
request_count = 0\n\
\n\
@app.route("/health")\n\
def health():\n\
    global request_count\n\
    request_count += 1\n\
    \n\
    # A cada 10 requests, retorna status não saudável\n\
    if request_count % 10 == 0:\n\
        return jsonify({\n\
            "status": "unhealthy",\n\
            "message": "Simulação de falha",\n\
            "request_count": request_count\n\
        }), 503\n\
    \n\
    return jsonify({\n\
        "status": "healthy",\n\
        "message": "API está funcionando",\n\
        "request_count": request_count\n\
    }), 200\n\
\n\
if __name__ == "__main__":\n\
    app.run(host="0.0.0.0", port=8000)\n\
' > app.py

# Expor a porta
EXPOSE 8000

# Comando para executar a aplicação
CMD ["python", "app.py"]

