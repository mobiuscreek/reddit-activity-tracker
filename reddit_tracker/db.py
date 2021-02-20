from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

def db_connect():
    ''' Connect to influxdb'''
    client = InfluxDBClient.from_config_file("praw.ini")
    return client

def db_write(client, bucket, org, data):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    for data_point in data:
        write_api.write(bucket, org, data_point)

def db_read(client, bucket):
    ''' Example query '''
    db_values = []
    tables = client.query_api().query('from(bucket:"reddit_tracker") |> range(start: -10m) |> filter(fn: (r) => r.subreddit == "wallstreetbets")')
    for table in tables:
        for record in table.records:
            db_values.append(record.values)
    return db_values
