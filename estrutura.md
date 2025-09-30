# Estrutura do Projeto VTO-Arenque

Este documento descreve a estrutura técnica, as principais tecnologias e a organização dos arquivos do projeto de provador virtual.

## 1. Framework Principal

O backend da aplicação é construído utilizando **FastAPI**, um framework web moderno e de alta performance para Python.

## 2. Linguagens e Tipos de Arquivos

- **Linguagem Principal**: Python
- **Frontend**: JavaScript (React)
- **Configuração de Ambiente**: `.env`, `.env.example`
- **Dados e Configuração**: `.json`
- **Conteinerização**: `Dockerfile`, `.dockerignore`
- **Documentação**: `.md`

## 3. Bibliotecas de IA

O núcleo de IA do projeto utiliza um conjunto de bibliotecas especializadas para processamento de imagem e modelos generativos:

- **Core**: PyTorch (`torch`, `torchvision`)
- **Processamento de Imagem**: OpenCV (`opencv-python`), MediaPipe (`mediapipe`), `rembg`
- **Modelos Generativos/Transformers**: Transformers, Diffusers
- **Execução de Modelos**: ONNX Runtime (`onnxruntime`)

## 4. Arquivos Grandes (Modelos de IA)

Os modelos de IA pré-treinados e os checkpoints, que são arquivos grandes, estão localizados no diretório:

- **`backend/idm_vton_model/ckpt/`**

Dentro deste diretório, os modelos são organizados em subpastas como `densepose`, `humanparsing`, e `openpose`, contendo arquivos como `.pkl` e `.onnx`.

## 5. Estrutura de Diretórios (Completa)

```
/
├── backend/
│   ├── main.py             # Ponto de entrada da API FastAPI
│   ├── ai_service.py       # Lógica do pipeline de IA
│   ├── requirements.txt    # Dependências Python
│   ├── Dockerfile          # Configuração do contêiner
│   ├── .env                # Variáveis de ambiente (local)
│   ├── __pycache__/        # Cache de bytecode Python
│   ├── venv/               # Ambiente virtual Python
│   ├── debug_images/       # Imagens de depuração do processo de IA
│   └── idm_vton_model/     # Modelo de IA para Virtual Try-On
│       └── ckpt/           # Checkpoints e pesos dos modelos
│
├── frontend/
│   ├── package.json        # Dependências e scripts do Node.js
│   ├── node_modules/       # Pacotes Node.js instalados
│   ├── src/
│   │   ├── App.js          # Componente principal do React
│   │   └── VirtualTryOn.js # Componente da interface do provador
│   └── public/
│       └── index.html      # Ponto de entrada do HTML
│
├── gemini-cli/             # Arquivos de contexto e relatórios do Gemini
│   ├── gemini-relatorio.md
│   └── proxima-etapa.md
│
├── logs/                   # Logs de execução e versionamento
│   ├── log-supabase.md
│   └── log-terminal.md
│
├── .gitignore              # Arquivos e pastas ignorados pelo Git
├── GEMINI.md               # Documentação e estratégia do projeto
├── README.md               # Documentação geral do projeto
└── estrutura.md            # Este arquivo
```
