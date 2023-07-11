from scripts.heplfull_scripts import (
    LOCAL_BLOCKCHAIN_ENVOIRONMENTS,
    get_account,
    get_contract,
)
from scripts.advance_collectible.deploy_and_create import deploy_and_create
from brownie import network
import pytest
import time


def test_can_create_advance_collectable_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVOIRONMENTS:
        pytest.skip("Only for live testnet testing")
    advance_collectible, tx = deploy_and_create()
    time.sleep(180)
    assert advance_collectible.tokenCounter() == 1
