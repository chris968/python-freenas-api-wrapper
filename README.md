# freenas-api-python-wrapper
Python wrapper to normalize interaction with FreeNAS API

Each function return a json output that contain a 'status' value set to 'ok' or 'error' and a 'data' value that return the output of fetch function like 'listusers' or the the error message when the 'status' was set to 'error'.
