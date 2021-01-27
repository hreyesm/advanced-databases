import redis

r =  redis.Redis(host='localhost', port=3001, db=0)

for i in range(5,1000000):
    try:
        r.set('key'+str(i),i)

print('todo cool')