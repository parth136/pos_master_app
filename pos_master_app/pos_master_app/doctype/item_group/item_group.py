# Copyright (c) 2024, Rajvi and contributors
# For license information, please see license.txt

# import frappe
from frappe.utils.nestedset import NestedSet


class ItemGroup(NestedSet):
	def autoname(self):
		self.name = self.franchise_doctype_id + "_" + self.franchise_code
	pass
