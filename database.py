import counts
import const

import uuid
from collections import defaultdict
from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect(const.KEYSPACE)

#DELETE AFTER TEST
annualTest = [(2008, 21823), (2009, 84464), (2010, 198499), (2011, 479181), (2012, 1103613), (2013, 2140347), (2014, 3708582), (2015, 6157012)]
langTest = { "python" : [(2008, 1446), (2009, 7304), (2010, 17024), (2011, 37955), (2012, 72248), (2013, 130200), (2014, 213544), (2015, 353165)], "r" : [(2008, 18), (2009, 69), (2010, 264), (2011, 830), (2012, 2420), (2013, 6104), (2014, 43983), (2015, 61744)] }

"""
Name is a unique identifier as determined by the Flask app
"""
def loadFreshData(queryName, languages):
    #session.execute("DROP TABLE {0}.data".format(const.KEYSPACE))
    createTable = """
    CREATE TABLE IF NOT EXISTS {0}.data (
    id uuid,
    queryid uuid,
    year int,
    count int,
    type text,
    PRIMARY KEY (queryid, id)
    )
    """
    createTable = createTable.format(const.KEYSPACE)
    session.execute(createTable)

    annualValues = counts.getTotalAnnual()

    #Store language values in dict
    langValues = {}
    for language in languages:
        langTotal = counts.getLangAnnual(language)
        langValues[language] = langTotal

    insert = """
    INSERT INTO {0}.data
    (id, queryid, year, count, type)
    VALUES ({1}, {2}, {3}, {4}, {5});
    """
    for year in annualValues:
        totalInsert = insert.format(const.KEYSPACE, uuid.uuid4(), queryName, year[0], year[1], "'total'")
        session.execute(totalInsert)

    for lang in langValues.keys():
        for year in langValues[lang]:
            langName = "'" + lang + "'"
            langInsert = insert.format(const.KEYSPACE, uuid.uuid4(), queryName, year[0], year[1], langName)
            session.execute(langInsert)

"""
Gets the combined total of languages as list
"""
def getCombined(results):
    combined = {}

    for repoType in results.keys():
        if repoType != 'total':
            langCount = results[repoType]
            for count in langCount:
                if count[0] in combined:
                    combined[count[0]] += count[1]
                else:
                    combined[count[0]] = count[1]

    combinedList = []
    for year in combined.keys():
        combinedList.append((year, combined[year]))

    return combinedList

"""
The current data modeling does not allow for maximally efficient querying across
a cluster but since the database is currently run over a single node, it is
less problematic
"""
def getData(queryName):
    query = """
    SELECT year, count, type FROM {0}.data WHERE queryid = {1}
    """
    query = query.format(const.KEYSPACE, queryName)
    queryResult = session.execute(query)

    results = defaultdict(list)
    for row in queryResult:
        results[row.type].append((row.year, row.count))

    combinedName = ""

    for lang in results.keys():
        if lang != 'total':
            combinedName += lang + ","

    combinedName = combinedName[:-1]

    results[combinedName] = getCombined(results)

    return results
