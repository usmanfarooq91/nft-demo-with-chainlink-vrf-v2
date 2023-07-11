from scripts.heplfull_scripts import get_account, fund_with_link, get_contract
from brownie import AdvanceCollectible
from web3 import Web3


def main():
    account = get_account()
    advance_collectible = AdvanceCollectible[-1]
    tx = advance_collectible.createCollectible({"from": account})
    tx.wait(1)
