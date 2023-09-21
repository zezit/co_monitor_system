# README para Utilizar o Código Python

Este README fornece instruções sobre como utilizar o código Python fornecido (`app.py`) e os módulos associados em um sistema de monitoramento de Monóxido de Carbono (CO). Este código integra-se com MQTT para comunicação de dados, um banco de dados local para armazenar configurações e o Telegram/WhatsApp para enviar notificações.

## Pré-requisitos

Antes de começar, assegure-se de ter os seguintes pré-requisitos instalados em seu sistema:

- Python 3.10.6
- Biblioteca Paho-MQTT (`paho-mqtt`)
- Biblioteca `dotenv` para Python
- Biblioteca `requests`
- Biblioteca `pyTelegramBotAPI`
- Broker MQTT (por exemplo, Mosquitto)
- Uma chave de API de Bot do Telegram
- Acesso à API do WhatsApp (opcional, para notificações via WhatsApp)

## Primeiros Passos

1. Clone ou faça o download do repositório de código para sua máquina local.

2. Crie um arquivo `.env` no mesmo diretório que o `app.py` e defina as seguintes variáveis de ambiente:

   - `MQTT_BROKER`: O URI do broker MQTT.
   - `MQTT_PORT`: A porta do broker MQTT.
   - `MQTT_SUBSCRIBE_TOPIC`: O tópico MQTT para se inscrever para leituras de nível de CO.
   - `MQTT_PUBLISH_TOPIC`: O tópico MQTT para publicar atualizações de configuração.
   - `TELEGRAM_BOT_API_KEY`: Sua chave de API do Bot do Telegram.

   Exemplo de arquivo `.env`:

   ```
   MQTT_BROKER=mqtt://localhost
   MQTT_PORT=1883
   MQTT_SUBSCRIBE_TOPIC=sensor/nivel_co
   MQTT_PUBLISH_TOPIC=sensor/config
   TELEGRAM_BOT_API_KEY=sua_chave_de_api_do_telegram_bot
   ```

3. Instale as bibliotecas Python necessárias usando o pip:
   ```shell
   pip install -r requirements.txt
   ```

4. Execute o script `app.py`:

   ```
   python app.py
   ```

## Uso

Depois que o código estiver em execução, você pode interagir com o sistema de monitoramento de CO por meio do Telegram. Aqui estão alguns comandos disponíveis:

- **/start**: Inicia o bot e exibe o menu inicial.

- **Configurar**: Acessa o menu de configuração.

- **Simular Alarme**: Inicia ou para a simulação de alarmes de CO.

- **Voltar ao Menu Principal**: Retorna ao menu principal.

- **Configurar Tempo**: Define o intervalo para o envio de leituras de CO (em segundos).

- **Configurar Modo**: Define o modo de operação (enviar todas as leituras ou enviar somente quando o limite for excedido).

- **Apenas quando ultrapassar o limite**: Define o modo de enviar dados somente quando o nível de CO exceder um limite.

- **Todas as leituras**: Define o modo de enviar todas as leituras de CO.

- **Ler configurações**: Exibe as configurações atuais.

- **Hab/Des Bot Telegram**: Habilita ou desabilita notificações via Telegram.

- **Hab/Des Whatsapp**: Habilita ou desabilita notificações via WhatsApp (requer configuração da API do WhatsApp).

- **Configurar Whatsapp**: Configura notificações via WhatsApp (requer API do WhatsApp e número de telefone).

## Notas Adicionais

- O código também inclui uma funcionalidade opcional para enviar notificações via WhatsApp. Para habilitar essa funcionalidade, você precisa configurar uma API do WhatsApp e fornecer a chave de API e o número de telefone na configuração.

- O código inclui tratamento de erros, portanto, se houver problemas com a configuração ou a comunicação, mensagens de erro serão exibidas.

- Você pode modificar o código para adaptá-lo às suas necessidades específicas ou integrar recursos adicionais conforme necessário.

- O banco de dados local (`localdb.json`) armazena dados de configuração e é criado automaticamente se não existir.

- Os tópicos MQTT e os formatos de payload podem ser personalizados conforme necessário para o seu caso de uso específico.

- O código oferece flexibilidade na configuração do modo de operação e do intervalo de envio para atender a diferentes cenários de monitoramento.