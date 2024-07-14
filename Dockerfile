FROM python:3.10-slim

SHELL ["/bin/bash", "-c"]

RUN apt-get update -qq && \
      mkdir /app


WORKDIR /app

# Copy as early as possible so we can cache ...
ADD requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

ADD . .

RUN pip install rasa==3.6.20
RUN pip install spacy==3.7.5
RUN python -m spacy download "pt_core_news_md"

RUN pip install sklearn_crfsuite
VOLUME ["/app/data"]

EXPOSE 5005

RUN rasa train

CMD python -m rasa run --enable-api --endpoints endpoints.yml --credentials credentials.yml --debug