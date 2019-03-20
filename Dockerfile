FROM python:3.6.5
MAINTAINER Dinda "dinda@alphatech.id"
RUN mkdir -p /demo
COPY . /demo
RUN pip install -r /demo/requirements.txt
WORKDIR /demo
ENTRYPOINT ["python"]
CMD ["app.py"]