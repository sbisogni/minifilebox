FROM ubuntu:latest
MAINTAINER Simone Bisogni "simone.bisogni@ayahoo.it"
RUN apt-get update -y
RUN apt-get install -qy python3-pip git
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]