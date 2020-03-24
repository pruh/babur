FROM python:3.8
ADD * /app/
RUN pip install -r /app/requirements.txt
CMD [ "python3", "/app/babur.py", "--username", "admin", "--password", "77LJC6BaZs4ipt1L", "--log-file-path", "/var/log/scripts/babur/babur.log" ]
