from redis import Redis
from random import randint

rd = Redis(host="redis-cluster", port=6379)

while (True):

	if rd.get('rev') == None:
		revolverStr = '000000'
		revolver = list(revolverStr)
		bala = randint(0,5)
		revolver[bala] = '1'
		revolver = "".join(revolver)
    
		rd.set('rev',revolver)
