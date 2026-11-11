"""Resolve requested fonts without substitutes, including newly installed fonts."""
from functools import lru_cache
import re

from matplotlib import font_manager
from matplotlib.ft2font import FT2Font
from matplotlib.text import Text


CJK = re.compile('[\u2e80-\u9fff\uf900-\ufaff\ufe30-\ufe4f\uff01-\uff60\U00020000-\U0003134f]')


@lru_cache(maxsize=1)
def _refresh_fonts():
    # Matplotlib's on-disk cache may predate fonts installed in this session.
    known = {entry.fname for entry in font_manager.fontManager.ttflist}
    for path in sorted(font_manager.findSystemFonts()):
        if path not in known:
            try:
                font_manager.fontManager.addfont(path)
            except (OSError, RuntimeError):
                continue


def resolve_font(family, *, required=True):
    prop = font_manager.FontProperties(family=family)
    for refresh in (False, True):
        if refresh:
            _refresh_fonts()
        try:
            path = font_manager.findfont(prop, fallback_to_default=False)
            if FT2Font(path).family_name.casefold() == family.casefold():
                return path
        except ValueError:
            pass
    if required:
        raise RuntimeError(
            f'Required font "{family}" is not installed. Install the actual font '
            'and restart Python; a substitute is not accepted. '
            'For 宋体, install SimSun (simsun.ttc or simsun.ttf).')
    return None


def check_figure_fonts(fig):
    """Reject a Chinese default-style export when SimSun is unavailable."""
    required = set()
    for text in fig.findobj(match=Text):
        if not text.get_visible() or not text.get_text().strip():
            continue
        families = text.get_fontfamily()
        # Explicit font overrides remain user choices; the glyph audit applies.
        if 'Times New Roman' in families:
            required.add('Times New Roman')
            if CJK.search(text.get_text()):
                required.add('SimSun')
    return {family: resolve_font(family) for family in sorted(required)}
