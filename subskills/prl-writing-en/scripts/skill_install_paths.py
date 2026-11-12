"""User-level skill directories shared by the source and portable installers."""
import os
from pathlib import Path

AGENTS = ('codex', 'claude-code', 'opencode', 'deepseek-harness')


def default_destination(agent):
    if agent == 'codex':
        return Path.home() / '.agents' / 'skills'
    if agent == 'claude-code':
        return Path.home() / '.claude' / 'skills'
    if agent == 'opencode':
        return Path(os.environ.get('XDG_CONFIG_HOME') or Path.home() / '.config').expanduser() / 'opencode' / 'skills'
    if agent == 'deepseek-harness':
        return Path(os.environ.get('DSH_HOME') or Path.home() / '.dsh').expanduser() / 'skills'
    raise ValueError('unknown agent: ' + agent)
