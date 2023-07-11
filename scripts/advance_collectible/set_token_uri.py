from brownie import AdvanceCollectible, network
from scripts.heplfull_scripts import get_breed, get_account, OPENSEA_URL

dog_metadata_dic = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "BARNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def main():
    print(f"Working on {network.show_active()}")
    advance_collectible = AdvanceCollectible[-1]
    number_of_collectibles = advance_collectible.tokenCounter()
    for token_id in range(number_of_collectibles):
        breed = get_breed(advance_collectible.tokenIdToBreed(token_id))
        if not advance_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advance_collectible, dog_metadata_dic[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenUri(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Great! You can view your NFT at {OPENSEA_URL.format(nft_contract.address,token_id)}"
    )
    print("please wait upto 20 minutes and hit refresh metadata button")
