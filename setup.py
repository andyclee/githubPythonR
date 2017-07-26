"""
Meant to be run initially to create Cassandra keyspace
"""
import const
from cassandra.cluster import Cluster
cluster = Cluster()
session = cluster.connect()

create = """
CREATE KEYSPACE IF NOT EXISTS {0}
WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
"""
create = create.format(const.KEYSPACE)

session.execute(create)
