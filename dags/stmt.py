CREATE_WEATHER_TABLE = """
create table if not exists weather_datas
(
    id          serial constraint pk_weather_datas primary key,
    city        varchar                 not null,
    date        timestamp default now() not null,
    temperature double precision        not null,
    humidity    double precision        not null
);
"""
INSERT_WEATHER_TABLE = """
insert into weather_data (city, date, temperature, humidity)
values (%s, %s, %s, %s);
"""
