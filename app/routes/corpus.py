from flask import Blueprint, render_template, request
from werkzeug.exceptions import NotFound

from core import corpus

bp = Blueprint("corpus", __name__, url_prefix="/corpus")


@bp.route("/<lang>")
def get_index(lang: str):
    try:
        return corpus.index(lang)
    except KeyError as e:
        raise NotFound(f"Unknown language {lang}") from e


@bp.route("/<lang>/<slug>/<path:ref>")
def get_treebank(lang: str, slug: str, ref: str):
    try:
        tb = corpus.get_treebank(lang, slug)
    except KeyError as e:
        raise NotFound(f"Unknown treebank {slug}") from e
    try:
        tb = tb[ref]
    except KeyError as e:
        raise NotFound(f"Unknown reference {ref}") from e
    content = tb.meta.partial_path.read_text()
    return render_template(
        "treebank.html", title=tb.meta.title, meta=tb.meta, content=content
    )
