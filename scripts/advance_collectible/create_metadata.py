from brownie import AdvanceCollectible, network
from scripts.heplfull_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json

ipfs_uri_file_name = f"./metadata/{network.show_active()}/ipfs-uri.json"


def main():
    advance_collectible = AdvanceCollectible[-1]
    print(advance_collectible)
    number_of_collectibles = advance_collectible.tokenCounter()
    print(f"You have created {number_of_collectibles} collectibles!")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advance_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! delete it to overwrite.")
        else:
            print(f"Creating metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_path = "./img/" + breed.lower() + ".png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri
            print(collectible_metadata)
            with open(metadata_file_name, "w") as file:
                json.dump(metadata_template, file)
            ipfs_json_uri = upload_to_ipfs(metadata_file_name)
            with open(ipfs_uri_file_name, "a") as file:
                file.write(ipfs_json_uri)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
