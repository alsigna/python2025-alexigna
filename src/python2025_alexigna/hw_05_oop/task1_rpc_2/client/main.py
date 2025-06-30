from python2025_alexigna.hw_05_oop.task1_rpc_2.rpc import RPC, RPCResult

with RPC(app_name="scrapli") as rpc:
    # tasks: list[RPCResult] = [rpc.send_command.no_wait(f"admin-{i:03}") for i in range(1, 101)]
    # rpc.gather(tasks)
    # for task in tasks:
    #     if task.exception is None:
    #         print(f"{task.job_id}: {task.result}")
    #     else:
    #         print(f"{task.job_id}: {task.exception}")
    task: RPCResult = rpc.send_command(host="1.2.3.4", command="show version")
    print(f"{task.is_failed=}")
    print(f"{task.is_finished=}")
    print(f"{task.result=}")
