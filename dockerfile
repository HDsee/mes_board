FROM python:3.8

WORKDIR /mes_board

ADD . /mes_borad

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .


EXPOSE 3010

CMD [ "python","./app.py"]
