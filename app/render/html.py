from typing import NamedTuple

from jinja2 import Environment, PackageLoader

from core import Metadata

jj = Environment(
    loader=PackageLoader("app.render", "templates"),
    lstrip_blocks=True,
    trim_blocks=True,
)


class HtmlDocumentRenderer(NamedTuple):
    """Renders a treebank as a standalone HTML document"""

    meta: Metadata

    def render(self) -> str:
        templ = jj.get_template("treebank.html.j2")
        text = self.meta.partial_path.read_text()
        return templ.render(text=text, meta=self.meta)
