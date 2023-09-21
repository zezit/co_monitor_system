<a name="readme-top"></a>

# Monitor de monóxido de carbono

Projeto de IoT com ESP32S2 para Detecção de Monóxido de Carbono e Notificação via MQTT

## Descrição

Este projeto foi desenvolvido como parte de uma competição de IoT e utiliza uma placa [Franzininho](https://docs.franzininho.com.br/docs/franzininho-wifi/franzininho-wifi/) com um [ESP32S2](https://www.espressif.com/en/products/socs/esp32-s2) para monitorar os níveis de monóxido de carbono em um ambiente. O dispositivo envia os dados coletados via MQTT para um servidor Python que controla o envio de notificações para Telegram e WhatsApp, podendo ser configurado para notificar várias pessoas.

## Recursos Principais

- Leitura de sensor de monóxido de carbono com ESP32S2
- Verificação dos parâmetros em relação aos limites estabelecidos
- Comunicação via MQTT para servidor Python
- Servidor Python para processar e encaminhar notificações para Telegram e WhatsApp

## Estrutura do Repositório

O repositório está organizado da seguinte forma:

- [**firmware**](./firmware/): Contém o código-fonte e os recursos relacionados à placa Franzininho com ESP32S2.
- [**python service**](./python-service/): Inclui o código do servidor em Python responsável por receber dados via MQTT e encaminhar notificações.

## Conclusões

### Itens Concluídos

- [x] Implementação da leitura do sensor de monóxido de carbono.
- [x] Configurar conexão em uma rede wifi
- [x] Configuração do envio de dados via MQTT.
- [x] Desenvolvimento do servidor Python para controle de notificações.
- [x] Configuração para envio de notificações para Telegram e WhatsApp.

### Próximos Passos

- [ ] Implementar mecanismo de fallback para notificação em caso de falha no envio.
- [ ] Melhorar a interface de configuração do bot do Telegram.
- [ ] Otimizar o bot de envio pelo whatsapp.
- [ ] Adicionar suporte a outros serviços de notificação.
- [ ] Realizar otimizações de consumo de energia no microcontrolador.
- [ ] Possibilidade de notificar várias pessoas.
- [ ] Implementar comunicação direta com o celular por meio de BLE
- [ ] Implementar salvamento de logs em banco de dados para uma futura análise dos níveis no ambiente

## Equipe

<ul>
    <li style="display: flex; align-itens: center; justify-content: left; margin-bottom: 15px">
        <span style="margin-right: 67px" text="center">José Dias</span>
        <a style="display: flex; align-itens: center; align-self: center;" 
        href="https://www.linkedin.com/in/josevmendes"
          target="_blank">
            <img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=flat&logo=linkedin&logoColor=white" target="_blank">  
        </a> 
        <a style="margin-left: 10px; display: flex; align-itens: center" href="https://www.github.com/zezit"
          target="_blank">
            <img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" target="_blank">  
        </a> 
    </li>
    <li style="display: flex; align-itens: center; justify-content: left; margin-bottom: 15px">
        <span style="margin-right: 43px" text="center">Pedro Hodge</span>
        <a style="display: flex; align-itens: center; align-self: center;"
         href="https://www.linkedin.com/in/pedrohodge/"
          target="_blank">
            <img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=flat&logo=linkedin&logoColor=white" target="_blank">  
        </a> 
        <a style="margin-left: 10px; display: flex; align-itens: center" href="https://gitlab.com/pedrohodge"
          target="_blank">
            <img src="https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white" target="_blank">  
        </a> 
    </li>
    <li style="display: flex; align-itens: center; justify-content: left; margin-bottom: 15px">
        <span style="margin-right: 10px" text="center">Walther Humberto</span>
        <a style="display: flex; align-itens: center; align-self: center;"
         href="https://www.linkedin.com/in/walther-humberto/"
          target="_blank">
            <img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=flat&logo=linkedin&logoColor=white" target="_blank">  
        </a> 
        <a style="margin-left: 10px; display: flex; align-itens: center" href="https://github.com/waltherHumberto"
          target="_blank">
            <img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" target="_blank">  
        </a> 
    </li>
</ul>


## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar solicitações pull requests para melhorias e/ou correções no projeto.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).