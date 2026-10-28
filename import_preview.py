#!/usr/bin/env python3
"""Target-independent import preview; deliberately contains no target network client."""
import argparse, csv, hashlib, json
from pathlib import Path
from validate import validate_directory

def prepare(data,output):
    data=Path(data);output=Path(output);result=validate_directory(data)
    if result['status']!='PASS':raise ValueError('Preflight refused: '+str(result['errors']))
    output.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((data/'manifest.json').read_text());relationships=json.loads((data/'relationships.json').read_text())
    objects=[];rollback=[]
    for p in sorted((data/'json').glob('*.jsonl')):
        rows=[json.loads(x) for x in p.read_text().splitlines()]
        objects.append({'object':p.stem,'source':str(p.relative_to(data)),'count':len(rows),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'external_id_field':'id','mapping_status':'TARGET_UNSELECTED','operation':'PROPOSED_MATCH_BY_STABLE_EXTERNAL_ID','relations':relationships.get(p.stem,{}),'phase':'create shells, resolve target IDs, then link; cycle-aware','preview_rows':rows[:3]})
        rollback.extend({'object':p.stem,'external_id':r['id'],'action':'NONE_DRY_RUN','target_id':None,'previous_snapshot':None,'delete_allowed':False} for r in rows)
    plan={'synthetic':True,'mode':'DRY_RUN_ONLY','target_configured':False,'execution_authorized':False,'network_calls':0,'dataset_id':manifest['dataset_id'],'objects':objects,'replay_policy':'Stable IDs and identical payload hashes identify a repeated plan. Actual target uniqueness/upsert behavior must be configured and tested separately.','rollback_policy':'No changes performed. A future importer must capture exact preimages and created target IDs; never delete pre-existing rows or infer rollback from source IDs.'}
    (output/'import-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    (output/'rollback-manifest.jsonl').write_text(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in rollback))
    (output/'preflight.json').write_text(json.dumps(result,indent=2)+'\n')
    (output/'README.md').write_text('# Synthetic import preview\n\nDRY RUN ONLY. No system selected and no live data changed. `import-plan.json` contains three sample rows per domain and canonical source checksums. `rollback-manifest.jsonl` records NONE_DRY_RUN for each stable external ID; it is not a deletion script. Imports require separately qualified field mapping, unique IDs, relation resolution, preimages, authority and target validation.\n')
    return {'status':'DRY_RUN_READY','objects':len(objects),'records':len(rollback),'network_calls':0,'live_import_attempted':False}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();print(json.dumps(prepare(a.data,a.output),indent=2))
