from models import Domains,Stock,Stocks
from connect import initGspreadClient
from utils import isUrl,get_tld
SHEET_URL="https://docs.google.com/spreadsheets/d/1ak_kWaLxTWuQXOasrYTMyJztdlQS2G_YnnYKs471APg/edit#gid=0"

MAX_TO_UPDATE=5
class Keywords:
  def __init__(self):
    self.sheet=initGspreadClient().open_by_url(SHEET_URL)
    self.Domains=Domains()

  def _loadData(self):
    #fetch MasterKeywords Worksheet
    MasterKeywordsSh=self.sheet.worksheet("MASTER KEYWORDS")
    data=MasterKeywordsSh.batch_get(["A2:N"])[0]
    def parseRow(row):
      if len(row)>=2:
        name=row[0]
        stocks=[x.strip() for x in row[1].split(";") if x!=""]
        return name,[[stock,row[4:]] for stock in stocks] if len(row)>=5 else [[stock,[]] for stock in stocks]
      else:
        return None,None

    masterData={}##contains {domain:[[stockname,kws]]}
    for row in data:
      n,kws=parseRow(row)
      if n:
        if n in masterData.keys():
          masterData[n]+=kws
        else:
          masterData[n]=kws
    for domain in masterData:
      stocks=Stocks(dict())
      for stock in masterData[domain]:
        stocks.addStock(stock[0],stock[1])
      self.Domains.addDomain(domain,stocks.items)

#k=Keywords()
#k._loadData()
#print(k.Domains.getKws("SE","CL-270"))



class Updater(Keywords):
  def __init__(self):
    super().__init__()
    self.toUpdate=[]
    self.ws=self.sheet.worksheet("Sheet12")
    
  def update(self):
    self._loadData()
    data=self.ws.batch_get(["A2:J"])[0]
    for rowid,row in enumerate(data):
      if len(row) >=2 and not len(row)>=5:
        if isUrl(row[0]):
          domain=get_tld(row[0]).upper()
          print(rowid)
          kws=self.Domains.getKws(domain,row[1])
          self._updateOnWs(rowid,kws)
    self._updateOnWs("","",True)
  def _updateOnWs(self,rowId,kws,Force=False):
    if Force:
      print("forcing update")
      self.ws.batch_update(self.toUpdate)
      self.toUpdate=[]
      return
    self.toUpdate.append({"range":f'E{rowId+2}:J{rowId+2}',"values":[kws]})
    if len(self.toUpdate)==MAX_TO_UPDATE:
      print("updating")
      self.ws.batch_update(self.toUpdate)
      self.toUpdate=[]
    
u=Updater()
u.update()