from flask_common.test_helpers import (
    Capture, DictCompare, RegexSetCompare, SetCompare
)


def test_set_compare():
    assert SetCompare([1, 2, 3]) == [2, 3, 1]
    assert not (SetCompare([1, 2, 3]) == [2, 2, 2])


def test_regex_set_compare():
    regex = '(.*) OR (.*) OR (.*)'
    assert RegexSetCompare(regex, ['1', '2', '3']) == '2 OR 3 OR 1'
    assert not (RegexSetCompare(regex, ['2', '2', '2']) == '2 OR 3 OR 1')


def test_capture():
	capture = Capture()
	assert capture == 'hello'
	assert capture() == 'hello'


def test_dict_compare():
	assert {'a': 'b'} == DictCompare({'a': 'b'})
	assert not ({'a': 'c'} == DictCompare({'a': 'b'}))
	assert {'a': 'b', 'c': 'd'} == DictCompare({'a': 'b'})
	assert not ({'a': 'c', 'c': 'd'} == DictCompare({'a': 'b'}))
	assert not ({'a': 'b'} == DictCompare({'c': 'd'}))
