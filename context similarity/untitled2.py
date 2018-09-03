# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 22:11:04 2018

@author: test
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 29 19:40:07 2018

@author: test
"""
from gensim.models.keyedvectors import KeyedVectors
import tkinter as tk
import jieba
import numpy as np

class DocSim(object):
    def __init__(self, w2v_model , stopwords=[]):
        self.w2v_model = w2v_model
        self.stopwords = stopwords

    def vectorize(self, doc):
        """Identify the vector values for each word in the given document"""
        doc = doc.lower()
        words = [w for w in doc.split(" ") if w not in self.stopwords]
        word_vecs = []
        for word in words:
            try:
                vec = self.w2v_model[word]
                word_vecs.append(vec)
            except KeyError:
                # Ignore, if the word doesn't exist in the vocabulary
                pass

        # Assuming that document vector is the mean of all the word vectors
        vector = np.mean(word_vecs, axis=0)
        return vector


    def _cosine_sim(self, vecA, vecB):
        """Find the cosine similarity distance between two vectors."""
        csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        if np.isnan(np.sum(csim)):
            return 0
        return csim

    def calculate_similarity(self, source_doc, target_docs=[], threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        if isinstance(target_docs, str):
            target_docs = [target_docs]

        source_vec = self.vectorize(source_doc)
        results = []
        for doc in target_docs:
            target_vec = self.vectorize(doc)
            sim_score = self._cosine_sim(source_vec, target_vec)
            if sim_score > threshold:
                results.append({
                    'score' : sim_score,
                    'doc' : doc
                })
            # Sort results by score in desc order
            results.sort(key=lambda k : k['score'] , reverse=True)

        return results
def compare():
    if languagel['text']=='Current language: English':
        s=entry1.get('1.0', tk.END)
        t=[]
        t.append(entry2.get('1.0', tk.END))
        sim_scores=[]
        sim_scores = ds.calculate_similarity(s, t)
        if sim_scores[0]['score']*100<91 and sim_scores[0]['score']-0.45>0:
            sim_scores[0]['score']=sim_scores[0]['score']-0.45
        similarity['text']=str(sim_scores[0]['score']*100)+"%"
        #print(str(sim_scores))
    else:
        s=entry1.get('1.0', tk.END)
        s1=entry2.get('1.0', tk.END)
        s=jieba.cut(s)
        s1=jieba.cut(s1)
        tt=""
        for a in s:
            tt+=a+" "
        s=tt
        tt=""
        for a in s1:
            tt+=a+" "
        s1=tt
        t=[]
        t.append(s1)
        sim_scores=[]
        sim_scores = ds2.calculate_similarity(s, t)
        if sim_scores[0]['score']*100<85 and sim_scores[0]['score']-0.4>0:
            sim_scores[0]['score']=sim_scores[0]['score']-0.4
        similarity['text']=str(sim_scores[0]['score']*100)+"%"
        #print(str(sim_scores))
def language_change():
    if languageb['text']=='Change to Chinese!':
        languageb['text']='轉換成英文'
        languagel['text']='目前的語言:中文'
        display['text']='相似度:'
        '''
        f3['text']='請把所有要比較的檔案放進一個資料夾。\n再輸入資料夾的路徑。'
        dictionary_compare['text']='開始'
        '''
    else:
        languageb['text']='Change to Chinese!'
        languagel['text']='Current language: English'
        display['text']='Similarity:'
        '''
        f3['text']='If you want to compare a lot of files, please place them in a dictionary.\n Afterwards, enter the path of the dictionary.'
        dictionary_compare['text']='Start comparing!'
        '''

model_path = 'GoogleNews-vectors-negative300.bin'
model_path2='Chinese.model.bin'
w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
ds = DocSim(w2v_model)
w2v_model2 = KeyedVectors.load(model_path2)
ds2 = DocSim(w2v_model2)


if __name__ =='__main__': 
    win=tk.Tk()
    win.title("File comparator")
    #win.geometry("1024x768") #The size of the app to be 1024x768
    #win.resizable(0,0) #不想讓使用者調整視窗大小
    
    #f1
    f1=tk.Frame()
    entry1=tk.Text(f1,width=50,wrap='word')
    entry2=tk.Text(f1,width=50,wrap='word')
    button=tk.Button(f1,text='Compare!',height=2,command=compare)
    
    entry1.grid(row=0,column=0,ipady=60,sticky='wens')
    entry2.grid(row=0,column=2,ipady=60,sticky='wens')
    button.grid(row=0,column=1,sticky='we')
    f1.grid(row=0,column=0)
    
    #f2
    f2=tk.Frame()
    display=tk.Label(f2,text="Similarity:",font=("Courier", 20))
    similarity=tk.Label(f2,text="   %",font=("Courier", 20))
    languagel=tk.Label(f2,text='Current language: English',font=("Courier", 20))
    languageb=tk.Button(f2,text='Change to Chinese!',command=language_change)
    
    display.pack()
    similarity.pack()
    languagel.pack()
    languageb.pack()
    f2.grid(row=1,column=0)

    '''
    #f3
    f3=tk.LabelFrame(text="If you want to compare a lot of files, please place them in a dictionary.\n Afterwards, enter the path of the dictionary.")
    file_path=tk.Entry(f3)
    dictionary_compare=tk.Button(f3,text='Start comparing!')
    file_path.pack()
    dictionary_compare.pack()
    f3.grid(row=0,column=1)
    '''
    win.mainloop()