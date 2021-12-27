FROM nikolaik/python-nodejs:latest

COPY . /usr/src/backend
WORKDIR /usr/src/backend
RUN pip install -r requirements.txt
EXPOSE 5000
# ENTRYPOINT [ "python" ]
CMD ["python", "server.py" ]

WORKDIR /usr/src/frontend
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD [ "npm", "start" ]