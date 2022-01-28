"""Tokenize a sentence to phrases.

plot_tree only works in jupyter/ipython notebook.
"""
# pylint: disable=broad-except

from typing import (
    List,
    Union,
)

# import sys
import re
import ssl
import nltk
from nltk.tree import Tree

# import tensorflow
from logzero import logger

# pylint: disable=wrong-import-position, invalid-name
import benepar
import svgling

# patch tensorflow 2.x for benepar
_ = """  # no need to patch since benepar 0.2.0?
# benepar switched to pytorch and spacy instead of tensorflow
try:
    if tensorflow.__version__ > "2.0":
        sys.modules["tensorflow"] = tensorflow.compat.v1  # for earlier tf2.x
except Exception as exc:
    logger.info("Trying one more time...")
    try:
        sys.modules["tensorflow"] = tensorflow.compat  # for later tf2.x
    except Exception as exc:
        logger.error("Patch exc: %s", exc)
        raise SystemExit(1) from exc
# """

# fix ssl certificate errors
try:
    _create_unverified_https_context = ssl._create_unverified_context  # pylint: disable=protected-access
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context  # pylint: disable=protected-access

# make sure punkt is available
nltk.download('punkt')
# benepar.download('benepar_en2')
benepar.download('benepar_en3')

try:
    # from IPython.core import display
    from IPython.display import display  # pylint: disable=import-error  # for notebook
except ModuleNotFoundError:
    display = ""

parser = benepar.Parser("benepar_en3")
c_list = ["TO", "S", "VP", "VB", "NP", "VBD", "VBG", "PP", "SBAR", "SB"]
c_list1 = ["CC", "IN"]


# pylint: disable=too-many-branches, too-many-statements
# fmt: off
def phrase_tok(
        sent: str,
        cnf: bool = False,
        verbose: bool = False,
) -> Union[str, List[str]]:
    # fmt: on
    """Segment a sent to list of phrases.

    Args:
        sent: sentence to segment
        cnf: (bool) transforms the tree to Chomsky normal form first

    Returns:
        segmenteed phrases
    """
    tree = parser.parse(sent)

    if cnf:
        tree.chomsky_normal_form()

    positions = tree.treepositions()
    # elm = tree[positions[i]]

    seq = ""
    for idx, pos in enumerate(positions):
        elm = tree[pos]
        if isinstance(elm, str):
            seq += elm
            continue
        _ = """
        # check previous, if "IN", do not split, out of in
        # sent = fangfang_en_sents[98]
        # 'The ones for sale online are all out of stock.'
        # """
        if elm.label() in c_list1:
            _ = positions[idx - 3]
            _ = tree[_]
            if not isinstance(_, str):
                _ = _.label()
            if _ in ["IN"]:
                seq += "^"
                continue
            seq += '/'
            continue

        if elm.label() in c_list:
            # check previous, if "IN", do not split, e.g.
            # for sale in sent = fangfang_en_sents[98]
            _ = positions[idx - 2]
            _ = tree[_]
            if not isinstance(_, str):
                _ = _.label()
            if _ in ["IN"]:
                seq += "^"
                continue

            o_list = []
            try:
                # lst is tuple, hence list(lst[i])
                _ = tree[list(pos) + [0]].label()
            except Exception:
                _ = '_'
            o_list.append(_[:2])
            try:
                _ = tree[list(pos) + [1]].label()
            except Exception:
                _ = '_'
            o_list.append(_[:2])

            # both true, return " "
            if all(map(lambda x: x in c_list, o_list)):
                seq += ","
                continue

            # one true, return "|"
            if any(map(lambda x: x in c_list, o_list)):
                seq += "|"
                continue

        seq += "."

    if verbose:
        logger.info("\n%s", seq)

    _ = re.split(r'(?:(?<!\d)[,]|[,](?!\d)|[;:/|—])', seq)
    _ = [re.sub(r"[\s.^]+", " ", elm).strip() for elm in _ if re.sub(r"[.\s^]+", " ", elm).strip()]

    return _


# fmt: off
def show_tree(
        sent: Union[str, Tree],
        cnf: bool = False
) -> None:
    # fmt: on
    """Display tree of sent."""
    if isinstance(sent, str):
        tree = parser.parse(sent)
    else:
        tree = sent  # already a Tree
    if cnf:
        tree.chomsky_normal_form()
    tree.pprint()


def plot_tree(sent: str, cnf: bool = False) -> None:
    """Plot sent's tree using svgling.draw_tree."""
    tree = parser.parse(sent)
    if cnf:
        tree.chomsky_normal_form()

    if callable(display):
        display(svgling.draw_tree(tree))
    else:
        show_tree(tree)
