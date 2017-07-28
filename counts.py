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
    curTime = time.time()
    timeLeft = resetTime - curTime

    if (timeLeft < 0):
        timeLeft = 0

    return timeLeft

#Authentication not required! Rate limiting is more severe though
queryURL = "https://api.github.com/search/repositories?q="

#Can be used per year
githubStartYear = 2008
lastYear = datetime.datetime.now().year - 1
yearRange = range(githubStartYear, lastYear)

"""
Try catch logic could also be included here but in order to minimize duplicate code
it is not
"""
def querySearch(query):
    req = requests.get(query)
    reqJSON = req.json()

    count = reqJSON['total_count']
    return count

#Returns array of tuples containing annual counts for all repos
def getTotalAnnual():
    reposPerYear = []

    for year in yearRange:
        dateQuery = "created:{0}-01-01..{0}-12-31".format(str(year))
        query = queryURL+dateQuery
        
        try:
            count = querySearch(query)
            reposPerYear.append((year, count))
        except KeyError:
            time.sleep(getSleepTime() + 1.0)
            count = querySearch(query)
            reposPerYear.append((year, count))

    return reposPerYear

#Helper method for getLangAnnual, validates language selected
def isValidLang(language):
    langQuery = "language:{0}".format(language.lower())
    query = queryURL + langQuery
    req = requests.get(query)
    reqJSON = req.json()

    if 'errors' in reqJSON:
        return False
    return True

#Returns array of tuples containing annual counts for all repos with a certain
#language
def getLangAnnual(language):
    if not isValidLang(language):
         return { 'error' : 'Language invalid' }
    
    langPerYear = []

    for year in yearRange:
        dateQuery = "created:{0}-01-01..{0}-12-31".format(str(year))
        langQuery = "language:{0}".format(language.lower())
        query = queryURL + dateQuery + "+" + langQuery

        try:
            count = querySearch(query)
            langPerYear.append((year, count))
        except KeyError:
            time.sleep(getSleepTime() + 1.0)
            count = querySearch(query)
            langPerYear.append((year, count))

    return langPerYear
