# Sistema de Ponto por QR Code

Sistema de registro de ponto (check-in / check-out) de funcionários baseado em
**visão computacional**: um totem com webcam lê o QR Code do crachá e registra o
horário, com feedback visual e sonoro imediato.

Este repositório contém o **protótipo do módulo de visão** (`visao_camera.py`) —
o primeiro marco de um projeto maior cuja arquitetura completa está documentada
em [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Status

🚧 **Em desenvolvimento** — módulo de visão funcional (detecção de QR Code em
tempo real, overlay de confirmação e beep). Persistência em banco, regras de
negócio e integrações estão planejadas no roadmap.

## Funcionalidades (protótipo atual)

- Captura de vídeo da webcam em tempo real (OpenCV).
- Detecção e decodificação de QR Code (`cv2.QRCodeDetector`).
- Destaque do QR Code na tela e **overlay verde de confirmação** por alguns segundos.
- **Feedback sonoro** multiplataforma (beep no Windows, `bell` no Linux/macOS).
- Exibição do horário da leitura na tela (**ainda não é salvo**: não há persistência).
- Bloqueio de novas leituras durante os 3 segundos da confirmação.

## Estrutura

```
visao_camera.py    # protótipo do módulo de visão (Vision Engine)
BD.txt             # modelo do banco planejado, em DBML; ainda não usado pelo código
docs/ROADMAP.md    # arquitetura completa e próximos passos
requirements.txt   # dependências: OpenCV e NumPy
```

## Pré-requisitos

- Python 3.10+
- Uma webcam

## Instalação

```sh
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Uso

```sh
# Usa a câmera padrão (índice 0)
python visao_camera.py

# Seleciona outra câmera
python visao_camera.py --camera 1
```

Aproxime um QR Code da câmera. Pressione **`q`** para encerrar.

## Arquitetura planejada

O projeto completo é organizado em quatro módulos (detalhes em
[`docs/ROADMAP.md`](docs/ROADMAP.md)):

| Módulo | Responsabilidade |
|---|---|
| **Vision Engine** | Captura de câmera e extração do dado do QR Code. |
| **Database Manager** | Persistência em PostgreSQL/Supabase + fila local offline. |
| **Business Logic** | Cálculo de saldo de horas, cooldown anti-duplicidade. |
| **Integrations** | Feedback sonoro e confirmação via API de WhatsApp. |

## Stack

`Python` · `OpenCV` · `NumPy` · *(planejado: PostgreSQL/Supabase, API WhatsApp)*
