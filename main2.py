from pyspark import SparkConf, SparkContext
from pyhanlp import *
# from pyspark.ml import Pipeline,PiplineModel
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import os
import jieba
from pyspark.mllib.util import MLUtils
from pyspark.sql import SQLContext
from pyspark.sql import Row
import jieba.posseg as pseg
from pyspark.sql import DataFrame
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.ml.classification import OneVsRest, LogisticRegression
from pyspark.mllib.classification import NaiveBayesModel, NaiveBayes
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark import ml
import heapq
from pyspark.sql import SQLContext
import numpy as np


# from pyspark.mllib.classification import
class ModelProcess:
    questionsPattern = dict()
    nbModel = None
    vocabulary = dict()
    abstractMap = dict()
    rootDirPath = "D:/QQPCmgr/Desktop/data/data"
    modelIndex = 0
    MyHanlp = None
    args = list()
    conf = None
    sc = None
    model = None
    spark = None

    # def __init__(self):
    #     questionsPattern=self.loadQuestionPattern()
    #     self.vocabulary=self.loadVocabulary()
    #     self.nbModel=self.loadClassifierModel()
    def __init__(self, rootDirPath: str):
        self.MyHanlp = HanLP
        self.rootDirPath = rootDirPath + '/'
        self.questionPattern = self.loadQuestionPattern()
        self.vocabulary = self.loadVocabulary()
        self.nbModel = self.loadClassifierModel()

    def analyQuery(self, queryString: str) -> dict():

        print("原始句子", queryString)
        print("------Hanlp分词---------")

        abstr = self.queryAbstract(queryString)
        print("句子抽象化结果:", abstr)

        strPatt = self.queryClassify(abstr)
        i=0
        print("句子套用模板结果：", strPatt[i])

        finalPattern, Args ,testPattern= self.queryExtension(strPatt[i])
        for key in self.abstractMap.keys():
            if key not in testPattern:
                i+=1
                self.modelIndex=self.index_list[i]
                self.args.remove(self.args[0])
                finalPattern,Args,testPattern=self.queryExtension(strPatt[i])
        self.abstractMap.clear()
        self.abstractMap = None
        Args = Args.copy()
        self.args.clear()
        print("原始句子替换成系统可识别的结果", finalPattern, Args)

        resultList = list()
        resultList.append(str(self.modelIndex))
        finalPattArray = finalPattern.split(" ")
        for word in finalPattArray:
            resultList.append(word)
        return resultList, Args

    def queryAbstract(self, querySentence: str):
        terms = self.MyHanlp.segment(querySentence)
        abstractQuery = ""
        self.abstractMap = dict()
        nrCount = 0
        for term in terms:
            word = term.word
            termStr = str(term.nature)
            print("-----------------")
            print(word)
            print(termStr)
            # abstractQuery+=termStr
            # abstractQuery+=" "
            # abstractMap[termStr]=word
            if "nm" in termStr or "nz" in termStr:
                abstractQuery += "nm "
                self.abstractMap["nm"] = word
            elif "nr" in termStr and nrCount == 0:
                abstractQuery += "nnt "
                self.abstractMap["nnt"] = word
                nrCount += 1
            elif "nr" in termStr and nrCount == 1:
                abstractQuery += "nnr "
                self.abstractMap["nnr"] = word
                nrCount += 1
            elif "x" in termStr:
                abstractQuery += "x"
                self.abstractMap["x"] = word
            elif "ng" in termStr:
                abstractQuery += "ng "
                self.abstractMap["ng"] = word
            else:
                abstractQuery += word + " "

        print("-----------HanLP 分词结束")
        return abstractQuery

    def queryExtension(self, queryPattern: str):
        Set = set(self.abstractMap.keys())
        self.args.append(self.modelIndex)
        testPattern=queryPattern
        tempPattern=queryPattern
        for key in Set:
            if key in queryPattern:
                value = self.abstractMap.get(key)
                self.args.append(value)
                testPattern = queryPattern
                tempPattern = queryPattern.replace(key, value)
        extendedQuery = tempPattern
        return extendedQuery, self.args,testPattern

    def loadVocabulary(self):
        vocabulary = dict()
        file = open(self.rootDirPath + "question/vocabulary.txt", 'r', encoding='UTF-8')
        # line=file.readline()
        for line in file.readlines():
            tokens = line.split(":")
            index = int(tokens[0])
            word = tokens[1].strip()
            vocabulary[word] = index
        return vocabulary

    def loadFile(self, filename: str):
        file = open(self.rootDirPath + filename, 'r', encoding='UTF-8')
        content = ""
        line = ""
        for line in file.readlines():
            content += line + "`"
        file.close()
        return content

    def sentenceToArrays(self, sentence: str):
        vector = list(range(len(self.vocabulary)))
        for i in range(len(self.vocabulary)):
            vector[i] = 0
        # terms=HanLP.segment(sentence)
        terms = list(jieba.cut(sentence, cut_all=False, HMM=True))
        for term in terms:
            word = term
            if word in self.vocabulary.keys():
                index = self.vocabulary.get(word)
                vector[index] = 1
        return vector

    def TrainClassifierModel(self) -> NaiveBayesModel:
        self.conf = SparkConf().setAppName("NaiveBayesTest").setMaster("local[*]")

        sc = SparkContext(conf=self.conf)
        spark = SparkSession.builder.config(conf=self.conf).getOrCreate()
        self.spark = sc
        train_list = list()
        train_list2 = list()
        sentences = None

        scoreQuestions = self.loadFile("question/【0】评分.txt")
        sentences = scoreQuestions.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)

            train_one = LabeledPoint(0.0, Vectors.dense(array))
            train_two = Row(label=0.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        timeQuestion = self.loadFile("question/【1】上映.txt")
        sentences = timeQuestion.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(1.0, Vectors.dense(array))
            train_two = Row(label=1.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        styleQuestions = self.loadFile("question/【2】风格.txt")
        sentences = styleQuestions.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(2.0, Vectors.dense(array))
            train_two = Row(label=2.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        storyQuestions = self.loadFile("question/【3】剧情.txt")
        sentences = storyQuestions.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(3.0, Vectors.dense(array))
            train_two = Row(label=3.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        actorsQuestion = self.loadFile("question/【4】某电影有哪些演员出演.txt")
        sentences = actorsQuestion.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(4.0, Vectors.dense(array))
            train_two = Row(label=4.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        actorInfos = self.loadFile("question/【5】演员简介.txt")
        sentences = actorInfos.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(5.0, Vectors.dense(array))
            train_two = Row(label=5.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)
        genreMovies = self.loadFile("question/【6】某演员出演过的类型电影有哪些.txt")
        sentences = genreMovies.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(6.0, Vectors.dense(array))
            train_two = Row(label=6.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        actorsMovie = self.loadFile("question/【7】某演员演了什么电影.txt")
        sentences = actorsMovie.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(7.0, Vectors.dense(array))
            train_two = Row(label=7.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        highScoreMovies = self.loadFile("question/【8】演员参演的电影评分【大于】.txt")
        sentences = highScoreMovies.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(8.0, Vectors.dense(array))
            train_two = Row(label=8.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        lowScoreMovies = self.loadFile("question/【9】演员参演的电影评分【小于】.txt")
        sentences = lowScoreMovies.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(9.0, Vectors.dense(array))
            train_two = Row(label=9.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        actorMovieGenres = self.loadFile("question/【10】某演员出演过哪些类型的电影.txt")
        sentences = actorMovieGenres.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(10.0, Vectors.dense(array))
            train_two = Row(label=10.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        withMovies = self.loadFile("question/【11】演员A和演员B合作了哪些电影.txt")
        sentences = withMovies.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(11.0, Vectors.dense(array))
            train_two = Row(label=11.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        countMovies = self.loadFile("question/【12】某演员一共演过多少电影.txt")
        sentences = countMovies.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(12.0, Vectors.dense(array))
            train_two = Row(label=12.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)

        actorBirthdayQuestion = self.loadFile("question/【13】演员出生日期.txt")
        sentences = actorBirthdayQuestion.split("`")
        for sentence in sentences:
            array = self.sentenceToArrays(sentence)
            train_one = LabeledPoint(13.0, Vectors.dense(array))
            train_two = Row(label=13.0, features=ml.linalg.Vectors.dense(array))
            train_list.append(train_one)
            train_list2.append(train_two)
        # print("训练集：",train_list)
        # trainingRDD=sc.parallelize(train_list)

        df = spark.createDataFrame(train_list2)
        nb = ml.classification.NaiveBayes(smoothing=1.0, modelType="multinomial")
        model = nb.fit(df)
        self.model = model
        # model.transform(df).show(truncate=False)

        # sqlContext = SQLContext(sc)
        # df=sqlContext.createDataFrame(train_list,["label","features"])
        # nb=NaiveBayes(smoothing=1.0,modelType="bernoulli")
        # nb_model = nb.fit(df)
        # nb_model.transform(df).show(truncate=False)
        # nb_model=NaiveBayes().train(trainingRDD)

        # lr_result=NaiveBayes().

        # nb_model=RandomForest.trainClassifier(data=trainingRDD,numClasses=14, categoricalFeaturesInfo={},
        #                              numTrees=3, featureSubsetStrategy="auto",
        #                              impurity='gini', maxDepth=4, maxBins=32)
        # lr = LogisticRegression(maxIter=10, tol=1E-6, fitIntercept=True)
        # ovr = OneVsRest(classifier=lr)
        #
        # train_list=SQLContext.createDataFrame(train_list, IntegerType())
        # nb_model=ovr.fit(train_list)
        # shutil.rmtree(output_dir, ignore_errors=True)
        # nb_model.save(sc,"target/tmp/myNaiveBayesModel")
        # nb_model.s
        self.sc = sc
        # sc.stop()
        return model

    def loadClassifierModel(self):
        # self.conf = SparkConf().setAppName("NaiveBayesTest").setMaster("local[*]")
        # sc = SparkContext(conf=self.conf)
        # # model_path="../target/tmp/myNaiveBayesModel"
        # model_path = "target/tmp/myNaiveBayesModel"
        # if os.path.isfile(model_path):
        #     nb_model = NaiveBayesModel.load(self.sc, "target/tmp/myNaiveBayesModel")
        #     sc.stop()
        #     return nb_model
        # else:
        #     sc.stop()
        nb_model = self.TrainClassifierModel()
        return nb_model

    def loadQuestionPattern(self) -> dict():
        questionsPattern = dict()
        file = open(self.rootDirPath + "question/question_classification.txt", 'r', encoding='UTF-8')
        for line in file.readlines():
            tokens = line.split(":")
            index = int(tokens[0])
            pattern = tokens[1]
            questionsPattern[index] = pattern
        return questionsPattern

    def queryClassify(self, sentence: str):
        testArray = self.sentenceToArrays(sentence)
        # v=Vectors.dense(testArray)
        # self.conf = SparkConf().setAppName("NaiveBayesTest").setMaster("local[*]")
        sc = self.sc
        v2 = sc.parallelize([Row(features=ml.linalg.Vectors.dense(testArray))]).toDF()
        # index=self.nbModel.predict(v)

        result = self.nbModel.transform(v2)
        # result=self.model.transform(v2)
        # print("预测分类：", result.head().rawPrediction)
        # print(result.show())
        sorted_probability = list()
        sorted_probability = result.head().probability.tolist()

        index_list = map(sorted_probability.index, heapq.nlargest(2, sorted_probability))
        index_list = list(index_list)
        self.modelIndex = int(index_list[0])
        print("the model index is ", self.modelIndex)
        print("预测分类排序：", index_list)
        # print("问题模板分类【0】概率 ",vRes)
        stR = self.questionPattern[int(self.modelIndex)]
        stR_list = list()
        for i in index_list:
            stR_list.append(self.questionPattern[int(i)])
        self.index_list=index_list
        # self.sc.stop()
        # return self.questionPattern[self.modelIndex]
        return stR_list
