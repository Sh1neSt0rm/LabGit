# Лабораторная работа: Docker Compose, KVM и Ansible

Небольшое клиент-серверное веб-приложение **Task Manager**, состоящее из фронтенда (Nginx + HTML/JS) и бэкенда (Python + FastAPI), развёрнутое с помощью Docker Compose внутри виртуальной машины KVM (в среде WSL2 на Windows) с автоматизацией через Ansible.

---

## Структура репозитория

```text
.
├── ansible/
│   ├── inventory.ini      # Инвентарь Ansible с адресом KVM VM
│   └── playbook.yml       # Идемпотентный playbook для установки Docker и запуска приложения
├── backend/
│   ├── Dockerfile         # Сборка образа FastAPI-бэкенда
│   ├── main.py            # API эндпоинты (/api/tasks, /api/health)
│   └── requirements.txt   # Зависимости Python
├── frontend/
│   ├── Dockerfile         # Сборка образа Nginx-фронтенда
│   ├── index.html         # Веб-интерфейс приложения
│   └── nginx.conf         # Раздача статики и reverse-proxy запросов /api/ на бэкенд
├── compose.yaml           # Конфигурация Docker Compose для запуска обоих сервисов
└── README.md              # Документация проекта
```

## Команды запуска
Локальный запуск через Docker Compose

```docker compose up -d --build``` 

Создание и запуск VM в KVM внутри WSL2 
```
sudo virt-install \
  --name lab-vm \
  --memory 2048 \
  --vcpus 2 \
  --disk /var/lib/libvirt/images/ubuntu-vm.qcow2,device=disk,bus=virtio \
  --disk /var/lib/libvirt/images/seed.iso,device=cdrom \
  --os-variant ubuntu24.04 \
  --virt-type kvm \
  --graphics none \
  --network network=default,model=virtio \
  --import \
  --noautoconsole  
``` 

Если существует

```sudo virsh net-start default 2>/dev/null || true```

``` sudo virsh start lab-vm```

Проверка статуса виртуальной машины и получение её IP-адреса

```sudo virsh list && sudo virsh domifaddr lab-vm```

Проброс порта из сети KVM (192.168.122.39) на localhost:8080

```ssh -L 0.0.0.0:8080:localhost:8080 ubuntu@192.168.122.39 -N```

Автоматическое развёртывание через Ansible

```ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ansible/inventory.ini ansible/playbook.yml```

## Способ проверки связи фронтенда с бэкендом
### Через терминал (curl)
Проверка получения данных от бэкенда через опубликованный порт фронтенда

```curl [http://192.168.122.39:8080/api/tasks](http://192.168.122.39:8080/api/tasks)```

Ожидаемый ответ

```{"tasks":[{"id":1,"title":"Изучить Docker Compose","done":true},{"id":2,"title":"Настроить KVM","done":true},{"id":3,"title":"Автоматизировать запуск через Ansible","done":true}]}```