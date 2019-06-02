# coding: utf8
# vim: set noexpandtab:

import es
import pytest

def test_string_from_byte():
    assert "'\\$'" == es.string_from_byte(-1) 
    assert "'A'" == es.string_from_byte(ord('A'))
    assert "'\\n'" == es.string_from_byte(ord('\n'))
    assert "'\\t'" == es.string_from_byte(ord('\t'))
    assert "'0'" == es.string_from_byte(ord('0'))
