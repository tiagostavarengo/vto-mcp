# Use uma imagem base da NVIDIA com CUDA e Python. Isso garante que a GPU seja utilizável.
# A versão do CUDA deve ser compatível com a versão do PyTorch instalada.
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# Evita que o apt-get peça interação durante o build
ENV DEBIAN_FRONTEND=noninteractive

# Instala Python, pip e dependências de sistema para libs como OpenCV
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências Python
# A instalação do torch é ajustada para garantir a compatibilidade com CUDA 12.1
RUN pip3 install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121

# Copia todo o resto do código do backend para o diretório de trabalho no contêiner
# Isso inclui main.py, ai_service.py, e o diretório idm_vton_model com seus checkpoints
COPY . .

# Expõe a porta em que o Uvicorn irá rodar
EXPOSE 8000

# Comando para iniciar a aplicação quando o contêiner for executado
# Usa 0.0.0.0 para ser acessível de fora do contêiner
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
