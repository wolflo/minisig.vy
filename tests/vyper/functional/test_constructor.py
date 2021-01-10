import pytest
import brownie

import utils.utils as utils
import utils.constants as C

def test_success(msigv, usr_ids):
    assert msigv.nonce() == 0
    assert msigv.threshold() == C.THRESHOLD
    assert msigv.allSigners() == usr_ids
    assert msigv.DOMAIN_SEPARATOR() == utils.encode_dom_sep(msigv)

def test_fail_zero_head(MinisigVyper, deployer, usr_ids):
    bad_usr_ids = usr_ids.copy()
    # bad_usr_ids.insert(0, C.ZERO_ADDRESS)
    bad_usr_ids[0] = C.ZERO_ADDRESS
    with brownie.reverts():
        MinisigVyper.deploy(C.THRESHOLD, bad_usr_ids, {'from': deployer})

def test_fail_unordered_signers(MinisigVyper, deployer, usr_ids):
    bad_usr_ids = usr_ids.copy()
    bad_usr_ids[0], bad_usr_ids[1] = bad_usr_ids[1], bad_usr_ids[0]
    with brownie.reverts():
        MinisigVyper.deploy(C.THRESHOLD, bad_usr_ids, {'from': deployer})

def test_fail_insufficient_signers(MinisigVyper, deployer, usr_ids):
    with brownie.reverts():
        MinisigVyper.deploy(len(usr_ids) + 1, usr_ids, {'from': deployer})

