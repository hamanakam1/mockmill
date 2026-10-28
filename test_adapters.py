import copy,csv,json,tempfile,unittest
from pathlib import Path
from generate import build
from adapters.offline import ADAPTERS,build_adapter,export_adapter,money

class AdapterTests(unittest.TestCase):
 def setUp(self):
  cfg={'company_name':'Example','company_expansion':'Fictional fixture','scenario':'SYNTHETIC','anchor_date':'2026-10-28','history_start':'2024-10-29','seed':7,'customers':5,'leads':25,'talent':20,'staff':10,'future_meetings':4,'currency':'USD','synthetic':True}
  self.tables,_=build(cfg,{'shapes':[{'title':'Consultant','skills':['analysis'],'count':20}]})
 def test_all_five_are_offline_and_cover_only_declared_entities(self):
  self.assertEqual(len(ADAPTERS),5)
  for name in ADAPTERS:
   files,plan=build_adapter(name,self.tables)
   self.assertTrue(files);self.assertFalse(plan['execution_authorized']);self.assertFalse(plan['live_import_tested']);self.assertEqual(plan['network_calls'],0)
   self.assertTrue(all(r[plan['synthetic_marker_column']] is True for rows in files.values() for r in rows))
   self.assertIn('invoices',plan['unmapped_domains']);self.assertIn('talent',plan['unmapped_domains'])
 def test_salesforce_external_relationships_use_existing_canonical_accounts(self):
  files,plan=build_adapter('salesforce',self.tables);accounts={r['StoryFoundry_ID__c'] for r in files['Account.csv']}
  self.assertTrue(all(r['Account.StoryFoundry_ID__c'] in accounts for r in files['Contact.csv']))
  self.assertTrue(all('Id' not in r for rows in files.values() for r in rows))
 def test_hubspot_requires_pipeline_and_unique_deal_key(self):
  files,plan=build_adapter('hubspot',self.tables)
  self.assertEqual(files['deals.csv'][0]['Pipeline'],'CONFIGURE_EXISTING_PIPELINE')
  self.assertTrue(all(r['Email'].endswith('.example.invalid') for r in files['contacts.csv']))
  self.assertTrue(all('Record ID' not in r for rows in files.values() for r in rows))
  self.assertIn('Deal name is not a unique key',plan['replay'])
 def test_stage_mapping_is_explicit_not_guessed_native_validation(self):
  files,plan=build_adapter('hubspot',self.tables,{'pipeline':'test_pipeline','stage_map':{'closed_won':'configured_won'}})
  self.assertEqual(files['deals.csv'][0]['Deal stage'],'configured_won');self.assertFalse(plan['live_import_tested'])
 def test_dynamics_lookup_rows_resolve_to_unique_synthetic_name(self):
  files,plan=build_adapter('dynamics365',self.tables);names={r['name'] for r in files['accounts.csv']}
  self.assertTrue(all(r['parentcustomerid'] in names for r in files['contacts.csv']))
 def test_zoho_does_not_claim_csv_external_id_upsert(self):
  files,plan=build_adapter('zoho_crm',self.tables)
  self.assertTrue(all(r['Last Name'] for r in files['Contacts.csv']))
  self.assertIn('does not claim generic external-ID CSV upsert',plan['replay'])
 def test_pipedrive_joins_deal_contact_and_org_without_fabricated_system_ids(self):
  files,plan=build_adapter('pipedrive',self.tables);rows=files['people-organizations-deals.csv']
  self.assertEqual(sum(bool(r['Deal title']) for r in rows),len(self.tables['opportunities']))
  self.assertEqual(len({r['Person StoryFoundry key'] for r in rows}),len(self.tables['contacts']))
  self.assertFalse(any('system id' in k.lower() for r in rows for k in r))
  self.assertIn('actual Pipedrive System IDs',plan['replay'])
 def test_relationship_corruption_fails_before_export(self):
  self.tables['contacts'][0]['account_id']='missing'
  with self.assertRaises(ValueError):build_adapter('salesforce',self.tables)
 def test_decimal_transform_has_no_float_rounding(self):
  self.assertEqual(money(100000000000001),'1000000000000.01')
  with self.assertRaises(ValueError):money(1.5)
 def test_replay_files_and_plan_are_identical(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)
   for name in ADAPTERS:
    a=export_adapter(name,self.tables,out/name);before={p.name:p.read_bytes() for p in (out/name).iterdir()}
    b=export_adapter(name,self.tables,out/name);after={p.name:p.read_bytes() for p in (out/name).iterdir()}
    self.assertEqual(a['plan_sha256'],b['plan_sha256']);self.assertEqual(before,after)
if __name__=='__main__':unittest.main()
