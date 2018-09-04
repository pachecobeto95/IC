import imp
from locale import setlocale, LC_NUMERIC, atof

class Module(object):
    # Create based on class name:
    @staticmethod
    def factory(type):
        try:
            type = type.lower()
            py_mod = imp.load_source(type, './app/api/crawlers/'+type+'.py')
            if hasattr(py_mod, type):
                return getattr(py_mod, type)()
            else:
                return None
        except Exception as e:
            print(e)
            raise e
        

    def getModule(self, source, url, stationId=None, tz=None):
        ''' Return the collected data in JSON format'''
        pass
