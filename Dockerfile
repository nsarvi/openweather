#Deriving the latest base image
FROM python:latest
RUN pip install requests
RUN pip install mysql-connector-python

#Labels as key value pair
LABEL Maintainer="nsarvi"

# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src

#to COPY the remote file at working directory in container
COPY openweathertest.py ./
COPY GPSLocation.py ./

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD [ "python", "./openweathertest.py"]