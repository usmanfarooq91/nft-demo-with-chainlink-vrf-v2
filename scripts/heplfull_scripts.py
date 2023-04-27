from brownie import (
    accounts,
    network,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
)
from web3 import Web3

DECIMALS = 8
INITIAL_VALUE = 200000000000

LOCAL_BLOCKCHAIN_ENVOIRONMENTS = [
    "development",
    "ganache_local",
    "mainnet-fork",
    "mainnet-fork-dev",
]
OPENSEA_URL = "https://testnets.opensea.io/assets/goerli/{}/{}"
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVOIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.

        args:
            contract_name (string)

        returns:
            brownie.network.contract.ProjectContract: The most resently deployed
            version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVOIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks(_decimals=DECIMALS, _initial_value=INITIAL_VALUE):
    account = get_account()
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks")
    MockV3Aggregator.deploy(_decimals, _initial_value, {"from": account})
    link = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link.address, {"from": account})
    print("Mocks Deployed...")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.2, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract funded!!")
    return tx
