# Configuração do Google Cloud / Principios básicos

Execute a sua carga de trabalho em uma arquitetura de base para ter a segurança e a escalonalidade em mente.

### Execute as suas cargas de trabalho (Escolha uma opção)

## **Prova de conceito**

Execute a carga de trabalho de prova de conceito da sua organização com a segurança básica em mente.

**Principios básicos**

- **Download ou implantação direta do Terraform**: Faça o download de sua configuração em arquivos do Terraform ou implante as opções diretamente no console.
- **Recurso da organização**: Instruções para configurar um recurso da organização, que vai representar sua empresa e servir como nó superior da sua estrutura de pastas e projetos.
- **Faturamento**: Aqui os administradores podem vincular uma conta de faturamento ao recurso de organização ou criar uma nova.
- **Grupos de administradores**: Cria grupos de administradores seguindo as práticas recomendadas, além de atribuir papéis do IAM de administrador com a segurança em mente. Aceite ou modifique as configurações padrão.
- **Hierarquia de recursos**: Cria uma hierarquia de pastas e projetos e atribui papéis do IAM com a segurança em mente. Aceite ou modifique as configurações padrão.

**Segurança**

- **Políticas da organização**: Configura políticas para controlar o acesso aos recursos do Google Cloud em toda a organização. Aceite ou modifique as configurações padrão.

## **Produção**

Execute cargas de trabalho prontas para produção com a segurança e a escalonabilidade em mente. O padrão são as arquiteturas baseadas nas práticas recomendadas do Google Cloud, mas é possível fazer modificações.

**Principios básicos**

- **Download ou implantação direta do Terraform**: Faça o download de sua configuração em arquivos do Terraform ou implante as opções diretamente no console.
- **Recurso da organização**: Instruções para configurar um recurso da organização, que vai representar sua empresa e servir como nó superior da sua estrutura de pastas e projetos.
- **Faturamento**: Aqui os administradores podem vincular uma conta de faturamento ao recurso de organização ou criar uma nova.
- **Grupos de administradores**: Cria grupos de administradores seguindo as práticas recomendadas, além de atribuir papéis do IAM de administrador com a segurança em mente. Aceite ou modifique as configurações padrão.
- **Hierarquia de recursos**: Cria uma hierarquia de pastas e projetos e atribui papéis do IAM com a segurança em mente. Aceite ou modifique as configurações padrão.
- **Geração de registros centralizada**: Configura a geração de registros centralizada para que os administradores visualizem o que está acontecendo na organização. Aceite ou modifique as configurações padrão.
- **Monitoramento centralizado**: Configura o monitoramento central para que os administradores visualizem o que está acontecendo na organização. Aceite ou modifique as configurações padrão.

**Rede**

- **Redes VPC compartilhadas**: Configura redes VPC compartilhadas, incluindo sub-redes, Cloud NAT e regras de firewall. Para isso, é preciso selecionar o intervalo de endereços IP e a região. Aceite ou modifique as configurações padrão.
- **Conectividade híbrida**: Configura a conectividade híbrida usando VPN de alta disponibilidade (HA VPN, na sigla em inglês). Exige entrada. Aceite ou modifique as configurações padrão.

**Segurança**

- **Políticas da organização**: Configura políticas para controlar o acesso aos recursos do Google Cloud em toda a organização. Aceite ou modifique as configurações padrão.
- **Security Command Center**: Configura o Security Command Center, que realiza inventário e descoberta de ativos, identifica vulnerabilidades e ajuda a reduzir riscos. Aceite ou modifique as configurações padrão.

## **Segurança reforçada**

Execute cargas de trabalho prontas para produção com maior segurança. O padrão são as arquiteturas baseadas nas práticas recomendadas do Google Cloud, mas é possível fazer modificações.

**Principios básicos**

- **Download ou implantação direta do Terraform**: Faça o download de sua configuração em arquivos do Terraform ou implante as opções diretamente no console.
- **Recurso da organização**: Instruções para configurar um recurso da organização, que vai representar sua empresa e servir como nó superior da sua estrutura de pastas e projetos.
- **Faturamento**: Aqui os administradores podem vincular uma conta de faturamento ao recurso de organização ou criar uma nova.
- **Grupos de administradores**: Cria grupos de administradores seguindo as práticas recomendadas, além de atribuir papéis do IAM de administrador com a segurança em mente. Aceite ou modifique as configurações padrão.
- **Hierarquia de recursos**: Cria uma hierarquia de pastas e projetos e atribui papéis do IAM com a segurança em mente. Aceite ou modifique as configurações padrão.
- **Geração de registros centralizada**: Configura a geração de registros centralizada para que os administradores visualizem o que está acontecendo na organização. Aceite ou modifique as configurações padrão.
- **Monitoramento centralizado**: Configura o monitoramento central para que os administradores visualizem o que está acontecendo na organização. Aceite ou modifique as configurações padrão.

**Rede**

- **Redes VPC compartilhadas**: Configura redes VPC compartilhadas, incluindo sub-redes, Cloud NAT e regras de firewall. Para isso, é preciso selecionar o intervalo de endereços IP e a região. Aceite ou modifique as configurações padrão.
- **Conectividade híbrida**: Configura a conectividade híbrida usando VPN de alta disponibilidade (HA VPN, na sigla em inglês). Exige entrada. Aceite ou modifique as configurações padrão.

**Segurança**

- **Políticas da organização**: Configura políticas para controlar o acesso aos recursos do Google Cloud em toda a organização. Aceite ou modifique as configurações padrão.
- **Security Command Center**: Configura o Security Command Center, que realiza inventário e descoberta de ativos, identifica vulnerabilidades e ajuda a reduzir riscos. Aceite ou modifique as configurações padrão.
- **Gerenciamento de chaves**: Configura a criptografia para recursos futuros de carga de trabalho usando o Cloud KMS com o Autokey. Aceite ou modifique as configurações padrão.
