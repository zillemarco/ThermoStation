from influxdb import InfluxDBClient

DB_ADDRESS = "localhost"
DB_USER = "user"
DB_PWD = "userpass"
DB_DB = "defaultdb"

class DB():
    class __DB():
        def __init__(self):
            self.influxdb_client = InfluxDBClient(host=DB_ADDRESS, port=8086, username=DB_USER, password=DB_PWD, database=DB_DB)

        def write_data(self, key, measurement, value):
            json_body = [{
                'measurement': measurement,
                'tags': {
                    'location': key
                },
                'fields': {
                    'value': value
                }
            }]

            self.influxdb_client.write_points(json_body)

    __instance = None

    def __new__(cls):
        if not DB.__instance:
            DB.__instance = DB.__DB()
        return DB.__instance

    def __getattr__(self, name):
        return getattr(self.__instance, name)
    
    def __setattr__(self, name):
        return setattr(self.__instance, name)