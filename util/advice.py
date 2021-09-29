import re
import sys
import traceback
from flask import jsonify
from util.exceptions import AppException
from util.logger import logger


class ErrorHandler:
    def __init__(self, error):
        if not isinstance(error, AppException):
            stack_trace = list()
            ex_type, ex_value, ex_traceback = sys.exc_info()
            trace_back = traceback.extract_tb(ex_traceback)

            for trace in trace_back:
                stack_trace.append(
                    'File : {}, Line : {}, Func.Name : {}, Message : {}'.format(trace[0], trace[1], trace[2], trace[3]))

            messages = str(error)
            logger.error(messages + " %s", stack_trace)

            if hasattr(error, 'messages'):
                messages = error.messages
            elif hasattr(error, 'message'):
                messages = error.message

            error = AppException(messages)

        response = jsonify(error.to_dict())
        response.status_code = error.status_code

        self.response = response

    @staticmethod
    def _snake_case(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str(name))
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
