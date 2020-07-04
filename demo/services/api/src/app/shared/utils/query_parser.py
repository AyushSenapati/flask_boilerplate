"""
Module contains few query parameters with default values,
allowed default query parameters, a class to extend these defaults
and parse the query parameters.
"""
from copy import deepcopy

# Application level imports
from app.shared.exceptions.parser import QueryParseError

DEFAULTS = {
    'order_by': 'desc',
    'order_by_field': 'updated_at',
    'page': 1,
    'max_per_page': 10
}

ALLOWED_KEYS_WITH_DTYPE = {
    'order_by': str,
    'order_by_field': str,
    'page': int,
    'max_per_page': int
}


class QueryParser(object):
    """Parser utility to help parsing query parameters.
    It comes with some default query parameters, which can easily be extended
    as per the need of the data managers.
    """
    def __init__(
            self, extend_defaults: dict = {},
            extend_allowed_keys_with_dtype: dict = {}):
        """Query parse constructor, which can be used
        to extend allowed query parameters for the specific data manager.
        Default values can also be updated and extended.
        """
        self.defaults = deepcopy(DEFAULTS)
        self.defaults.update(extend_defaults)
        self.allowed_keys_with_dtype = deepcopy(ALLOWED_KEYS_WITH_DTYPE)
        self.allowed_keys_with_dtype.update(extend_allowed_keys_with_dtype)

    def parse_query_param(self, **kwargs) -> dict:
        """
        Takes request args as parameters and
        returns a dictionary of parsed query parameters.
        In case of error while parsing it raises parsing exception,
        with appropriate status code and error reasons.
        """
        parsed_kwargs = {}
        err_list = []

        # Check if `query_param` is provided,
        # prepare the statement accordingly
        query_param = kwargs.get('query_param')
        statement = "{container}.get(key)".format(
            container='query_param' if query_param else 'kwargs'
        )

        for key in self.allowed_keys_with_dtype:
            # try to fetch values of allowed keys
            val = eval(statement)
            if val:
                try:
                    # Type cast the values as per provided
                    # allowed keys with data types
                    dtype = self.allowed_keys_with_dtype[key]
                    parsed_kwargs[key] = dtype(val)
                except ValueError:
                    err_list.append(f"{key} must be of type: {dtype.__name__}")

        # If error list is not empty due to wrongly
        # passed query parameters by the user, raise parsing exception
        # with appropriate content.
        if err_list:
            raise QueryParseError(
                400,
                msg="Error parsing query parameters",
                data={
                    "type": "error",
                    "class": "QueryParseError",
                    "reason": err_list
                }
            )

        # In case of no exception, update the defaults
        # with parsed key word arguments and return it
        self.defaults.update(parsed_kwargs)
        return self.defaults
