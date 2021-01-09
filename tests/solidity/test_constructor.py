#!/usr/bin/python3

import pytest
import brownie

import utils.utils as utils
import utils.constants as C
import utils.reverts as reverts

def test_success(msig, usr_ids):
    assert msig.nonce() == 0
    assert msig.threshold() == C.THRESHOLD
    assert msig.allSigners() == usr_ids
    assert msig.DOMAIN_SEPARATOR() == utils.encode_dom_sep(msig)

def test_fail_zero_head(Minisig, deployer, usr_ids):
    bad_usr_ids = usr_ids.copy()
    bad_usr_ids.insert(0, C.ZERO_ADDRESS)
    with brownie.reverts(reverts.BAD_SIGNER):
        Minisig.deploy(C.THRESHOLD, bad_usr_ids, {'from': deployer})

def test_fail_unordered_signers(Minisig, deployer, usr_ids):
    bad_usr_ids = usr_ids.copy()
    bad_usr_ids[0], bad_usr_ids[1] = bad_usr_ids[1], bad_usr_ids[0]
    with brownie.reverts(reverts.BAD_SIGNER):
        Minisig.deploy(C.THRESHOLD, bad_usr_ids, {'from': deployer})

def test_fail_insufficient_signers(Minisig, deployer, usr_ids):
    with brownie.reverts(reverts.INSUFFICIENT_SIGNERS):
        Minisig.deploy(len(usr_ids) + 1, usr_ids, {'from': deployer})

# def test_fail_zero_threshold(Minisig, deployer, usr_ids):
#     with brownie.reverts():
#         Minisig.deploy(0, [], {'from': deployer})
