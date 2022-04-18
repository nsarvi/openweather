CREATE DATABASE IF NOT EXISTS openweather;

USE openweather;
create table weatherhistory(id int(16) auto_increment, hourlydt timestamp, lat DECIMAL(10, 8), lng DECIMAL(11, 8), temp int, feels_like int, pressure int, humidity int, wind_speed int, primary key (id) );
create table temperaturebymonth(id int(16) auto_increment, lat DECIMAL(10, 8), lng DECIMAL(11, 8), yearmonth int, max_temp int, primary key (id) );
create table temperaturesbyday(id int(16) auto_increment, lat DECIMAL(10, 8), lng DECIMAL(11, 8), date timestamp, avg_temp int, min_temp int, max_temp int, primary key (id) );

