import sys
import logging
import warnings

import coffee_rag_openai
import coffee_rag_openai_with_okahu

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "okahu":
        mode = "okahu"
    else:
        mode = "normal"
    
    if mode == "okahu":
       coffee_rag_openai_with_okahu.init()
    else:
        coffee_rag_openai.init()

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
    logging.getLogger().setLevel(logging.ERROR)
    warnings.filterwarnings("ignore")
    main()
