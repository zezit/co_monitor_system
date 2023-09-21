# Carbon Monoxide Monitor

IoT Project with ESP32S2 for Carbon Monoxide Detection and MQTT Notification

## Description

This project was developed as part of an IoT competition and utilizes a [Franzininho](https://docs.franzininho.com.br/docs/franzininho-wifi/franzininho-wifi/) board with an [ESP32S2](https://www.espressif.com/en/products/socs/esp32-s2) to monitor carbon monoxide levels in an environment. The device sends the collected data via MQTT to a Python server that handles notifications to Telegram and WhatsApp, and it can be configured to notify multiple people.

## Key Features

- Reading of carbon monoxide sensor with ESP32S2
- Checking parameters against established limits
- Communication via MQTT to Python server
- Python server for processing and forwarding notifications to Telegram and WhatsApp

## Repository Structure

The repository is organized as follows:

- [**firmware**](./firmware/): Contains the source code and resources related to the Franzininho board with ESP32S2.
- [**python service**](./python-service/): Includes the Python server code responsible for receiving data via MQTT and forwarding notifications.

## Conclusions

### Completed Items

- [x] Implementation of carbon monoxide sensor reading.
- [x] Configuring connection to a Wi-Fi network.
- [x] Setting up data transmission via MQTT.
- [x] Development of Python server for notification control.
- [x] Configuration for sending notifications to Telegram and WhatsApp.

### Next Steps

- [ ] Implement a fallback mechanism for notifications in case of transmission failure.
- [ ] Improve the configuration interface of the Telegram bot.
- [ ] Optimize the WhatsApp message sending bot.
- [ ] Add support for other notification services.
- [ ] Implement power consumption optimizations on the microcontroller.
- [ ] Enable the possibility to notify multiple people.
- [ ] Implement direct communication with mobile devices via BLE (Bluetooth Low Energy).
- [ ] Implement logging data to a database for future environmental level analysis.

## Team

<ul>
    <li style="display: flex; align-items: center; justify-content: left; margin-bottom: 15px">
        <span style="margin-right: 67px" text="center">José Dias</span>
        <a style="display: flex; align-items: center; align-self: center;" 
        href="https://www.linkedin.com/in/josevmendes"
          target="_blank">
            <img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=flat&logo=linkedin&logoColor=white" target="_blank">  
        </a> 
        <a style="margin-left: 10px; display: flex; align-items: center" href="https://www.github.com/zezit"
          target="_blank">
            <img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" target="_blank">  
        </a> 
    </li>
    <li style="display: flex; align-items: center; justify-content: left; margin-bottom: 15px">
        <span style="margin-right: 43px" text="center">Pedro Hodge</span>
        <a style="display: flex; align-items: center; align-self: center;"
         href="https://www.linkedin.com/in/pedrohodge/"
          target="_blank">
            <img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=flat&logo=linkedin&logoColor=white" target="_blank">  
        </a> 
        <a style="margin-left: 10px; display: flex; align-items: center" href="https://gitlab.com/pedrohodge"
          target="_blank">
            <img src="https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white" target="_blank">  
        </a> 
    </li>
    <li style="display: flex; align-items: center; justify-content: left; margin-bottom: 15px">
        <span style="margin-right: 10px" text="center">Walther Humberto</span>
        <a style="display: flex; align-items: center; align-self: center;"
         href="https://www.linkedin.com/in/walther-humberto/"
          target="_blank">
            <img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=flat&logo=linkedin&logoColor=white" target="_blank">  
        </a> 
        <a style="margin-left: 10px; display: flex; align-items: center" href="https://github.com/waltherHumberto"
          target="_blank">
            <img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" target="_blank">  
        </a> 
    </li>
</ul>

## Contribution

Contributions are welcome! Feel free to open issues and send pull requests for improvements and/or fixes in the project.

## License

This project is licensed under the [MIT License](LICENSE).