# Provador Virtual - MVP

## Visão Geral do Projeto

Este projeto é um MVP (Produto Mínimo Viável) de um provador virtual, utilizando as mais modernas tecnologias de Visão Computacional e Inteligência Artificial. O objetivo é permitir que clientes de varejo de moda, tanto em e-commerce quanto em lojas físicas, possam "experimentar" roupas virtualmente a partir de fotos, aumentando a taxa de conversão em vendas e reduzindo a logística de devolução.

Nossa solução busca combinar a experiência imersiva e visual da **Doris.ai** com a abordagem de eficiência de negócios da **Sizebay**, construindo um sistema escalável e com baixo custo inicial, seguindo a metodologia **Lean Startup**.

## Arquitetura da Solução

A arquitetura do projeto é baseada em microsserviços e utiliza uma pilha de software (stack) moderna e de código aberto.

- **Frontend**:
  - **Tecnologia**: React (**Web App PWA**)
  - **Descrição**: A interface de usuário para interação com o provador virtual, incluindo autenticação social e upload/visualização de imagens.
- **Backend**:
  - **Tecnologia**: FastAPI (Python)
  - **Descrição**: Uma API leve e de alta performance que gerencia a lógica do negócio, a comunicação com o banco de dados e a orquestração do pipeline de IA.
- **Serviço de IA**:
  - **Tecnologia**: PyTorch e modelos de IA generativa.
  - **Descrição**: O coração do provador virtual. Este serviço processa as imagens do usuário e da roupa para gerar a simulação visual realista, rodando em um ambiente na nuvem.
- **Banco de Dados & Autenticação**:
  - **Tecnologia**: Supabase
  - **Descrição**: Utilizado para armazenamento de dados, gerenciamento de perfis de usuário e autenticação social (Google e Meta). O Supabase simplifica a infraestrutura de backend.

## Pipeline de IA

O pipeline de IA foi reestruturado para superar as limitações das abordagens de sobreposição e deformação 2D, optando por um modelo generativo.

1. **Entrada de Dados**: Recebe a foto do usuário e a foto da roupa.
2. **Pré-processamento**:
   - **Remoção de Fundo**: A biblioteca `rembg` é utilizada para isolar a silhueta do corpo do usuário e a peça de roupa.
   - **Detecção de Pose**: Um modelo de `pose estimation` (como o **OpenPose**) é usado para identificar pontos-chave no corpo do usuário (ombros, cintura, quadris, etc.). Isso permite que a IA generativa entenda a pose e a proporção da pessoa, tornando a simulação mais precisa.
3. **Geração da Imagem**:
   - Um modelo de **IA Generativa** (`TryOnGAN` ou um modelo de `Diffusion`) recebe as imagens pré-processadas e as coordenadas de pose. Ele gera uma nova imagem onde a roupa é "vestida" no corpo do usuário de forma realista, com dobras e caimento adequados.
4. **Entrega**: A imagem final é retornada para o frontend para visualização.

## Ambiente de Desenvolvimento (Recomendado)

Devido à alta demanda de processamento dos modelos de IA, o desenvolvimento e teste do backend **deve ser feito em um ambiente de nuvem com acesso a uma GPU**. A máquina de um desenvolvedor local geralmente não é suficiente.

O workflow recomendado é usar um editor de código com capacidade de desenvolvimento remoto (como o VS Code com a extensão "Remote - SSH") conectado a uma Máquina Virtual (VM) no Google Cloud.

### Configuração do Ambiente na Nuvem (Passo a Passo)

1.  **Crie uma VM com GPU:** No Google Cloud, crie uma instância do **Compute Engine**.
    *   Na configuração, escolha uma família de máquinas otimizada para computação (ex: N1).
    *   Adicione uma GPU à VM (ex: NVIDIA T4 ou V100).
    *   Escolha uma imagem de sistema operacional como "Deep Learning on Linux" ou um Ubuntu padrão (e instale os drivers CUDA manualmente).

2.  **Clone o Repositório na VM:**
    *   Conecte-se à sua nova VM via SSH.
    *   Instale o Git (`sudo apt-get install git`) e clone o projeto:
        ```bash
        git clone https://github.com/tiagostavarengo/vto-arenque.git
        cd vto-arenque/backend
        ```

3.  **Instale as Dependências Python:**
    *   Dentro do diretório `backend`, crie um ambiente virtual e instale os pacotes do `requirements.txt`.
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```

4.  **Configure as Variáveis de Ambiente:**
    *   O projeto precisa das chaves do Supabase para funcionar. Use o arquivo `.env.example` como template.
        ```bash
        # Copie o template
        cp .env.example .env
        ```
    *   Agora, edite o arquivo `.env` (`nano .env`) e preencha com as suas chaves do Supabase.

5.  **Execute o Servidor de Desenvolvimento:**
    *   O script `run_dev.sh` inicia o servidor FastAPI com "auto-reload", que reinicia o servidor automaticamente a cada mudança no código.
    *   Primeiro, dê permissão de execução ao script:
        ```bash
        chmod +x run_dev.sh
        ```
    *   Execute o servidor:
        ```bash
        ./run_dev.sh
        ```
    *   O backend estará rodando na porta 8000 da sua VM. Você precisará configurar as regras de firewall no Google Cloud para permitir o acesso a essa porta.

Com este ambiente, você pode editar o código remotamente no seu editor preferido e ver as alterações refletidas instantaneamente na VM, sem a necessidade de construir ou enviar imagens Docker para cada teste.

## Como Contribuir

Contribuições são bem-vindas! Se você tiver uma sugestão de melhoria ou um problema, por favor, abra uma `issue` ou um `pull request`.

1. Faça um `fork` do projeto.
2. Crie uma `branch` para sua feature: `git checkout -b feature/minha-nova-feature`
3. Faça suas mudanças e comite: `git commit -m 'feat: adiciona nova funcionalidade'`
4. Envie para a `branch` principal: `git push origin feature/minha-nova-feature`
5. Abra um `pull request`.

## Contato

Para qualquer dúvida ou colaboração, entre em contato através do e-mail: contato@dataarenque.com
