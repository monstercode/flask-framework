from functools import wraps
import time


# https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d
# https://flask-restful.readthedocs.io/en/latest/extending.html#response-formats
def time_profiler():
    def decorator(method):
        @wraps(method)
        def decorated_function(*args, **kwargs):
            start = time.time() 
            res = method(*args, **kwargs)
            finish = time.time()
            # fix adding header with X-Time-Elapse
            #res.headers.extend( {'X-Time-Elapsed': '{0:.{1}f}ms'.format((finish-start)*100, 4)} or {})
            return res
            
        return decorated_function
    return decorator
