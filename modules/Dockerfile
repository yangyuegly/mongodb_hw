FROM python:3
ADD . /app
WORKDIR /app
EXPOSE 4000
RUN pip install --upgrade pip
RUN python3 -m pip install pymongo[srv]
RUN pip install -r requirements.txt
RUN npm i plotly.js-dist
ENTRYPOINT ["python","index.py"]


