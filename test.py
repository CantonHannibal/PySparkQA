from pyspark import SparkConf, SparkContext
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayesModel, NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.rdd import RDD

conf = SparkConf().setAppName("myApp").setMaster("local")
sc = SparkContext(conf=conf)

vMale = Vectors.dense(1, 0, 1, 0, 1, 0)
length = 6
index = [0, 1, 2, 3, 5]
values = [1, 1, 1, 1, 1]
vFemale = Vectors.sparse(length, index, values)

train_one = LabeledPoint(1.0, vMale)
train_two = LabeledPoint(2.0, vFemale)
train_three = LabeledPoint(2.0, Vectors.dense(0, 1, 1, 1, 0, 1))

trains = list()
trains.append(train_one)
trains.append(train_two)
trains.append(train_three)
trainingRDD = sc.parallelize(trains)
nb = NaiveBayes()
nb_model = NaiveBayes.train(trainingRDD)

evaluator = MulticlassClassificationEvaluator(metricName="accuracy")

dTest = [0, 1, 1, 0, 0, 1]
vTest = Vectors.dense(dTest)

# nb_model.clearThreshold()
modelIndex = nb_model.predict(vTest)
print("标签分类编号：", modelIndex)

print(nb_model.predict(vTest))

if (modelIndex == 1):
    print("答案：这个人是男性")
elif (modelIndex == 2):
    print("答案：这个人是女性")

sc.stop()
