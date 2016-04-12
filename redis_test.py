import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

r.set('foo','bar')

if r.get('foo'):
    variable = r.get('foo')
else:
    print "Can't find stuff"

print "got", variable
