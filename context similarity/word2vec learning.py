# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 16:06:53 2017

@author: test
"""

from gensim.models import word2vec
import logging

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus("wiki_seg.txt")
    model = word2vec.Word2Vec(sentences, size=250)

    # Save our model.
    model.save("Chinese.model.bin")

    # To load a model.
    # model = word2vec.Word2Vec.load("your_model.bin")

if __name__ == "__main__":
    main()