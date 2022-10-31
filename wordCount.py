#file name should be changed to tokenize.py
import string
import re
from bs4 import BeautifulSoup
import json
import logging


tokenTotalFrequencies = {}

# This function runs in linear time because it checks every character in a file
def tokenize(raw_content) -> list:
    page_txt = re.sub(r'\d+', '', raw_content)
    tok_txt = page_txt.split() # get each token string, to be trimmed of punctuation
    num_words = 0
    tokens = []
    for token in tok_txt:
        low_word = token.lower()
        low_word.strip(string.punctuation) # get rid of the punctuation surrounding the word
        for char in token:
            if isAlphaNumeric(char):
                token += char
            else:
                if token != "":
                    tokens.append(token)
                token = ""
        if isAlphaNumeric(token):
            tokens.append(token)
    return tokens


# This function is linear time because it will check all elements of the input list
def computeWordFrequencies(tokens : list) -> dict:
    tokenCurrentFrequencies = {}
    
    for token in tokens:
        if token not in tokenCurrentFrequencies:
            tokenCurrentFrequencies[token] = 1
            if token not in tokenTotalFrequencies:
                tokenTotalFrequencies[token] = 1
        else:
            tokenCurrentFrequencies[token] += 1
            tokenTotalFrequencies[token] += 1
        
    return tokenCurrentFrequencies


def sort_tokens(tokenDict: dict) -> list:
    return sorted(tokenDict.items(), key=lambda x: x[1], reverse=True)


# This function is O(nlogn) because it will sort the input
def printTokens(tokenFrequencies: dict):
    for token in sort_tokens(tokenFrequencies):
        print(token[0], token[1])


# This function is linear time because it will check if the entire input matches regex pattern
def isAlphaNumeric(text) -> bool:
    if re.match("^[a-z0-9]+$", text):
        return True
    return False

def count_tokens(tokens: dict) -> int:
    total = 0
    for token in tokens:
        total += tokens[token]
    return total


def write_to_log(content, url) -> string:
    tokens = computeWordFrequencies(tokenize(content))
    tokenCount = count_tokens(tokens)
    logging.basicConfig(filename='numTokens.log', filemode='w', level=logging.INFO)
    logging.info(f'Number of words in {url} is {tokenCount}')
    # file1 = open("numTokens.txt", "w")
    # file1.writelines(f"Number of words in {url} is {str(count_tokens(tokens))}")
    # file1.close()
    file2 = open("wordCount.txt", "w")
    json.dump(tokenTotalFrequencies, file2)
    file2.close()

    # msg = "Total number of tokens: " + str(count_tokens(tokens))
    # return msg
    return
   


# def main():
#     try:
#         textFilePath = sys.argv[1]
#         tokens = computeWordFrequencies(tokenize(textFilePath))
#         printTokens(tokens)
#     except IndexError:
#         print("please provide file name to count tokens")
#
#
# if __name__ == "__main__":
#     main()

