import numpy as np
import codecs
import re
from pypinyin import pinyin, Style
import sys,getopt
import os

from pypinyin import lazy_pinyin,Style
from pypinyin.core import Pinyin
from pypinyin.contrib.neutral_tone import NeutralToneWith5Mixin
from pypinyin.converter import DefaultConverter

class MyConvferter(NeutralToneWith5Mixin, DefaultConverter):
    pass
my_pinyin = Pinyin(MyConvferter())
pinyin = my_pinyin.pinyin
lazy_pinyin = my_pinyin.lazy_pinyin

def _load_res(path):
    lines = codecs.open(path, 'r' ,'UTF-8').readlines()
    max_index = []
    for line in lines:
        max_index.append(np.argmax(np.array(line.strip().split(),dtype= np.float32).tolist(), axis= 0))
    return (max_index)
def prob2label_try(ori_file_path,outfile):
    ori_dev = [line.strip() for line in
               codecs.open(ori_file_path, 'r', 'UTF-8').readlines()]
    pinyin_result = []
    for i in ori_dev:
        #print(i)
        pinyinlist = []
        pin = lazy_pinyin(''.join(re.findall(r'[\u4e00-\u9fa5_a-zA-Z0-9]', i)),style=Style.TONE3)
        pinyinlist.append(i)
        pinyinlist.append(' '.join(pin))
        pinyin_result.append(pinyinlist)
    with open(outfile,'w',encoding='utf-8') as f:
        x = []

        for i in range(len(pinyin_result)):
            l = ' '.join(pinyin_result[i][1].split(' ')[1:])
            list =[]
            m = l.split(' ')
            for j in range(len(m)-1):

                if m[j][-1] == m[j+1][-1] =='3':  # 判断33变调
                    o = m[j].replace('3','2')
                    list.append(o)
                #不，在4声之前念2声，例如：不三不四 bu4 san1 bu2 si4
                elif m[j][:-1] =='bu' and m[j+1][-1] =='4':
                    p = m[j].replace('4','2')
                    list.append(p)
                #一 ,夹在叠词之间念轻声
                elif j>1 and m[j-1][:-1] == m[j+1][:-1] and m[j][:-1] =='yi':
                    q = m[j].replace('1','5')
                    list.append(q)
                # 一 ,非4声前都变4声，4声前变2声
                elif m[j][:-1] == 'yi' and m[j][-1] !='4':
                    l = m[j].replace('1','4')
                    list.append(l)
                else:
                    list.append(m[j])
            list.append(m[-1])
            line = ' '.join(list)

            f.write(pinyin_result[i][0] + '\n')
            f.write('\t' + line+ '\n')
def find(input):
    files = os.listdir(input)
    for obj in files:
        if obj.endswith(".txt"):   #endswith()  判断以什么什么结尾
            return os.path.join(input,obj)

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "-i:-o:")
    print(opts)
    inputfile = find(opts[0][1])
    outfiles = opts[1][1]
    file_name = inputfile.split('\\')[-1].replace('.txt','')
    outfile = os.path.join(outfiles, '{}_pinyin.txt'.format(file_name))
    #inputfile = r'D:\项目\TTS_tools\try.txt'
    #outfile = r'D:\项目\TTS_tools\TTS_Pinyin\res.txt'
    prob2label_try(inputfile,outfile)