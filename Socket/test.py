# -*- coding:utf-8 -*-
import jpype
from jpype import *
jvmPath = jpype.getDefaultJVMPath()
print(jvmPath)
startJVM(jpype.getDefaultJVMPath(),
         "-Djava.class.path=H:\hanlp(1)\hanlp\hanlp-1.3.2.jar;H:\hanlp(1)\hanlp",
         "-Xms1g",
         "-Xmx1g")
NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
print(NLPTokenizer.segment('中国科学院计算技术研究所的教授正在教授自然语言处理课程'))

