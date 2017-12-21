import pathlib
import os
import gensim
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import string
class word2vec ():

    def __init__(self, pathToCorpus, pathToWord2vec):
        self.pathToCorpus = pathToCorpus
        self.textPaths = []
        self.pathToWord2vec = pathToWord2vec + ".bin"

    def getTextPaths(self):
        for path, subdirs, files in os.walk(self.pathToCorpus + "/"):
            for name in files:
                if name.endswith(".txt"):
                    self.textPaths.append(str(pathlib.PurePath(path, name)))
        print(len(self.textPaths))
    def buildWord2vec(self):
        for path in self.textPaths:
            tekst = text()
            tekst.getText(path)
            tekst.clean_text()
            try:
                model = gensim.models.Word2Vec.load(self.pathToWord2vec)
                model.build_vocab(tekst.tokenizedText, update = True)
            except FileNotFoundError:
                model = gensim.models.Word2Vec(iter=2)
                model.build_vocab(tekst.tokenizedText)
                print("Modellen eksisterer ikke, lager ny")
                pass
            print("oppdater vokabular og modell")
            #model.build_vocab(vocab_sentences_tokenized, update = True)
            model.train(tekst.tokenizedText, total_examples= model.corpus_count, epochs= 30)
            model.save(self.pathToWord2vec)
            print("Ferdig!!!")

class text ():

    def __init__(self):
        self.text = "None"
        self.tokenizedText = []
        self.cleanText = None

    def getText(self, textPath):
        with open(textPath,'r') as text_file:
            data = text_file.read().replace('\n',' ')
        self.text = data

    def tokenize_text(self):
        self.tokenizedText = word_tokenize(self.text)

    def lowerText(self):
        self.tokenizedText = [word.lower() for word in self.tokenizedText]

    def removeStopwords(self):
        self.tokenizedText = [word for word in self.tokenizedText if word not in stopwords.words('norwegian')]

    def removeWordsShorterThanTwoLetters(self):
        tmp = [word for word in self.tokenizedText if len(word)>2]
        self.tokenizedText = tmp

    def removeAllNonAlphabeticLetters(self):
        regex = re.compile('[^a-zA-z æøåÆØÅ]')
        tmp = [] #[re.sub('',word) for word in self.tokenizedText
        for word in self.tokenizedText:
            tmp.append(regex.sub('',str(word)))
        self.tokenizedText = tmp

    def catText(self):
        self.text = ' '.join(self.tokenizedText)

    def clean_text(self):
        self.tokenize_text()
        self.lowerText()
        self.removeStopwords()
        self.removeWordsShorterThanTwoLetters()
        self.removeAllNonAlphabeticLetters()
        self.catText()




if __name__ == '__main__':

    word2vec = word2vec("/home/ubuntu/PycharmProjects/word2Vecforbigcorpora/test_data/test3"
                        ,'/home/ubuntu/PycharmProjects/word2Vecforbigcorpora/test3')
    word2vec.getTextPaths()
    word2vec.buildWord2vec()
