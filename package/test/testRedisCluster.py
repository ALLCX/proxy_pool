
from rediscluster import StrictRedisCluster

REDIS_NODES = [
    {'host': '10.10.20.106', 'port': 1079},
    {'host': '10.10.20.106', 'port': 1080},
    {'host': '10.10.20.106', 'port': 1081},
    {'host': '10.10.20.107', 'port': 1079},
    {'host': '10.10.20.107', 'port': 1080},
    {'host': '10.10.20.107', 'port': 1081},
]

REDIS_PASSWORD = 'qizvg5DB'


def test_redis_cluster():
    redis_client = StrictRedisCluster(startup_nodes=REDIS_NODES, password=REDIS_PASSWORD)
    return redis_client


if __name__ == '__main__':
    redisClient = test_redis_cluster()

    print(type(REDIS_NODES))

    print(redisClient.cluster_info())

