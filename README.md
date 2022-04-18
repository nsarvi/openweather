# Current Design

The python program calls a OpenWeatherMap API to get the historical weather data from the API 
https://api.openweathermap.org/data/2.5/onecall/timemachine for 10 locations and inserts into the MySQL database as show in the below figure.



![Current Design](images/current-design.png?raw=true "Current Design")

The current implementation has many drawbacks such as
1. Resilient 
2. Scalable
3. Fault tolerant 
4. 12 factors complaint for microservices architecture style. 
5. DB specific indexes/hints for parser
6. DB table partition based on lat/lng 

In case, Openweather OR MySQL is down, is Python resilient to faults in the upstream and/or downstream  ? No.
What if there is a need to ingest weather data in real time from all the cities around the world ? Is this scalable ? No.

We can improve the current design as outlined in the proposed architecture

# Proposed Architecture

The proposed design is highly scalable as long as the producer and consumer are implemented for 12 factor and resiliency. 

## Resiliency
1. Connections through Load balancer
2. Retries, Retry interval and retry elapsed 
3. Publisher confirmation/Acks
4. Consumer Acks
5. Dead letter/reprocessing (Seems overkill for timeseries data ? may be)

## Scalable
1. Idempotent
2. Disposable
3. Externalize configurations
4. Multiple producers and consumers

I still see DB will become bottleneck for real time and scalable ingestion data flows. This can be replaced with NoSQL and/or Massively parallel processing (MPP) distributed 
systems like Snowflake, Greenplum, Redshift etc.


![Propsed Design](images/proposed-design.png?raw=true "Proposed Design")

# Check out 
Check out the repo
git clone https://github.com/nsarvi/openweather.git

# Run
```
cd openweather
```
create a file name called api.env and enter the APIKEY environment variable as below

APIKEY=<your-api-key>
```
docker compose up

```
```
The docker compose initializes mysql DB, creates few tables and then run the openweathermain.py once mysql is healthy.

openweathermain.py simply calls API and extracts fields from the JSON response and inserts into MySQL in batches. 

```
docker exec -it <mysql-container-id> /bin/bash
```
```
/# mysql -u test -p
Enter the password as test
```

```
mysql> use openweather;

mysql>select * from temperaturebymonth;

mysql>select * from temperaturesbyday;
```


![Results](images/results.png?raw=true "Results")