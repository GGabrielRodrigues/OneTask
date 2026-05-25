# ===== Dockerfile — OneTask =====
# Build completo para produção com Gunicorn

FROM python:3.12-slim

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia o código-fonte
COPY . .

# Cria diretório para arquivos estáticos (caso não exista)
RUN mkdir -p staticfiles

# Coleta arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expõe a porta
EXPOSE $PORT

# Entrypoint: aplica migrations e inicia o gunicorn
CMD sh -c "python manage.py migrate --noinput && \
           gunicorn onetask_project.wsgi:application \
           --bind 0.0.0.0:${PORT} \
           --workers 2 \
           --timeout 120"
