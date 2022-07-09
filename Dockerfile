FROM python:3.10

WORKDIR /app

COPY . .

RUN python -m venv .venv

RUN .venv\Scripts\activate

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD ["app.py"]
