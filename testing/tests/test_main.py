import sys
import os
path = os.path.abspath('')

sys.path.insert(0, f"{path}\development\scripts")

import main

def test_scan_for_email_or_phone_single_email():
    """
        Can correctly determine if single email in string?
    """

    expected_0 = ['Email']
    expected_1 = ['test@email.com']

    actual = main.scan_for_email_or_phone('test@email.com')

    assert expected_0 == actual[0]
    assert expected_1 == actual[1]


def test_scan_for_email_or_phone_multi_email():
    """
        Can correctly determine if multiple emails in string?
    """

    expected_0 = ['Emails']
    expected_1 = ['test@email.com', 'email24@test.co.uk']

    actual = main.scan_for_email_or_phone('test@email.com and email24@test.co.uk')

    assert expected_0 == actual[0]
    assert expected_1 == actual[1]


def test_scan_for_email_or_phone_single_phone():
    """
        Can correctly determine if single phone number in string?
    """

    expected_0 = ['Telephone Number']
    expected_1 = ['01234567891']

    actual = main.scan_for_email_or_phone('01234567891')

    assert expected_0 == actual[0]
    assert expected_1 == actual[1]


def test_scan_for_email_or_phone_multi_phone():
    """
        Can correctly determine if multiple phone numbers in string?
    """

    expected_0 = ['Telephone Numbers']
    expected_1 = ['01234567891', '+442345-678-910']

    actual = main.scan_for_email_or_phone('01234567891 and +442345-678-910')

    assert expected_0 == actual[0]
    assert expected_1 == actual[1]


def test_scan_for_email_or_phone_email_phone():
    """
        Can correctly determine if email and phone number in string?
    """

    expected_0 = ['Email', 'Telephone Number']
    expected_1 = ['test@email.com', '+442345-678-910']

    actual = main.scan_for_email_or_phone('test@email.com and +442345-678-910')

    assert expected_0 == actual[0]
    assert expected_1 == actual[1]


def test_scan_for_email_or_phone_filler_text():
    """
        Can correctly determine if email in string with dummy text around?
    """

    expected_0 = ['Email']
    expected_1 = ['test@email.com']

    actual = main.scan_for_email_or_phone('hello this is a test@email.com please check for an email')

    assert expected_0 == actual[0]
    assert expected_1 == actual[1]


def test_scan_for_email_or_phone_no_pii():
    """
        Can correctly determine if no email or phone number?
    """

    expected_0 = []
    expected_1 = []

    actual = main.scan_for_email_or_phone('hello I would like you to check this string for an email')

    assert expected_0 == actual[0]
    assert expected_1 == actual[1]


def test_cleanse_string_stop_words():
    """
        Can correctly remove stop words?
    """

    expected = ['hello', 'would', 'like', 'check', 'string', 'email']

    actual = main.cleanse_string('hello I would like you to check this string for an email')

    for _word in expected:
        assert _word in actual


def test_cleanse_string_punctuation():
    """
        Can correctly remove punctuation?
    """

    expected = ['hello']

    actual = main.cleanse_string('hello!?().,%*&')

    assert expected == actual