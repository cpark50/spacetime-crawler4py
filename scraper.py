import re
from urllib.parse import urlparse, urldefrag, urljoin
from bs4 import BeautifulSoup
from string import punctuation
import json
import os

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
    word_count = {}
    if is_valid(resp.url):
        if re.match(r"pdf", resp.headers['Content-Type'].lower()): # skip hidden pdfs?
        #     print(resp.status, resp.error)
             return list()
        if resp.status >= 200 or resp.status <= 399: 
            if resp.raw_response != None: # returns no data
                # need to make sure each url is valid before adding it to the list
                soup = BeautifulSoup(resp.raw_response.content,"lxml-xml")
                # get all urls
                if re.match(r".*\.ics\.uci\.edu.*", resp.url):
                    update_subdomainpgs(resp.url)
                for link in soup.find_all('a'):
                    if not bool(urlparse(link.get('href')).netloc):
                        lk = urljoin(resp.url,link.get('href'))
                    else:
                        lk = link.get('href')
                    if is_valid(lk):
                        fixed, throwaway = urldefrag(lk)
                        return_urls.append(fixed)                 
                for tag in soup("script"):
                    tag.decompose()
                for tag in soup("style"):
                    tag.decompose()
                page_txt = soup.get_text()
                page_txt = re.sub(r'\d+', '', page_txt) # remove numbers
                tok_txt = page_txt.split() # get each token string, to be trimmed of punctuation
                num_words = 0
                for token in tok_txt:
                    low_word = token.lower()
                    low_word = low_word.strip(punctuation) # get rid of the punctuation surrounding the word
                    for char in token: # if any part of it is a number, skip
                        if len(low_word) <= 3:
                            continue
                        elif char.isdigit():
                            continue
                        elif re.match(r".*(=|\/).*", low_word):
                            continue
                        elif low_word not in stopwords: # add to dict if not a stop word
                            num_words += 1
                            if low_word not in word_count:
                                word_count[low_word] = 1
                            else:
                                word_count[low_word] += 1

                update_wordcount(word_count)
                update_largestfile(resp.url, num_words)
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
        if re.match(r"mailman\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"hombao\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"awareness\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"hana\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"checkmate\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"tippers\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"cgvw\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r" ?codeexchange\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"dataprotector\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"dataguard\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"password\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"coronavirustwittermap\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"cybert\.ics\.uci\.edu$", parsed.netloc.lower()) and parsed.path:
            return False
        if re.match(r"closeup\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"contact14\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"contact\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"metaviz\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"mapgrid\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"satware\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"timesheet\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"sconce\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"gonet\.genomics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"sidepro\.proteomics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"tmbpro\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"www\.isg\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"sprout\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"mine10\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"honors\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"cloudberry\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"chime\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"jujube\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"duke\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"yarra\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"seraja\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"auge\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"dblp\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"cocoa-krispies\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"kdd\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"asterixdb\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"action=login$", parsed.query.lower()):
            return False
        if re.match(r"\/files\/pdf\/.*", parsed.path.lower()) and re.match(r"www\.informatics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"\/static\/downloadables\/example_input_file.tsv", parsed.path.lower()) and re.match(r"circadiomics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"\/localsearch\/fuzzysearch", parsed.path.lower()) and re.match(r"flamingo\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"\/fuzzyjoin-mapreduce", parsed.path.lower()) and re.match(r"asterix\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r".*\/((zip|raw)-)?attachment\/.*", parsed.path.lower()) and re.match(r"grape\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        
        if re.match(r"\/~ccsp|\/pub\/((ietf\/(webdav|html|http|uri))|websoft)|\/software", parsed.path.lower()) and re.match(r"www\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"\/wp-content\/uploads\/mjolsnesscunhapmav24oct2012", parsed.path.lower()) and re.match(r"emj\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"\/mgs\/dbases\/agns", parsed.path.lower()) and re.match(r"emj-pc\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"\/events?\/.*", parsed.path.lower()) and re.match(r"wics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"\/author\/admin\/page\/(19|8)", parsed.path.lower()) and re.match(r"wics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"\/category\/news\/page\/(15|11)", parsed.path.lower()) and re.match(r"wics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"\/(3|recurse-center)", parsed.path.lower()) and re.match(r"wics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r".*img_[0-9]+", parsed.path.lower()) and re.match(r"wics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"\/(fall-2020-week-5-wics-committee-applications-qa|fall-2021-week-3-committee-applications-qa|winter-2022-week-8-virtual-kahoot-clash-collab)", parsed.path.lower()) and re.match(r"wics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        
        if re.match(r"\/(spring-2022-week-1-general-retreat|spring-2022-week-9-wicsxpics|spring-2021-week-1-wics-first-general-meeting)", parsed.path.lower()) and re.match(r"wics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        
        if re.match(r"\/week-8-thanksgiving-potluck", parsed.path.lower()) and re.match(r"wics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        
        if re.match(r"\/(wics-fall-quarter-week-5-facebook-coding-event|wics-fall-quarter-week-6-mentorship-reveal|wics-spring-quarter-week-6-acing-the-technical-interview-with-the-portal|wics-winter-quarter-week-5-study-session|wics-winter-quarter-week-3-mock-technical-interviews|wics-hosts-a-toy-hacking-workshop-with-dr-garnet-hertz\/13-02-03-toy-hacker-020)", parsed.path.lower()) and re.match(r"wics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        
        if re.match(r".*page_id=.*", parsed.query.lower()) and re.match(r"wics\.ics\.uci\.edu$", parsed.netloc.lower()):
            return False
        if re.match(r"share=(facebook|twitter)$", parsed.query.lower()):
            return False
        if re.match(r"\/community\/alumni\/index\.php\/(stayconnected\/)+index\.php$", parsed.path.lower()):
            return False
        # 500
        if re.match(r"old-reactions\.ics\.uci\.edu", parsed.netloc.lower()) and re.match(r"\/admin", parsed.path.lower()):
            return False
        if re.match(r"www\.ics\.uci\.edu", parsed.netloc.lower()) and re.match(r"\/~ics54\/00w", parsed.path.lower()):
            return False
        if re.match(r"sli\.ics\.uci\.edu", parsed.netloc.lower()) and re.match(r"(\/PmWiki\/FAQ)|(\/PmWiki\/CustomMarkup)", parsed.path):
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
        if re.match(r".*format=txt", parsed.query.lower()):
            return False
        if re.match(r"version=.*", parsed.query.lower()):
            return False
        if re.match(r"action=upload.*", parsed.query.lower()):
            return False
        if re.match(r"action=history.*", parsed.query.lower()):
            return False
        if re.match(r"action=download.*", parsed.query.lower()):
            return False
        if re.match(r"action=edit.*", parsed.query.lower()):
            return False
        if re.match(r"www\.ics\.uci\.edu", parsed.netloc.lower()) and re.match(r"\/community\/news\/spotlight_.*", parsed.path.lower()):
            return False
        if re.match(r"support\.ics\.uci\.edu", parsed.netloc.lower()) and re.match(r"\/passwd\/index\.php", parsed.path.lower()):
            return False
        if re.match(r"www\.stat\.uci\.edu", parsed.netloc.lower()) and re.match(r"\/filter-test", parsed.path.lower()):
            return False
        if re.match(r"www\.informatics\.uci\.edu", parsed.netloc.lower()) and re.match(r"\/filter-test", parsed.path.lower()):
            return False
        if re.match(r"www\.cs\.uci\.edu", parsed.netloc.lower()) and re.match(r"(\/category\/((uncategorized\/page\/2)|(feature\/page\/2)))|\/events-filter-test|\/filter-test|\/reappointment-of-dean-marios-papaefthymiou|\/sandy-irani-and-sameer-singh-receive-distinguished-faculty-awards", parsed.path.lower()):
            return False
        
        if re.match(r"action=edit.*", parsed.query.lower()):
            return False
        if re.match(r"from=.*", parsed.query.lower()) and re.match(r".*timeline$", parsed.path.lower()):
            return False
        if re.match(r"\/~agelfand\/largefam3.html", parsed.path.lower()) and re.match(r"www\.ics\.uci\.edu", parsed.netloc.lower()):
            return False
        if re.match(r"\/~agelfand\/figs.*", parsed.path.lower()) and re.match(r"www\.ics\.uci\.edu", parsed.netloc.lower()):
            return False
        if re.match(r"\/~agelfand\/figs.*", parsed.path.lower()) and re.match(r"www\.ics\.uci\.edu", parsed.netloc.lower()):
            return False
        if re.match(r"\/~dechter\/r.+\.html", parsed.path.lower()) and re.match(r"www\.ics\.uci\.edu", parsed.netloc.lower()):
            return False
        if re.match(r".*(\/seminar\/nanda)+.*", parsed.path.lower()) and re.match(r"www\.cert\.ics\.uci\.edu", parsed.netloc.lower()):
            return False
        if re.match(r"www\.omni\.ics\.uci\.edu", parsed.netloc.lower()):
            return False
        if re.match(r"omni\.ics\.uci\.edu", parsed.netloc.lower()):
            return False
        if re.match(r"alumni\.ics\.uci\.edu", parsed.netloc.lower()):
            return False
        if re.match(r"honors\.ics\.uci\.edu", parsed.netloc.lower()):
            return False
        if re.match(r".*\/zip-attachment\/.*", parsed.netloc.lower()):
            return False
        if re.match(r"(\/emws09)+.*", parsed.path.lower()):
            return False
        if re.match(r"ucinetid=.*", parsed.query.lower()):
            return False
        if re.match(r"pid=.*=bib", parsed.query.lower()):
            return False
        if re.match(r"(image=.*)|(.*image=.*)", parsed.query.lower()):
            return False
        # if re.match(r"\/download\/download.*", parsed.path.lower()) and re.match(r"www\.ics\.uci\.edu", parsed.netloc.lower()):
        #     return False
        # if re.match(r"\/doku\.php.*", parsed.path.lower()) and re.match(r"www\.ics\.uci\.edu", parsed.netloc.lower()):
        #     return False
        # if re.match(r"\/research.*", parsed.path.lower()) and re.match(r"www\.ics\.uci\.edu", parsed.netloc.lower()):
        #     return False
        # if re.match(r"\/video\/cs178\/Lecture.*", parsed.path.lower()):
        #     return False
        # if re.match(r"\/tag\/.*", parsed.path.lower()):
        #     return False
        # if re.match(r"\/category\/.*", parsed.path.lower()):
        #     return False
        # if re.match(r".*\/tag\/.*", parsed.path.lower()):
        #     return False
        if re.match(r"ical=1", parsed.query.lower()): # i think this downloads a calendar
            return False
        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|odp|ova"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|seq|sh"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|svn|tsv"
            + r"|epub|dll|cnf|tgz|sha1|apk|sql|war|svg|pd|ppsx?|psp"
            + r"|thmx|mso|arff|rtf|jar|csv|img|mpg|conf|mexglx|mlx"
            + r"|m|n?py|c|h|ipynb|lck|h5|nb|bib|class|frk|java|jsp"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.query.lower()):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|odp|ova"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|seq|sh"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|svn|tsv"
            + r"|epub|dll|cnf|tgz|sha1|apk|sql|war|svg|pd|ppsx?|psp"
            + r"|thmx|mso|arff|rtf|jar|csv|img|mpg|conf|mexglx|mlx"
            + r"|m|n?py|c|h|ipynb|lck|h5|nb|bib|class|frk|java|jsp"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

        
# How many unique pages did you find? Uniqueness for the purposes of this assignment is ONLY established by the URL, but discarding the fragment part. So, for example, http://www.ics.uci.edu#aaa and http://www.ics.uci.edu#bbb are the same URL. Even if you implement additional methods for textual similarity detection, please keep considering the above definition of unique pages for the purposes of counting the unique pages in this assignment.
# What is the longest page in terms of the number of words? (HTML markup doesn’t count as words)
# What are the 50 most common words in the entire set of pages crawled under these domains ? (Ignore English stop words) Submit the list of common words ordered by frequency.
# How many subdomains did you find in the ics.uci.edu domain? Submit the list of subdomains ordered alphabetically and the number of unique pages detected in each subdomain. The content of this list should be lines containing subdomain, number, for example:
# vision.ics.uci.edu, 10 (not the actual number here)
def update_wordcount(data):
    try:
        file = open("word_count.json", "r")
        counts = json.load(file)
    except FileNotFoundError:
        file = open("word_count.json", "w")
        json.dump(data, file)
        file.flush()
        os.fsync(file.fileno())
        file.close()
    else:
        file = open("word_count.json", "r")
        counts = json.load(file)
        file.close()
        for k,v in data.items():
            if k not in counts.keys():
                counts[k] = v
            else:
                counts[k] += v
        file = open("word_count.json", "w")
        json.dump(counts, file)
        file.flush()
        os.fsync(file.fileno())
        file.close()

def update_largestfile(newurl, newcount):
    try:
        file = open("longest_file.txt", "r")
        url = file.readline().rstrip('\n')
        count = int(file.readline().rstrip('\n'))
        if newcount > count:
            file.close()
            file = open("longest_file.txt", "w")
            file.write(newurl)
            file.write("\n")
            file.write(str(newcount))
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())
        file.close()
    except FileNotFoundError:
        file = open("longest_file.txt", "w")
        file.write(newurl)
        file.write("\n")
        file.write(str(newcount))
        file.write("\n")
        file.flush()
        os.fsync(file.fileno())
        file.close()

def update_subdomainpgs(domain_path):
    domain = urlparse(domain_path)
    domain = domain.netloc
    try:
        file = open("subdomains.json", "r")
        counts = json.load(file)
    except FileNotFoundError:
        file = open("subdomains.json", "w")
        json.dump({domain:1}, file)
        file.flush()
        os.fsync(file.fileno())
        file.close()
    else:
        file = open("subdomains.json", "r")
        counts = json.load(file)
        file.close()
        if domain not in counts.keys():
            counts[domain] = 1
        else:
            counts[domain] += 1
        file = open("subdomains.json", "w")
        json.dump(counts, file)
        file.flush()
        os.fsync(file.fileno())
        file.close()
