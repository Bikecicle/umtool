FROM python:2.7

ADD main $HOME/main
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "main/spawner_internal.py" ]
