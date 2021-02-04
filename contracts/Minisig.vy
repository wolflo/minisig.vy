# @version ^0.2.0

NUM_SIGNERS: constant(uint256) = 3
MAX_UINT8: constant(uint256) = 255

# --- EIP712 ---
DOMAIN_SEPARATOR: public(bytes32) # immutable
# keccak256("EIP712Domain(uint256 chainId,uint256 deployBlock,address verifyingContract)");
DOMAIN_SEPARATOR_TYPEHASH: constant(bytes32) = 0x0a684fcd4736a0673611bfe1e61ceb93fb09bcd288bc72c1155ebe13280ffeca
# keccak256("Execute(address target,uint8 callType,uint256 nonce,uint256 txGas,uint256 value,bytes data)");
EXECUTE_TYPEHASH: constant(bytes32) = 0x9c1370cbf5462da152553d1b9556f96a7eb4dfe28fbe07e763227834d409103a

# --- State ---
nonce: public(uint256)

# --- Immutable ---
threshold: public(uint256) # uint8, immutable
numSigners: uint256
signers: address[NUM_SIGNERS] # signers: address[]

# --- Constructor ---
@external
def __init__(_threshold: uint256, _signers: address[NUM_SIGNERS]):
    assert _threshold <= MAX_UINT8
    assert NUM_SIGNERS >= _threshold
    assert NUM_SIGNERS <= MAX_UINT8

    self.DOMAIN_SEPARATOR = keccak256(
        concat(
            DOMAIN_SEPARATOR_TYPEHASH,
            convert(chain.id, bytes32),
            convert(block.number, bytes32),
            convert(self, bytes32)
        )
    )

    prevSigner: address = ZERO_ADDRESS
    for signer in _signers:
        assert convert(signer, uint256) > convert(prevSigner, uint256)
        prevSigner = signer

    self.threshold = _threshold
    self.signers = _signers

# --- Fallback function ---
@external
@payable
def __default__():
    return


@external
@payable
def execute(
    _target: address,
    _callType: uint256,
    _gas: uint256,
    _value: uint256,
    _data: Bytes[100],
    _sigs: Bytes[65*NUM_SIGNERS]
) -> bool:
    assert len(_sigs) >= self.threshold
    assert _callType == 0 or _callType == 1

    origNonce: uint256 = self.nonce
    newNonce:uint256 = origNonce + 1
    self.nonce = newNonce

    digest: bytes32 = keccak256(
        concat(
            b'\x19\x01',
            self.DOMAIN_SEPARATOR,
            keccak256(
                concat(
                    EXECUTE_TYPEHASH,
                    convert(_target, bytes32),
                    convert(_callType, bytes32),
                    convert(origNonce, bytes32),
                    convert(_gas, bytes32),
                    convert(_value, bytes32),
                    keccak256(_data)
                )
            )
        )
    )

    signerIdx: uint256 = 0
    count: uint256 = 0
    # we actually want to go up to threhsold number of iterations
    for i in range(NUM_SIGNERS):
        if count == self.threshold:
            break
        sigIdx:uint256 = 65 * i
        r: uint256 = convert(slice(_sigs, sigIdx, 32), uint256)
        s: uint256 = convert(slice(_sigs, sigIdx + 32, 32), uint256)
        v: uint256 = convert(slice(_sigs, sigIdx + 64, 1), uint256)
        addr: address = ecrecover(digest, v, r, s)

        elem: bool = False
        # for j in range(signerIdx, NUM_SIGNERS):
        for j in range(NUM_SIGNERS):
            if j < signerIdx:
                continue
            if addr == self.signers[j]:
                elem = True
                count = count + 1
                break
        assert elem
    assert count == self.threshold

    # make call
    # delegatecall
    if _callType == 1:
        retdata: Bytes[MAX_UINT8] = raw_call(_target,
                                             _data,
                                             max_outsize=MAX_UINT8,
                                             gas=_gas,
                                             value=_value,
                                             is_delegate_call = True)
        assert self.nonce == newNonce
    # call
    else:
        retdata: Bytes[MAX_UINT8] = raw_call(_target,
                                             _data,
                                             max_outsize=MAX_UINT8,
                                             gas=_gas,
                                             value=_value)

    return True


# return signers array
@external
@view
def allSigners() -> address[NUM_SIGNERS]:
    return self.signers
