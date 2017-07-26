import counts
import const
import datetime
from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect(const.KEYSPACE)

"""
Name is a unique identifier as determined by the Flask app
"""
def loadFreshData(name):
   create = """
USE {0}
CREATE TABLE {1} (
year int,
count int,
type text
PRIMARY KEY (
