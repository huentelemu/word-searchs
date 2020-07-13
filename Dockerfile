FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache gcc libc-dev linux-headers jpeg-dev zlib-dev freetype-dev
RUN pip install -r /requirements.txt

RUN mkdir /django_project
COPY ./django_project /django_project

WORKDIR /django_project
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
RUN chown -R user:user /django_project
RUN chmod -R 755 /django_project

USER user

CMD ["entrypoint.sh"]
