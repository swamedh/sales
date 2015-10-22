cur_frm.add_fetch("flat_type","flat_type","type")
cur_frm.add_fetch("flat_type","plc","plc_rate")
cur_frm.add_fetch("floor_link","floor","floor")
cur_frm.add_fetch("floor_link","frc","frc_rate")
frappe.ui.form.on("Flat Master","flat_no",function(frm)
{
	frm.set_value("flat_name",frm.doc.flat_no);
});


frappe.ui.form.on("Flat Master", "save", function(frm) {
    frappe.msgprint("JS")
    if(frm.doc.flat_no) {
        cur_frm.call({
            method: "insertItem",
            args: {
            },
            callback: function(r, rt) {
                if(r.message) {
                    
                }
            }
        });
    }
})
