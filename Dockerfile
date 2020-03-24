FROM python:3.8
ADD * /app/
RUN pip install -r /app/requirements.txt
CMD [ "python3", "/app/babur.py", "--log-file-path", "/var/log/scripts/babur/babur.log" ]
