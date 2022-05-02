FROM python:3.8

WORKDIR /mes_board

ADD . /mes_borad

COPY requirements.txt requirements.txt

ENV rdsHost = "mes-db.c2ubtzynxmfz.ap-northeast-1.rds.amazonaws.com"

ENV rdsDatabase = "table1"

ENV rdsUser = "admin"

ENV rdsPassword = "00000000"

ENV s3ID = "AKIA4YTBU64H4OFMBZV2"

ENV s3Key = "s8s+Cb7nOhtLjOt+opsDmtLE9k9WhalMmqgEudHX"

RUN pip3 install -r requirements.txt

COPY . .


EXPOSE 3010

CMD [ "python","./app.py"]
