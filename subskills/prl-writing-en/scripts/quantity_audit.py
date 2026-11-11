#!/usr/bin/env python3
"""Audit declared quantity identities against exported labels and actual text.

This checks explicit mappings, not whether a source or a mapping is scientifically
correct. Values are deliberately irrelevant to quantity identity.
"""
import json
from pathlib import Path
import re
from corpus_lib import sha256


def normalize_symbol(text):
    """Normalize limited TeX presentation while preserving ordinary word boundaries."""
    text = text.replace('$', '')
    for _ in range(4):
        text = re.sub(r'\\(?:mathrm|mathit|mathbf|text)\{([^{}]*)\}', r'\1', text)
        text = re.sub(r'([_^])\{([^{}]*)\}', r'\1\2', text)
    text = re.sub(r'\\[,;! ]', '', text)
    text = re.sub(r'\s*([_^])\s*', r'\1', text)
    return re.sub(r'\s+', ' ', text).strip()


def contains_symbol(text, symbol):
    # Do not erase ordinary prose spaces: that would concatenate adjacent words.
    normalized = normalize_symbol(text)
    token = normalize_symbol(symbol)
    def continues_identifier(char):
        # Chinese prose routinely touches Latin/Greek notation without spaces.
        # Preserve boundaries for Latin/Greek letters, digits and subscripts.
        if not char or '\u3400' <= char <= '\u9fff' or '\U00020000' <= char <= '\U000323af':
            return False
        return char.isalnum() or char in '_\\'
    if not token:
        return False
    return any(not continues_identifier(normalized[m.start()-1:m.start()] if m.start() else '')
               and not continues_identifier(normalized[m.end():m.end()+1])
               for m in re.finditer(re.escape(token), normalized))


def collect_labels(fig):
    """Read actual visible artists, including inset axes; locators are stable within a figure."""
    rows, seen = [], set()

    def add(locator, artist):
        if artist is not None and artist.get_visible() and artist.get_text().strip():
            rows.append({'locator': locator, 'text': artist.get_text()})

    def axes(ax, locator):
        if id(ax) in seen or not ax.get_visible():
            return
        seen.add(id(ax))
        add(locator + '.xlabel', ax.xaxis.label)
        add(locator + '.ylabel', ax.yaxis.label)
        for name, artist in [('title', ax.title), ('title_left', ax._left_title), ('title_right', ax._right_title)]:
            add(locator + '.' + name, artist)
        for i, artist in enumerate(ax.texts):
            add(f'{locator}.text[{i}]', artist)
        legend = ax.get_legend()
        if legend is not None and legend.get_visible():
            add(locator + '.legend.title', legend.get_title())
            for i, artist in enumerate(legend.get_texts()):
                add(f'{locator}.legend[{i}]', artist)
        for i, child in enumerate(ax.child_axes):
            axes(child, f'{locator}.inset[{i}]')

    for i, ax in enumerate(fig.axes):
        axes(ax, f'axes[{i}]')
    for i, artist in enumerate(fig.texts):
        add(f'figure.text[{i}]', artist)
    for i, legend in enumerate(fig.legends):
        if legend.get_visible():
            add(f'figure.legend[{i}].title', legend.get_title())
            for j, artist in enumerate(legend.get_texts()):
                add(f'figure.legend[{i}][{j}]', artist)
    return rows


def load_artifacts(figure_reports=(), texts=()):
    """Load ID=PATH bindings and verify the images recorded by each figure report."""
    artifacts, provenance = {}, {}
    for kind, specs in [('figure', figure_reports), ('text', texts)]:
        for spec in specs:
            if '=' not in spec:
                raise ValueError('artifact binding must be ID=PATH')
            ident, filename = spec.split('=', 1)
            if not ident.strip() or ident in artifacts:
                raise ValueError('empty or duplicate artifact ID: ' + ident)
            path = Path(filename)
            if kind == 'text':
                artifacts[ident] = {'text': path.read_text(encoding='utf-8')}
            else:
                report = json.loads(path.read_text(encoding='utf-8'))
                if not isinstance(report, dict):
                    raise ValueError('figure report must be an object: ' + str(path))
                if 'artifacts' in report:
                    outputs=report['artifacts']
                    if not isinstance(outputs,dict) or not outputs:
                        raise ValueError('report lacks exported image bindings: ' + str(path))
                    for output in outputs.values():
                        filename=output.get('path') if isinstance(output,dict) else None
                        if not isinstance(filename,str) or not filename or Path(filename).name!=filename:
                            raise ValueError('invalid exported image binding: ' + str(path))
                        image=path.parent/filename
                        if not image.is_file() or output.get('sha256')!=sha256(image):
                            raise ValueError('stale or absent exported image: ' + str(image))
                else:
                    # Existing archived reports bind only a sibling PDF.
                    pdf = path.with_suffix('.pdf')
                    if not pdf.is_file() or report.get('pdf_sha256') != sha256(pdf):
                        raise ValueError('stale or absent PDF for report: ' + str(path))
                rows = report.get('labels')
                if not isinstance(rows, list) or not rows:
                    raise ValueError('report lacks actual label inventory: ' + str(path))
                labels = {}
                for row in rows:
                    if not isinstance(row, dict) or not isinstance(row.get('locator'), str) or not isinstance(row.get('text'), str):
                        raise ValueError('malformed actual label inventory: ' + str(path))
                    if row['locator'] in labels:
                        raise ValueError('duplicate label locator: ' + row['locator'])
                    labels[row['locator']] = row['text']
                artifacts[ident] = labels
            provenance[ident] = {'path': str(path.resolve()), 'sha256': sha256(path), 'kind': kind}
    return artifacts, provenance


def audit(ledger, artifacts=None):
    errors = []
    def fail(code, where):
        errors.append({'code': code, 'where': where})
    if 'quantities' not in ledger and 'quantity_usages' not in ledger:
        return {'status': 'not_requested', 'passed': None, 'errors': [], 'coverage': 'no quantity audit'}
    quantities, usages = ledger.get('quantities'), ledger.get('quantity_usages')
    if not isinstance(quantities, list) or not quantities or not isinstance(usages, list) or not usages:
        return {'status': 'failed', 'passed': False, 'errors': [{'code': 'quantity_lists_required', 'where': 'quantities/quantity_usages'}]}
    artifacts = artifacts or {}
    records, owners, aliases = {}, {}, {}
    evidence_ids = {r.get('id') for r in ledger.get('evidence', []) if isinstance(r, dict) and isinstance(r.get('id'), str)} if isinstance(ledger.get('evidence'), list) else set()
    for i, quantity in enumerate(quantities):
        where = f'quantities[{i}]'
        required = ['id', 'meaning', 'source_symbol', 'unit', 'scope', 'evidence_id', 'source_locator']
        if not isinstance(quantity, dict) or any(not isinstance(quantity.get(k), str) or not quantity[k].strip() for k in required):
            fail('quantity_fields_required', where)
            continue
        ident = quantity['id']
        if ident in records:
            fail('duplicate_quantity_id', ident)
            continue
        records[ident] = quantity
        if quantity['evidence_id'] not in evidence_ids:
            fail('unknown_quantity_evidence', ident)
        key = (quantity['scope'], normalize_symbol(quantity['source_symbol']))
        if key in owners:
            fail('source_symbol_collision', ident)
        owners[key] = ident
    for ident, quantity in records.items():
        rows = quantity.get('aliases', [])
        if not isinstance(rows, list):
            fail('aliases_not_list', ident)
            continue
        for alias in rows:
            if not isinstance(alias, dict) or any(not isinstance(alias.get(k), str) or not alias[k].strip() for k in ['symbol', 'reason', 'definition', 'artifact_id', 'locator']):
                fail('alias_fields_required', ident)
                continue
            symbol = normalize_symbol(alias['symbol'])
            key = (quantity['scope'], symbol)
            if key in owners and owners[key] != ident:
                fail('alias_symbol_collision', ident + ':' + alias['symbol'])
            if (ident, symbol) in aliases:
                fail('duplicate_alias', ident + ':' + alias['symbol'])
            owners[key] = ident
            aliases[ident, symbol] = alias
    checked = []
    for i, usage in enumerate(usages):
        where = f'quantity_usages[{i}]'
        if not isinstance(usage, dict) or any(not isinstance(usage.get(k), str) or not usage[k].strip() for k in ['quantity_id', 'symbol', 'artifact_id', 'locator']):
            fail('usage_fields_required', where)
            continue
        ident = usage['quantity_id']
        if ident not in records:
            fail('unknown_quantity', where)
            continue
        quantity = records[ident]
        symbol = normalize_symbol(usage['symbol'])
        alias = aliases.get((ident, symbol))
        if symbol != normalize_symbol(quantity['source_symbol']) and alias is None:
            fail('undeclared_quantity_rename', where)
        if alias is not None:
            definition_text = artifacts.get(alias['artifact_id'], {}).get(alias['locator'])
            if not isinstance(definition_text, str) or alias['definition'] not in definition_text:
                fail('alias_definition_not_in_artifact', where)
            elif not contains_symbol(alias['definition'], alias['symbol']) or not contains_symbol(alias['definition'], quantity['source_symbol']):
                fail('alias_definition_missing_symbols', where)
        actual = artifacts.get(usage['artifact_id'], {}).get(usage['locator'])
        if not isinstance(actual, str):
            fail('quantity_artifact_missing', where)
        elif not contains_symbol(actual, usage['symbol']):
            fail('quantity_symbol_not_in_artifact', where)
        checked.append({**usage, 'actual_text': actual, 'source_symbol': quantity['source_symbol'], 'meaning': quantity['meaning'], 'unit': quantity['unit'], 'source_locator': quantity['source_locator']})
    return {'status': 'passed' if not errors else 'failed', 'passed': not errors, 'errors': errors,
            'checked_usages': checked, 'quantities': len(records), 'semantic_review_required': True,
            'coverage': 'declared identities and artifact locations only; omissions, source truth, dimensions and meaning require review'}
