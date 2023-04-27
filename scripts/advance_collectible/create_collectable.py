from scripts.heplfull_scripts import get_account, fund_with_link
from brownie import AdvanceCollectible
from web3 import Web3


def main():
    account = get_account()
    advance_collectable = AdvanceCollectible[-1]
    fund_with_link(advance_collectable.address)
    tx = advance_collectable.createCollectible({"from": account})
    tx.wait(1)
