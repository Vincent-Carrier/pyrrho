from flask import Blueprint, request

from core import corpus

bp = Blueprint('corpus', __name__, url_prefix='/corpus')


@bp.route("/<lang>")
async def get_index(lang: str):
    try:
        return corpus.index(lang)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Unknown language {lang}") from e


@bp.route("/<lang>/<slug>")
async def get_treebank(lang: str, slug: str, ref: str | None = None):
    # if request.accept_mimetypes.best == "application/json":
    try:
        tb = corpus.get_treebank(lang, slug)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Unknown treebank {slug}") from e
    try:
        if ref is not None:
            tb = tb[ref]
        return HtmlDocumentRenderer(tb.meta).render()
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Unknown reference {ref}") from e
