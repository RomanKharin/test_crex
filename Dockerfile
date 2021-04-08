FROM python:3.8-alpine
LABEL maintainer=romiq.kh@gmail.com

COPY /requirements.txt /build/requirements.txt

RUN apk add build-base &&\
    pip install -r /build/requirements.txt &&\
    adduser -D -H -h /app -u 1000 crawler crawler &&\
    mkdir -p /app/crawler &&\
    echo "#!/bin/sh" > /app/entrypoint.sh &&\
    echo "set -e" >> /app/entrypoint.sh &&\
    echo "exec \"\$@\"" >> /app/entrypoint.sh &&\
    mkdir -p /spool &&\
    echo "# min   hour    day     month   weekday command" > /spool/crawler && \
    echo "*/2	*	*	*	*	python -m crawler" >> /spool/crawler

WORKDIR /app

COPY /crawler/*.py /app/crawler/

RUN chmod a+x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["crond", "-c", "/spool", "-f", "-d", "8"]
