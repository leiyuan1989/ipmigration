#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 10:27:08 2025

@author: leiyuan
"""
import functools
import signal
def timeout(sec):
    """
    timeout decorator
    :param sec: function raise TimeoutError after ? seconds
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):

            def _handle_timeout(signum, frame):
                err_msg = f'Function {func.__name__} timed out after {sec} seconds'
                raise TimeoutError(err_msg)

            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(sec)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapped_func
    return decorator


if __name__ == 'main':
    import time
    @timeout(3)
    def slow_func():
        time.sleep(100)
    
    
    try:
        slow_func()
    except TimeoutError:
        pass