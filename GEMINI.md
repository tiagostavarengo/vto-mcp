# Estratégia de Desenvolvimento do MVP de Provador Virtual (Evolução)

Este documento detalha a nova abordagem técnica para o MVP do provador virtual, com base na análise do relatório de progresso e em uma estratégia alinhada com as melhores práticas da indústria. A abordagem anterior, baseada em `overlay` e `TPS warping`, foi substituída por um pipeline que utiliza modelos de IA generativa para criar um resultado mais realista e convincente.

## 1. Visão Geral da Nova Arquitetura

A solução será baseada em uma arquitetura de microsserviços. O frontend e o backend (`FastAPI`) permanecem, mas o serviço de IA será totalmente reestruturado para implementar um processo de "geração de imagem" em vez de uma simples deformação geométrica.

- **Frontend (React)**: Interface de usuário para upload de fotos.
- **Backend (FastAPI)**: API que recebe as imagens, orquestra o pipeline de IA e retorna a imagem final.
- **Serviço de IA (Python/PyTorch)**: O núcleo da solução. Responsável por todo o processamento computacionalmente intensivo na nuvem.

## 2. O Pipeline de IA (Passo a Passo)

A nova abordagem é mais complexa, mas garante um resultado final de alta qualidade, semelhante ao que é esperado de soluções como a Doris.ai.

### 2.1. Pré-processamento e Análise de Imagem

- **Entrada**: Duas imagens – uma do usuário (corpo inteiro) e uma da peça de roupa.
- **Remoção de Fundo (Ambas as Imagens)**: Utilize a biblioteca `rembg` para remover o fundo tanto da foto do usuário quanto da foto da roupa. Isso isola o objeto de interesse (o corpo e a roupa).
- **Detecção de Pose e Pontos-Chave**:
  - **Objetivo**: Obter pontos de referência precisos (ombros, cintura, quadris, etc.) no corpo do usuário e, idealmente, na peça de roupa. Isso substitui a definição heurística que causou problemas.
  - **Ferramenta**: Use um modelo de código aberto como o `OpenPose` ou `AlphaPose`. Eles fornecem as coordenadas exatas dos pontos-chave do corpo, que servirão como entrada para o próximo passo.
  - **Saída**: Um conjunto de coordenadas para os principais pontos do corpo do usuário.

### 2.2. Geração da Imagem (O Coração do `Virtual Try-On`)

- **Objetivo**: Gerar uma nova imagem que combine o corpo do usuário com a peça de roupa, de forma que a roupa pareça naturalmente "vestida".
- **Ferramenta**: Utilizar um modelo de **IA generativa** treinado para `virtual try-on`.

  - **Recomendação**: Implementar um modelo como o `TryOnGAN` ou um modelo de Difusão open-source. Eles são treinados especificamente para deformar a roupa, gerando dobras e texturas realistas.
  - **Entradas para o Modelo**:
    1. A imagem do corpo do usuário (sem fundo).
    2. A imagem da peça de roupa (sem fundo).
    3. As coordenadas de pose extraídas no passo anterior.
  - **Saída**: Uma nova imagem com a roupa "vestida" no corpo do usuário.

### 2.3. Pós-processamento e Entrega

- **Ajuste Final**: A imagem gerada pelo modelo de IA pode precisar de pequenos ajustes de cor ou iluminação. O `OpenCV` pode ser utilizado para isso.
- **Compressão e Retorno**: Comprimir a imagem final e retorná-la ao frontend para exibição.

## 3. Hospedagem e Custos (Revisão)

- **Frontend**: Hospedado gratuitamente no `Vercel` ou `Netlify`.
- **Backend (FastAPI)**: Hospedado em um serviço de contêiner com cobrança por uso, como o `Google Cloud Run`.
- **Serviço de IA**: O modelo de IA generativa será implantado como um serviço `serverless` com suporte a GPU, também no **Google Cloud Run**. O pagamento por uso é ideal para manter os custos baixos no início do projeto, já que você só paga pelo tempo de processamento quando uma solicitação é feita.
