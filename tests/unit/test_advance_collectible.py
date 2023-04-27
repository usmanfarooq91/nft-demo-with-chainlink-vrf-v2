from scripts.heplfull_scripts import (
    LOCAL_BLOCKCHAIN_ENVOIRONMENTS,
    get_account,
)
from scripts.advance_collectible.deploy_and_create import deploy_and_create
from brownie import network
import pytest


def test_can_create_advance_collectable():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVOIRONMENTS:
        pytest.skip()
    advance_collectable = deploy_and_create()
    assert advance_collectable.ownerOf(0) == get_account()
    assert advance_collectable.tokenCounter == 1
