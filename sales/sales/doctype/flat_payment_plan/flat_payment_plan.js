cur_frm.add_fetch("flat_invoice","customer_name","customer_name")
cur_frm.add_fetch("flat_invoice","flat_no","flat_number")
cur_frm.add_fetch("flat_invoice","rounded_total","total_sales_consideration")
//-------------------------Payment Plan--------------------------------------------------------------------
cur_frm.cscript.refresh= function(doc,cdt,cdn) {
            var me = this;
            //msgprint("from js Charges function")
            if(0==0) {
                return this.frm.call({
                    doc: this.frm.doc,
                    //method: "method1",
                    method: "method1",
                    callback: function(r) {
                        if(!r.exc) {
                            cur_frm.set_value("event1",r.message)
                            //refresh_field('event1');
                            //cur_frm.set_value("event2",doc.event1)
                            console.log("flat_invoice call")
                            //console.log(cur_frm.doc.event1)
                            //cur_frm.cscript.payment_scheme(doc)
                           //cur_frm.cscript.event2(doc, cdt, cdn)
                            refresh_field('payment_schedule_table');
                        }
                    }
                })
            }
        }



cur_frm.cscript.flat_invoice= function(doc) {
            var me = this;
            //msgprint("from js Charges function")
            if(0==0) {
                return this.frm.call({
                    doc: this.frm.doc,
                    //method: "method1",
                    method: "method1",
                    callback: function(r) {
                        if(!r.exc) {
                            cur_frm.set_value("event1",r.message)
                            refresh_field('event1');
                            console.log("flat_invoice call")
                            console.log(cur_frm.doc.event1)
                            
                        
                        }
                    }
                })
            }
        }


frappe.ui.form.on("Flat Payment Plan","down_payment",function(frm)
{
    //console.log(frm.doc.event1)
    frm.set_value("balance_amount",frm.doc.total_sales_consideration - frm.doc.down_payment);
});


		

cur_frm.cscript.payment_scheme= function(doc, cdt, cdn) {
            var me = this;
            //msgprint("from js Charges function")
            if(0==0) {
                return this.frm.call({
                    doc: this.frm.doc,
                    //method: "method1",
                    //method: "payment_schedule_method",
                    method: "get_taxes_and_charges",
                    callback: function(r) {
                        if(!r.exc) {
                        me.frm.set_value("payment_schedule_table", r.message);
                        //cur_frm.set_value("event1",r.message)  
                        cur_frm.set_value("event2",doc.payment_scheme)
                        //console.log(doc.event1)
                        //cur_frm.cscript.event2(doc, cdt, cdn)
                        //refresh_field('payment_schedule_table');
                        
                        }
                    }
                })
            }
        }




cur_frm.cscript.event2 = function(doc, cdt, cdn) {
    
    console.log("event2 onload")
    console.log("Method1 Call From Onload")
    var pst=doc.payment_schedule_table || [];
    tot_amt_to_be_paid=tot_amt_recv=tot_bal=0.00
    rm=doc.event1 - doc.down_payment
    console.log("Paid",rm)
    for(var i=0;i<pst.length;i++)
    {
        pst[i].paid_amount=(doc.balance_amount*pst[i].rate)/100
        pst[i].sales_tax_amount=(doc.balance_amount*pst[i].sales_tax_rate)/100
        pst[i].service_tax_amount=(doc.balance_amount*pst[i].service_tax_rate)/100
        pst[i].total=(pst[i].paid_amount + pst[i].sales_tax_amount + pst[i].service_tax_amount)
        if (rm >= pst[i].total)
        {
            rm= rm - pst[i].total
            pst[i].received_amount=pst[i].total
            console.log(rm)

        } 
        else if (rm <= pst[i].total) 
            {
                bal= pst[i].total - rm
                pst[i].received_amount=rm
                pst[i].balance=bal 
                rm=0.00
                console.log(rm)           
            }
        else if (rm==0.00) 
            {
                pst[i].balance=pst[i].total
                console.log(rm)

            }
        
    }
    refresh_field('payment_schedule_table');
    for(var i=0;i<pst.length;i++)
    {
        tot_amt_to_be_paid=tot_amt_to_be_paid+pst[i].total
        tot_amt_recv=tot_amt_recv+pst[i].received_amount
        tot_bal=tot_bal+pst[i].balance
        cur_frm.set_value("_total_amount_to_be_paid",tot_amt_to_be_paid)
        cur_frm.set_value("total_amount_received",tot_amt_recv)
        cur_frm.set_value("total_balance",tot_bal)
    }
};





cur_frm.cscript.event1 = function(doc, cdt, cdn) {
    
    console.log("event1")
    var pst=doc.payment_schedule_table || [];
    tot_amt_to_be_paid=tot_amt_recv=tot_bal=0.00
    rm=doc.event1 - doc.down_payment
    console.log("Paid",rm)
    for(var i=0;i<pst.length;i++)
    {
        pst[i].paid_amount=(doc.balance_amount*pst[i].rate)/100
        pst[i].sales_tax_amount=(doc.balance_amount*pst[i].sales_tax_rate)/100
        pst[i].service_tax_amount=(doc.balance_amount*pst[i].service_tax_rate)/100
        pst[i].total=(pst[i].paid_amount + pst[i].sales_tax_amount + pst[i].service_tax_amount)
        if (rm >= pst[i].total)
        {
            rm= rm - pst[i].total
            pst[i].received_amount=pst[i].total
            console.log(rm)

        } 
        else if (rm <= pst[i].total) 
            {
                bal= pst[i].total - rm
                pst[i].received_amount=rm
                pst[i].balance=bal 
                rm=0.00
                console.log(rm)           
            }
        else if (rm==0.00) 
            {
                pst[i].balance=pst[i].total
                console.log(rm)

            }
        
    }
    refresh_field('payment_schedule_table');
    for(var i=0;i<pst.length;i++)
    {
        tot_amt_to_be_paid=tot_amt_to_be_paid+pst[i].total
        tot_amt_recv=tot_amt_recv+pst[i].received_amount
        tot_bal=tot_bal+pst[i].balance
        cur_frm.set_value("_total_amount_to_be_paid",tot_amt_to_be_paid)
        cur_frm.set_value("total_amount_received",tot_amt_recv)
        cur_frm.set_value("total_balance",tot_bal)
    }
};


// cur_frm.cscript.onload= function(doc,cdt,cdn) {
//             var me = this;
//             if(0==0) {
//                 return this.frm.call({
//                     doc: this.frm.doc,
//                     //method: "method1",
//                     method: "method1",
//                     callback: function(r) {
//                         if(!r.exc) {
//                             //me.frm.set_value("event1", r.message);  
//                             refresh_field('event1');
//                             console.log("flat_invoice call onload")
//                             console.log(cur_frm.doc.event1)
//                             //cur_frm.cscript.payment_scheme(doc)
//                             //cur_frm.cscript.event2(doc, cdt, cdn)
//                             refresh_field('payment_schedule_table');
                        
//                         }
//                     }
//                 })
//             }
//         }







// cur_frm.cscript.onload= function(doc) {
//             var me = this;
//             //msgprint("from js Charges function")
//             if(0==0) {
//                 return this.frm.call({
//                     doc: this.frm.doc,
//                     //method: "method1",
//                     //method: "payment_schedule_method",
//                     method: "get_taxes_and_charges",
//                     callback: function(r) {
//                         if(!r.exc) {
//                         me.frm.set_value("payment_schedule_table", r.message); 
//                         refresh_field('payment_schedule_table'); 
//                         cur_frm.set_value("event2",doc.payment_scheme)
//                         console.log(" Table Onload Event")

                        
//                         }
//                     }
//                 })
//             }
//         }





// cur_frm.cscript.rate = function(doc, cdt, cdn) {
//     var payment = frappe.get_doc(cdt, cdn);
//     frappe.model.set_value(cdt, cdn, "paid_amount", (doc.total_sales_consideration*payment.rate)/100);
//     frappe.model.set_value(cdt, cdn,"total",(payment.sales_tax_amount + payment.paid_amount ) );
//     frappe.model.set_value(cdt, cdn, "balance", payment.total - payment.received_amount);
// };

        
// cur_frm.cscript.received_amount = function(doc, cdt, cdn) {
//     var payment = frappe.get_doc(cdt, cdn);
//     var balance = (payment.total - payment.received_amount)  ;
//  frappe.model.set_value(cdt, cdn, "balance", balance);
    
// };       
// cur_frm.cscript.sales_tax_rate = function(doc, cdt, cdn) {
//     var payment = frappe.get_doc(cdt, cdn);
//     frappe.model.set_value(cdt, cdn, "sales_tax_amount", (doc.total_sales_consideration*payment.sales_tax_rate)/100);
//     frappe.model.set_value(cdt, cdn,"total",(payment.sales_tax_amount + payment.paid_amount ) );
//     frappe.model.set_value(cdt, cdn, "balance", payment.total - payment.received_amount);
//     };

// cur_frm.cscript.service_tax_rate = function(doc, cdt, cdn) {
//     var payment = frappe.get_doc(cdt, cdn);
//     frappe.model.set_value(cdt, cdn, "service_tax_amount", (doc.total_sales_consideration*payment.service_tax_rate)/100);
//     frappe.model.set_value(cdt, cdn,"total",(payment.sales_tax_amount + payment.paid_amount + payment.service_tax_rate) );
//     frappe.model.set_value(cdt, cdn, "balance", payment.total - payment.received_amount);
//     };

// cur_frm.cscript.sales_tax_amount = function(doc, cdt, cdn) {
//     var payment = frappe.get_doc(cdt, cdn);
//     frappe.model.set_value(cdt, cdn,"total",(payment.sales_tax_amount + payment.paid_amount + payment.service_tax_rate) );
//     frappe.model.set_value(cdt, cdn, "balance", payment.total - payment.received_amount);
//     };
// cur_frm.cscript.service_tax_amount = function(doc, cdt, cdn) {
//     var payment = frappe.get_doc(cdt, cdn);
//     frappe.model.set_value(cdt, cdn,"total",(payment.sales_tax_amount + payment.paid_amount  + payment.service_tax_rate) );
//     frappe.model.set_value(cdt, cdn, "balance", payment.total - payment.received_amount);
//     };

// cur_frm.cscript.paid_amount = function(doc, cdt, cdn) {
//     var payment = frappe.get_doc(cdt, cdn);
//     frappe.model.set_value(cdt, cdn,"total",(payment.sales_tax_amount + payment.paid_amount + payment.service_tax_rate) );
//     frappe.model.set_value(cdt, cdn, "balance", payment.total - payment.received_amount);
//     };



/*cur_frm.cscript.payment_scheme= function(doc) {
        var me = this;
        msgprint("from js Charges function")
        if(this.frm.doc.payment_scheme) {
            return this.frm.call({
                method: "get_taxes_and_charges",
                args: {
                    "master_doctype": frappe.meta.get_docfield(this.frm.doc.doctype, "payment_scheme",
                        this.frm.doc.name).options,
                    "master_name": this.frm.doc.payment_scheme,
                },
                callback: function(r) {
                    if(!r.exc) {
                        me.frm.set_value("payment_schedule_table", r.message);
                        //me.calculate_taxes_and_totals();
                        //cur_frm.set_value("event3",doc.taxes)
                    }
                }
            });
        }
    },

*/



// cur_frm.cscript.refresh= function(doc,cdt,cdn) {
//             cur_frm.cscript.flat_invoice(doc)
//             cur_frm.cscript.payment_scheme(doc)
//             // refresh_field('payment_schedule_table');
//             // cur_frm.cscript.event2(doc, cdt, cdn)
//         }








