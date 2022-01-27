"""Tokenize a sentence to phrases.

plot_tree only works in jupyter/ipython notebook.
"""
# pylint: disable=broad-except

from typing import (
    List,
    Union,
)

import sys
import re
import nltk
from nltk.tree import Tree
import tensorflow
from logzero import logger

# patch tensorflow 2.x for benepar
try:
    if tensorflow.__version__ > "2.0":
        sys.modules["tensorflow"] = tensorflow.compat.v1  # for earlier tf2.x
except Exception as exc:
    logger.info("Trying one more time...")
    try:
        sys.modules["tensorflow"] = tensorflow.compat  # for later tf2.x
    except Exception as exc:
        print("Patch exc: %s" % exc)
        raise SystemExit(1) from exc

# pylint: disable=wrong-import-position, invalid-name
import benepar
import svgling

# make sure punkt is available
nltk.download('punkt')
benepar.download('benepar_en2')

try:
    from IPython.core import display  # pylint: disable=import-error  # for notebook
except ModuleNotFoundError:
    display = ""

parser = benepar.Parser("benepar_en2")

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

    dis_label2
    cnf: transforms the tree to Chomsky normal form first
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
#                 try:
            _ = positions[idx - 3]
#             print(idx, idx - 3, _)
            _ = tree[_]
            if not isinstance(_, str):
                _ = _.label()
#                 print('label', _)
            if _ in ["IN"]:
                seq += "^"
                continue
            seq += '/'
            continue

        if elm.label() in c_list:
            # check previous, if "IN", do not split, e.g.
            # for sale in sent = fangfang_en_sents[98]
#                 try:
            _ = positions[idx - 2]
#             print(idx, idx - 2, _)
            _ = tree[_]
            if not isinstance(_, str):
                _ = _.label()
#                 print('label', _)
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

        # return ''
        seq += "."

    if verbose:
        # print(seq)
        logger.info("\n%s", seq)

    _ = re.split(r'(?:(?<!\d)[,]|[,](?!\d)|[;:/|—])', seq)
    _ = [re.sub(r"[\s.^]+", " ", elm).strip() for elm in _ if re.sub(r"[.\s^]+", " ", elm).strip()]

    return _


# fmt: off
def show_tree(
        sent: Union[str,  Tree],
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
    # if "display" in globals():
    if callable(display):
        display(svgling.draw_tree(tree))
    else:
        show_tree(tree)
