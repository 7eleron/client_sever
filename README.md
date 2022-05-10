# Клиент-серверное приложение
![Иконка](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSp5Z2C0Jzc6zFpiQuBEcdPc9-LnUTWFqViGg&usqp=CAU)

## Описание
Позволяет выполнять действия для установленного оборудования. 

*Пример: получить список плат определенного типа* 

### Библиотеки
**Клиент**
  * PyQt5 - *графическая основа программы*
  * ElementTree - *сохранение данны в файле xml*
  * request - *отправка запросов на сервер*
  * json - *форматирует запрос в json обьект*

**Сервер**
  * werkzeug - *используется для запуска сервера, а так же получения и отправки запросов-ответов*
  * jsonrpc - *служит для обработки запроса в формате JSON-RPC 2.0*
  * json - *форматирует ответ в json обьект*

### Имеющееся оборудование на сервере

1.Плата Advantech
  * Серия PCI-1602
  * Порт RS422, 1 шт
  * Порт RS485, 1 шт

2.Плата Advantech
  * Серия PCI-1610
  * Порт RS232, 2 шт
  * Порт RS422, 1 шт
  * Порт RS485, 1 шт

3.Плата MOXA
  * Серия CP-102E
  * Порт RS-232, 2 шт

### Методы(возможности)

*  **EnumerateBoards** - возвращает список устройств сервера с полным описанием установленных на нем плат и их характеристик
* **CallPortMethod** - осуществляет вызов метода выбранного порта с получением результата выполнения метода от сервера.
     * в поле `params` вводиться наименование платы, тип(серия), порт, метод
   
#### Форма заполнение запроса

```Python
payload = {
        "method": "enumirateBoard",
        "params": [""],
        "jsonrpc": "2.0",
        "id": 1,
    }
```

![](https://img.shields.io/pypi/v/werkzeug?color=orange&label=werkzeug-python&style=for-the-badge)
![](https://img.shields.io/pypi/v/jsonrpc?label=JSON-RPC%202.0&style=social)







