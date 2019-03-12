# PySparkQA
PySpark's NaiveBayes Based QA System
Most important python files are listed as follows:
main2.py:ModelProcess             
-------participle based on hanlp/jieba
-------NaiveBayes classification based on Spark
-------NaiveBayesModel's training
-------queryExtension,queryAbstract,loadVocabulary,sentenceToArrays,loadQuestionPattern
test_Unit3.py
-------server module based on socket,it can be able to receive msgs and handle them by ModelProcess then send it in form of json
QuestionRepository.py
-------functions integrated the QL of NEO4J by py2neo and Nodes.py.
-------Equipped with a router which can be able to connect the classifications and the functions
Nodes.py
-------OGM of NEO4J 
