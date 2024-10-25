FROM python:3.9

WORKDIR /docker/app/get_answer_rozetka

COPY . .

RUN pip install --no-cache-dir -r req.txt

CMD ["python", "-u", "main.py"]