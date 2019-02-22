FROM python:3.6-slim

RUN echo 'Dockerfile-Application'

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# environment variables
ENV APP_SETTINGS="config.ProductionConfig"
ENV FLASK_APP="app/__init__.py"

# expose port
EXPOSE 5000

# run
ENTRYPOINT flask run --host=0.0.0.0