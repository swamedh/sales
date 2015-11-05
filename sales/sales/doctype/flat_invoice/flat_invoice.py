# -*- coding: utf-8 -*-
# Copyright (c) 2015, d and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
import logging
import string
import datetime
import re
import json

from frappe.utils import getdate, flt,validate_email_add, cint
from frappe.model.naming import make_autoname
from frappe import throw, _, msgprint
import frappe.permissions
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe import throw, _, msgprint
import sys,os
import MySQLdb



class FlatInvoice(Document):

	
		
	
	def charges_method(self):
		from frappe.model import default_fields	
		doc_req = []
		charges_table=[]
		#<<<<<<< HEAD
#=======
#>>>>>>> d1c12b8ead7aa6bf31699eff964584c774e6ae17
		if self.charges and not charges_table:
			doc_master = frappe.get_doc("Sales Taxes and Charges Template", self.charges)
			val=0
			for value in doc_master.get("taxes"):
				if value.charge_type=="Actual":
					val=val+value.tax_amount
					doc_req = {
						"doctype": "Sales Taxes and Charges",
						"charge_type":value.charge_type,
						"description": value.description,
						"tax_amount":value.tax_amount,
						}
				elif value.charge_type=="On Net Total":
					val=val+(self.net_total * (value.rate/100))
					doc_req = {
						"doctype": "Sales Taxes and Charges",
						"charge_type":value.charge_type,
						"description": value.description,
						"rate": value.rate,
						"tax_amount":self.total_a * (value.rate/100),
						}
					self.other_charges_total=val
					#for fieldname in doc_req:
					#	frappe.msgprint(fieldname)
						#if fieldname in charges_table:
							#frappe.msgprint(doc_req)
				self.append("charges_table", doc_req)
			self.other_charges_total=val
			self.total_a=self.total_a+self.other_charges_total
			#self.flag1=1
						

	def discounts_method(self):
		#frappe.msgprint(self.charges_table)
		#frappe.msgprint(self.discounts)
		doc_req = []
		val1=0
		#if not self.discounts_table:
		if self.discounts and not len(self.get("discounts_table")):
			doc_master = frappe.get_doc("Sales Taxes and Charges Template", self.discounts)
			#frappe.msgprint("From Python discounts_method")
			for value in doc_master.get("taxes"):
				#if "discount" or "Discount" in value.description:
				#frappe.msgprint(value.description)
				if value.charge_type=="Actual":
					val1=val1+value.tax_amount
					doc_req = {
						"doctype": "Sales Taxes and Charges",
						"charge_type":value.charge_type,
						"description": value.description,
						"tax_amount":value.tax_amount,
						}
				elif value.charge_type=="On Net Total":
					val1=val1+(self.total_a * (value.rate/100))
					doc_req = {
						"doctype": "Sales Taxes and Charges",
						"charge_type":value.charge_type,
						"description": value.description,
						"rate": value.rate,
						"tax_amount":self.total_a * (value.rate/100),
						}	
					
				self.append("discounts_table", doc_req)
			self.discounts_total=val1
			self.total_b=self.total_a-self.discounts_total			
			self.flag2=1;

	
	
	def taxes_method(self):
		#frappe.msgprint(self.charges_table)
		#frappe.msgprint(self.charges)
		doc_req = []
		val2=0
		if self.taxes and not len(self.get("taxes_table")):
			doc_master = frappe.get_doc("Sales Taxes and Charges Template", self.taxes)
			#frappe.msgprint("From Python taxes_method")
			for value in doc_master.get("taxes"):
				if value.charge_type=="Actual":
					val2=val2+value.tax_amount
					doc_req = {
						"doctype": "Sales Taxes and Charges",
						"charge_type":value.charge_type,
						"description": value.description,
						"tax_amount":value.tax_amount,
						}
					self.append("taxes_table", doc_req)
				elif value.charge_type=="On Net Total":
					val2=val2+(self.total_b * (value.rate/100))
					doc_req = {
						"doctype": "Sales Taxes and Charges",
						"charge_type":value.charge_type,
						"description": value.description,
						"rate": value.rate,
						"tax_amount":self.total_b * (value.rate/100),
						}
					self.append("taxes_table", doc_req)
			self.taxes_total=val2
			self.total_c=self.total_b+self.taxes_total
			
			
			
			
	def flatInfo(self):
		#flatCheck=frappe.db.sql("""select isBooked from `tabFlat Master` where flat_no='%s'"""%(self.flat_no))
		flatMaster=frappe.get_doc("Flat Master",self.flat_no)
		if flatMaster.isbooked==1:
			frappe.msgprint("Flat Already Sold Out")
			
			
			
			
			

@frappe.whitelist(allow_guest=True)			
def validateDoc(self,method):
	flag1=0
	if self.invoice_flat_no is None:
		frappe.msgprint("Select Flat")
		flag1=1
	if self.invoice_flat_no:
		flatMaster=frappe.get_doc("Flat Master",self.flat_no)
		if flatMaster.isbooked==1:
			frappe.msgprint("Flat Already Sold Out")
			flag1=1
	if self.customer_name_link is None:
		frappe.msgprint("Select Customer")
		flag1=1
	if self.booking_date is None:
		frappe.msgprint("Enter Booking Date")
		flag1=1

	return flag1
	

	

@frappe.whitelist(allow_guest=True)			
def insertData(self,method):
	flatMaster=frappe.get_doc("Flat Master",self.flat_no)
	if flatMaster.isbooked==0 and self.flag1==0:
		#frappe.msgprint("Start")
		si=frappe.get_doc({"doctype": "Sales Invoice",
					"items": [{	"item_name": self.flat_no,"item_code": self.flat_no,"description": self.flat_no,"qty": 1,"rate": self.rounded_total,
					"amount": self.rounded_total,
					"income_account": "Administrative Expenses - ST",}],
					"customer":self.customer_name_link,
					"customer_name":self.customer_name_link,
					"posting_date":self.booking_date,
					"due_date":self.booking_date,
					"debit_to":"Deepak - ST",
					"total":self.rounded_total,
					"net_total": self.rounded_total,
					"grand_total": self.rounded_total,
					"territory":"India",
					"base_grand_total":self.rounded_total,
					"grand_total":self.rounded_total,
					"rounded_total":self.rounded_total,
					"grand_total_export":self.rounded_total,
					"outstanding_amount":self.rounded_total,	
					}).insert()
		self.flag1=1
    		#si.submit()
  		#frappe.msgprint("insert")

'''@frappe.whitelist(allow_guest=True)			
def insertData(self,method):
	val=0.00
	flatMaster=frappe.get_doc("Flat Master",self.flat_no)
	if flatMaster.isbooked==0 and self.flag1==0:
		#frappe.msgprint("Start")
		si=frappe.get_doc({"doctype": "Sales Invoice",
					"items": [{	"item_name": self.flat_no,"item_code": self.flat_no,"description": self.flat_no,"qty": 1,"rate": self.net_total,
					"amount": self.net_total,
					"income_account": "Administrative Expenses - ST",}],
					"customer":self.customer_name_link,
					"customer_name":self.customer_name_link,
					"posting_date":self.booking_date,
					"due_date":self.booking_date,
					"debit_to":"Deepak - ST",
					"total":self.rounded_total,
					"net_total": self.rounded_total,
					"grand_total": self.rounded_total,
					"territory":"India",
					"base_grand_total":self.rounded_total,
					"grand_total":self.rounded_total,
					"rounded_total":self.rounded_total,
					"grand_total_export":self.rounded_total,
					"outstanding_amount":self.rounded_total,	
					}).insert()
		taxes_and_charges=[]
		for tax in self.get("charges_table"):
			tax = tax.as_dict()
			frappe.msgprint(tax)
			taxes_and_charges.append(tax)
			name=self.name
			name=name.replace(name[0],"S")
			doc_m=frappe.get_doc("Sales Invoice",name)
			doc_m.set("taxes",taxes_and_charges);
			
'''



@frappe.whitelist(allow_guest=True)
def submitDoc(self,method):
	name=self.name
	name=name.replace(name[0],"S")
	#frappe.msgprint(name)
	doc_m=frappe.get_doc("Sales Invoice",name)
	doc_m.submit()
	#frappe.msgprint("Submitted")

@frappe.whitelist(allow_guest=True)
def cancelDoc(self,method):
	name=self.name
	name=name.replace(name[0],"S")
	frappe.msgprint(name)
	doc_m=frappe.get_doc("Sales Invoice",name)
	doc_m.cancel()
	self.flag1=2
	#doc_m.amend_doc()
	#frappe.msgprint("cancel and amend")


@frappe.whitelist(allow_guest=True)
def amendDoc(self,method):
	'''name1=""
	name=self.name
	name=name.replace(name[0],"S")
	for i in range(0,len(name)-2):
		name1+=name[i]
	frappe.msgprint(name1)
	doc_m=frappe.get_doc("Sales Invoice",name1)
	#doc_n=frappe.get_doc("Sales Invoice",sel)
	#doc_m.amend_from=doc_n.name
	#doc_m.save()
	frappe.msgprint("amend")
	#self.flag1=1'''
	'''val=0.00
	doc_master = frappe.get_doc("Flat Invoice", self.name)
	for value in doc_master.get("charges_table"):
		if value.charge_type=="Actual":
			val=val+value.tax_amount
			doc_req = {
				"doctype": "Sales Taxes and Charges",
				"charge_type":value.charge_type,
				"description": value.description,
				"tax_amount":value.tax_amount,
				"account_head":value.account_head
				}
			self.append("discounts_table",doc_req)
		'''
	taxes_and_charges=[]
	for tax in doc_master.get("charges_table"):
		tax = tax.as_dict()
		taxes_and_charges.append(tax)

	name=self.name
	name=name.replace(name[0],"S")
	doc_m=frappe.get_doc("Sales Invoice",name)
	doc_m.set("taxes",taxes_and_charges);




@frappe.whitelist(allow_guest=True)			
def updateDoc(self,method):
	name=self.name
	name=name.replace(name[0],"S")
	frappe.db.sql("""update `tabSales Invoice Item` set item_name='%s',item_code='%s',description='%s',rate='%s',amount='%s' where parent='%s'"""
		%(self.flat_no,self.flat_no,self.flat_no,self.rounded_total,self.rounded_total,name))		
	doc_m=frappe.get_doc("Sales Invoice",name)
	doc_m.set("due_date",self.booking_date);
	doc_m.set("customer",self.customer_name_link);
	doc_m.set("customer_name",self.customer_name_link);
	doc_m.set("posting_date",self.booking_date);
	doc_m.set("debit_to","Deepak - ST");
	doc_m.set("total",self.rounded_total);
	doc_m.set("net_total",self.rounded_total);
	doc_m.set("grand_total",self.rounded_total);
	doc_m.set("territory","India");
	doc_m.set("base_grand_total",self.rounded_total);
	doc_m.set("grand_total",self.rounded_total);
	doc_m.set("rounded_total",self.rounded_total);
	doc_m.set("grand_total_export",self.rounded_total);
	doc_m.set("outstanding_amount",self.rounded_total);
	doc_m.save()
	#frappe.msgprint("Update")




@frappe.whitelist(allow_guest=True)			
def beforeInsertDoc(self,method):
	#self.flag1=1
	if self.flag1==1:
		updateDoc(self,method)
	#	amendDoc(self,method)
	#if self.flag1==2:
	#	amendDoc(self,method)
	#if self.flag1==0:
	if validateDoc(self,method)==0 and self.flag1==0:
		insertData(self,method)
	
	
	
	
	