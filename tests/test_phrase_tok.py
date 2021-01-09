"""Test phrase_tok."""
from phrase_tokenizer import phrase_tok


def test_phrase_tok():
    """Test phrase_tok."""
    sent = "Short cuts make long delay."
    phr = phrase_tok(sent)
    assert len(phr) == 2
