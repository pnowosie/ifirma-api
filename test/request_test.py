import pytest, os
from ifirma.request import Request


def test_request_passing_params():
    req = Request('user', 'api_key')

    assert req.api_user == 'user'
    assert req.api_key == 'api_key'

def test_request_from_config():
    os.environ['IFIRMA_API_KEY'] = 'api_key'
    os.environ['IFIRMA_API_USERNAME'] = 'user'

    req = Request()

    # it's important to tear down
    del os.environ['IFIRMA_API_USERNAME']
    del os.environ['IFIRMA_API_KEY']

    assert req.api_user == 'user'
    assert req.api_key == 'api_key'

def test_request_mixed_passing_params_and_config():
    os.environ['IFIRMA_API_USERNAME'] = 'user'

    req = Request(api_key='api_key')

    # it's important to tear down
    del os.environ['IFIRMA_API_USERNAME']

    assert req.api_user == 'user'
    assert req.api_key == 'api_key' 

def test_request_email_data_is_required():
    with pytest.raises(AssertionError):
        Request().email(0, data=None)

def test_request_email_data_has_to_be_dict_or_str():
    with pytest.raises(AssertionError):
        Request().email(0, data=tuple("wrong data type"))

def test_request_invoice_submit_data_is_required():
    with pytest.raises(AssertionError):
        Request().submit(data=None)

def test_request_invoice_submit_data_has_to_be_dict_or_str():
    with pytest.raises(AssertionError):
        Request().submit(data=tuple("wrong data type"))

def test_request_assert_data_leaves_string_unchanged():
    expected = "json string will not be changed"
    assert Request.assert_data(expected) is expected

def test_request_assert_data_jsonifies_dictionary():
    from json import dumps
    data = dict(invoice_id=1337, customer="Ala")
    expected = dumps(data)
    assert Request.assert_data(data) == expected
