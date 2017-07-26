import requests, json, datetime, time

"""
Makes series of github requests starting from the start year, 2008 to the last year
Gets the total number of repositories per year
Since these are static values they only have to be requested once
This has its own method so that the app can be used year over year

While only a .5% sample is required to be representative, github api returns total count
So why not
"""

"""
Returns the amount of time needed to sleep before search API
rate limit resets
"""
def getSleepTime():
    rateLimitURL = "https://api.github.com/rate_limit"
    req = requests.get(rateLimitURL)
    reqJSON = json.loads(req.content.decode("utf-8"))

    resetTime = int(reqJSON['resources']['search']['reset'])
    timeLeft = time.time() - resetTime

    if (timeLeft < 0):
        timeLeft = 0

    return timeLeft

#Authentication not required! Rate limiting is more severe though
queryURL = "https://api.github.com/search/repositories?q="

#Can be used per year
githubStartYear = 2008
lastYear = datetime.datetime.now().year - 1
yearRange = range(githubStartYear, lastYear)

#Returns array of tuples containing annual counts for all repos
def getTotalAnnual():
    reposPerYear = []

    for year in yearRange:
        dateQuery = "created:{0}-01-01..{0}-12-31".format(str(year))
        query = queryURL+dateQuery
        req = requests.get(query)
        
        #Query is returned as a byte string so decode it then load as JSON
        reqJSON = json.loads(req.content.decode("utf-8"))
        try:
            count = reqJSON['total_count']
            reposPerYear.append((year, count))
        except KeyError:
            time.sleep(getSleepTime())
            count = reqJSON['total_count']
            reposPerYear.append((year, count))

    return reposPerYear

#Returns array of tuples containing annual counts for all python repos
def getPythonAnnual():
    pythonPerYear = []

    for year in yearRange:
        dateQuery = "created:{0}-01-01..{0}-12-31".format(str(year))
        pythonQuery = "language:python"
        query = queryURL + dateQuery + "+" + pythonQuery
        req = requests.get(query)

        reqJSON = json.loads(req.content.decode("utf-8"))

        try:
            count = reqJSON['total_count']
            pythonPerYear.append((year, count))
        except KeyError:
            time.sleep(getSleepTime())
            count = reqJSON['total_count']
            pythonPerYear.append((year, count))

    return pythonPerYear

def getRAnnual():
    rPerYear = []

    for year in yearRange:
        dateQuery = "created:{0}-01-01..{0}-12-31".format(str(year))
        pythonQuery = "language:r"
        query = queryURL + dateQuery + "+" + pythonQuery
        req = requests.get(query)

        reqJSON = json.loads(req.content.decode("utf-8"))

        try:
            count = reqJSON['total_count']
            rPerYear.append((year, count))
        except KeyError:
            time.sleep(getSleepTime())
            count = reqJSON['total_count']
            rPerYear.append((year, count))
        
        rPerYear.append((year, count))

    return rPerYear
