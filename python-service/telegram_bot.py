import requests
import telebot
from telebot import types  # Import the 'types' module for reply keyboard markup

initial_message = """
Monitoramento de Monóxido de Carbono! 📡

Opções de comandos:
- Configurar - Configura modo de operação, tempo de envio e valor limite

- Ler Sensor - Lê o valor atual do sensor

- Ler Configurações - Lê as configurações atuais

- Hab/Des Bot Telegram - Habilita ou desabilita o envio de mensagens pelo Telegram

- Hab/Des Whatsapp - Habilita ou desabilita o envio de mensagens pelo Whatsapp

- Simular Alarme - Simular/Parar simulação alarme de CO
"""

configure_instructions = """
Menu de configuração ⚙️:

Opções de comandos:
- Configurar Tempo - Configura o tempo de envio (valor inteiro em segundos)

- Configurar Modo - Configura o modo de operação
    - Envia apenas quando o valor limite é ultrapassado
    - Envia todas as leituras no tempo configurado
    
- Configurar Whatsapp - Configura o número de telefone e a API do Whatsapp

- Voltar ao Menu Principal - Volta ao menu principal
"""

registration_instructions = """
É necessário se registrar para poder receber as notificações.

Envie a seguinte mensagem:
Registrar Produto
"""


# Create a custom keyboard with menu options
menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_configure_button = types.KeyboardButton("Configurar")
menu_keyboard.add(menu_configure_button)
menu_keyboard.row('Ler configurações', 'Ler Sensor')
menu_keyboard.row('Hab/Des Bot Telegram', 'Hab/Des Whatsapp')
menu_keyboard.row('Simular Alarme')

# Create a custom keyboard for the configuration menu
config_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
config_menu_keyboard.row('Configurar Modo', 'Configurar Whatsapp')
config_menu_keyboard.row('Configurar Tempo')
config_menu_keyboard.row('Voltar ao Menu Principal')

# Modos opçoes
modo_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
modo_keyboard.row('Apenas quando ultrapassar o limite')
modo_keyboard.row('Todas as leituras')

# Initialize the bot


def botInit(token, config_manager, mqtt_service, db):
    global bot
    bot = telebot.TeleBot(str(token))

    global configuration_service
    configuration_service = config_manager

    global sender_service
    sender_service = mqtt_service

    global db_repo
    db_repo = db

    # Define a message handler function
    @bot.message_handler(func=lambda message: message.text == "/start")
    def send_welcome(message):
        bot.reply_to(message, text=initial_message, reply_markup=menu_keyboard)

    @bot.message_handler(func=lambda message: message.text == "Configurar")
    def send_configure_command(message):
        bot.reply_to(message, configure_instructions,
                     reply_markup=config_menu_keyboard)

    @bot.message_handler(func=lambda message: message.text == "Simular Alarme")
    def send_simulate_command(message):
        try:
            if (config_manager.send_all_readings == 'Alarm'):
                config_manager.set_send_all_readings()
                mqtt_service.config_send_all_readings(
                    config_manager.get_config())
                print(
                    "\033[94mSended: Modo de envio configurado para enviar todas as leituras\033[0m")
            else:
                config_manager.send_all_readings = 'Alarm'
                mqtt_service.simulate(config_manager.get_config())
                bot.reply_to(message, "Parando simulação de alarme...")
                print("\033[94mSended: Simulando alarme...\033[0m")
        except:
            bot.reply_to(message, "Erro ao simular alarme de CO")

        bot.reply_to(message, text='Menu Inicial:', reply_markup=menu_keyboard)

    @bot.message_handler(func=lambda message: message.text == "Voltar ao Menu Principal")
    def send_main_menu(message):
        bot.reply_to(message, text='Menu Inicial:', reply_markup=menu_keyboard)

    @bot.message_handler(func=lambda message: message.text == "Configurar Tempo")
    def set_timeout(message):
        try:
            msg = bot.reply_to(
                message, "Digite o intervalo de envio em segundos:")
            bot.register_next_step_handler(msg, set_interval_send_time_value)
        except:
            bot.reply_to(message, "Erro ao configurar tempo de envio")
            print("\033[94mSended: Erro ao configurar tempo de envio\033[0m")

    @bot.message_handler(func=lambda message: message.text == "Configurar Modo")
    def set_mode(message):
        try:
            bot.reply_to(message, "Selecione o modo",
                         reply_markup=modo_keyboard)
        except:
            bot.reply_to(message, "Erro ao configurar modo de envio")
            print("\033[94mSended: Erro ao configurar modo de envio\033[0m")

    @bot.message_handler(func=lambda message: message.text == "Apenas quando ultrapassar o limite")
    def set_mode_threshold(message):
        try:
            config_manager.set_send_only_threshold(True)
            mqtt_service.config_send_only_threshold()
            bot.reply_to(
                message, "Modo de envio configurado para enviar apenas quando o valor limite é ultrapassado")
            print(
                "\033[94mSended: Modo de envio configurado para enviar apenas quando o valor limite é ultrapassado\033[0m")
        except:
            bot.reply_to(message, "Erro ao configurar modo de envio")
            print("\033[94mSended: Erro ao configurar modo de envio\033[0m")

        bot.reply_to(message, text='Menu Inicial:', reply_markup=menu_keyboard)

    @bot.message_handler(func=lambda message: message.text == "Todas as leituras")
    def set_mode_all(message):
        try:
            config_manager.set_send_all_readings()
            mqtt_service.config_send_all_readings(config_manager.get_config())
            # msg = bot.reply_to(
            #     message, "Digite o intervalo de envio em segundos:")
            # bot.register_next_step_handler(msg, set_interval_send_time_value)
            print(
                "\033[94mSended: Modo de envio configurado para enviar todas as leituras\033[0m")
        except:
            bot.reply_to(message, "Erro ao configurar modo de envio")
            print("\033[94mSended: Erro ao configurar modo de envio\033[0m")

        bot.reply_to(message, text='Menu Inicial:', reply_markup=menu_keyboard)

    @bot.message_handler(func=lambda message: message.text == "Ler configurações")
    def read_config(message):
        try:
            _, send_all_readings, sending_timeout_seconds = config_manager.get_config()
            reply = "⚙️ Configurações atuais:\n"
            reply += f"Tempo de envio: {sending_timeout_seconds} segundos\n"
            reply += f"Modo de envio: {'Apenas quando ultrapassar o limite' if not send_all_readings else 'Todas as leituras'}\n"
            reply += f"Envio Telegram: {'Habilitado' if config_manager.chat_id is not None else 'Desabilitado'}\n"
            reply += f"Envio Whatsapp: {'Habilitado' if config_manager.wpp_send else 'Desabilitado'}\n"
            if (config_manager.telefone is not None):
                reply += f"API whatsapp: {config_manager.wpp_api}\n"
            if (config_manager.wpp_api is not None):
                reply += f"Número whatsapp: ({config_manager.telefone})\n"
            bot.reply_to(message, reply)
            print(f"\033[94mSended:\n{reply}\033[0m")
        except:
            bot.reply_to(message, "Erro ao ler configurações")
            print("\033[94mSended: Erro ao ler configurações\033[0m")
        bot.reply_to(message, text='Menu Inicial:', reply_markup=menu_keyboard)

    @bot.message_handler(func=lambda message: message.text == "Hab/Des Bot Telegram")
    def register_product(message):
        try:
            if (config_manager.chat_id is None):
                config_manager.chat_id = message.chat.id
                bot.reply_to(message, "Produto registrado com sucesso")
                db_repo.update_chat_id(message.chat.id)
                print("\033[94mSended: Produto registrado com sucesso\033[0m")
            else:
                config_manager.chat_id = None
                bot.reply_to(message, "Produto desregistrado com sucesso")
                db_repo.update_chat_id(config_manager.chat_id)
                print("\033[94mSended: Produto desregistrado com sucesso\033[0m")

        except:
            bot.reply_to(message, "Erro ao registrar produto")
        bot.reply_to(message, text='Menu Inicial:', reply_markup=menu_keyboard)

    @bot.message_handler(func=lambda message: message.text == "Ler Sensor")
    def read_sensor(message):
        try:
            bot.reply_to(message, "Ainda não implementado...")
            print("\033[94mSended: Ainda não implementado...\033[0m")
        except:
            bot.reply_to(message, "Erro ao comunicar com o sensor")
            print("\033[94mSended: Erro ao comunicar com o sensor\033[0m")
        bot.reply_to(message, text='Menu Inicial:', reply_markup=menu_keyboard)

    @bot.message_handler(func=lambda message: message.text == "Configurar Whatsapp")
    def set_whatsapp(message):
        try:
            msg = bot.reply_to(
                message, """Primeiro é necessário permitir o envio de mensagens do bot
Clique no link abaixo e envie a mensagem 'I allow callmebot to send me messages'

https://w.app/cGDgRZ

Insira o Código recebido:
""")
            print(
                "\033[94mSended: Primeiro é necessário permitir o envio de mensagens do bot\033[0m")
            bot.register_next_step_handler(msg, set_whatsapp_api)
        except:
            bot.reply_to(message, "Erro ao configurar whatsapp")
            print("\033[94mSended: Erro ao configurar whatsapp\033[0m")

    # 'Hab/Des Whatsapp'
    @bot.message_handler(func=lambda message: message.text == "Hab/Des Whatsapp")
    def set_whatsapp(message):
        try:
            if (config_manager.wpp_send):
                config_manager.wpp_send = False
                bot.reply_to(message, "Whatsapp desabilitado")
                print("\033[94mSended: Whatsapp desabilitado\033[0m")
            else:
                config_manager.wpp_send = True
                bot.reply_to(message, "Whatsapp habilitado")
                print("\033[94mSended: Whatsapp habilitado\033[0m")

            db_repo.update_send(config_manager.wpp_send)
        except:
            bot.reply_to(message, "Erro ao configurar whatsapp")

    print("Telegram bot initialized")
    # Start polling
    bot.polling()


def send_reading(message, config_manager):
    if (config_manager.chat_id is None):
        print("Chat id not set")
        print(registration_instructions)
        return
    try:
        if config_manager.chat_id is not None:
            bot.send_message(config_manager.chat_id, message)

        if (config_manager.telefone is not None and config_manager.wpp_api is not None):
            messagem = f"https://api.callmebot.com/whatsapp.php?phone={config_manager.telefone}&text={message}&apikey={config_manager.wpp_api}"
            x = requests.post(messagem, json={})

    except Exception as e:
        print("Erro ao enviar mensagem", e)


# Function to set the interval send time value


def set_interval_send_time_value(message):
    try:
        value = int(message.text)
        if (value < 0):
            value = 1
        if (value > 255):
            value = 255
        config = configuration_service.set_sending_timeout_seconds(value)
        sender_service.config_send_time(value, config)

        bot.reply_to(
            message, "Tempo de envio configurado para " + str(value) + " segundos")
        print("\033[94mSended: Tempo de envio configurado para " +
              str(value) + " segundos\033[0m")
    except ValueError:
        bot.reply_to(
            message, "Valor inserido não é válido. Digite um valor inteiro em segundos.")
        print(
            "\033[94mSended: Valor inserido não é válido. Digite um valor inteiro em segundos.\033[0m")
    bot.reply_to(message, text='Menu Inicial:', reply_markup=menu_keyboard)

# Function to set the mode value


def set_mode_value(message):
    try:
        value = int(message.text)
        if (value == 0):
            config = configuration_service.set_send_only_threshold(True)
            sender_service.config_send_only_threshold(config)

            bot.reply_to(
                message, "Modo de envio configurado para enviar apenas quando o valor limite é ultrapassado")
        elif (value == 1):
            config = configuration_service.set_send_all_readings(True)
            sender_service.config_send_all_readings(config)

            bot.reply_to(
                message, "Modo de envio configurado para enviar todas as leituras")

            msg = bot.reply_to(
                message, "Digite o intervalo de envio em segundos:")
            bot.register_next_step_handler(msg, set_interval_send_time_value)
        else:
            bot.reply_to(message, "Modo de envio inválido")
    except:
        bot.reply_to(message, "Erro ao configurar modo de envio")

    bot.reply_to(message, text='Menu Inicial:', reply_markup=menu_keyboard)

# Function to set the whatsapp api value


def set_whatsapp_api(message):
    try:
        value = str(message.text)
        configuration_service.wpp_api = value
        bot.reply_to(
            message, "Bot Whatsapp configurado!")

        db_repo.update_api_key(value)

        msg = bot.reply_to(
            message, """Insira seu número de telefone no seguinte formato:

5512345678901

""")
        print("\033[94mSended: Bot Whatsapp configurado!\033[0m")
        bot.register_next_step_handler(msg, set_telefone)
    except ValueError:
        bot.reply_to(
            message, "Valor inserido não é válido. Digite um valor válido.")
        print(
            "\033[94mSended: Valor inserido não é válido. Digite um valor válido.\033[0m")
        bot.reply_to(message, text='Menu Inicial:', reply_markup=menu_keyboard)

# Function to set the telefone value


def set_telefone(message):
    try:
        value = str(message.text)
        configuration_service.telefone = value
        bot.reply_to(
            message, "Telefone configurado!")
        db_repo.update_telefone(value)
        print("\033[94mSended: Telefone configurado!\033[0m")
    except ValueError:
        bot.reply_to(
            message, "Valor inserido não é válido. Digite um valor válido.")
        print(
            "\033[94mSended: Valor inserido não é válido. Digite um valor válido.\033[0m")
    bot.reply_to(message, text='Menu Inicial:', reply_markup=menu_keyboard)
