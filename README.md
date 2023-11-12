# Chat em Rede com Python e PyQt5

Este projeto é um chat simples de rede implementado em Python utilizando a biblioteca PyQt5 para a interface gráfica e sockets para comunicação em rede. O programa pode funcionar tanto como servidor quanto como cliente. Quando iniciado, ele tenta se conectar a um servidor existente; se não encontrar um, ele mesmo inicia como servidor.

## Funcionalidades

- **Modo Dual Servidor/Cliente**: Cada instância do programa pode atuar como servidor ou cliente, dependendo da disponibilidade de um servidor na rede.
- **Broadcast de Mensagens**: Mensagens enviadas são compartilhadas com todos os clientes conectados, incluindo o servidor.
- **Fallback de Servidor**: Quando o servidor se desconecta, o cliente conectado há mais tempo (com base no timestamp) assume o papel de servidor.

## Estrutura do Código

- `JanelaChat`: Classe principal que cria a janela do chat e gerencia a lógica de conexão e comunicação.
- `inicializarUI`: Constrói a interface gráfica do usuário, incluindo campos de texto e botões.
- `obter_ip_local`: Determina o endereço IP local do host para configuração da conexão de rede.
- `iniciar_como_cliente`: Tenta conectar-se a um servidor existente; se falhar, chama `iniciar_como_servidor`.
- `iniciar_como_servidor`: Inicializa a instância atual como servidor, aceitando conexões de clientes.
- `aceitar_conexoes`: Aguarda e aceita conexões de entrada de novos clientes.
- `manipular_cliente`: Gerencia a comunicação com um cliente conectado.
- `retransmitir`: Envia a mensagem recebida para todos os clientes conectados.
- `enviar_mensagem`: Envia uma mensagem do campo de texto para o servidor ou retransmite para os clientes, se for o servidor.
- `receber_mensagem`: Recebe mensagens do servidor e as exibe na interface do chat.
- `verificar_e_tornar_servidor`: Verifica se deve iniciar como servidor após a desconexão do servidor atual.

## Como Usar

1. **Iniciar o Chat**: Execute o script `python main.py` para iniciar o chat. A primeira instância tentará atuar como servidor.
2. **Conectar como Cliente**: Execute o script em outra máquina ou instância para conectar-se ao servidor existente.
3. **Enviar Mensagens**: Use o campo de texto para digitar mensagens e clique em "Enviar" para compartilhá-las com todos na rede.
4. **Servidor Fallback**: Se o servidor se desconectar, o cliente mais antigo (com base no timestamp de conexão) assumirá automaticamente como novo servidor.

## Requisitos

- Python 3
- PyQt5
- Uma rede local onde as instâncias do chat podem se descobrir e se conectar.

