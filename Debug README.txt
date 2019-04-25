if testing in windows, make sure your env PATH has your anaconda instalation adress correct.

libraries:
-tweepy
-time
-argparse
-string
-config
-json
-pyodbc 
-datetime
-pathlib

#ERRORS#
pyodbc.InterfaceError: ('IM002', '[IM002] [Microsoft][ODBC Driver Manager] Data source name not found and no default driver specified (0) (SQLDriverConnect)')
	install ODBC sql driver for your OS