from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from src.config.settings import Config
from src.db.models import Asset, DataSource, BaseFinancialData

class DatabaseManager:
    def __init__(self):
        self.cluster = Cluster(Config.CASSANDRA_NODES, port=Config.CASSANDRA_PORT)
        self.session = self.cluster.connect()
        connection.set_session(self.session)

    def create_keyspace(self):
        self.session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {Config.KEYSPACE_NAME}
            WITH REPLICATION = {{ 'class': 'SimpleStrategy', 'replication_factor': 1 }}
        """)

    def create_tables(self):
        sync_table(Asset)
        sync_table(DataSource)

    def close(self):
        self.cluster.shutdown()
