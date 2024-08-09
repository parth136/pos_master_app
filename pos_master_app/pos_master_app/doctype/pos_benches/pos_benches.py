# Copyright (c) 2024, Rajvi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class POSBenches(Document):
	def validate(self):
		for franchise in self.franchise_details:
			franchise.franchise_naming_series = franchise.name

	def before_save(self):
		all_franchise = frappe.get_all("POS Franchise", filters={'parent':self.name},fields=['status','name'])
		all_franchise_dict =  {franchise['name']: franchise['status'] for franchise in all_franchise}
		new_franchise_dict =  {franchise.name: franchise.status for franchise in self.franchise_details}
		new_franchise_list = list(new_franchise_dict.keys())
		for franchise,status in all_franchise_dict.items():
			if  franchise not in new_franchise_list or new_franchise_dict[franchise] != status:
				frappe.enqueue('pos_master_app.pos_master_app.api.api.delete_records_by_franchise_code',franchise_code=franchise, queue='short',timeout=1000)

	def on_trash(self):
		all_franchise = frappe.get_all("POS Franchise", filters={'parent':self.name},fields=['name'])
		for franchise in all_franchise:
			frappe.enqueue('pos_master_app.pos_master_app.api.api.delete_records_by_franchise_code',franchise_code=franchise['name'], queue='short',timeout=1000)							 



