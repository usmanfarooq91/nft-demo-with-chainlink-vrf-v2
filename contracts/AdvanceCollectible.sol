// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";

contract AdvanceCollectible is ERC721URIStorage, VRFConsumerBaseV2 {
    uint256 public tokenCounter;
    bytes32 private immutable keyHash;
    uint64 private immutable s_subscriptionId;
    uint32 private immutable callbackGasLimit;
    uint16 private constant requestConfirmations = 3;
    uint32 private constant numWords = 1;

    VRFCoordinatorV2Interface private immutable i_vrfCoordinator;

    enum Breed {
        PUG,
        SHIBA,
        BARNARD
    }
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(uint256 => address) public requestIdToSender;

    event requestedCollectible(uint256 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        uint32 _callbackGasLimit,
        address _vrfCoordinator,
        bytes32 _keyHash,
        uint64 subscriptionId
    ) VRFConsumerBaseV2(_vrfCoordinator) ERC721("Robo Dog", "RBDG") {
        callbackGasLimit = _callbackGasLimit;
        s_subscriptionId = subscriptionId;
        tokenCounter = 0;
        keyHash = _keyHash;
        i_vrfCoordinator = VRFCoordinatorV2Interface(_vrfCoordinator);
    }

    function createCollectible() public returns (uint256 requestId) {
        requestId = i_vrfCoordinator.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
        return requestId;
    }

    function fulfillRandomWords(
        uint256 requestId,
        uint256[] memory randomNumber
    ) internal override {
        Breed breed = Breed(randomNumber[0] % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenUri(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner no approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
