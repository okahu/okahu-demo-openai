import sys
import coffee_rag_openai
import coffee_rag_openai_with_okahu
from credential_utilties.environment import setOpenaiEnvironmentVariablesFromConfig
from credential_utilties.environment import setDataEnvironmentVariablesFromConfig

def main():
    setDataEnvironmentVariablesFromConfig(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] == "okahu":
        mode = "okahu"
    else:
        mode = "normal"
    
    if mode == "okahu":
       coffee_rag_openai_with_okahu.init()
    else:
        coffee_rag_openai.init()
    setOpenaiEnvironmentVariablesFromConfig(sys.argv[1])

    while True:
        prompt = input("Ask a coffee question [Press return to exit]: ")
        if prompt == "":
            break
        if mode == "okahu":
            response = coffee_rag_openai_with_okahu.run(prompt)
        else:
            response = coffee_rag_openai.run(prompt)
        print("Got Answer: " + response[0] + "\n")

if __name__ == "__main__":
    main()
