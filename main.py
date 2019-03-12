import os
import pyspark
# from pyhanlp import *
# from pyspark.mllib.linalg import Vectors
# from pyspark.mllib.regression import LabeledPoint
# vocabulary =dict()
#
# file =open('question/【0】评分.txt','r',encoding='UTF-8')
# # scoreQuestion=file.read(10)
# print(file.readline())

# def sentenceToArrays(sentence:str):
#     vector = list(0,len(vocabulary))
#     for i in range(len(vocabulary)):
#         vector[i]=0
#     terms=HanLP.segment(sentence)
#     for term in terms:
#         word =term.word
#         if word in vocabulary.keys():
#             index=vocabulary.get(word)
#             vector[index]=1
#     return vector

# trains =list()
# for sentence in sentences:
#     array=sentenceToArrays(sentence)
#     train_one =  LabeledPoint(0.0,Vectors.dense(array))
#     trains.add(train_one)

# def a(func,*args):
#     return func(*args)
# def b(i,j,k):
#     return(i,j,k)
# d=[0,1,2,3]
# k=list()
# k.append(b)
# k+=d[1:]
# # k=tuple(k)
# print(a(*k))

# re = map((lambda x,y: x+y),[1,2,3],[6,7,9])
model_path="target/tmp/myNaiveBayesModel.obj"
if os.path.isfile(model_path):
    print('yes')
else:
    print("no")

print(pyspark.)