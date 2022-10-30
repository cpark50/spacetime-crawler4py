import string
import re


# This function runs in linear time because it checks every character in a file
def tokenize(resp) -> list:
    tokens = []
    file = resp.raw_response.content
    for line in file:
        line = line.lower()
        token = ""
        for char in line:
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
    tokenFrequencies = {}
    for token in tokens:
        if token not in tokenFrequencies:
            tokenFrequencies[token] = 1
        else:
            tokenFrequencies[token] += 1
    return tokenFrequencies


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

def count_tokens(tokens: dict) -> int:
    total = 0
    for token in tokens:
        total += tokens[token]
    return total


def write_to_log(url: string) -> string:
    tokens = computeWordFrequencies(tokenize(url))

    msg = ""
    msg += "Total number of tokens: " + str(count_tokens(tokens))
    return msg
