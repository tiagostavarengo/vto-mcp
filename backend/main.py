import os
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Validação básica das variáveis de ambiente
if not all([SUPABASE_URL, SUPABASE_SERVICE_KEY]):
    raise ValueError("SUPABASE_URL e SUPABASE_SERVICE_KEY devem ser definidos no arquivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

app = FastAPI()

# Configuração do CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Endereço do seu frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependência para validar o token JWT do Supabase
async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Esquema de autorização inválido")

    token = authorization.split(" ")[1]
    try:
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        if not user:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
        return user
    except Exception as e:
        # O Supabase pode lançar uma exceção específica que podemos capturar melhor
        # mas para um MVP, uma captura geral é suficiente.
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

@app.get("/")
def read_root():
    return {"message": "Backend do Provador Virtual está no ar!"}

@app.get("/api/protected")
def read_protected_data(current_user: dict = Depends(get_current_user)):
    """
    Um endpoint protegido que só pode ser acessado com um token válido.
    """
    return {
        "message": "Olá, você acessou um endpoint protegido com sucesso!",
        "user_email": current_user.email,
        "user_id": current_user.id,
    }

from pydantic import BaseModel, HttpUrl
from ai_service import process_tryon_images # Importa o nosso novo serviço
import uuid # Para gerar nomes de arquivo únicos
import traceback # Importar o módulo traceback

class TryOnRequest(BaseModel):
    body_image_url: HttpUrl
    garment_image_url: HttpUrl
    garment_description: str = "a piece of clothing" # Adiciona o campo com um valor padrão

@app.post("/api/tryon")
async def virtual_tryon(request: TryOnRequest, current_user: dict = Depends(get_current_user)):
    """
    Recebe as URLs da imagem do corpo e da roupa, aciona o serviço de IA,
    salva o resultado e retorna a URL da imagem processada.
    """
    try:
        # 1. Chamar o serviço de IA para processar as imagens
        # A função agora aceita a descrição da roupa
        image_buffer = process_tryon_images(
            str(request.body_image_url),
            str(request.garment_image_url),
            request.garment_description
        )

        # 2. Fazer upload do resultado para um novo bucket no Supabase
        file_name = f"result-{current_user.id}-{uuid.uuid4()}.png"
        
        # O método upload espera bytes, então usamos .getvalue()
        response = supabase.storage.from_("results_photos").upload(
            file=image_buffer.getvalue(),
            path=file_name,
            file_options={"content-type": "image/png"}
        )

        # 3. Obter a URL pública da imagem recém-criada
        public_url = supabase.storage.from_("results_photos").get_public_url(file_name)

        return {
            "message": "Imagem processada com sucesso!",
            "processed_image_url": public_url
        }

    except Exception as e:
        print(f"Ocorreu um erro durante o processo de try-on: {e}")
        traceback.print_exc() # Imprime o traceback completo
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")
