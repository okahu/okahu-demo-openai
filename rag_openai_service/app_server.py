import sys
import os
from flask import Flask, request, jsonify
import coffee_rag_openai
from credential_utilties.environment import setOpenaiEnvironmentVariablesFromConfig
from credential_utilties.environment import setDataEnvironmentVariablesFromConfig

web_app = Flask(__name__)

def main():
    print("Starting web server for OpenAI coffee app ")
    setDataEnvironmentVariablesFromConfig(sys.argv[1])
    coffee_rag_openai.init()
    setOpenaiEnvironmentVariablesFromConfig(sys.argv[1])
    web_app.run(host="0.0.0.0", port=8096, debug=False)

@web_app.route('/',methods = ["GET"])
def processclaim():
    try:
        query = request.args["request"]
        response = coffee_rag_openai.run(query)
        return response[0]
    except Exception as e:
        print(e)
        return jsonify({"Status":"Failure --- some error occured"})
    
if __name__ == "__main__":
    main()
