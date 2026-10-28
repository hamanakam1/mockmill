#!/usr/bin/env python3
"""Export reviewed offline adapter fixtures; no live import mode exists."""
import argparse,json
from pathlib import Path
from adapters import ADAPTERS,export_adapter
from validate import validate_directory

def main():
 p=argparse.ArgumentParser();p.add_argument('--data',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--adapter',choices=['all',*ADAPTERS],default='all');p.add_argument('--options',type=Path);p.add_argument('--profiles',type=Path);a=p.parse_args()
 check=validate_directory(a.data,a.profiles)
 if check['status']!='PASS':raise SystemExit('Canonical preflight failed: '+str(check['errors']))
 tables={f.stem:[json.loads(x) for x in f.read_text().splitlines()] for f in sorted((a.data/'json').glob('*.jsonl'))}
 options=json.loads(a.options.read_text()) if a.options else {}
 for name in ADAPTERS if a.adapter=='all' else [a.adapter]:
  plan=export_adapter(name,tables,a.output/name,options.get(name,{}));print(name,plan['status'],plan['plan_sha256'])
if __name__=='__main__':main()
