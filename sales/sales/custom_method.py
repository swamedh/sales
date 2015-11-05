import frappe




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


def beforeInsertDoc(self,method):
	frappe.msgprint("Start Validate")
	'''if self.invoice_flat_no is None:
		frappe.msgprint("Select Any Flat")
	if self.customer_name_link is None:
		frappe.msgprint("Select Customer")
	if self.booking_date is None:
		frappe.msgprint("Enter Booking Date")'''
	if validateDoc(self,method)==0:
		insertData(self,method)
	frappe.msgprint("End Validate")



def insertData(self,method):
	frappe.msgprint("Start")
	flatMaster=frappe.get_doc("Flat Master",self.flat_no)
	if flatMaster.isbooked==1:
		frappe.msgprint("Flat Already Sold Out")
	else:
		si =  frappe.get_doc({      
			"doctype": "Sales Invoice",
				"customer":self.customer_name_link,
				"customer_name":self.customer_name_link,
				"posting_date":self.booking_date,
				"due_date":self.booking_date,
				"debit_to":"Deepak - ST",
				"net_total": self.net_total,
				"grand_total": self.basic_cost,
				"territory":"India",
				"grand_total":self.rounded_total,
				"rounded_total":self.rounded_total,
				"grand_total_export":self.rounded_total,
				"outstanding_amount":self.rounded_total,	
			"items": [{
				"item_name": self.flat_no,
				"item_code": self.flat_no,
				"description": self.flat_no,
				"qty": self.flag1,
				"rate": self.net_total,
				"amount": self.net_total,
				"income_account": "Administrative Expenses - ST",
			}],
    	}).insert()
		si.submit()
		frappe.msgprint("Over")



def submitDoc(self,method):
	frappe.msgprint("submit")



def cancelDoc(self,method):
	frappe.msgprint("cancelDoc")