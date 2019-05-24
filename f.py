#/usr/bin/env python3
#-*- coding: utf-8 -*-


import sys
import csv
from collections import namedtuple




class Args(object):
    def __init__(self):
        self._args = sys.argv[1:]
        if len(self._args) != 6:
            print("Parameter Error")
            sys.exit()
        self._filelist = []
        try:
            self._index = self._args.index('-c')
            self._filelist.append(self._args[self._index+1])
            self._index = self._args.index('-d')
            self._filelist.append(self._args[self._index+1])
            self._index = self._args.index('-o')
            self._filelist.append(self._args[self._index+1])
        except:
            print("Parameter Error")
            sys.exit()
    def get_configfile(self):
        return self._filelist[0]
    def get_userdatafile(self):
        return self._filelist[1]
    def get_outputfile(self):
        return self._filelist[2]

class Config(object):
    def __init__(self,configfile):
        self.config = self._read_config(configfile)
    def _read_config(self,configfile):
        config = {}
        try:
            with open(configfile,'r') as f:
                for line in f.readlines():
                     
                    if len(line.split('=')) != 2:
                        print('Parameter Error')
                        sys.exit()
                     
                    key,value = line.split('=')
                    key = key.strip()
                    value = value.strip()
                    value = float(value)
                    config[key] = value
        except:
            print('Parameter Error')
            sys.exit()
        return config
    def get_config(self,str):
        try:
            return self.config[str]
        except:            
            print('Parameter Error')
            sys.exit()

class UserData(object):
    def __init__(self,userdata_file):
        self.userdata = self._read_userdata_file(userdata_file)

    def _read_userdata_file(self,userdata_file):
        userdata = []
        userdata_item_tuple = namedtuple('userdata_item_tuple',['ID','income'])
        try:
            with open(userdata_file,'r') as f:
                file_list = list(csv.reader(f))
        except:
            print('Parameter Error')
            sys.exit()
        for item_list in file_list:
            if len(item_list) != 2:
                print('Userdata Input Error')
                continue
            try:
                userdata_item = userdata_item_tuple(ID=item_list[0],income=float(item_list[1]))
            except:
                print('Userdata Input Error')
                continue
            userdata.append(userdata_item)
        return userdata


class IncomeTaxCalculator(object):
    def __init__(self):
        self._result = []

    def calc_for_all_userdata(self,Config,userdata):
       result = []
       shebao_rate_list=['YangLao','YiLiao','ShiYe','GongShang','ShengYu','GongJiJin']
       shebao_rate = 0
       for s in shebao_rate_list:
           shebao_rate += Config.get_config(s)
       shebao_jishul = Config.get_config('JiShuL')
       shebao_jishuh = Config.get_config('JiShuH')

       income_tax_item = namedtuple('income_tax_item',['startp','rate','susuanshu'])
       income_tax_list = [
                           income_tax_item(80000,0.45,15160),
                           income_tax_item(55000,0.35,7160),
                           income_tax_item(35000,0.3,4410),
                           income_tax_item(25000,0.25,2660),
                           income_tax_item(12000,0.2,1410),
                           income_tax_item(3000,0.1,210),
                           income_tax_item(0,0.03,0)
                          ]
       for userdata_item in userdata:
           if not isinstance(userdata_item,tuple):
               print('Parameter Error:4')
               continue
           if len(userdata_item) !=2:
               print('Parameter Error:5')
               continue
           ID = userdata_item.ID
           income = userdata_item.income
           if income < shebao_jishul:
               shebao = shebao_jishul*shebao_rate
           elif shebao_jishul<= income <=shebao_jishuh:
               shebao = income*shebao_rate
           else:
               shebao = shebao_jishuh*shebao_rate
           income_before_tax = income - shebao
           income_by_tax = income_before_tax - 5000
           if income_by_tax <= 0:
                tax = 0
           for item in income_tax_list:
                if income_by_tax > item.startp:
                    tax = income_by_tax*item.rate-item.susuanshu
                    break
           income_after_tax = income_before_tax - tax
           result_item = [ID,round(income,2),round(shebao,2),round(tax,2),round(income_after_tax,2)]
           self._result.append(result_item)

    def export(self,outputfile):
        try:
            with open(outputfile,'w') as f:
                csv.writer(f).writerows(self._result)
        except:
            print('Parameter Error :6')
            sys.exit()





if __name__ == '__main__':
    a = Args()
  #  print('configfile:  {0}\nuserdatafile:  {1}\noutputfile:  {2}'.format(a.get_configfile(),a.get_userdatafile(),a.get_outputfile()))
    b = Config(a.get_configfile())
   # print(b.config)
    c = UserData(a.get_userdatafile())
   # print(c.userdata)
    d = IncomeTaxCalculator()
    d.calc_for_all_userdata(b,c.userdata)
    d.export(a.get_outputfile())




