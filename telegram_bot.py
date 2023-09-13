import requests
import telebot

initial_message = """
Bem vindo ao Configurador do Sensor de Monóxido de Carbono!

Opções de comandos:
/iniciar - Inicia o bot e mostra as opções de comandos
/configurar - Configura modo de operação, tempo de envio e valor limite
/ler - Lê o valor atual do sensor
/ler_configuracoes - Lê as configurações atuais
/registrar_produto - Registra o produto no servidor
"""

configure_instructions = """
Menu de configuração:

Opções de comandos:
* configurar-limite - Configura o valor limite de CO (valor inteiro em porcentagem)
    Ex.: "/configurar_limite 100"
    
* configurar-tempo - Configura o tempo de envio (valor inteiro em segundos)
    Ex.: "/configurar_tempo 10"
    
* configurar-modo - Configura o modo de operação (valor inteiro)
 - 0 (Envia apenas quando o valor limite é ultrapassado)
 - 1 (Envia todas as leituras no tempo configurado)
    Ex.: "/configurar_modo 0"
    
* configurar_nome - Configura o nome do produto (string)
    Ex.: "/configurar_nome "Sensor de CO""
"""

registration_instructions = """
É necessário se registrar para poder receber as notificações.

Envie a seguinte mensagem:
/registrar_produto
"""
# Initialize the bot


def botInit(token, config_manager, mqtt_service):
    global bot
    bot = telebot.TeleBot(str(token))

    # Define a message handler function
    @bot.message_handler(commands=['iniciar'])
    def send_welcome(message):
        bot.reply_to(message, initial_message)

    @bot.message_handler(commands=['configurar'])
    def send_config(message):
        bot.reply_to(message, configure_instructions)

    @bot.message_handler(commands=['configurar_limite'])
    def set_threshold(message):
        try:
            value = int(message.text.split()[1])
            print("Value: ", value)
            config = config_manager.set_threshold(value)
            print("Config: ", config)
            mqtt_service.config_threshold(value, config)
            print("Enviou")
            bot.reply_to(
                message, "Valor limite configurado para " + str(value))
        except:
            bot.reply_to(message, "Erro ao configurar valor limite")

    @bot.message_handler(commands=['configurar_tempo'])
    def set_timeout(message):
        try:
            value = int(message.text.split()[1])
            config = config_manager.set_sending_timeout_seconds(value)
            mqtt_service.config_send_time(value, config)

            bot.reply_to(
                message, "Tempo de envio configurado para " + str(value) + " segundos")
        except:
            bot.reply_to(message, "Erro ao configurar tempo de envio")

    @bot.message_handler(commands=['configurar_modo'])
    def set_mode(message):
        try:
            value = int(message.text.split()[1])
            if (value == 0):
                config = config_manager.set_send_only_threshold(True)
                mqtt_service.config_send_only_threshold(config)

                bot.reply_to(
                    message, "Modo de envio configurado para enviar apenas quando o valor limite é ultrapassado")
            elif (value == 1):
                config = config_manager.set_send_all_readings(True)
                mqtt_service.config_send_all_readings(config)

                bot.reply_to(
                    message, "Modo de envio configurado para enviar todas as leituras")
            else:
                bot.reply_to(message, "Modo de envio inválido")
        except:
            bot.reply_to(message, "Erro ao configurar modo de envio")

    @bot.message_handler(commands=['ler_configuracoes'])
    def read_config(message):
        try:
            threshold, send_all_readings, sending_timeout_seconds, send_only_threshold = config_manager.get_config()
            bot.reply_to(message, "Valor limite: " + str(threshold) +
                         "\nTempo de envio: " + str(sending_timeout_seconds) + " segundos" +
                         "\nModo de envio: " + ("Apenas quando ultrapassar o limite" if send_only_threshold else "Todas as leituras"))
        except:
            bot.reply_to(message, "Erro ao ler configurações")

    @bot.message_handler(commands=['registrar_produto'])
    def register_product(message):
        try:
            if(config_manager.chat_id is None):
                config_manager.chat_id = message.chat.id
                bot.reply_to(message, "Produto registrado com sucesso")
            else:
                bot.reply_to(message, "Produto já registrado")
        except:
            bot.reply_to(message, "Erro ao registrar produto")
            
    @bot.message_handler(commands=['ler'])
    def read_sensor(message):
        try:
            bot.reply_to(message, "Ainda não implementado...")
        except:
            bot.reply_to(message, "Erro ao comunicar com o sensor")
            
    @bot.message_handler(commands=['configurar_nome'])
    def set_name(message):
        try:
            name = message.text.split()[1]
            config_manager.name = name
            bot.reply_to(message, "Nome configurado para " + name)
        except:
            bot.reply_to(message, "Erro ao configurar nome")

    print("Telegram bot initialized")
    # Start polling
    bot.polling()


def send_reading(message, config_manager,telefonenumber, apikey):
    if(config_manager.chat_id is None):
        print("Chat id not set")
        print(registration_instructions)
        return
    try:
        bot.send_message(config_manager.chat_id, message)
        messagem = f"https://api.callmebot.com/whatsapp.php?phone={telefonenumber}&text={message}&apikey={apikey}"
        x = requests.post(messagem, json = {})

    except Exception as e:
            print("Erro ao enviar mensagem", e)