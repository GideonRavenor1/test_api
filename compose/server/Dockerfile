FROM python:3.10.6-slim-buster

WORKDIR /opt/test_api/

# Скачивание скрипта ожидания загрузки бд https://github.com/ufoscout/docker-compose-wait
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait

ARG USER_UID=4224
ARG USER_NAME=test_api
RUN adduser --system --uid $USER_UID --group $USER_NAME
RUN mkdir -p /opt/test_api/logs && mkdir -p /opt/test_api/static && \
    chown -R $USER_UID:$USER_UID /opt/test_api/logs && chown -R $USER_UID:$USER_UID /opt/test_api/static

RUN pip install poetry==1.3.2 --no-cache-dir && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /opt/test_api/

RUN poetry install --no-interaction --no-ansi --directory=/opt/test_api/ && \
    rm -rf ~/.cache/pypoetry/cache/ && \
    rm -rf ~/.cache/pypoetry/artifacts/

COPY . /opt/test_api/

RUN chmod +x /wait && chown $USER_UID:$USER_UID /wait

EXPOSE 8000

USER $USER_UID

# Запуск скрипта ожидания
CMD /wait
