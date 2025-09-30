# backend/ai_service.py

import httpx
import numpy as np
import cv2
from PIL import Image
import io
from rembg import remove
import mediapipe as mp
import json
import os
import sys
import shutil

# --- Funções Auxiliares ---

def download_image(url: str) -> np.ndarray:
    """Baixa uma imagem de uma URL e a converte para um array NumPy (formato OpenCV)."""
    try:
        response = httpx.get(url, follow_redirects=True)
        response.raise_for_status()
        image_array = np.frombuffer(response.content, np.uint8)
        return cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    except httpx.RequestError as e:
        print(f"Erro de rede ao baixar a imagem {url}: {e}")
        raise
    except Exception as e:
        print(f"Erro ao processar a imagem {url}: {e}")
        raise

def save_image_to_buffer(image: np.ndarray) -> io.BytesIO:
    """Salva uma imagem (array NumPy BGR ou BGRA) em um buffer de bytes em memória."""
    if image.shape[2] == 4:
        image_rgba = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        pil_image = Image.fromarray(image_rgba)
    else:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
    
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# --- Lógica Principal do Serviço de IA ---

def detect_pose_keypoints(image: np.ndarray, output_dir: str = "debug_images") -> str:
    """
    Detecta os pontos-chave da pose humana na imagem usando MediaPipe,
    salva a imagem com os pontos desenhados e um arquivo JSON com as coordenadas.
    """
    print("Executando detecção de pose com MediaPipe...")

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        print("Nenhum ponto de referência de pose detectado.")
        return None

    annotated_image = image.copy()
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
        mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pose_image_path = os.path.join(output_dir, "debug_02_pose_estimation.png")
    cv2.imwrite(pose_image_path, annotated_image)
    print(f"Imagem com pose salva em: {pose_image_path}")

    h, w, _ = image.shape
    keypoints = []
    for landmark in results.pose_landmarks.landmark:
        keypoints.append({
            "x": landmark.x * w,
            "y": landmark.y * h,
            "z": landmark.z,
            "visibility": landmark.visibility,
        })

    keypoints_path = os.path.join(output_dir, "debug_02_pose_keypoints.json")
    with open(keypoints_path, "w") as f:
        json.dump(keypoints, f, indent=4)
    print(f"Pontos-chave da pose salvos em: {keypoints_path}")

    pose.close()
    return keypoints_path

def segment_garment(image: np.ndarray) -> np.ndarray:
    """Usa a biblioteca rembg para remover o fundo da imagem da roupa."""
    print("Executando remoção de fundo com rembg...")
    _, img_encoded = cv2.imencode('.png', image)
    image_bytes = img_encoded.tobytes()
    output_bytes = remove(image_bytes)
    output_array = np.frombuffer(output_bytes, np.uint8)
    output_bgra = cv2.imdecode(output_array, cv2.IMREAD_UNCHANGED)
    print("Remoção de fundo concluída.")
    return output_bgra

# Adicionar o diretório do modelo IDM-VTON ao sys.path
idm_vton_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "idm_vton_model"))
if idm_vton_path not in sys.path:
    sys.path.append(idm_vton_path)

# Imports do IDM-VTON e outras libs de IA
import torch
from transformers import (
    CLIPImageProcessor,
    CLIPVisionModelWithProjection,
    CLIPTextModel,
    CLIPTextModelWithProjection,
    AutoTokenizer,
)
from diffusers import DDPMScheduler, AutoencoderKL
from typing import List

# Imports dos scripts locais do IDM-VTON
from src.tryon_pipeline import StableDiffusionXLInpaintPipeline as TryonPipeline
from src.unet_hacked_garmnet import UNet2DConditionModel as UNet2DConditionModel_ref
from src.unet_hacked_tryon import UNet2DConditionModel
from gradio_demo.utils_mask import get_mask_location
from torchvision import transforms
from gradio_demo import apply_net
from preprocess.humanparsing.run_parsing import Parsing
from preprocess.openpose.run_openpose import OpenPose
from detectron2.data.detection_utils import convert_PIL_to_numpy, _apply_exif_orientation
from torchvision.transforms.functional import to_pil_image

# --- Gerenciamento de Modelos ---
# Dicionário global para armazenar os modelos carregados e evitar recarregá-los
models = {}
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

def load_models():
    """Carrega todos os modelos necessários para a inferência e os armazena no dicionário global."""
    if "pipeline_loaded" in models:
        print("Modelos já carregados.")
        return

    print("Carregando modelos de IA... Isso pode levar alguns minutos na primeira vez.")
    base_path = 'yisol/IDM-VTON'
    
    unet = UNet2DConditionModel.from_pretrained(
        base_path, subfolder="unet", torch_dtype=torch.float16
    )
    unet.requires_grad_(False)
    
    tokenizer_one = AutoTokenizer.from_pretrained(
        base_path, subfolder="tokenizer", use_fast=False
    )
    tokenizer_two = AutoTokenizer.from_pretrained(
        base_path, subfolder="tokenizer_2", use_fast=False
    )
    noise_scheduler = DDPMScheduler.from_pretrained(base_path, subfolder="scheduler")
    text_encoder_one = CLIPTextModel.from_pretrained(
        base_path, subfolder="text_encoder", torch_dtype=torch.float16
    )
    text_encoder_two = CLIPTextModelWithProjection.from_pretrained(
        base_path, subfolder="text_encoder_2", torch_dtype=torch.float16
    )
    image_encoder = CLIPVisionModelWithProjection.from_pretrained(
        base_path, subfolder="image_encoder", torch_dtype=torch.float16
    )
    vae = AutoencoderKL.from_pretrained(
        base_path, subfolder="vae", torch_dtype=torch.float16
    )
    unet_encoder = UNet2DConditionModel_ref.from_pretrained(
        base_path, subfolder="unet_encoder", torch_dtype=torch.float16
    )

    # Modelos de pré-processamento
    parsing_model = Parsing(0) # Usa GPU 0 se disponível
    openpose_model = OpenPose(0) # Usa GPU 0 se disponível

    # Mover modelos para o dispositivo
    unet_encoder.requires_grad_(False)
    image_encoder.requires_grad_(False)
    vae.requires_grad_(False)
    text_encoder_one.requires_grad_(False)
    text_encoder_two.requires_grad_(False)

    pipe = TryonPipeline.from_pretrained(
        base_path,
        unet=unet,
        vae=vae,
        feature_extractor=CLIPImageProcessor(),
        text_encoder=text_encoder_one,
        text_encoder_2=text_encoder_two,
        tokenizer=tokenizer_one,
        tokenizer_2=tokenizer_two,
        scheduler=noise_scheduler,
        image_encoder=image_encoder,
        torch_dtype=torch.float16,
    )
    pipe.unet_encoder = unet_encoder
    
    models['pipe'] = pipe
    models['parsing_model'] = parsing_model
    models['openpose_model'] = openpose_model
    models['tensor_transform'] = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),
    ])
    
    # Carregar modelo DensePose
    # Os argumentos são baseados no script `gradio_demo/app.py`
    densepose_args = apply_net.create_argument_parser().parse_args(
        ('show', 
         os.path.join(idm_vton_path, 'configs/densepose_rcnn_R_50_FPN_s1x.yaml'), 
         os.path.join(idm_vton_path, 'ckpt/densepose/model_final_162be9.pkl'), 
         'dp_segm', '-v', '--opts', 'MODEL.DEVICE', device)
    )
    models['densepose_args'] = densepose_args

    models["pipeline_loaded"] = True
    print("Todos os modelos foram carregados com sucesso.")

# Chame a função para carregar os modelos quando o serviço iniciar
load_models()


def generate_tryon_image_idm_vton(body_image_path: str, garment_image_path: str, garment_desc: str = "a piece of clothing") -> np.ndarray:
    """
    Gera a imagem de try-on usando o pipeline completo do IDM-VTON.
    """
    print("Iniciando geração de imagem com pipeline IDM-VTON completo...")
    
    # --- Carregar modelos do dicionário global ---
    pipe = models['pipe']
    parsing_model = models['parsing_model']
    openpose_model = models['openpose_model']
    tensor_transform = models['tensor_transform']
    densepose_args = models['densepose_args']

    # Mover modelos para o dispositivo (GPU/CPU)
    openpose_model.preprocessor.body_estimation.model.to(device)
    pipe.to(device)
    pipe.unet_encoder.to(device)

    # --- Preparar imagens de entrada ---
    garm_img = Image.open(garment_image_path).convert("RGB").resize((768, 1024))
    human_img = Image.open(body_image_path).convert("RGB").resize((768, 1024))

    # --- Etapa 1: Gerar máscara agnóstica, pose e segmentação ---
    # Lógica adaptada de `gradio_demo/app.py`
    human_img_resized_for_models = human_img.resize((384, 512))
    
    # OpenPose
    keypoints = openpose_model(human_img_resized_for_models)
    
    # Human Parsing
    model_parse, _ = parsing_model(human_img_resized_for_models)
    
    # Criar máscara (assumindo 'upper_body' por padrão)
    mask, _ = get_mask_location('hd', "upper_body", model_parse, keypoints)
    mask = mask.resize((768, 1024))

    # DensePose
    human_img_for_densepose = _apply_exif_orientation(human_img_resized_for_models)
    human_img_for_densepose = convert_PIL_to_numpy(human_img_for_densepose, format="BGR")
    pose_img = densepose_args.func(densepose_args, human_img_for_densepose)
    pose_img = pose_img[:, :, ::-1]
    pose_img = Image.fromarray(pose_img).resize((768, 1024))

    # --- Etapa 2: Chamar o pipeline de difusão ---
    with torch.no_grad():
        with torch.cuda.amp.autocast():
            # Preparar embeddings de texto
            prompt = "model is wearing " + garment_desc
            negative_prompt = "monochrome, lowres, bad anatomy, worst quality, low quality"
            
            with torch.inference_mode():
                prompt_embeds, neg_prompt_embeds, pooled_prompt_embeds, neg_pooled_prompt_embeds = pipe.encode_prompt(
                    prompt, num_images_per_prompt=1, do_classifier_free_guidance=True, negative_prompt=negative_prompt
                )
                
                cloth_prompt = "a photo of " + garment_desc
                prompt_embeds_c, _, _, _ = pipe.encode_prompt(
                    cloth_prompt, num_images_per_prompt=1, do_classifier_free_guidance=False
                )

            # Preparar tensores de imagem
            pose_tensor = tensor_transform(pose_img).unsqueeze(0).to(device, torch.float16)
            garm_tensor = tensor_transform(garm_img).unsqueeze(0).to(device, torch.float16)
            
            generator = torch.Generator(device).manual_seed(42)

            # Executar o pipeline
            images = pipe(
                prompt_embeds=prompt_embeds.to(device, torch.float16),
                negative_prompt_embeds=neg_prompt_embeds.to(device, torch.float16),
                pooled_prompt_embeds=pooled_prompt_embeds.to(device, torch.float16),
                negative_pooled_prompt_embeds=neg_pooled_prompt_embeds.to(device, torch.float16),
                num_inference_steps=30,
                generator=generator,
                strength=1.0,
                pose_img=pose_tensor,
                text_embeds_cloth=prompt_embeds_c.to(device, torch.float16),
                cloth=garm_tensor,
                mask_image=mask,
                image=human_img,
                height=1024,
                width=768,
                ip_adapter_image=garm_img.resize((768, 1024)),
                guidance_scale=2.0,
            )[0]

    # --- Etapa 3: Pós-processar e retornar a imagem ---
    final_image_pil = images[0]
    # Converter de PIL (RGB) para NumPy array (BGR) para o OpenCV
    final_image_np = np.array(final_image_pil)
    final_image_bgr = cv2.cvtColor(final_image_np, cv2.COLOR_RGB2BGR)
    
    print("Geração de imagem com IDM-VTON concluída.")
    return final_image_bgr

# --- Função Principal de Orquestração ---

def process_tryon_images(body_image_url: str, garment_image_url: str, garment_desc: str) -> io.BytesIO:
    """Orquestra o processo completo de virtual try-on."""
    print("Iniciando processo de Virtual Try-On com pipeline completo...")
    
    # Diretório para salvar imagens temporárias para o processo
    temp_dir = "temp_processing_images"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Baixar imagens
    body_image = download_image(body_image_url)
    garment_image = download_image(garment_image_url)
    
    # Salvar imagens em arquivos temporários, pois o pipeline espera caminhos de arquivo
    body_image_path = os.path.join(temp_dir, f"{uuid.uuid4()}.png")
    garment_image_path = os.path.join(temp_dir, f"{uuid.uuid4()}.png")
    cv2.imwrite(body_image_path, body_image)
    cv2.imwrite(garment_image_path, garment_image)

    try:
        # Chamar a função de geração de imagem principal e completa
        # A descrição da roupa é passada como um parâmetro
        final_image = generate_tryon_image_idm_vton(body_image_path, garment_image_path, garment_desc)
        
        # Salvar resultado final para depuração
        output_dir = "debug_images"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        final_image_path = os.path.join(output_dir, "debug_final_result.png")
        cv2.imwrite(final_image_path, final_image)
        
        # Converter a imagem final para um buffer de bytes para ser retornado pela API
        output_buffer = save_image_to_buffer(final_image)
        
        print("Processo de Virtual Try-On concluído com sucesso.")
        return output_buffer
    finally:
        # Limpar os arquivos temporários
        print("Limpando arquivos temporários...")
        if os.path.exists(body_image_path):
            os.remove(body_image_path)
        if os.path.exists(garment_image_path):
            os.remove(garment_image_path)