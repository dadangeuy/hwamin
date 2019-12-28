FROM python:3.7-slim
MAINTAINER Irsyad Rizaldi <irsyad.rizaldi97@gmail.com>

WORKDIR application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --no-input
ENTRYPOINT ["daphne"]
CMD ["-b", "0.0.0.0", "-p", "80", "hwamin.asgi:application"]
