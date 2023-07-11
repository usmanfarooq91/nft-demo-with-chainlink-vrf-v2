from scripts.heplfull_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVOIRONMENTS,
)
from brownie import AdvanceCollectible, network, config


def deploy_and_create():
    account = get_account()
    print(account)
    vrf_coordinator, sub_id = get_contract("vrf_coordinator")
    advance_collectible = AdvanceCollectible.deploy(
        100000,
        vrf_coordinator,
        config["networks"][network.show_active()]["keyhash"],
        sub_id,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("varify", False),
    )
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVOIRONMENTS:
        tx = vrf_coordinator.addConsumer(
            sub_id, advance_collectible.address, {"from": account}
        )
        tx.wait(1)
    else:
        consumer = vrf_coordinator.getSubscription(sub_id)[3]
        if advance_collectible.address not in consumer:
            tx = vrf_coordinator.addConsumer(
                sub_id, advance_collectible.address, {"from": account}
            )
            tx.wait(1)
    print("Successfully deployed")
    tx2 = advance_collectible.createCollectible({"from": account})
    tx2.wait(1)


def main():
    deploy_and_create()
