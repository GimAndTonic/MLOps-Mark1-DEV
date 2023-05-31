from bin.fetch.fetch import SplunkFetch
from bin.secretparser.splunk import read_token

host, port, token = read_token()

splunk = SplunkFetch(host, port, token)
print(splunk.search("inputlookup iris-data.csv"))