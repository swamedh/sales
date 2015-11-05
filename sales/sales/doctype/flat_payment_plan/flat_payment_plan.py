# -*- coding: utf-8 -*-
# Copyright (c) 2015, d and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
#from erpnext.accounts.doctype.sales_invoice import sales_invoice

class FlatPaymentPlan(Document):
	def payment_schedule_method(self):
		#doc_req = []
		#payment_schedule_table=[]
		val2=0
		if self.payment_scheme:
			#doc_req=[]
			#dict1=self.get("payment_schedule_table")

			name=self.flat_invoice
			name=name.replace(name[0],"S")
			doc_jv= frappe.get_doc("Sales Invoice", name)
			tot=(doc_jv.grand_total) - (doc_jv.outstanding_amount)
			frappe.msgprint("From Python")
			if doc_jv.grand_total == doc_jv.outstanding_amount:
				frappe.msgprint("No Payment")
			ps=self.payment_scheme
			p=""
			for i in ps:
				if i.isdigit():
					p+=i
			self.down_payment=self.total_sales_consideration * eval(p)/100 
			self.balance_amount=self.total_sales_consideration - self.down_payment
			doc_master = frappe.get_doc("Payment Schedule Template", self.payment_scheme)
			for value in doc_master.get("payment_schedule"):
				if value.charge_type=="Actual":
					val2= (value.paid_amount + value.sales_tax_amount + value.service_tax_amount)
					doc_req = {
						"doctype": "Payment Schedule",
						"charge_type":value.charge_type,
						"description": value.description,
						"rate": value.rate,
						"paid_amount":value.paid_amount,
						"sales_tax_rate":value.sales_tax_rate,
						"service_tax_rate":value.service_tax_rate,
						"sales_tax_amount":value.sales_tax_amount,
						"service_tax_amount":value.service_tax_amount,
						"total": val2,

						}
					self.append("taxes_table", doc_req)
				elif value.charge_type=="On Net Total":
					val2=((self.balance_amount * (value.service_tax_rate/100)) + (self.balance_amount * (value.sales_tax_rate/100)) + (self.balance_amount * (value.rate/100)))
					t=val2
					bal=recv=0.00
					rm=tot
					if tot >= val2:
						rm= rm - t
						tot=rm
						bal=0.00
						doc_req = {
							"doctype": "Payment Schedule",
							"charge_type":value.charge_type,
							"description": value.description,
							"rate": value.rate,
							"paid_amount":self.balance_amount * (value.rate/100),
							"sales_tax_rate":value.sales_tax_rate,
							"service_tax_rate":value.service_tax_rate,
							"sales_tax_amount":self.balance_amount * (value.sales_tax_rate/100),
							"service_tax_amount":self.balance_amount * (value.service_tax_rate/100),
							"total": val2,
							"received_amount" : t,
							"balance" : bal
						}
					elif tot <=val2 :
						bal= t - rm
						tot=0.00
						doc_req = {
							"doctype": "Payment Schedule",
							"charge_type":value.charge_type,
							"description": value.description,
							"rate": value.rate,
							"paid_amount":self.balance_amount * (value.rate/100),
							"sales_tax_rate":value.sales_tax_rate,
							"service_tax_rate":value.service_tax_rate,
							"sales_tax_amount":self.balance_amount * (value.sales_tax_rate/100),
							"service_tax_amount":self.balance_amount * (value.service_tax_rate/100),
							"total": val2,
							"received_amount" : rm,
							"balance" : bal
							}
					elif tot ==0.00 :
						frappe.msgprint(value.description)
						frappe.msgprint("Total")
						frappe.msgprint(rm)
						frappe.msgprint("val2")
						frappe.msgprint(t)
						bal= t - rm
						tot=0.00
						frappe.msgprint("balance")
						frappe.msgprint(bal)
						doc_req = {
							"doctype": "Payment Schedule",
							"charge_type":value.charge_type,
							"description": value.description,
							"rate": value.rate,
							"paid_amount":self.balance_amount * (value.rate/100),
							"sales_tax_rate":value.sales_tax_rate,
							"service_tax_rate":value.service_tax_rate,
							"sales_tax_amount":self.balance_amount * (value.sales_tax_rate/100),
							"service_tax_amount":self.balance_amount * (value.service_tax_rate/100),
							"total": val2,
							"received_amount" : rm,
							"balance" : bal
							}							
		return doc_req
					#self.append("payment_schedule_table", doc_req)
			#self.total_c=val2
			#self.total_b_c2=self.total_b-self.total_c 



	def method1(self):
		if self.flat_invoice:
			#frappe.msgprint("From Python")
			name=self.flat_invoice
			name=name.replace(name[0],"S")
			doc_jv= frappe.get_doc("Sales Invoice", name)
			tot=(doc_jv.grand_total) - (doc_jv.outstanding_amount)
			if doc_jv.grand_total == doc_jv.outstanding_amount:
				frappe.msgprint("No Payment")
			else:
				return tot

		
		#if self.balance_amount == 0.00 and self.down_payment == 0.00:
		#	payment_schedule_method(self)

	def get_taxes_and_charges(self):
		#frappe.msgprint("From Python")
		if self.flat_invoice and self.payment_scheme:
			name=self.flat_invoice
			name=name.replace(name[0],"S")
			doc_jv= frappe.get_doc("Sales Invoice", name)
			tot=(doc_jv.grand_total) - (doc_jv.outstanding_amount)
			#self.event1=tot
			#frappe.msgprint(tot)
			#frappe.msgprint("From Python")
			if doc_jv.grand_total == doc_jv.outstanding_amount:
				frappe.msgprint("No Payment")
			'''ps=self.payment_scheme
			p=""
			for i in ps:
				if i.isdigit():
					p+=i
			self.down_payment=self.total_sales_consideration * eval(p)/100 
			self.balance_amount=self.total_sales_consideration - self.down_payment'''
			if not self.payment_scheme:
				return
			from frappe.model import default_fields
			tax_master = frappe.get_doc("Payment Schedule Template", self.payment_scheme)
			taxes_and_charges = []
			for i, tax in enumerate(tax_master.get("payment_schedule")):
				tax = tax.as_dict()

				for fieldname in default_fields:
					if fieldname in tax:
						del tax[fieldname]
				#frappe.msgprint(tax.total)	
				taxes_and_charges.append(tax)

			return taxes_and_charges











'''@frappe.whitelist()
def get_taxes_and_charges(master_doctype, master_name):
		frappe.msgprint("From Python")
		name=self.flat_invoice
		name=name.replace(name[0],"S")
		doc_jv= frappe.get_doc("Sales Invoice", name)
		tot=(doc_jv.grand_total) - (doc_jv.outstanding_amount)
		frappe.msgprint("From Python")
		if doc_jv.grand_total == doc_jv.outstanding_amount:
			frappe.msgprint("No Payment")
		ps=self.payment_scheme
		p=""
		for i in ps:
			if i.isdigit():
				p+=i
		self.down_payment=self.total_sales_consideration * eval(p)/100 
		self.balance_amount=self.total_sales_consideration - self.down_payment
		if not master_name:
			return
		from frappe.model import default_fields
		tax_master = frappe.get_doc(master_doctype, master_name)

		taxes_and_charges = []
		for i, tax in enumerate(tax_master.get("payment_schedule")):
			tax = tax.as_dict()

			for fieldname in default_fields:
				if fieldname in tax:
					del tax[fieldname]
			frappe.msgprint(tax.description)	
			taxes_and_charges.append(tax)

		return taxes_and_charges

'''