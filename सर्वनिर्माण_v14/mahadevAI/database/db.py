
db={}

def save(k,v):

    db[k]=v

def load(k):

    return db.get(k)
