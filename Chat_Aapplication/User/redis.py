import redis,json
red = redis.StrictRedis(host="localhost", db=0, port=6379)


class Redis:
    
    def set(self,key,value):
        red.set(key, value)


    def get(self,key):
        get = red.get(key)
        return get

    def delete(self):
        red.flushall()
        return
