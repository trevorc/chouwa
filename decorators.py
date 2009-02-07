def jinjaglobal(function):
    '''
    Mark a callable as a jinja global.

    '''

    function.is_jinja_global = True
    return function

def jinjafilter(function):
    '''
    Mark a callable as a jinja filter.

    '''

    function.is_jinja_filter = True
    return function
