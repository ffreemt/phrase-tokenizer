"""Test phrase_tokenizer."""
from phrase_tokenizer import __version__


def test_version():
    """Test phrase_tokenizer."""
    assert __version__[:4] == "0.1."
