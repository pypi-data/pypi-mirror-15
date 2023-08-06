# encoding: utf-8

import unittest

from sd.utils.enum import EnumMetaCls, CommonNameValueEnum, can_not_init

__author__ = 'yonka'


class AgentType(CommonNameValueEnum, metaclass=EnumMetaCls):
    def __str__(self):
        return "AgentType(%d)" % self.v


AgentType.STRATEGY_TRADE = AgentType(1)
AgentType.STRATEGY_QUOTE = AgentType(2)

AgentType.__init__ = can_not_init


class TestAgentType(unittest.TestCase):
    def test_init(self):
        print(AgentType.STRATEGY_TRADE)
        res = False
        try:
            AgentType(1)
        except AssertionError:
            res = True
        assert res
