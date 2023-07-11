from brownie import (
    accounts,
    network,
    config,
    MockV3Aggregator,
    VRFCoordinatorV2Mock,
    LinkToken,
    Contract,
)
from web3 import Web3

DECIMALS = 8
INITIAL_VALUE = 200000000000
GAS_PRICE_LINK = 1000000000

LOCAL_BLOCKCHAIN_ENVOIRONMENTS = [
    "development",
    "ganache_local",
    "mainnet-fork",
    "mainnet-fork-dev",
]
OPENSEA_URL = "https://testnets.opensea.io/assets/goerli/{}/{}"
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorV2Mock,
    "link_token": LinkToken,
}

BREED_MAPPING = {0: "PUG", 1: "SHIBA", 2: "BARNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


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
            tx = deploy_mocks()
            subId = tx.events["SubscriptionCreated"]["subId"]
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        subId = config["networks"][network.show_active()]["sub_id"]
    return contract, subId


def deploy_mocks(_decimals=DECIMALS, _initial_value=INITIAL_VALUE):
    account = get_account()
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks")
    # MockV3Aggregator.deploy(_decimals, _initial_value, {"from": account})
    # link = LinkToken.deploy({"from": account})
    vrf_coordinator = VRFCoordinatorV2Mock.deploy(
        config["networks"][network.show_active()]["fee"],
        GAS_PRICE_LINK,
        {"from": account},
    )
    tx = vrf_coordinator.createSubscription()
    tx.wait(1)
    tx2 = vrf_coordinator.fundSubscription(tx.return_value, 10)
    old_balance = tx2.events["SubscriptionFunded"]["oldBalance"]
    new_balance = tx2.events["SubscriptionFunded"]["newBalance"]
    print(
        f"Mocks deployed and funded, old balance was {old_balance}, new balance is {new_balance}"
    )
    return tx


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.2, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract funded!!")
    return tx
