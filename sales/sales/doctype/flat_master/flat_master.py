# -*- coding: utf-8 -*-
# Copyright (c) 2015, d and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FlatMaster(Document):
	pass

	

	

#Insert Same Item in to the Item master
@frappe.whitelist(allow_guest=True)
def saveItem(self,method):
	if self.flag1==0:
		im=frappe.get_doc({"doctype": "Item",
					"item_name":self.flat_no,
				"item_code":self.flat_no,
				"description":self.flat_no,
				"item_group":"All Item Groups",
				"default_warehouse":"Stores - ST",
    	}).insert()
    	self.flag1=1
    	frappe.msgprint("Save")
	
	#im.save()
	#im.submit()


