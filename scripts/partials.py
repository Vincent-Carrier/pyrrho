import json
from dataclasses import asdict

from core import corpus
from core.render import HtmlPartialRenderer
from core.utils import filter_none

for slug, tb in corpus.all_treebanks().items():
    dir = tb.meta.partial_path.parent
    dir.mkdir(parents=True, exist_ok=True)
    meta = dir / "metadata.json"
    meta.write_text(json.dumps(filter_none(asdict(tb.meta)), indent=2))
    for chunk in tb.chunks():
        f = chunk.meta.partial_path
        f.write_text(HtmlPartialRenderer(chunk).render())