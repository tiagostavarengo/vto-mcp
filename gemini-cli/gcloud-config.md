C:\projects-arenque\vto-arenque>gcloud auth login
Your browser has been opened to visit:

    https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=32555940559.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8085%2F&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fappengine.admin+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fsqlservice.login+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcompute+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Faccounts.reauth&state=Y60LrOlEqy33NMev8eECzAObDVzAwc&access_type=offline&code_challenge=2r3in25Tz2rdxd1zZyjDdt9dkUTvq-aobiJmqOjRhUw&code_challenge_method=S256

You are now logged in as [admin@dataarenque.com].
Nome do projeto [Projeto de POC]
Número do projeto [767223008651]
ID do projeto [cs-poc-iqb5kekqhitu6zfumgspntd]

You can change this setting by running:
$ gcloud config set project PROJECT_ID

Updates are available for some Google Cloud CLI components. To install them,
please run:
$ gcloud components update

## Configuração de Instância de VM

**Configuração da máquina**

- **Nome**: instance-vto-dev-vm-23092025
- **Região**: Alguma com disponibilidade de GPU
- **Zona**: Tudo

**GPUs**

- **Tipo de GPU**: NVIDIA T4
- **Número de GPUs**: 1
- **Tipo de máquina**: n1-standard-4 (4 vCPU, 2 núcleos, 15 GB memória)

```
Custos Google Cloud (c/ GPU) 17/09/2025

northamerica-northeast1 (Montreal)	314,62
us-east1 (Carolina do Sul)		    285,94
us-east4 (Norte da Virgínia)	    309,42
us-central1 (Iowa)				    285,94
us-west1 (Oregon)				    285,94
us-west2 (Los Angeles)		    	338,13
us-west3 (Salt Lake City)	    	338,13
us-west4 (Las Vegas)		    	309,42
europe-west1 (Bélgica)		    	295,65
europe-west2 (Londres)		    	346,60
europe-west3 (Frankfurt)	    	346,60
europe-west4 (Países Baixos)    	296,73
europe-central2 (Varsóvia)	    	339,99
southamerica-east1 (São Paulo)		414,40
me-west1 (Tel Aviv)			    	314,53
asia-northeast1	(Tóquio)       		326,43
asia-northeast3	(Seul)		    	326,43
asia-east1 (Taiwan)	    			301,27
asia-east2 (Hong Kong)			    371,69
asia-southeast2 (Jacarta)		    349,64
australia-southeast1 (Sydney)		376,10
```

**Sistema Operacional e Armazenamento**

- **Sistema operacional**: Deep Learning on Linux
- **Tamanho (GB)**: 100

**Rede**

- **Permitir o trágefo HTTP**: Sim
- **Permitir tráfegos HTTPS**: Sim
