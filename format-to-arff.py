import sys

#modify here if want more or less word around interest ( 2 takes 2 words before and 2 words after interest)
number_of_words_before_n_after = 2
#modify here if want stoplist or not
use_stoplist = True

#arff HEADER
out = open("interest.arff", 'w')
out.write("%Title: Word-sense disambiguation data: 2369 instances of the noun interest\n\n"
          "@RELATION interest\n\n"
          "@ATTRIBUTE sens {1,2,3,4,5,6}\n"
          "@ATTRIBUTE prevwords string\n"
          "@ATTRIBUTE prevtags string\n"
          "@ATTRIBUTE nextwords string\n"
          "@ATTRIBUTE nexttags string\n\n"
          "@DATA\n")

try:
    input = open("interest.acl94.txt", 'r')
    text = input.read().replace("%", "PERCENT").replace("====================================== ", "").replace("$$\n", "").replace('[ ', "").replace('] ', "").replace("n't", 'not').replace('interests', 'interest')

except:
    print("interest.acl94.txt not found")
    sys.exit()

input.close()

#TODO Quelles efface? quelle garde en X? quelle touche pas? ['#', '$', '&', '*', '(', ')', '-', '+', ',', '.', ':', ';', '{', '}', "'", "`" ]
for punctuation in ['&/CC ', "#/# ", '(/( ', ')/) ', '+/NN ', ',/, ', ' ./. ', ':/: ', ';/; ', '{/{ ', '}/} ', "``/`` ", "''/'' ", "'s/POS " ]:
    text = text.replace(punctuation, "")
for punctuation in ['#', '$', '&', '*', '(', ')', '+', ',', '.', ':', ';', '{', '}', "'", "`" ]:
    text = text.replace(punctuation, 'X')

#remove stoplist-english words
if use_stoplist:
    with open('stoplist-english.txt', 'r') as stoplist:
        for stopword in stoplist.read().splitlines():
            index = text.find(" " + stopword +"/") + 1
            if index != 0:
                end = len(stopword)+4
                w = text[index:index + end].strip()
                text = text.replace(" " + w + " ", " ")

text = text.splitlines()

for line in text:
    finding_sens = line.split("_")
    if len(finding_sens) == 2:
        out.write('\n')
        sens = finding_sens[1][0]
        line = line.replace("interest_" + sens + '/NNS', "interest_" + sens + "/NN")
        line = line.replace("interest_" + sens + '/VBZ', "interest_" + sens + "/NN")
        line = line.replace("interest_" + sens + '/VB', "interest_" + sens + "/NN")
        words = line.split(" ")
        index = words.index('interest_' + sens + "/NN")

        prevwords = ''
        prevtags = ''
        nextwords = ''
        nexttags = ''

        #add in order the words and tags
        for i in reversed(range(1, number_of_words_before_n_after + 1)):
            if index - i >= 0:
                prev_words_tags = words[index - i].split('/')
                if len(prev_words_tags) == 2:
                    prevwords += ", " + prev_words_tags[0]
                    prevtags += ", " + prev_words_tags[1]
                #if the word have a missing tag
                else:
                    prevwords += ", " + prev_words_tags[0]
                    prevtags += ", NULL"
            # else:
                # prevwords += ", NULL"
                # prevtags += ", NULL"
        #if it doesnt have previous word
        if len(prevwords) == 0:
            prevwords += ", NULL"
            prevtags += ", NULL"

        for i in range(1, number_of_words_before_n_after + 1):
            if index + i < len(words):
                next_words_tags = words[index + i].split('/')
                if len(next_words_tags) == 2 :
                    nextwords += ", " + next_words_tags[0]
                    nexttags += ", " + next_words_tags[1]
                #if there is a word without tag
                else:
                    nextwords += ", " + next_words_tags[0]
                    nexttags += ", NULL"
                # else:
                # nextwords += ", NULL"
                # nexttags += ", NULL"
            #if it doesnt have next word
            elif len(nextwords) == 0:
                nextwords += ", NULL"
                nexttags += ", NULL"

        out.write(sens + ", \'" + prevwords[2:] + "\', \'" + prevtags[2:] + "\', \'" + nextwords[2:] + "\', \'"  + nexttags[2:] + "\'")






out.close()