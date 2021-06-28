from app import app
from app.utils import extractElement

class Opinion:

    selectors = {
        "opinionId": ['div.revz_head'],
        "author": ["span.revz_nick"],
        "stars": ["span.review_badge > strong"],
        "content": ["div.revz_txt > span"],
        "trusty": ["span.revz_wo_badge"],
        "publishDate": ["span.revz_date"]
    }

    def __init__(self, opinionId=None, author=None, stars=None, content=None, trusty=None, publishDate=None):
        self.opinionId = opinionId
        self.author = author
        self.stars = stars
        self.content = content
        self.trusty = trusty
        self.publishDate = publishDate
    
    def extractOpinion(self,opinionTree):
        for key, value in self.selectors.items():
            setattr(self, key, extractElement(opinionTree, *value))
        self.opinionId = opinionTree.select('div.revz_head a').pop(0)['href'].strip()
        self.trusty = True if len(opinionTree.select('span.revz_wo_badge')) > 0 else False
        return self

    def transformOpinion(self):
        try:
            self.stars = float(self.stars)
        except TypeError:
            self.stars = None
        self.opinionId = int(self.opinionId.split('/')[2])
        if self.content:
            self.content = self.content.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        return self

    def __str__(self):
        return 'opinionId: '+str(self.opinionId)+'<br>'+'<br>'.join(key+": "+str(getattr(self, key)) for key in self.selectors.keys())

    def todict(self):
        return {'opinionId': self.opinionId} | {key: getattr(self, key) for key in self.selectors.keys()}
        #return {'opinionId': self.opinionId}.update({key: getattr(self, key)
                                                     #for key in self.selectors.keys()})
        



