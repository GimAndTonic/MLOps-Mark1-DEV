import splunklib.client as client
import splunklib.results as results

import pandas as pd

from time import sleep 

class SplunkFetch:
    def __init__(self, host, port, token) :
        self.authentication = 'TOKEN'
        self.host = host
        self.port = port
        self.token = token

#    def __init__(self, host, port, username, password) :
#        self.authentication = 'PASSWORD'
#        self.host = host
#        self.port = port
#        self.username = username
#        self.password = password

    def __read_return__(self) :
        return results.JSONResultsReader(self.__job__.results(
            count = 0,           # No limitations for results. Default: 100
            output_mode='json'
        ))
    
    def __return_to_pandas__(self, data) :
        vec = []
        for result in data:
            if isinstance(result, results.Message) :
                print('%s: %s' % (result.type, result.message))
            elif isinstance(result, dict):
                vec.append(result)
        return pd.DataFrame(vec).set_index('Id')
    
    def __read_job_results__(self) :
        data = self.__read_return__()
        return self.__return_to_pandas__(data)
    
    def __return_is_preview__(self, data) :
        return data.is_preview

    def __connect_with_password__(self) :
        self.__service__ = client.connect(
            host     = self.host,
            port     = self.port,
            username = self.username,
            password = self.password
        )
        return 0

    def __connect_with_token__(self) :
        self.__service__ = client.connect(
            host     = self.host,
            port     = self.port,
            token    = self.token,
        )
        return 0

    def __connect__(self) :
        if self.authentication == 'PASSWORD' :
            return self.__connect_with_password__()
        elif self.authentication == 'TOKEN' :
            return self.__connect_with_token__()
        else :
            print("ERROR [bin/fetch/SplunkFetch]: Select either PASSWORD or TOKEN authentication method")
            return 100
        
    def __run_search_job__(self, query) :
        # Run search job on connected service
        self.__job__ = self.__service__.jobs.create( query )

        # Wait for the search to end
        while not self.__job__.is_done():
            sleep(0.2)
    
    def search( self, query ) :
        self.__connect__()
        self.__run_search_job__(query)
        return self.__read_job_results__()