FROM python:3.12

ADD crawler.py .

ADD user_agents.py .

ADD domains.txt .

ADD blacklist.py .

RUN pip install requests

RUN pip install colorama

RUN pip install bs4

CMD ["python", "./crawler.py"]