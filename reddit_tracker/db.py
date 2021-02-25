from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

def db_connect():
    ''' Connect to influxdb'''
    client = InfluxDBClient.from_config_file("praw.ini") # Configuration of influxdb lives in praw.ini too!
    return client

def db_write(client, bucket, org, data):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket, org, data)

def check_exists(client, bucket, created_utc):
    ''' Example query '''
    db_values = []

    response = client.query_api().query(f'from(bucket:"{bucket}")'
                                        f'|> range (start: 2021-01-01T00:00:00Z, stop: 2021-02-21T00:00:00Z)'
                                        f'|> filter(fn: (r) => r._time == {created_utc})') 
    for table in response:
        for record in table.records:
            db_values.append(record.values)
    return db_values
