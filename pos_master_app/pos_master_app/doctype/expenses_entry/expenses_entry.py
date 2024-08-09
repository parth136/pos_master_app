# Copyright (c) 2024, Rajvi and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ExpensesEntry(Document):
	def autoname(self):
		self.name = self.franchise_doctype_id + "_" + self.franchise_code
	pass
