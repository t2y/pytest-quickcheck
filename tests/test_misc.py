# -*- coding: utf-8 -*-
import pytest

@pytest.mark.parametrize("prime", [3, 5, 7])
def test_is_prime(prime):
    assert prime in [3, 5, 7]

def test_create_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1
