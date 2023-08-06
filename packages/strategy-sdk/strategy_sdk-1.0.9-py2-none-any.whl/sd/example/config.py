# -*- coding:utf-8 -*-
from agent.agent_type import AgentType
from sd.example import logconfig
from strategy.bean.bean import StrategyConnectionInfo, StrategyConfiguration

__author__ = 'fzh89'


############只需要修改服务器的配置，帐号，密码，策略名##############
trader_port = 8080
trader_server_ip = u"127.0.0.1"
quote_port = 8180
# quote_server_ip = u"127.0.0.1"
quote_server_ip = u"211.152.51.189"
account = "test"
password = "96e79218965eb72c92a549dd5a330112"
# password="96e79218965ea549dd5a330112"
strategy_id = "tangtao-test-strategy"
log_file = "mylog"

trader_conn_info = StrategyConnectionInfo(
    ip=trader_server_ip,
    port=trader_port,
    account_id=account,
    password=password,
    strategy_id=strategy_id
)
trader_config = StrategyConfiguration(
    trader_server_ip, trader_port, strategy_connection_info=trader_conn_info,
    usage_type=AgentType.STRATEGY_TRADE.get_value())
quote_conn_info = StrategyConnectionInfo(
    ip=quote_server_ip,
    port=quote_port,
    account_id=account,
    password=password,
    strategy_id=strategy_id
)
quote_config = StrategyConfiguration(
    quote_server_ip, quote_port, strategy_connection_info=quote_conn_info,
    usage_type=AgentType.STRATEGY_QUOTE.get_value())
logging = logconfig.configure_log(log_file)
