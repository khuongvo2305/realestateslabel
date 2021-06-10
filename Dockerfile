FROM python:3.8-slim

RUN mkdir -p /meow
RUN adduser --disabled-password --gecos '' code_boy_9x
RUN chown -R code_boy_9x:code_boy_9x /meow

RUN apt update
RUN pip install --upgrade pip

RUN python3 -m venv /meow/venv
RUN /meow/venv/bin/pip install --upgrade pip
COPY requirements.txt /meow/requirements.txt
RUN /meow/venv/bin/pip install -r /meow/requirements.txt

USER code_boy_9x
WORKDIR /meow

COPY . .

ENTRYPOINT [ "venv/bin/python", "-u", "./app.py" ]
