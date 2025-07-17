


# 🚴‍♂️ API-тесты для сервиса Яндекс.Самокат

Проект содержит автотесты для проверки API сервиса Яндекс.Самокат. Написан на Python с использованием `pytest`, `requests`, `allure-pytest`.

---

## 📁 Структура проекта
```text
Sprint_7/
│
├── conftest.py                     # фикстуры pytest
├── .gitignore                      # гитигнор =)
├── README.md                       # вы здесь
├── requirements.txt                # зависимости проекта
│
├── data/                           # тестовые данные и константы
│   └── urls.py                     # URL - адреса
│
├── helpers/                        # вспомогательные функции
│   └── generator.py                # генератор пользователей и другие утилиты
│
├── api/                            # запросы к API (Page Object слой)
│   └── courier_api.py              # методы: создать курьера, логин и т.п.
│   └── order_api.py                # методы: создать заказ, получить список
│
├── tests/                          # все тесты, организованные по тематике
│   ├── test_courier_create.py      # тесты создания курьера
│   ├── test_courier_login.py       # тесты логина курьера
│   ├── test_courier_delete.py      # тесты удаления курьера
│   ├── test_orders_create.py       # тесты создания заказов
│   ├── test_orders_list.py         # тесты списка заказов
│   ├── test_order_accept.py        # тесты подтверждения заказа
│   └── test_order_get_by_track.py  # тесты удаления курьера
│
└── allure-results/                 # allure - отчет о тестирование
```

---

## 🧪 Как запустить тесты

### 🔧 Установи зависимости:

```bash
pip install -r requirements.txt
```
### ▶️ Запусти все тесты:

```bash
pytest -v
```

### 📌 Запусти тесты с генерацией Allure-отчёта:

```bash
# Сделать и посмотреть
pytest --alluredir=allure-results
allure serve allure-results
# Сгенерировать и сохранить, открыть сгенерированный
pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```
## 🧰 Используемый стек

* Python 3.11+
* pytest
* requests
* allure-pytest


## 🧬 Примеры тестов (не полный перечень)
✅ Регистрация курьера:
* Успешная регистрация
* Дубликат логина
* Ошибки при нехватке данных (с параметризацией)

✅ Авторизация:
* Успешный вход
* Неверный логин/пароль
* Отсутствие обязательных полей

✅ Заказы:
* Создание заказа (все кейсы с цветом)
* Получение заказа по номеру
* Получение списка заказов