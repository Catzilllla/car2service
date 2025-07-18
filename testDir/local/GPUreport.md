## ✅ 1: Проверка есть ли GPU на ПК

```
pip install torch
```

```bash
python -c "import torch; print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'GPU не найден')"
```
---
## 📌 Если GPU нет или недоступен:
* Будет использоваться **CPU**.
* Убедись, что ты ставишь **CPU-версии `torch`**, чтобы не ловить ошибок.

## ✅ 2: Выбор модели и установка соотв-х зависимостей

## 📌 GPU:


## 📌 CPU:
