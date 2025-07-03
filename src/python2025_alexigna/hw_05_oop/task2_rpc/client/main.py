from python2025_alexigna.hw_05_oop.task2_rpc.rpc import RPC, RPCResult

with RPC() as rpc:
    result: RPCResult = rpc.hello(user="admin", count=3)
    result.wait_for_result()
    print(result.result)
    print(result.is_failed)
    print(result.is_finished)
