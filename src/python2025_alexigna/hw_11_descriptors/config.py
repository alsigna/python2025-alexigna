from python2025_alexigna.hw_11_descriptors.utils import Parameter


class Config:
    network: Parameter[str] = Parameter(env="MY_APP_NETWORK", default="dc")
    developer_mode: Parameter[bool] = Parameter(env="MY_APP_DEVELOPER_MODE", default=False)
    dump_to_file: Parameter[bool] = Parameter(env="MY_APP_DUMP_TO_FILE", default=False)
    cli_username: Parameter[str] = Parameter(env="MY_APP_CLI_USERNAME", type_=str)
    cli_password: Parameter[str] = Parameter(env="MY_APP_CLI_PASSWORD", type_=str)
    scrapli_cli_transport: Parameter[str] = Parameter(env="MY_APP_CLI_SCRAPLI_TRANSPORT", default="system")
    scrapli_cli_port: Parameter[int] = Parameter(env="MY_APP_CLI_SCRAPLI_PORT", default=22)
    scrapli_timeout_socket: Parameter[int] = Parameter(env="MY_APP_SCRAPLI_TIMEOUT_SOCKET", default=15)
    scrapli_timeout_transport: Parameter[int] = Parameter(env="MY_APP_SCRAPLI_TIMEOUT_TRANSPORT", default=30)
    scrapli_timeout_ops: Parameter[int] = Parameter(env="MY_APP_SCRAPLI_TIMEOUT_OPS", default=30)


config = Config()
