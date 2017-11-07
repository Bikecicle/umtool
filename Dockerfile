FROM python

ADD main $HOME/main
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "main/run_standalone_pollermanager.py" ]
