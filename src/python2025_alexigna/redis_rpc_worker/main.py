from redis import Redis

from python2025_alexigna.redis_rpc.rpc import ProxyRPC

with Redis() as redis:
    rpc = ProxyRPC(redis)
    result = rpc.send_command(
        hostnames="1.2.3.4",
        platform="cisco_iosxe",
        command="show version",
        timeout=10,
    )
    print(result.result)
