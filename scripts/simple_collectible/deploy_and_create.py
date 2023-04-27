from scripts.heplfull_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"


def deploy_and_create():
    account = get_account()
    simple_collectable = SimpleCollectible.deploy({"from": account})

    tx2 = simple_collectable.createCollectible(sample_token_uri, {"from": account})
    tx2.wait(1)

    print(
        f"Awesome, you can view your NFT at {OPENSEA_URL.format(simple_collectable.address,simple_collectable.tokenCounter()-1)}"
    )
    return simple_collectable


def main():
    deploy_and_create()
