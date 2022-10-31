#file name should be changed to tokenize.py
import string
import re
from bs4 import BeautifulSoup
import json
import logging


tokenTotalFrequencies = {}
stopwords = set(["a","about","above","after","again","against","all","am","an","and","any","are","aren't",\
            "as","at","be","because","been","before","being","below","between","both","but","by","can't",\
            "cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during",\
            "each","few","for","from","further","had","hadn't", 'has', "hasn't", 'have', "haven't", 'having', \
            'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', \
            'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", \
            'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of',\
            'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',\
            'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than',\
            'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', \
            'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', \
            'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", \
            'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', \
            'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", \
            'your', 'yours', 'yourself', 'yourselves'])

# This function runs in linear time because it checks every character in a file
def tokenize(raw_content) -> list:
    page_txt = re.sub(r'\d+', '', raw_content)
    tok_txt = page_txt.split() # get each token string, to be trimmed of punctuation
    num_words = 0
    tokens = []
    for token in tok_txt:
        low_word = token.lower()
        if len(token) > 1:
            if token not in stopwords:
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
    file2 = open("wordCount.txt", "w")
    json.dump(tokenTotalFrequencies, file2)
    file2.close()

    # msg = "Total number of tokens: " + str(count_tokens(tokens))
    # return msg
    return
   

def del_global_token():
    global tokenTotalFrequencies
    del tokenTotalFrequencies

def sort_total():
    global tokenTotalFrequencies
    sort_tokens(tokenTotalFrequencies)
    file2 = open("wordCount.txt", "w")
    json.dump(tokenTotalFrequencies, file2)
    file2.close()

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

