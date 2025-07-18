**DeepSeek локально для семантического поиска и дообучения**

## 🚀 Шаг 1: Подготовка окружения

#    ### ✅ ollama Docker:

    ```bash
    FROM ollama/ollama:latest

    EXPOSE 11434

    CMD ["ollama", "serve"]
    ```

    docker-compose.yml

    ```bash
    version: '3.8'

    services:
    ollama:
        build: .
        container_name: ollama
        ports:
        - "12000:11434"
        volumes:
        - ollama_data:/root/.ollama   # Хранение моделей вне контейнера
        restart: unless-stopped
        command: serve

    volumes:
    ollama_data:

    ```

#    ### ✅ ollama закачиваем модель:

    https://ollama.com/library/deepseek-r1

    ```bash
    docker exec -it c08b52f5323f ollama pull mxbai-embed-large
    ```

#    ### Тестирование ollama:

    ChromaDB требует Python-библиотеку ollama, чтобы взаимодействовать с локальным Ollama-сервером:

    ```bash
    pip install ollama
    ```

    Тест ollama клиента:

    ```python
    from ollama import Client

    client = Client()
    print(client.list())
    ```
---

## 🚀 Шаг 2: Настройка  бота

export $(grep -v '^#' .env | xargs) && nohup python3 bot.py > bot.log 2>&1 &
nohup python3 bot.py > bot.log 2>&1 &
pkill -f bot.py
ps aux | grep bot.py

docker ps --format "table {{.ID}}\t{{.Status}}\t{{.Ports}}\t{{.Names}}"
    

## 🎓 Шаг 5 (по желанию): Дообучение модели DeepSeek (LoRA)

Если поиск работает, и ты хочешь сделать его **ещё точнее на своих данных**, тогда:

* Создай датасет: `["Запрос пользователя", "Целевая услуга/ответ"]`
* Я помогу тебе дообучить DeepSeek через [LoRA](https://github.com/huggingface/peft)

Готов адаптировать под твою задачу.

---

## 📦 Результат:

| Компонент            | Назначение                              |
| -------------------- | --------------------------------------- |
| `Ollama + DeepSeek`  | Генерация эмбеддингов и (в будущем) LLM |
| `ChromaDB`           | Векторная база для поиска               |
| `pandas`             | Работа с CSV                            |
| `semantic_search.py` | Терминальный интерфейс для общения      |

---

Хочешь, я помогу тебе:

* собрать датасет для дообучения?
* встроить это всё в Telegram-бота?
* или сделать локальный веб-интерфейс?

С чего продолжим?
