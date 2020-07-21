FROM python:3.8-alpine

LABEL maintainer="Pablo Huentelemu <pablo.huentelemu@gmail.com>"

# copy project dependencies
COPY requirements/ /requirements

CMD ls /requirements/
CMD env

# Install dependencies required for building the pip packages below
RUN apk add --update --no-cache gcc libc-dev linux-headers jpeg-dev zlib-dev freetype-dev bash

# Install project dependencies
RUN pip install -r /requirements/k8s.txt

# copy project files
RUN mkdir /django
COPY . /django
WORKDIR /django

EXPOSE 80

#RUN mkdir -p /vol/web/media
#RUN mkdir -p /vol/web/static

#RUN adduser -D user
#RUN chown -R user:user /vol
#RUN chmod -R 755 /vol/web
#RUN chown -R user:user /django_project
#RUN chmod -R 755 /django_project

#USER user

CMD ["/django/docker_entrypoint.sh"]
