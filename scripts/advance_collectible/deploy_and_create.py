from scripts.heplfull_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
)
from brownie import AdvanceCollectible, network, config
import time


def deploy_and_create():
    account = get_account()
    advance_collectible = AdvanceCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("varify", False),
    )
    print("Successfully deployed....")
    fund_with_link(advance_collectible.address)
    tx = advance_collectible.createCollectible({"from": account})
    tx.wait(1)
    print("Successfully created....")


def main():
    deploy_and_create()
