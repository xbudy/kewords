from dataclasses import dataclass
from typing import List,Dict
import random


@dataclass
class Stock:
    kws:List[str]
    def shuffle(self):
        kws=[]
        kws+=random.sample(self.kws[0:3],3)
        kws+=random.choices(random.sample(self.kws[3:6],3),k=2)
        kws+=[random.choice(self.kws[6:])]
        return kws

@dataclass
class Stocks:
    items: Dict[str,Stock]
    def addStock(self,name,kws:List[str]):
        if not len(kws)==10:
            kws+=["" for x in range(10-len(kws))]
        self.items[name]=Stock(kws)##############
l=["aukso spalvos maisytuvai","auksinis kranas","zalvarinis maisytuvas","auksinis maisytuvas","auksiniai maisytuvai","virtuves maisytuvai aukso spalvos","auksiniai kranai","auksinis virtuvinis maisytuvas","virtuvinis maisytuvas auksinis","maisytuvas aukso spalvos"]
@dataclass
class Domains:
    def getDomain(self,d):
        if hasattr(self,d):
            return self.__getattribute__(d)
        else:
            return None
    def addDomain(self,name,stocks:Dict[str,Stock]):
        self.__setattr__(name,stocks)
    def append(self,name,stocks:Dict[str,Stock]):
      if not hasattr(self,name):
        self.addDomain(name,stocks)
      else:
        pass
    def getKws(self,name,stock:str)-> List[str]:
        if hasattr(self,name):
            return self.generateKws(stock,self.__getattribute__(name))
        else:
          return ["-" for x in range(10)]
    @staticmethod
    def generateKws(stock,stocks:Dict[str,Stock])-> List[str]:
        if stock in stocks:
          return stocks[stock].shuffle()
        else:
          return ["-" for x in range(10)]
