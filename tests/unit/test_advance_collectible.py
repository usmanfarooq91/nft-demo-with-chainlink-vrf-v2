from scripts.heplfull_scripts import (
    LOCAL_BLOCKCHAIN_ENVOIRONMENTS,
    get_account,
    get_contract,
)
from scripts.advance_collectible.deploy_and_create import deploy_and_create
from brownie import network
import pytest


def test_can_create_advance_collectable():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVOIRONMENTS:
        pytest.skip("Only for local testing")
    advance_collectible, tx = deploy_and_create()
    requestId = tx.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advance_collectible.address, {"from": get_account()}
    )
    assert advance_collectible.tokenCounter() == 1
    assert advance_collectible.tokenIdToBreed(0) == random_number % 3
