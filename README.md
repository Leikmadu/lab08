## Домашнее задание

В репозитории приведен код web-приложения, которое сохраняет в БД введенную информацию о задаче - ее имя.

## Часть I. Docker

1. Добавьте в код Dockerfile, который позволит запустить web-приложение с исходным кодом в каталоге app/ через docker.

Клонируем исходный репозиторий с заданием:

```sh
$ git clone https://github.com/tp-lessons/lab_docker.git
```

```
Cloning into 'projects/lab_docker'...
remote: Enumerating objects: 16, done.
remote: Counting objects: 100% (16/16), done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 16 (delta 1), reused 13 (delta 1), pack-reused 0 (from 0)
Receiving objects: 100% (16/16), 5.01 KiB | 5.01 MiB/s, done.
Resolving deltas: 100% (1/1), done.

```

Перемещаемся в папку app и создаем здесь Dockerfile:

```sh
$ nano Dockerfile
```

такой код:

```sh
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Собираем контейнер:

```sh
$ docker build -t my-flask-app .
```

Вывод:

```
[+] Building 1.6s (10/10) FINISHED                               docker:default
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 199B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.9-slim         1.1s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [1/5] FROM docker.io/library/python:3.9-slim@sha256:2d97f6910b16bd338  0.1s
 => => resolve docker.io/library/python:3.9-slim@sha256:2d97f6910b16bd338  0.1s
 => [internal] load build context                                          0.0s
 => => transferring context: 1.91kB                                        0.0s
 => CACHED [2/5] WORKDIR /app                                              0.0s
 => CACHED [3/5] COPY requirements.txt .                                   0.0s
 => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt        0.0s
 => CACHED [5/5] COPY . .                                                  0.0s
 => exporting to image                                                     0.2s
 => => exporting layers                                                    0.0s
 => => exporting manifest sha256:507e2b5325250dc7d0dc090f2b36723915dc5e1d  0.0s
 => => exporting config sha256:e3b20d037c350d4e12642a0e99c41b52afe6e598af  0.0s
 => => exporting attestation manifest sha256:8ae3b10f0790160057d5958367a3  0.0s
 => => exporting manifest list sha256:32112791e42ac0c0af0c058b1b94c8b57fb  0.0s
 => => naming to docker.io/library/my-flask-app:latest                     0.0s
 => => unpacking to docker.io/library/my-flask-app:latest                  0.0s

```

2. Выполните запуск контейнера с этим приложением.

Запускаем его:

```sh
$ docker run -d --name my-running-app -p 5000:5000 my-flask-app
```

Вывод (его id):

```sh
beabd04e3ec205626635a833b9e4bd2ca23e1661cc85eb70e1d59f45545617da
```

Проверяем, что он запустился:

```sh
$ docker ps
```

Вывод:

```sh
CONTAINER ID   IMAGE          COMMAND           CREATED              STATUS              PORTS                                         NAMES
beabd04e3ec2   my-flask-app   "python app.py"   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   my-running-app

```

3. Скопируйте из консоли в каталог /home/ контейнера файл README.md.

```sh
$ echo "Это пример README" > README.md
```

```sh
docker cp README.md my-running-app:/home/
```

Вывод:

```sh
Successfully copied 27B (transferred 2.05kB) to my-running-app:/home/
```

4. Подключитесь к терминалу контейнера с приложением в интерактивном режиме. Проверьте, что скопированный файл находится в нужном каталоге.

```sh
docker exec -it my-running-app bash
```

```sh
root@beabd04e3ec2:/app# ls /home/
README.md


```

5. Выйти из интерактивного режима.

```sh
root@beabd04e3ec2:/app# exit
exit
```

6. Остановить контейнер с приложением.

```sh
$ docker stop my-running-app

$ docker rm my-running-app
```

## Часть II. Docker compose
1. Создайте файл docker-compose.yml таким образом, чтобы совместно с описанным в части 1 контейнером работала бы база данных mysql. Файл инициализации БД в каталоге db/init.sql. Также пропишите порт подключения к приложению. Например 5000.

```sh
$ cat > docker-compose.yml <<'EOF'
services:
  web:
    build: ./app
    ports:
      - "5000:5000"
    environment:
      DB_HOST: db
      DB_USER: user
      DB_PASS: example
      DB_NAME: mydb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: example
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-prootpassword"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db_data:
 EOF"
```

2. Запустите связку web-приложение - БД.

```sh
$ docker compose up --build
```

3. Проверьте подключение к приложению через браузер. Сделайте снимок экрана.


По ссылке http://localhost:5000 все отображается корректно.
