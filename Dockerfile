FROM authz_shared:latest

COPY requirements.txt .
#we first install the packages, because there is not too much changes in packages, so whenever we have to rebuild it, 
# it wont create this layer
RUN pip install -r requirements.txt

ARG APP_PORT=8000
ENV APP_PORT $APP_PORT
EXPOSE $APP_PORT

ENV APP_WORKERS 6
ENV APP_THREADS 3

#copy anything that we have in this directory to the container
COPY . .

CMD ./start.sh