import json

def print_top50():
    with open("word_count.json", "r") as file:
        data = json.load(file)
        print(sorted(data.items(), key=lambda x: x[1], reverse=True)[:50])


def print_subdomains():
    with open("subdomains.json", "r") as file:
        data = json.load(file)
        print(sorted(data.items(), key=lambda x: x[0].lower()))

if __name__ == '__main__':
    print_top50()
    print_subdomains()

# honestly i just left it as untitled.py in my folder lmao
