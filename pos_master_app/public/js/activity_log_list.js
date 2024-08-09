

frappe.listview_settings['API Activity Log'] = {
    refresh: function(listview) {
        listview.page.add_inner_button("Click to Retrieve Franchise Data", function() {
            frappe.call({
                method: 'pos_master_app.pos_master_app.api.api.master_enq_pos_data',
                freeze: false,
                callback: function (response) {
                    try {
                        frappe.msgprint(response.message.message)
                    } catch (e) { }
                }
            })
        });
    },
};