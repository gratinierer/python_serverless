from parliament import Context
from flask import Request
import json
import csv
import pandas as pd
from sqlalchemy import create_engine, types

# parse request body, json data or URL query parameters
def payload_print(req: Request) -> str:
    if req.method == "POST":
        if req.is_json:
            return json.dumps(req.json) + "\n"
        else:
            # MultiDict needs some iteration
            ret = "{"

            for key in req.form.keys():
                ret += '"' + key + '": "'+ req.form[key] + '", '

            return ret[:-2] + "}\n" if len(ret) > 2 else "{}"

    elif req.method == "GET":
        # MultiDict needs some iteration
        ret = "{"

        for key in req.args.keys():
            ret += '"' + key + '": "' + req.args[key] + '", '

        return ret[:-2] + "}\n" if len(ret) > 2 else "{BAMGET}"


# pretty print the request to stdout instantaneously
def pretty_print(req: Request) -> str:
    ret = str(req.data)
    engine = create_engine('mysql://root:testur@mariadb/testdb') # enter your password and database names here

    df = pd.read_csv(ret,sep=',',quotechar='\'',encoding='utf8') # Replace Excel_file_name with your excel sheet name
    df.to_sql('Table_name',con=engine,index=False,if_exists='append') # Replace Table_name with your sql table name
    return ret

 
def main(context: Context):
    """ 
    Function template
    The context parameter contains the Flask request object and any
    CloudEvent received with the request.
    """

    # Add your business logic here
    print("Received request")

    if 'request' in context.keys():
        ret = pretty_print(context.request)
        print(ret, flush=True)
        return "processed", 200
    else:
        print("Empty request", flush=True)
        return "{GET??}", 200
