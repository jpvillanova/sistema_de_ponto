# Roadmap — Sistema de Ponto por QR Code

> Plano de desenvolvimento original do projeto (3 meses), mantido como referência de arquitetura e escopo.

---

Mês 1: Fundação e Core Engine
Semana 1: Engenharia de Requisitos e Design de Dados

Seg/Ter: Definição das Regras de Negócio (ex: tolerância de atraso, horas extras, limites de jornada).

Qua/Qui: Arquitetura do Banco de Dados (ERD). Tabelas: users, logs_ponto, work_schedules.

Sex: Definição da stack final e configuração do repositório (Git).

Semana 2: Visão Computacional e Prototipagem de Hardware

Seg/Ter: Script Python para acesso à câmera e captura de frames.

Qua/Qui: Implementação da decodificação de QR Code (OpenCV + PyZbar).

Sex: Testes de distância, iluminação e velocidade de leitura.

Semana 3: Backend e Persistência de Dados

Seg/Ter: Criação das conexões com o banco de dados (PostgreSQL/Supabase).

Qua/Qui: Lógica de "Check-in/Check-out" (verificar se o último registro do dia foi entrada ou saída).

Sex: Implementação do sistema de logs locais para caso de queda de internet.

Semana 4: Lógica de Negócio e Cálculos de Horas

Seg-Qua: Algoritmo de cálculo de saldo de banco de horas em tempo real.

Qui-Sex: Sistema de feedback sonoro (Bips diferentes para Sucesso/Erro) e feedback visual em tela.

Mês 2: Integrações e Interface
Semana 5: Integração com WhatsApp API

Seg/Ter: Configuração da API de mensagens (Twilio ou similar).

Qua/Qui: Criação dos gatilhos (Triggers) após inserção no banco.

Sex: Formatação das mensagens automáticas com resumo do dia e saldo.

Semana 6: Desenvolvimento da Interface do Totem (Frontend)

Seg-Qua: Criação da UI (PyQt6 ou Tkinter) para mostrar a câmera e status do funcionário.

Qui/Sex: Integração da UI com o script de visão computacional (Multi-threading para a câmera não travar a interface).

Semana 7: Painel Administrativo (Web ou Desktop)

Seg-Qua: Tela para cadastro de novos funcionários e edição de registros falhos.

Qui/Sex: Função de "Gerar QR Code" e exportar PDF com os crachás dos funcionários.

Semana 8: Segurança e Refatoração

Seg/Ter: Implementação de segurança (evitar que alguém use uma foto do QR Code - validação básica).

Qua/Qui: Refatoração de código para performance (limpeza de memória do Python).

Sex: Tratamento de exceções (ex: banco de dados offline, câmera desconectada).

Mês 3: Deploy e Finalização
Semana 9: Testes de Stress e QA (Quality Assurance)

Seg-Qua: Testes de carga (simular 100 registros em sequência).

Qui/Sex: Teste de "Caminho Infeliz" (sem internet, QR Code rasgado, queda de energia).

Semana 10: Deploy Final e Documentação

Seg/Ter: Configuração do hardware definitivo (Mini PC/Raspberry Pi) para ligar automaticamente.

Qua: Documentação do usuário e manual de suporte.

Qui/Sex: Entrega oficial e monitoramento de primeira semana.

🛠️ Stack Tecnológica Recomendada
Linguagem: Python 3.10+

Visão: OpenCV

Banco de Dados: Supabase (PostgreSQL na nuvem com facilidade de integração)

WhatsApp: Evolution API (Open Source) ou Twilio

Hardware: Webcam 1080p + Mini PC (Windows ou Linux)

🚦 Principais Marcos (Milestones)
M1 (Fim da Semana 2): Câmera reconhecendo IDs e imprimindo no terminal.

M2 (Fim da Semana 4): Ponto gravando no banco e calculando saldo corretamente.

M3 (Fim da Semana 6): WhatsApp apitando no celular ao passar o QR Code.

M4 (Fim da Semana 10): Sistema rodando em hardware dedicado sem intervenção humana.


1. Módulo de Visão (Vision Engine)
Este módulo cuida apenas da câmera e da extração do dado bruto.

detectar_qrcode(frame): Recebe a imagem da câmera, processa e retorna o conteúdo do QR Code se encontrar um, ou None.

gerar_token_qrcode(funcionario_id): Função utilitária para gerar a imagem .png do QR Code para novos funcionários.

2. Módulo de Banco de Dados (Database Manager)
Responsável por toda a conversa com o PostgreSQL/Supabase.

obter_funcionario_por_token(token): Busca no banco quem é o dono daquele QR Code.

verificar_ultimo_registro(funcionario_id): Checa se a última batida foi "Entrada" ou "Saída" para decidir o que registrar agora.

salvar_ponto(funcionario_id, tipo): Insere o novo registro com o timestamp atual.

sincronizar_dados_locais(): Função que roda em segundo plano para enviar pontos salvos no SQLite (offline) para a nuvem quando a internet volta.

3. Módulo de Regras de Negócio (Business Logic)
Onde o "cálculo" acontece.

calcular_saldo_diario(funcionario_id): Soma as horas trabalhadas no dia atual e compara com a carga horária cadastrada.

validar_cooldown(funcionario_id): Verifica se o funcionário não acabou de bater o ponto (ex: nos últimos 2 minutos) para evitar registros duplicados por erro de leitura.

4. Módulo de Comunicação (Integrations)
Responsável pelo feedback externo.

emitir_alerta_sonoro(sucesso=True): Toca o "Bip" de sucesso ou um som de erro se o QR Code for inválido.

enviar_confirmacao_whatsapp(funcionario_id, horario, saldo): Formata a string de texto e dispara para a API do WhatsApp.