# encoding: utf-8

__author__ = 'fzh89'

from strategy.bean.datatype import *

from strategy.stragety import BaseStrategy
from sd.example.config import logging


class DataExample(BaseStrategy):
    def __init__(self, quote_config):
        super(DataExample, self).__init__(quote_config)

    def on_notify_quote(self, dataType, data):
        if (dataType == TICK_LEVEL_TWO_STOCK or dataType == TICK_LEVEL_ONE_STOCK):
            logging.debug("Received stock data:%s", data.to_dict())
        elif (dataType == TICK_LEVEL_TWO_FUTURE or dataType == TICK_LEVEL_ONE_FUTURE):
            logging.debug("Received future data:%s", data.to_dict())
        elif (dataType > SAMPLE_DATA_BEGIN and dataType < SAMPLE_DATA_END):
            logging.debug("Received kline data:%s", data.to_dict())
        else:
            logging.warn("Unexpected data type:%d,content:%s", dataType, data.to_dict())


if __name__ == "__main__":
    from sd.example.config import quote_config

    print
    quote_config.to_json()
    dataExample = DataExample(quote_config)

    if not dataExample.init():
        logging.error("Failed to login,exit")
        exit(1)
    # #######订阅上期所行情
    # symbol="%d.%s.%s"%(TICK_LEVEL_TWO_FUTURE,"SHFE","rb1610")
    # ret=dataExample.req_subscribe(symbol)
    # if ret.errorId!=0:
    # logging.error("Failed to subscribe %s because of %s",symbol,ret.to_json())
    # #######订阅中金所行情
    # symbol="%d.%s.%s"%(TICK_LEVEL_TWO_FUTURE,"CFFEX","IC1610")
    # ret=dataExample.req_subscribe(symbol)
    # if ret.errorId!=0:
    # logging.error("Failed to subscribe %s because of %s",symbol,ret.to_json())
    # #######订阅大商所行情
    # symbol="%d.%s.%s"%(TICK_LEVEL_TWO_FUTURE,"DCE","i1609")
    # ret=dataExample.req_subscribe(symbol)
    # if ret.errorId!=0:
    # logging.error("Failed to subscribe %s because of %s",symbol,ret.to_json())
    # #######订阅郑商所行情
    # symbol="%d.%s.%s"%(TICK_LEVEL_TWO_FUTURE,"CZCE","CF609")
    # ret=dataExample.req_subscribe(symbol)
    # if ret.errorId!=0:
    # logging.error("Failed to subscribe %s because of %s",symbol,ret.to_json())
    # #######订阅上交所行情
    # symbol="%d.%s.%s"%(TICK_LEVEL_TWO_STOCK,"SHSE","600600")
    # ret=dataExample.req_subscribe(symbol)
    # if ret.errorId!=0:
    #     logging.error("Failed to subscribe %s because of %s",symbol,ret.to_json())
    # #######订阅深交所行情
    symbol = "%d.%s.%s" % (SAMPLE_DATA_MINUTE, "SHFE", "RB1610")
    ret = dataExample.req_subscribe(symbol)
    if ret.errorId != 0:
        logging.error("Failed to subscribe %s because of %s", symbol, ret.to_json())
    (data, error) = dataExample.req_kline("SHSE.600895", dataType=SAMPLE_DATA_MINUTE, cycDef=5, beginDate=20160506,
                                          beginTime=90000000)
    for item in data:
        print
        item.to_json()
    dataExample.run()
