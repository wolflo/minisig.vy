import pytest

import utils.constants as C

@pytest.fixture(scope="module")
def msigv(MinisigVyper, deployer, usr_ids):
    assert C.THRESHOLD == 3
    assert len(usr_ids) == 3  # hardcode errrythang
    return MinisigVyper.deploy(C.THRESHOLD, usr_ids, {'from': deployer})
