from gtts import gTTS
import os
import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import pdfplumber
import io
import random
import time


def get_audio():

    # text = "Global warming is the long-term rise in the average temperature of the Earth’s climate system"
    # language = 'en'
    # speech = gTTS(text = text, lang = language, slow = False)
    # speech.save("text.mp3")

    #db = make_db()
    db = check_directory()
    language  = 'en'
    localpath = 'audios\\'
    
    for word in db:
        rand_int = random.randint(1, 11)
        time.sleep(rand_int*0.01)
        speech    = gTTS(text = word, lang = language, slow = False)
        file_name = basepath + localpath + word + ".mp3"
        speech.save(file_name)
        #print(file_name)

def make_db():

    file_name  = 'db\senior_high_school_Ewords_db'

    file_read  = basepath + file_name
    #file_write = basepath + file_name + "_db"

    f_r = open(file_read,"r",encoding='utf-8')
    lines = f_r.readlines()
    #f_w = open(file_write,"w")

    db = {};
    for line in lines:
        word       = line.split(' ')[0]
        frequency  = line.split(' ')[1]
        senior     = line.split(' ')[2]
        junior     = line.split(' ')[3]
        elementary = line.split(' ')[4].rstrip()
        #print(line, word, senior, junior, elementary)
        #print(index, word, frequency, senior, junior, elementary)
        db[word] = [frequency, senior, junior, elementary]
        #print(index, word)

    f_r.close()
    #f_w.close()

    return db

def modify_file():

    db_word = make_db()

    # pronunciation 
    file_name  = 'db\senior_high_school_Ewords_sentence_db'
    file_read  = basepath + file_name
    file_write = basepath + file_name + '_modify'  

    f_r = open(file_read, encoding="utf-8") 
    f_w = open(file_write,"a", encoding="utf-8")  

    lines = f_r.readlines()

    for word, line in zip(db_word, lines):     
        row = word + line
        f_w.write(row)

    # file writing closing            
    f_w.close()
    f_r.close()

    return 0

def web_scraping_meaning():

    db_word = make_db()

    # pronunciation 
    file_name  = 'db\senior_high_school_Ewords_meaning'
    file_write = basepath + file_name + '_db'
    
    for word in db_word:     
        f_w = open(file_write,"a", encoding="utf-8")  
        req = urllib.request.Request('https://ejje.weblio.jp/content/'+ word,
                                 headers={'User-Agent': 'PracticalMachineLearning'})
        #respose from server
        f = urllib.request.urlopen(req)

        # bs object out of html respose
        soup = BeautifulSoup(f.read(), "html.parser")
        metatags = soup.findAll('meta')

        meaning = str(metatags[-1]).split(':')[1]
        meaning = meaning.split('"')[0]
        meaning = meaning.strip()

        data = word + " " + meaning + "\n"

        # file writing
        f_w.write(data)

        # file writing closing            
        f_w.close()

        # closing http request
        f.close()

    return 0

def web_scraping_pronunciation():

    db_word = make_db()

    #word = 'ability'
    url = 'https://en.hatsuon.info/word/'

    # pronunciation 
    file_name  = 'data\senior_high_school_Ewords'
    file_write = basepath + file_name + '_db'
    
    for word in db_word:     
        f_w = open(file_write,"a", encoding="utf-8")  
        req = urllib.request.Request(url+ word,
                                    headers={'User-Agent': 'PracticalMachineLearning'})
        #respose from server
        f = urllib.request.urlopen(req)

        # bs object out of html respose
        soup = BeautifulSoup(f.read(), "html.parser")
        text = soup.find_all("div", {"class": "font4"})

        # extract pronunciation.
        pronunciation = []
        for item in text:
            temp = re.sub(r'.*</font>', '', str(item))
            temp = re.sub(r'<a.*', '', temp)
            temp = re.sub(r'</div>', '', temp) 
            pronunciation.append(str(temp).strip())

        # write db
        pronunciation_en = pronunciation[0]
        pronunciation_jp = pronunciation[1]
        frequency        = db_word[word][0]
        senior           = db_word[word][1]
        junior           = db_word[word][2]
        elementary       = db_word[word][3]

        data = word+" "+pronunciation_en+" "+pronunciation_jp+" "+frequency+" "+senior+" "+junior+" "+elementary+"\n"

        # file writing
        f_w.write(data)

        # file writing closing            
        f_w.close()

        # closing http request
        f.close()

    return 0

def web_scraping_sentence():

    # max num sentences
    MAX = 5

    db_word = make_db()

    # pronunciation 
    file_name  = 'db\senior_high_school_Ewords_sentence'
    file_write = basepath + file_name + '_db'
    
    for word in db_word:     
        f_w = open(file_write,"a", encoding="utf-8")  
        req = urllib.request.Request('https://www.ei-navi.jp/dictionary/content/'+ word,
                                 headers={'User-Agent': 'PracticalMachineLearning'})
        #respose from server
        f = urllib.request.urlopen(req)
 
        # bs object out of html respose
        soup = BeautifulSoup(f.read(), "html.parser")
        sentences_en = soup.find_all('li',{'class': "en"})
        sentences_jp = soup.find_all('li',{'class': "ja"})

        #######################################################
        # check whether it has sentences or not
        sentence_en_all = []
        sentence_jp_all = []
        count = 1
        if len(sentences_en) ==0:
            for each_blockquote in soup.find_all('blockquote'):
                for onesentence in each_blockquote.find_all('p'):
  
                    if onesentence.find('cite'):
                        onesentence.cite.decompose()

                    if count%2 == 1: # english
                        sentence_en_all.append(onesentence.text)
                        count = count + 1
                    else:            # japanese
                        sentence_jp_all.append(onesentence.text)
                        count = count + 1

                if len(sentence_en_all) == MAX:
                    break 
        else:          
            #clean eng sentence
            for item in sentences_en:  
                sentence_en_all.append(item.text)
                if len(sentence_en_all) == MAX:
                    break            
            #clean jp sentence
            for item in sentences_jp:     
                sentence_jp_all.append(item.text)
                if len(sentence_jp_all) == MAX:
                    break   
        
        row = '| '
        for en, jp in zip(sentence_en_all, sentence_jp_all):
            if en == sentence_en_all[-1]:
                row = row + en + " " + jp 
            else:
                row = row + en + " " + jp + " | "
            row = re.sub(r'\u3000','',row)

        row = row + '\n'
 
        #print(row)

        # file writing
        f_w.write(row)
        
        # file writing closing            
        f_w.close()

        # closing http request
        f.close()

    return 0

def check_directory():
    localpath = 'audios\\'
    fullpath  = basepath + localpath

    db = make_db()
    
    done_list = []
    for entry in os.listdir(fullpath):
        if os.path.isfile(os.path.join(fullpath, entry)):
            done_list.append(entry.split('.')[0])
    
    not_done_list = []
    for word in db:
        if word not in done_list: 
            not_done_list.append(word)
    
    print ("Total words:", len(db))
    print ("Done words: ", len(done_list))
    print ("Not done words: ", len(not_done_list))

    return not_done_list

def check_words():

    spell = SpellChecker()

    db_word = make_db()

    list_words = []
    for word in db_word:
        list_words.append(word)
    
    misspelled = spell.unknown(list_words)
    for word in misspelled:
        print(word, spell.candidates(word))

    return 0

def read_pdf():
    # creating a pdf file object
    file_name  = 'data\senior_high_school_Ewords.pdf'
    fullpath   = basepath + file_name
    small_ABC  = 'abcdefghijklmnopqrstuvwxyz'

    file_write = basepath + 'data\enior_high_school_Ewords'

    f_w = open(file_write,"w", encoding="utf-8")

    with pdfplumber.open(fullpath) as pdf:
        #first_page = pdf.pages[6]
        #first_page = pdf.pages[20]
        index = 1
        for i in range(6, 21): #6-20
            page = pdf.pages[i]
            lines_ =  page.extract_text()
            buf = io.StringIO(lines_)
            lines = buf.readlines()
            for line in lines:
                if line[0] in small_ABC or line[0] in 'I': # real row selection
                    #result = re.split(r"([a-z]+)", line)
                    result = re.split("\s", line)
                    row = []
                    for item in result:  # splited small items
                        if item != '':
                            row.append(item)
                            if len(row) == 5:
                                print (index, row)
                                for i in row:
                                    f_w.write(i + " ")
                                f_w.write('\n')
                                index = index + 1
                                row = []          
                    
        f_w.close()

    return 0

def clean_web_scraping_db():
    # creating a pdf file object
    file_name  = 'data\senior_high_school_Ewords_db'
    fullpath   = basepath + file_name
    small_ABC  = 'abcdefghijklmnopqrstuvwxyz'

    file_read  = basepath + 'data\senior_high_school_Ewords_scraped'
    file_write = basepath + 'db\senior_high_school_Ewords_pronunciation_db'

    f_w = open(file_write,"w", encoding="utf-8")
    f_r = open(file_read,encoding="utf-8")

    lines = f_r.readlines()

    index = 1
    for line in lines:
        items = line.split(' ')

        eng_p = []
        jp_p  = []
        for i in range(0, len(items)):   
            item = items[i].strip(',').strip(';').strip('|').strip('\n').strip('−')
            item = re.sub('\s+', '', item)
            item = re.sub('\(\(関係代名詞の弱形\)\)', '', item)
            if i == 0:
                word = item
                continue
            else:
                if not re.search('[0-9]', item) and item !='': # not number 
                    if re.search('[a-zA-Z]', item) or 'ʃ' in item or 'θ' in item:
                        eng_p.append(item)
                    else:
                        jp_p.append(item)
        f_w.write(word)
        f_w.write(' || ')
        for item in eng_p:
            if item == eng_p[-1]:
                f_w.write(item)
            else:
                f_w.write(item)
                f_w.write(", ")
        f_w.write(' || ')
        for item in jp_p:
            if item == jp_p[-1]:
                f_w.write(item)
            else:
                f_w.write(item)
                f_w.write(", ")
        f_w.write('\n')
            
        # print(index, word)
        # print(eng_p)
        # print(jp_p)
        # index = index + 1
          
    f_w.close()
    f_r.close() 

    return 0

def icons8com():

    # url = "https://search.icons8.com/api/iconsets/v5/search?term=ability&token=eVahCKnqVkgFJTwJ5xZmXPL6JN2OV6TwfIauZXIf"
    # headers={'x-api-key':'eVahCKnqVkgFJTwJ5xZmXPL6JN2OV6TwfIauZXIf'}
    # resp = requests.get(url,headers=headers)

    # print(resp.status_code)
    # print(resp.content)
    # print(resp)

    # url = "https://api-icons.icons8.com/publicApi/icons/icon?id=9bLZQZMri5Xi&token=eVahCKnqVkgFJTwJ5xZmXPL6JN2OV6TwfIauZXIf"
    # headers={'x-api-key':'eVahCKnqVkgFJTwJ5xZmXPL6JN2OV6TwfIauZXIf'}
    # resp = requests.get(url,headers=headers)

    # print(resp.status_code)
    # print(resp.content.icon.svg)
    # print(resp) 

    return 0

def generate_html():

    return 0

# Press the green button in the gutter to run the script.
# basepath   = 'D:\projects\ecards\\'         # HOME
basepath   = 'F:\EDIC_project\ecards\\'     # WORK

if __name__ == '__main__':

    # ###############################
    # Scrapping codes
    # web_scraping_sentence()
    # web_scraping_meaning()
    # web_scraping_pronunciation()

    #################################
    # Parsing pdf and extract data
    # read_pdf()    

    ################################
    # Read 'senior_high_school_Ewords_db' and return words.
    # make_db()

    ################################
    # Utilities
    # check_directory()  
    # clean_web_scraping_db()
    # modify_file()

    ################################
    # mp3 for each word
    # get_audio()    

    ################################
    # icon8s.com image API
    icons8com()

    ################################
    # html generation
    # generate_html()