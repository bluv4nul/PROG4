# Паттерн Command: Реализация в управлении заказами

## Описание паттерна

Паттерн Command (Команда) - это поведенческий паттерн проектирования, который превращает запросы в объекты, позволяя передавать их как аргументы, ставить в очередь, логировать и поддерживать отмену операций.

### Когда использовать паттерн Command?

- Когда нужно параметризовать объекты выполняемым действием
- Когда нужно ставить операции в очередь, выполнять их по расписанию или передавать по сети
- Когда нужна операция undo (отмена)
- Когда нужно логировать все действия системы

### Основные участники паттерна

- **Command**: Интерфейс для выполнения операций. Обычно содержит метод `execute()`
- **Concrete Command**: Реализация конкретных команд. Хранит ссылку на Receiver и параметры операции
- **Invoker**: Вызывает команды для выполнения. Не знает деталей реализации
- **Receiver**: Объект, который знает, как выполнить операцию
- **Client**: Создает команды и передает их Invoker'у

## Применение паттерна: Управление заказами в интернет-магазине

В качестве примера я реализовал систему управления заказами, где паттерн Command позволяет:
- Логировать все операции с заказами для аудита
- Обеспечивать единообразную обработку всех команд через один интерфейс
- Легко добавлять новые операции без изменения существующего кода
- Поддерживать историю действий для отладки и анализа

### Проблема без паттерна

Без паттерна Command код выглядел бы так:

```python
# В контроллере
@app.post("/orders")
def create_order(params):
    order = service.create_order(params.customer_name, params.address, params.total_amount)
    # Логирование дублируется в каждом методе
    logger.info(f"Created order {order.id}")
    return order

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id):
    order = service.confirm_order(order_id)
    logger.info(f"Confirmed order {order_id}")
    return order
```

Проблемы:
- Логика логирования дублируется
- API контроллеры напрямую зависят от бизнес-логики
- Трудно добавить новые операции
- Невозможно отменить действия

## Структура реализации

Проект состоит из следующих модулей:

### 1. Модель данных (`models/order.py`)

Класс `Order` представляет заказ с полями: id, имя клиента, адрес, сумма, статус, скидка.

```python
class Order:
    def __init__(self, order_id: int, customer_name: str, address: str, total_amount: float):
        self._order_id = order_id
        self._customer_name = customer_name
        self._address = address
        self._total_amount = total_amount
        self._status = OrderStatus.NEW
        self._discount_percent = 0

    @property
    def order_id(self): return self._order_id
    @property
    def status(self): return self._status
    @property
    def final_amount(self): return self._total_amount * (1 - self._discount_percent / 100)
```

Модель включает валидацию данных и вычисляемые свойства.

### 2. Получатель (`receiver/receiver.py`)

Класс `OrderService` содержит всю бизнес-логику операций с заказами:

```python
class OrderService:
    @staticmethod
    def create_order(customer_name: str, address: str, total_amount: float) -> Order:
        order_id = max(Orders.keys(), default=0) + 1
        order = Order(order_id, customer_name, address, total_amount)
        Orders[order_id] = order
        return order

    @staticmethod
    def confirm_order(order_id: int) -> Order:
        order = OrderService.get_order_by_id(order_id)
        if order.status == OrderStatus.CANCELLED:
            raise ValueError("ORDER CANNOT BE CHANGED!")
        order.status = OrderStatus.CONFIRMED
        return order
```

Receiver знает, как выполнять операции, но не знает, кто их вызывает.

### 3. Команды (`commands/`)

#### Базовый класс команды (`commands/base.py`)

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> Order:
        pass

    @abstractmethod
    def describe(self) -> dict:
        pass
```

Интерфейс Command определяет контракт для всех команд.

#### Конкретная команда (`commands/create_order.py`)

```python
class CreateOrderCommand(Command):
    def __init__(self, service: OrderService, customer_name: str, address: str, total_amount: float):
        self._service = service
        self._customer_name = customer_name
        self._address = address
        self._total_amount = total_amount

    def execute(self) -> Order:
        return self._service.create_order(
            self._customer_name, self._address, self._total_amount
        )

    def describe(self) -> dict:
        return {
            "command_name": "CreateOrderCommand",
            "parameters": {
                "customer_name": self._customer_name,
                "address": self._address,
                "total_amount": self._total_amount,
            },
        }
```

Каждая команда:
- Хранит ссылку на Receiver
- Сохраняет параметры операции
- Реализует `execute()` - вызывает метод Receiver'а
- Реализует `describe()` - возвращает описание для логирования

### 4. Диспетчер команд (`manager/command_manager.py`)

```python
class CommandManager:
    def __init__(self):
        self._commands_history = []

    def dispatch(self, command: Command):
        result = command.execute()
        self._commands_history.append(command.describe())
        return result

    @property
    def history(self):
        return self._commands_history
```

CommandManager:
- Принимает любую команду через единый интерфейс
- Выполняет ее
- Автоматически логирует операцию
- Возвращает результат

### 5. API слой (`main.py`)

FastAPI приложение связывает HTTP запросы с командами:

```python
app = FastAPI()
manager = CommandManager()
service = OrderService()

@app.post("/orders", response_model=OrderResponse)
async def create_order(params: CreateOrderRequest):
    return manager.dispatch(
        CreateOrderCommand(
            service,
            params.customer_name,
            params.address,
            params.total_amount,
        )
    )
```

API контроллеры стали очень простыми - они только создают команды и передают их менеджеру.

## Как работает паттерн в коде

### Последовательность выполнения

1. **Клиент (API контроллер)** получает HTTP запрос
2. Создает конкретную команду с параметрами
3. Передает команду Invoker'у (CommandManager)
4. **Invoker** вызывает `execute()` у команды
5. **Команда** делегирует выполнение Receiver'у
6. **Receiver** выполняет бизнес-логику
7. Результат возвращается по цепочке обратно клиенту
8. **Invoker** автоматически логирует операцию через `describe()`

### Пример полного цикла

```python
# 1. HTTP запрос: POST /orders
# 2. Контроллер создает команду
command = CreateOrderCommand(service, "Иван", "ул. Ленина 1", 1000.0)

# 3. Передает менеджеру
result = manager.dispatch(command)

# 4. Менеджер вызывает execute()
# 5. CreateOrderCommand вызывает service.create_order()
# 6. OrderService создает заказ
# 7. Возвращается Order объект
# 8. Менеджер логирует: {"command_name": "CreateOrderCommand", ...}
```

## Схема паттерна

![alt text](image.png)

## Сопоставление с кодом

| Элемент паттерна | Реализация в коде | Файл |
|------------------|-------------------|------|
| Client | FastAPI контроллеры | `main.py` |
| Invoker | `CommandManager` | `manager/command_manager.py` |
| Command | Абстрактный класс `Command` | `commands/base.py` |
| Concrete Command | `CreateOrderCommand`, `ConfirmOrderCommand` и др. | `commands/*.py` |
| Receiver | `OrderService` | `receiver/receiver.py` |

## Преимущества реализации

### 1. Разделение ответственности
- API слой занимается только HTTP
- Бизнес-логика сосредоточена в Receiver
- Команды обеспечивают единый интерфейс

### 2. Расширяемость
Новая операция добавляется созданием нового класса команды:

```python
class UpdateOrderCommand(Command):
    def execute(self):
        return self._service.update_order(self._order_id, self._updates)
```

### 3. Логирование
Все операции автоматически логируются без дублирования кода.

### 4. Тестируемость
Команды можно тестировать независимо:

```python
def test_create_order():
    service = OrderService()
    command = CreateOrderCommand(service, "Test", "Address", 100.0)
    order = command.execute()
    assert order.customer_name == "Test"
```

### 5. Поддержка отмены
Можно добавить метод `undo()` в базовый класс Command.

## Запуск проекта

```bash
# Активация виртуального окружения
.venv\Scripts\activate

# Запуск сервера
uvicorn main:app --reload

# Документация API доступна по адресу http://localhost:8000/docs
```

## Примеры использования API

### Создание заказа
```bash
POST /orders
Content-Type: application/json

{
  "customer_name": "Иван Иванов",
  "address": "ул. Ленина, 1",
  "total_amount": 1000.0
}
```

### Получение списка заказов
```bash
GET /orders
```

### Подтверждение заказа
```bash
PATCH /orders/1/confirm
```

### Применение скидки
```bash
PATCH /orders/1/apply_discount
Content-Type: application/json

{
  "discount_percent": 10.0
}
```

### История команд
```bash
GET /commands/history
```

Возвращает массив всех выполненных команд с параметрами.</content>
<parameter name="filePath">c:\Users\andre\Desktop\Uni\repos\PROG4\lab4-pattern-command\README.md