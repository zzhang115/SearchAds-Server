"""Deterministic JSONL ad normalization; standard library only."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile


def normalize(record):
    """Return a new record without inventing prices, IDs or missing values."""
    if not isinstance(record, dict):
        raise ValueError('record must be an object')
    for field in ('title', 'query', 'brand'):
        if not isinstance(record.get(field), str):
            raise ValueError(field + ' must be a string')
    keywords = record.get('keyWords', [])
    if not isinstance(keywords, list) or any(not isinstance(k, str) for k in keywords):
        raise ValueError('keyWords must be a list of strings')
    result = dict(record)
    title = re.sub(r"[,\-\.\"']", '', record['title'])
    result['title'] = ' '.join(title.lower().split())
    result['query'] = record['query'].strip().lower()
    result['brand'] = record['brand'].replace("'", '')
    result['keyWords'] = list(dict.fromkeys(keywords + result['title'].split()))
    return result


def reject_constant(value):
    raise ValueError('non-finite JSON number: ' + value)


def convert(source, destination):
    """Write validated JSONL atomically; never overwrite an existing output."""
    if destination.exists():
        raise ValueError('output already exists; choose a new path')
    temporary = None
    count = 0
    try:
        with source.open(encoding='utf-8') as reader, tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', dir=destination.parent, delete=False
        ) as writer:
            temporary = Path(writer.name)
            for line_number, line in enumerate(reader, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line, parse_constant=reject_constant)
                    output = normalize(record)
                    writer.write(json.dumps(output, ensure_ascii=False, allow_nan=False) + '\n')
                except (ValueError, TypeError) as exc:
                    raise ValueError('invalid record at line ' + str(line_number)) from exc
                count += 1
            writer.flush()
            os.fsync(writer.fileno())
        os.link(temporary, destination)
        return count
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path, help='New JSONL output path')
    args = parser.parse_args()
    try:
        count = convert(args.input, args.output)
    except (OSError, ValueError, UnicodeError) as exc:
        print('Conversion failed: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps({'records_written': count, 'output': str(args.output)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
