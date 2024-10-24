FROM python:3.10-slim

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

# Set work directory
# Maine folder will be create with such name in docker container
WORKDIR /app

# Install dependencies
RUN pip3 install --upgrade pip
COPY /requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

# migratons
CMD ["sh", "-c", "python manage.py makemigrations"]

EXPOSE 8000