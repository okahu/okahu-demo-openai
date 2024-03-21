import os
import configparser

import credential_utilties.openai_creds
import credential_utilties.self_hosted_creds
import credential_utilties.okahu_creds

def setEnvironmentVariables():
    jsonDict_openai = credential_utilties.openai_creds.env_dict
    jsonDict_self_hosted = credential_utilties.self_hosted_creds.env_dict
    jsonDict_okahu = credential_utilties.okahu_creds.env_dict

    for jsonDict in [jsonDict_openai, jsonDict_self_hosted, jsonDict_okahu]:
        # Iterate over the JSON dictionary and set the environment variables
        for key, value in jsonDict.items():
            # Substitute the environment variables in the value if needed
            value = os.path.expandvars(value)
            # Set the environment variable with the same key as the JSON field
            os.environ[key] = value

def setTritonEnvironmentVariablesFromConfig(configFilePath):
    setCredEnvironmentVariablesFromConfig(configFilePath,
        [credential_utilties.self_hosted_creds.env_dict, 
         credential_utilties.okahu_creds.env_dict])

def setOpenaiEnvironmentVariablesFromConfig(configFilePath):
    setCredEnvironmentVariablesFromConfig(configFilePath,
        [credential_utilties.openai_creds.env_dict, 
         credential_utilties.okahu_creds.env_dict])

def setCredEnvironmentVariablesFromConfig(configFilePath, jsonDicts):
    config = configparser.ConfigParser()
    config.read(configFilePath)
    
    for jsonDict in jsonDicts:
        # Iterate over the JSON dictionary and set the environment variables
        for key, value in jsonDict.items():
            # Substitute the environment variables in the value if needed
            value = config.get("CREDENTIALS", key)
            value = os.path.expandvars(value)
            # Set the environment variable with the same key as the JSON field
            os.environ[key] = value

def setDataEnvironmentVariablesFromConfig(configFilePath):
    config = configparser.ConfigParser()
    config.read(configFilePath)
    os.environ["AZUREML_MODEL_DIR"] = config.get("DATA", "AZUREML_MODEL_DIR")
