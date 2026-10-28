"""Deterministic CSV/JSON starter adapters. Target import behavior is not exercised.

Caller-supplied stages/pipelines are configuration assertions, not live validation.
Source external IDs are NEVER emitted as vendor-native record IDs.
"""
from __future__ import annotations
import csv, hashlib, json
from decimal import Decimal
from pathlib import Path
from generate import csv_value

ADAPTERS={
 'salesforce':{'mechanism':'Data Loader CSV per object; configured custom external-ID matching and relationship mapping','sources':['https://help.salesforce.com/s/articleView?id=000313396&language=en_US&type=1','https://help.salesforce.com/s/articleView?id=sf.for_accounts_and_contacts.htm&language=en_US&type=5'],'required_configuration':['Create and verify unique External ID Text field MockMill_ID__c on Account, Contact and Opportunity before upsert','Confirm Account.MockMill_ID__c relationship mapping for the selected loader mode','Verify StageName values, permissions, duplicate rules and validation rules','Accounts before child rows; do not substitute source IDs for Salesforce IDs'],'replay':'Conditional upsert only after custom external-ID uniqueness and loader behavior are qualified. Repeated insert is not idempotent.'},
 'hubspot':{'mechanism':'UI CSV import with explicitly mapped object properties and multi-object associations','sources':['https://knowledge.hubspot.com/import-and-export/set-up-your-import-file','https://knowledge.hubspot.com/import-and-export/import-objects'],'required_configuration':['Map Email for contact uniqueness and Company domain name for company matching','Create a permitted unique-value property for MockMill source key on deals or obtain actual target Record IDs','Select existing Pipeline and Deal stage internal values; fixture labels are not target validation','Configure company-domain association mapping in the selected import workflow; check edition/property eligibility','Blank imported cells do not mean clear existing values'],'replay':'Email/domain matching is scoped to configured objects; repeated deals require actual Record ID or supported custom unique property. Deal name is not a unique key.'},
 'dynamics365':{'mechanism':'Power Apps model-driven application CSV import wizard with mapped Dataverse fields','sources':['https://learn.microsoft.com/en-us/power-apps/user/import-data','https://learn.microsoft.com/en-us/power-apps/developer/data-platform/use-alternate-key-reference-record'],'required_configuration':['Define and select an active alternate key for sf_sourcekey on each chosen table','Map account/contact/opportunity logical field names through the import wizard','Resolve parentcustomerid/customerid lookup references to exactly one target account','Validate target required columns, currency, ownership and security roles'],'replay':'Updates require the configured selected alternate key or actual target identity; synthetic source keys alone do not establish target uniqueness.'},
 'zoho_crm':{'mechanism':'CRM module CSV import with module-specific field mapping; Accounts before Contacts/Deals','sources':['https://help.zoho.com/portal/en/kb/crm/data-administration/import-data/articles/import-data'],'required_configuration':['Map Account Name; Contact Last Name; Deal Name, Closing Date and all target-layout-required fields','Import Accounts first and resolve Account Name or a real target account ID','Map MockMill source key to ordinary provenance text; it is not a claim that CSV updates external-ID fields','Select the actual permitted unique-field/module-ID duplicate/update mode and test it before replay','Validate stage, owner, layout and edition restrictions'],'replay':'CSV replay depends on target-supported unique-field/module-ID matching. Zoho external-ID fields have API-specific update behavior; this package does not claim generic external-ID CSV upsert.'},
 'pipedrive':{'mechanism':'Pipedrive spreadsheet import with manually mapped person, organization and deal columns','sources':['https://support.pipedrive.com/en/article/importing-data-into-pipedrive-with-spreadsheets','https://support.pipedrive.com/en/article/updating-pipedrive-data-with-a-spreadsheet'],'required_configuration':['Map Person name and Organization name plus Deal title/value/currency/stage for deal rows','Map the three MockMill provenance keys to separately configured custom text fields or retain the sidecar','Choose existing pipeline/stage values; verify duplicate detection and item linking','For updates obtain genuine Pipedrive System IDs from the target; never use synthetic IDs as System IDs'],'replay':'Initial fixtures are create-oriented. Updates require actual Pipedrive System IDs; repeated upload is not declared idempotent.'},
}

def money(cents):
    if type(cents) is not int or cents<0:raise ValueError('Nonnegative integer cents required')
    return format(Decimal(cents)/Decimal(100),'.2f')
def canonical_index(tables):return {d:{r['id']:r for r in rows} for d,rows in tables.items()}
def default_stage(stage):return {'closed_won':'Closed Won','closed_lost':'Closed Lost','qualified':'Qualification','nurturing':'Nurturing','contacted':'Contacted','new':'Prospecting'}.get(stage,'Prospecting')
def build_adapter(name,tables,options=None):
    if name not in ADAPTERS:raise ValueError('Unknown adapter')
    options=options or {};idx=canonical_index(tables);files={};relations=[];mappings=[]
    stages=options.get('stage_map',{})
    def stage(row):return stages.get(row['stage'],default_stage(row['stage']))
    def relation(child_domain,child,parent_domain,parent,field):
        if child not in idx.get(child_domain,{}) or parent not in idx.get(parent_domain,{}):raise ValueError('Unresolved canonical relationship')
        relations.append({'child_domain':child_domain,'child_external_id':child,'parent_domain':parent_domain,'parent_external_id':parent,'target_lookup_field':field,'target_parent_id':None,'resolution_status':'REQUIRES_TARGET_IMPORT_MAPPING'})
    def mapped(file,domain,rows,keys):
        files[file]=rows;mappings.append({'file':file,'canonical_domain':domain,'row_count':len(rows),'external_key_columns':keys})
    if name=='salesforce':
        mapped('Account.csv','accounts',[{'Name':a['name'],'Website':a['website'],'Industry':a.get('industry',''),'Phone':a.get('phone',''),'NumberOfEmployees':a.get('employee_count',''),'AnnualRevenue':money(a['annual_revenue_cents']) if 'annual_revenue_cents' in a else '','Description':'SYNTHETIC FICTION; '+a['account_type'],'MockMill_ID__c':a['id']} for a in tables['accounts']],['MockMill_ID__c'])
        mapped('Contact.csv','contacts',[{'FirstName':c['first_name'],'LastName':c['last_name'],'Title':c['title'],'Department':c.get('department',''),'Email':c['email'],'Account.MockMill_ID__c':c['account_id'],'Description':'SYNTHETIC FICTION','MockMill_ID__c':c['id']} for c in tables['contacts']],['MockMill_ID__c'])
        mapped('Opportunity.csv','opportunities',[{'Name':o['name'],'Amount':money(o['amount_cents']),'StageName':stage(o),'CloseDate':o['closed_on'] or o['expected_close_on'],'Probability':o.get('probability_percent',''),'ForecastCategoryName':o.get('forecast_category',''),'Type':o.get('opportunity_type',''),'NextStep':o.get('next_step',''),'Account.MockMill_ID__c':o['account_id'],'Description':'SYNTHETIC FICTION','MockMill_ID__c':o['id']} for o in tables['opportunities']],['MockMill_ID__c'])
        for c in tables['contacts']:relation('contacts',c['id'],'accounts',c['account_id'],'Account.MockMill_ID__c')
        for o in tables['opportunities']:relation('opportunities',o['id'],'accounts',o['account_id'],'Account.MockMill_ID__c')
    elif name=='hubspot':
        domain=lambda account:idx['accounts'][account]['website'].split('://',1)[1]
        mapped('companies.csv','accounts',[{'Name':a['name'],'Company domain name':domain(a['id']),'Industry':a.get('industry',''),'Phone number':a.get('phone',''),'Number of employees':a.get('employee_count',''),'Annual revenue':money(a['annual_revenue_cents']) if 'annual_revenue_cents' in a else '','Description':'SYNTHETIC FICTION','MockMill source key':a['id']} for a in tables['accounts']],['Company domain name','MockMill source key'])
        mapped('contacts.csv','contacts',[{'First name':c['first_name'],'Last name':c['last_name'],'Job title':c['title'],'Department':c.get('department',''),'Email':c['email'],'Company domain name':domain(c['account_id']),'Preferred language':'en','MockMill source key':c['id']} for c in tables['contacts']],['Email','MockMill source key'])
        mapped('deals.csv','opportunities',[{'Deal name':o['name'],'Pipeline':options.get('pipeline','CONFIGURE_EXISTING_PIPELINE'),'Deal stage':stage(o),'Amount':money(o['amount_cents']),'Close date':o['closed_on'] or o['expected_close_on'],'Forecast category':o.get('forecast_category',''),'Next step':o.get('next_step',''),'Company domain name':domain(o['account_id']),'MockMill source key':o['id']} for o in tables['opportunities']],['MockMill source key'])
        for c in tables['contacts']:relation('contacts',c['id'],'accounts',c['account_id'],'Company domain name association')
        for o in tables['opportunities']:relation('opportunities',o['id'],'accounts',o['account_id'],'Company domain name association')
    elif name=='dynamics365':
        mapped('accounts.csv','accounts',[{'name':a['name'],'websiteurl':a['website'],'industrycode':a.get('industry',''),'numberofemployees':a.get('employee_count',''),'revenue':money(a['annual_revenue_cents']) if 'annual_revenue_cents' in a else '','description':'SYNTHETIC FICTION','sf_sourcekey':a['id']} for a in tables['accounts']],['sf_sourcekey'])
        mapped('contacts.csv','contacts',[{'firstname':c['first_name'],'lastname':c['last_name'],'jobtitle':c['title'],'department':c.get('department',''),'emailaddress1':c['email'],'parentcustomerid':idx['accounts'][c['account_id']]['name'],'description':'SYNTHETIC FICTION','sf_sourcekey':c['id']} for c in tables['contacts']],['sf_sourcekey'])
        mapped('opportunities.csv','opportunities',[{'name':o['name'],'estimatedvalue':money(o['amount_cents']),'estimatedclosedate':o['closed_on'] or o['expected_close_on'],'salesstagecode':o['stage'],'closeprobability':o.get('probability_percent',''),'customerid':idx['accounts'][o['account_id']]['name'],'description':'SYNTHETIC FICTION; scenario stage '+o['stage'],'sf_sourcekey':o['id']} for o in tables['opportunities']],['sf_sourcekey'])
        for c in tables['contacts']:relation('contacts',c['id'],'accounts',c['account_id'],'parentcustomerid')
        for o in tables['opportunities']:relation('opportunities',o['id'],'accounts',o['account_id'],'customerid')
    elif name=='zoho_crm':
        mapped('Accounts.csv','accounts',[{'Account Name':a['name'],'Website':a['website'],'Industry':a.get('industry',''),'Employees':a.get('employee_count',''),'Annual Revenue':money(a['annual_revenue_cents']) if 'annual_revenue_cents' in a else '','Description':'SYNTHETIC FICTION','MockMill source key':a['id']} for a in tables['accounts']],['MockMill source key'])
        mapped('Contacts.csv','contacts',[{'First Name':c['first_name'],'Last Name':c['last_name'],'Title':c['title'],'Department':c.get('department',''),'Email':c['email'],'Account Name':idx['accounts'][c['account_id']]['name'],'Description':'SYNTHETIC FICTION','MockMill source key':c['id']} for c in tables['contacts']],['MockMill source key'])
        mapped('Deals.csv','opportunities',[{'Deal Name':o['name'],'Amount':money(o['amount_cents']),'Closing Date':o['closed_on'] or o['expected_close_on'],'Stage':stage(o),'Probability':o.get('probability_percent',''),'Type':o.get('opportunity_type',''),'Account Name':idx['accounts'][o['account_id']]['name'],'Description':'SYNTHETIC FICTION','MockMill source key':o['id']} for o in tables['opportunities']],['MockMill source key'])
        for c in tables['contacts']:relation('contacts',c['id'],'accounts',c['account_id'],'Account Name')
        for o in tables['opportunities']:relation('opportunities',o['id'],'accounts',o['account_id'],'Account Name')
    else:
        rows=[];used_contacts=set()
        for o in tables['opportunities']:
            lead=idx['leads'][o['lead_id']];c=idx['contacts'][lead['contact_id']];a=idx['accounts'][o['account_id']];used_contacts.add(c['id'])
            rows.append({'Organization name':a['name'],'Organization industry':a.get('industry',''),'Person name':c['display_name'],'Person title':c['title'],'Person email':c['email'],'Deal title':o['name'],'Deal value':money(o['amount_cents']),'Deal currency':o['currency'],'Deal stage':stage(o),'Deal probability':o.get('probability_percent',''),'Organization MockMill key':a['id'],'Person MockMill key':c['id'],'Deal MockMill key':o['id']})
            relation('opportunities',o['id'],'accounts',a['id'],'Organization name linked row');relation('opportunities',o['id'],'contacts',c['id'],'Person name/email linked row')
        for c in tables['contacts']:
            if c['id'] in used_contacts:continue
            a=idx['accounts'][c['account_id']]
            rows.append({'Organization name':a['name'],'Organization industry':a.get('industry',''),'Person name':c['display_name'],'Person title':c['title'],'Person email':c['email'],'Deal title':'','Deal value':'','Deal currency':'','Deal stage':'','Deal probability':'','Organization MockMill key':a['id'],'Person MockMill key':c['id'],'Deal MockMill key':''})
        mapped('people-organizations-deals.csv','accounts+contacts+opportunities',rows,['Organization MockMill key','Person MockMill key','Deal MockMill key'])
        for c in tables['contacts']:relation('contacts',c['id'],'accounts',c['account_id'],'Organization name linked row')
    marker={'salesforce':'MockMill_Synthetic__c','hubspot':'MockMill synthetic','dynamics365':'sf_synthetic','zoho_crm':'MockMill Synthetic','pipedrive':'MockMill synthetic'}[name]
    for rows in files.values():
        for row in rows:row[marker]=True
    specification={**ADAPTERS[name],'adapter':name,'contract_version':'0.1.0','documentation_retrieved_on':'2026-10-28','synthetic':True,'status':'OFFLINE_FIXTURE_TARGET_CONFIGURATION_REQUIRED','mode':'DRY_RUN_ONLY','live_import_tested':False,'execution_authorized':False,'network_calls':0,'native_record_ids_fabricated':False,'canonical_domains_mapped':['accounts','contacts','opportunities'],'unmapped_domains':sorted(set(tables)-{'accounts','contacts','opportunities'}),'coverage_limit':'Three CRM entity families only. All other canonical domains remain portable JSON/CSV; no native import coverage is implied. Lead acquisition and customer lineage remain in canonical sidecars. Dynamics opportunity closure is descriptive only; no state transition is executed.','files':mappings,'relationships':relations,'options':options,'unknown_target_configuration_is_a_hold':True,'rollback':'No target changes made. Capture target IDs and preimages before any future approved import; never delete by a synthetic source ID.'}
    specification['required_configuration']=[*specification['required_configuration'],f'Map explicit synthetic marker {marker} to a configured compatible custom property; keep the file synthetic if a target lacks that property']
    specification['synthetic_marker_column']=marker
    return files,specification

def export_adapter(name,tables,output,options=None):
    files,spec=build_adapter(name,tables,options);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    for filename,rows in files.items():
        with (output/filename).open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows({k:csv_value(v) for k,v in row.items()} for row in rows)
        (output/(filename+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
    spec['payload_manifest']=[{'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(output.iterdir()) if p.is_file() and p.name.endswith(('.csv','.csv.json'))]
    canonical=json.dumps(spec,sort_keys=True,separators=(',',':')).encode();spec['plan_sha256']=hashlib.sha256(canonical).hexdigest()
    (output/'import-plan.json').write_text(json.dumps(spec,indent=2)+'\n')
    return spec
