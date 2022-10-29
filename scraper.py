import re
from urllib.parse import urlparse, urldefrag, urljoin
from bs4 import BeautifulSoup
from string import punctuation

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. 
    # Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    return_urls = []
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

    if is_valid(resp.url):
        # if resp.status >= 300 or resp.status <= 399: # error response idk how we should filter this
        #     print(resp.status, resp.error)
        #     return list()
        if resp.status >= 200 or resp.status <= 399: 
            if resp.raw_response != None: # returns no data
                # need to make sure each url is valid before adding it to the list
                soup = BeautifulSoup(resp.raw_response.content,"lxml-xml")
                # get all urls
                for link in soup.find_all('a'):
                    if not bool(urlparse(link.get('href')).netloc):
                        lk = urljoin(resp.url,link.get('href'))
                    else:
                        lk = link.get('href')
                    if is_valid(lk):
                        fixed, throwaway = urldefrag(lk)
                        return_urls.append(fixed)
#                 page_txt = soup.get_text()
#                 page_txt = re.sub(r'\d+', '', page_txt) # remove numbers
#                 tok_txt = page_txt.split() # get each token string, to be trimmed of punctuation
#                 
#                 num_words = 0
#                 for token in tok_txt:\\
#                     low_word = token.lower()
#                     low_word.strip(punctuation) # get rid of the punctuation surrounding the word
#                     for char in token: # if any part of it is a number, skip
#                         if char.isdigit():
#                             continue
#                     elif low_word not in stopwords: # add to dict if not a stop word
#                         num_words += 1
#                         if low_word not in word_count:
#                             word_count[low_word] = 1
#                         else:
#                             word_count[low_word] += 1
#                 if num_words > longest_page_count:
#                     longest_page_count = num_words
#                     longest_page = resp.url
                return return_urls
                        
            else:
                return list()
        else:
            return list()
    else:
        return list()

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url, allow_fragments=False)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not re.match(r".*\.(ics|stat|cs|informatics)\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"action=login$", parsed.query.lower()):
            return False
        if re.match(r".*\/pdf\/.*", parsed.path.lower()) and re.match(r"informatics\.uci\.edu$", parsed.netloc.lower()):
            return False
        #if re.match(r"\/events.*", parsed.path.lower()) and re.match(r"wics\.ics\.uci\.edu$", parsed.netloc.lower()):
            #return False
        if re.match(r"share=(facebook|twitter)$", parsed.query.lower()):
            return False
        if re.match(r"\/community\/alumni\/index\.php\/(stayconnected\/)+index\.php$", parsed.path.lower()):
            return False
        if re.match(r"\/community\/alumni\/index\.php(\/stayconnected)+$", parsed.path.lower()):
            return False
        if re.match(r"\/alumni\/(stayconnected\/)+index\.php$", parsed.path.lower()):
            return False
        if re.match(r"\/alumni\/mentor(\/stayconnected)+\/index\.php$", parsed.path.lower()):
            return False
        if re.match(r"\/community\/alumni\/index\.php\/mentor(\/stayconnected)+\/index\.php$", parsed.path.lower()):
            return False
        if re.match(r"\/community\/alumni\/index\.php\/mentor(\/stayconnected)+$", parsed.path.lower()):
            return False
        if re.match(r"s?wiki\.ics\.uci\.edu", parsed.netloc.lower()) and parsed.query:
            return False
        if re.match(r".*&difftype=sidebyside", parsed.query.lower()):
            return False
        if re.match(r".*\/computing(\/computing)+\/.*", parsed.path.lower()):
            return False
        if re.match(r".*(\/computing\/resources)+\/.*", parsed.path.lower()):
            return False
        if re.match(r".*(\/policies)+\/.*", parsed.path.lower()):
            return False
        if re.match(r".*index.php(\/computing|\/advising|\/resources|\/overview|\/sao|\/degrees|\/courses).*", parsed.path.lower()):
            return False
        if re.match(r"\/honors(\/computing|\/advising|\/resources|\/overview|\/sao|\/degrees|\/courses).*", parsed.path.lower()):
            return False
        if re.match(r"action=diff.*", parsed.query.lower()):
            return False
        if re.match(r".*&format=txt", parsed.query.lower()):
            return False
        if re.match(r"version=.*", parsed.query.lower()):
            return False
        if re.match(r"action=upload.*", parsed.query.lower()):
            return False
        if re.match(r"action=download.*", parsed.query.lower()):
            return False
        if re.match(r"action=edit.*", parsed.query.lower()):
            return False
        if re.match(r"www.ics.uci.edu", parsed.netloc.lower()) and re.match(r"/community/news/spotlight_.*", parsed.path.lower()):
            return False
        if re.match(r"action=edit.*", parsed.query.lower()):
            return False
        if re.match(r"from=.*", parsed.query.lower()) and re.match(r".*timeline$", parsed.path.lower()):
            return False
        if re.match(r"\/~agelfand\/largeFam3.html", parsed.path.lower()) and re.match(r"www.ics.uci.edu", parsed.netloc.lower()):
            return False
        if re.match(r"\/~agelfand\/figs.*", parsed.path.lower()) and re.match(r"www.ics.uci.edu", parsed.netloc.lower()):
            return False
        if re.match(r"\/~dechter\/r.+\.html", parsed.path.lower()) and re.match(r"www.ics.uci.edu", parsed.netloc.lower()):
            return False
        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1|apk|sql"
            + r"|thmx|mso|arff|rtf|jar|csv|img|mgp"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.query.lower()):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1|apk|sql"
            + r"|thmx|mso|arff|rtf|jar|csv|img|mgp"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

        
# How many unique pages did you find? Uniqueness for the purposes of this assignment is ONLY established by the URL, but discarding the fragment part. So, for example, http://www.ics.uci.edu#aaa and http://www.ics.uci.edu#bbb are the same URL. Even if you implement additional methods for textual similarity detection, please keep considering the above definition of unique pages for the purposes of counting the unique pages in this assignment.
# What is the longest page in terms of the number of words? (HTML markup doesn’t count as words)
# What are the 50 most common words in the entire set of pages crawled under these domains ? (Ignore English stop words) Submit the list of common words ordered by frequency.
# How many subdomains did you find in the ics.uci.edu domain? Submit the list of subdomains ordered alphabetically and the number of unique pages detected in each subdomain. The content of this list should be lines containing subdomain, number, for example:
# vision.ics.uci.edu, 10 (not the actual number here)
