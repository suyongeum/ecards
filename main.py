from gtts import gTTS
import os

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
        speech    = gTTS(text = word, lang = language, slow = False)
        file_name = basepath + localpath + word + ".mp3"
        speech.save(file_name)
        #print(file_name)

def make_db():

    file_name  = 'data\senior_high_school_Ewords'

    file_read  = basepath + file_name
    file_write = basepath + file_name + "_db"

    f_r = open(file_read,"r",encoding='utf-8')
    lines = f_r.readlines()
    f_w = open(file_write,"w")

    index = 0
    db = {};
    for line in lines:
        if index != 0:
            word       = line.split('\t')[0]
            frequency  = line.split('\t')[1]
            senior     = line.split('\t')[2]
            junior     = line.split('\t')[3]
            elementary = line.split('\t')[4].rstrip()
            #print(line, word, senior, junior, elementary)
            #print(index, word, frequency, senior, junior, elementary)
            db[word] = [frequency, senior, junior, elementary]
            #print(index, word)
            index = index + 1
        else:
            index = index + 1

    f_r.close()
    f_w.close()

    return db

def web_scraping():
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


# Press the green button in the gutter to run the script.
basepath   = 'F:\EDIC_project\ecards\\'

if __name__ == '__main__':

    #make_db()
    #check_directory()
    #web_scraping()
    get_audio()