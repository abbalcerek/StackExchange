import pandas as pd
from html.parser import HTMLParser

class MLStripper(HTMLParser):
  def __init__(self):
    self.reset()
    self.strict = False
    self.convert_charrefs= True
    self.fed = []
  
  def handle_data(self, d):  
    self.fed.append(d)
    
  def get_data(self):
    return ''.join(self.fed)

def strip_tags(html):
  s = MLStripper()
  s.feed(html)
  return s.get_data()

def flatmap(func, *iterable):
  import itertools
  return itertools.chain.from_iterable(map(func, *iterable))

biology = pd.read_csv("train/biology.csv")
cooking = pd.read_csv("train/cooking.csv")
crypto = pd.read_csv("train/crypto.csv")
diy = pd.read_csv("train/diy.csv")
robotics = pd.read_csv("train/robotics.csv")
travel = pd.read_csv("train/travel.csv")

allFrames = [biology, cooking, crypto, diy, robotics, travel]
biology.name = "biology"
cooking.name = "cooking"
crypto.name = "crypto"
diy.name = "diy"
robotics.name = "robotics"
travel.name = "travel"

#print(biology['tags'])

allTags = [set(flatmap(lambda t: t.split(' '), frm['tags'])) for frm in allFrames]

tags = set()
for t in allTags:
  tags = tags.union(t)
    
tags = set(flatmap(lambda t: t.split(' '), tags))
print(len(tags))
print([len(set(t)) for t in allTags])

print(allFrames[0].name)
names = [frm.name for frm in allFrames]
print(names)

zippedCounts = zip(names, [len(t) for t in allTags])
print(list(zippedCounts))

zipped = list(zip(names, allTags))

for key, value in zipped:
  for key2, value2 in zipped:
    if (key < key2):
      print(key, len(value), key2, len(value2), "difference:", len(value.difference(value2)))
  
#print(strip_tags("""<p>Can anyone suggest the best way to get from Seattle-Tacoma (SEA) airport up to Redmond?</p>
#
#<p>I guess one option might be the new tram into the center of Seattle, then try to change onto one of the Express buses out to Redmond (e.g. the 545), assuming you don't have to walk too far to change? Or are you better off trying to stick with buses the whole way?</p>
#
#<p>I'm not keen on the idea of hiring a car to do it, but if a taxi could do it for a sensible price then I might not be averse...!</p>"""))