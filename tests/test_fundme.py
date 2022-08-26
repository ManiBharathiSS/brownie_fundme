from multiprocessing.connection import wait
from scripts.deploy import deploy_fund_me
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest
from brownie import network, accounts, exceptions


def test_fundme_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx_fund = fund_me.fund({"from": account, "value": entrance_fee})
    tx_fund.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx_withdraw = fund_me.withdraw({"from": account})
    tx_withdraw.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_onlyowner_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local network")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
