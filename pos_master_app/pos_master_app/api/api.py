import requests
import frappe
from datetime import datetime


# Define mappings for each document type
# document_mappings = {
#     "Doctype Name" : {
#         "fields" : {
#             "Masteer Bench Doctype Field Name":"Field Name Of Franchise"
#         },
#         "dynamic_fields" : [], # Link Fields of This Doctype Who is connected to other doctype
#         "have_relating_records" : True or False ,# If This Doctype Name is in another doctype field list
#         "parentfield" : "" ,# Field Name of Child Table Name in their parent if it is Child Doctype
#         "parenttype" :"",# Parent Doctype Name if this is Child Doctype
#         "clear_related_fields" : [
#             {
#                 "related_doctype": "Customer",  # doctye name
#                 "parent_field": "customer_group", # filter doctype on this field on given dynamic value
#                 "fields_to_clear": ["customer_group", "customer_group_name"] # If this Doctype document is deleting then Blank this field value on other documents which have matched value
#             },
#             {

#             }
#         ]
#     }
# }


document_mappings = {
    "Customer Group": {
        "fields": {
            "customer_group_name": "customer_group_name",
            "parent_customer_group_name": "parent_customer_group",
            "is_group": "is_group",
            "default_price_list": "default_price_list",
            "creation_time": "creation",
            "modified_time": "modified",
            "franchise_doctype_id": "name",
        },
        "dynamic_fields": ["parent_customer_group"],
        "have_relating_records": True,
        "parentfield": None,
        "parenttype": None,
        "clear_related_fields": [
            {
                "related_doctype": "Customer",
                "parent_field": "customer_group",
                "fields_to_clear": ["customer_group", "customer_group_name"]
            },
            {
                "related_doctype": "POS Invoice",
                "parent_field": "customer_group",
                "fields_to_clear": ["customer_group", "customer_group_name"]
            },
            {
                "related_doctype": "Sales Invoice",
                "parent_field": "customer_group",
                "fields_to_clear": ["customer_group", "customer_group_name"]
            }
        ]
    },
    "Customer": {
        "fields": {
            "customer_name": "customer_name",
            "customer_type": "customer_type",
            "customer_group_name": "customer_group",
            "territory": "territory",
            "type_of_customer": "type_of_customer",
            "account_manager": "account_manager",
            "address_description": "address_description",
            "average_purchase_time": "average_purchase_time",
            "default_commission_rate": "default_commission_rate",
            "credit_status": "credit_status",
            "default_price_list": "default_price_list",
            "disabled": "disabled",
            "posa_discount": "posa_discount",
            "email_id": "email_id",
            "first_purchase_date": "first_purchase_date",
            "lead_name": "lead_name",
            "gender": "gender",
            "gps_location": "gps_location",
            "last_purchase_date": "last_purchase_date",
            "lead_source": "lead_source",
            "loyalty_program": "loyalty_program",
            "loyalty_program_tier": "loyalty_program_tier",
            "market_segment": "market_segment",
            "mobile_no": "mobile_no",
            "next_projected_purchase_date": "next_projected_purchase_date",
            "outstanding_amount": "outstanding_amount",
            "pending_bottles": "pending_bottles",
            "pending_bottles_count": "pending_bottles_count",
            "primary_address": "primary_address",
            "referral_company": "posa_referral_company",
            "default_sales_partner": "default_sales_partner",
            "time_since_last_purchase": "time_since_last_purchase",
            "type_of_customer": "type_of_customer",
            "status": "status",
            "creation_time": "creation",
            "modified_time": "modified",
            "franchise_doctype_id": "name",
        },
        "dynamic_fields": ["customer_group"],
        "have_relating_records": True,
        "parentfield": None,
        "parenttype": None,
        "clear_related_fields": [
        {
            "related_doctype": "POS Invoice",
            "parent_field": "customer",
            "fields_to_clear": ["customer", "customer_name", "customer_group", "customer_group_name"]
        },
        {
            "related_doctype": "Sales Invoice",
            "parent_field": "customer",
            "fields_to_clear": ["customer", "customer_name", "customer_group", "customer_group_name"]
        },
        {
            "related_doctype": "Stock Entry",
            "parent_field": "customer",
            "fields_to_clear": ["customer", "customer_name"]
        }

    ],
    },
    "Item Group": {
        "fields": {
            "item_group_name": "item_group_name",
            "parent_item_group": "parent_item_group",
            "is_group": "is_group",
            "default_price_list": "default_price_list",
            "creation_time": "creation",
            "modified_time": "modified",
            "franchise_doctype_id": "name",
        },
        "dynamic_fields": ["parent_item_group"],
        "have_relating_records": True,
        "parentfield": None,
        "parenttype": None,
        "clear_related_fields": [
        {
            "related_doctype": "Item",
            "parent_field": "item_group",
            "fields_to_clear": ["item_group", "item_group_name"]
        }
    ],
    },
    "Item": {
        "fields": {
            "item_group_name": "item_group",
            "stock_uom": "stock_uom",
            "item_code": "item_code",
            "description": "description",
            "disabled": "disabled",
            "item_name": "item_name",
            "creation_time": "creation",
            "modified_time": "modified",
            "franchise_doctype_id": "name",
        },
        "dynamic_fields": ["item_group"],
        "have_relating_records": True,
        "parentfield": None,
        "parenttype": None,
        "clear_related_fields": [
        {
            "related_doctype": "POS Invoice Item",
            "parent_field": "item_code",
            "fields_to_clear": ["item_code", "item_code_name"]
        },
        {
            "related_doctype": "Packed Item",
            "parent_field": "item_code",
            "fields_to_clear": ["item_code", "item_code_name"]
        },
        {
            "related_doctype": "Packed Item",
            "parent_field": "parent_item",
            "fields_to_clear": ["parent_item", "parent_item_name"]
        },
        {
            "related_doctype": "Sales Invoice Item",
            "parent_field": "item_code",
            "fields_to_clear": ["item_code", "item_code_name"]
        },
        {
            "related_doctype": "Damaged Bottle Items",
            "parent_field": "item_code",
            "fields_to_clear": ["item_code", "item_code_name"]
        }
    ]
    },
    "POS Invoice": {
        "fields": {
            "company": "company",
            "currency": "currency",
            "posting_date": "posting_date",
            "grand_total": "grand_total",
            "selling_price_list": "selling_price_list",
            "discount_amount": "discount_amount",
            "additional_discount_percentage": "additional_discount_percentage",
            "amount_eligible_for_commission": "amount_eligible_for_commission",
            "coupon_code": "coupon_code",
            "current_loyalty_points": "current_loyalty_points",
            "customer_group_name": "customer_group",
            "customer_name": "customer_name",
            "delivery_date": "delivery_date",
            "is_discounted": "is_discounted",
            "is_opening": "is_opening",
            "is_return": "is_return",
            "loyalty_amount": "loyalty_amount",
            "loyalty_points": "loyalty_points",
            "loyalty_program": "loyalty_program",
            "contact_mobile": "contact_mobile",
            "mpesa_receipt_number": "mpesa_receipt_number",
            "net_total": "net_total",
            "delivery_option_status": "delivery_option_status",
            "previous_outstanding_amount": "previous_outstanding_amount",
            "paid_amount": "paid_amount",
            "due_date": "due_date",
            "picking_date": "picking_date",
            "pos_profile": "pos_profile",
            "posting_time": "posting_time",
            "redeem_loyalty_points": "redeem_loyalty_points",
            "remarks": "remarks",
            "return_against": "return_against",
            "status": "status",
            "territory": "territory",
            "delivered_by": "delivered_by",
            "picked_by": "picked_by",
            "to_date": "to_date",
            "total": "total",
            "total_qty": "total_qty",
            "total_taxes_and_charges": "total_taxes_and_charges",
            "id_sales_invoice_payment": "id_sales_invoice_payment",
            "account_sales_invoice_payment": "account_sales_invoice_payment",
            "amount_sales_invoice_payment": "amount_sales_invoice_payment",
            "default_sales_invoice_payment": "default_sales_invoice_payment",
            "mode_of_payment_sales_invoice_payment": "mode_of_payment_sales_invoice_payment",
            "type_sales_invoice_payment": "type_sales_invoice_payment",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields": ["customer_group", "customer"],
        "parentfield": None,
        "parenttype": None
    },
    "POS Invoice Item": {
        "fields": {
            "company": "company",
            "amount": "amount",
            "description": "description",
            "item_name": "item_name",
            "rate": "rate",
            "uom": "uom",
            "discount_percentage": "discount_percentage",
            "discount_amount": "discount_amount",
            "item_code_name": "item_code",
            "item_group": "item_group",
            "net_amount": "net_amount",
            "net_rate": "net_rate",
            "price_list_rate": "price_list_rate",
            "qty": "qty",
            "stock_uom": "stock_uom",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields": ["item_code", "parent"],
        "parentfield": "pos_invoice_item",
        "parenttype": "POS Invoice",
    },
    "Sales Invoice": {
        "fields": {
            "company": "company",
            "currency": "currency",
            "posting_date": "posting_date",
            "grand_total": "grand_total",
            "selling_price_list": "selling_price_list",
            "discount_amount": "discount_amount",
            "additional_discount_percentage": "additional_discount_percentage",
            "amount_eligible_for_commission": "amount_eligible_for_commission",
            "customer_group_name": "customer_group",
            "customer_name": "customer_name",
            "net_total": "net_total",
            "outstanding_amount": "outstanding_amount",
            "paid_amount": "paid_amount",
            "due_date": "due_date",
            "pos_profile": "pos_profile",
            "posting_time": "posting_time",
            "redeem_loyalty_points": "redeem_loyalty_points",
            "remarks": "remarks",
            "rounded_total": "rounded_total",
            "status": "status",
            "territory": "territory",
            "total": "total",
            "total_qty": "total_qty",
            "total_taxes_and_charges": "total_taxes_and_charges",
            "id_sales_invoice_payment": "id_sales_invoice_payment",
            "amount_sales_invoice_payment": "amount_sales_invoice_payment",
            "mode_of_payment_sales_invoice_payment": "mode_of_payment_sales_invoice_payment",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields": ["customer", "customer_group"],
        "parentfield": None,
        "parenttype": None
    },
    "Packed Item": {
        "fields": {
            "company": "company",
            "description": "description",
            "warehouse": "warehouse",
            "item_code_name": "item_code",
            "item_name": "item_name",
            "ordered_qty": "ordered_qty",
            "packed_qty": "packed_qty",
            "parent_item_name": "parent_item",
            "parent_detail_docname": "parent_detail_docname",
            "qty": "qty",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields": ["item_code", "parent", "parent_item"],
        "parentfield": "packed_items",
        "parenttype": "Sales Invoice",
    },
    "Sales Invoice Item": {
        "fields": {
            "company": "company",
            "amount": "amount",
            "description": "description",
            "item_name": "item_name",
            "rate": "rate",
            "uom": "uom",
            "discount_percentage": "discount_percentage",
            "discount_amount": "discount_amount",
            "item_code_name": "item_code",
            "item_group": "item_group",
            "net_amount": "net_amount",
            "net_rate": "net_rate",
            "price_list_rate": "price_list_rate",
            "qty": "qty",
            "stock_uom": "stock_uom",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields": ["item_code", "parent"],
        "parentfield": "sales_invoice_items",
        "parenttype": "Sales Invoice",
    },
    "Expenses Entry": {
        "fields": {
            "company": "company",
            "posting_date": "posting_date",
            "is_payment": "is_payment",
            "book_an_expense": "book_an_expense",
            "mode_of_payment": "mode_of_payment",
            "liability_or_asset_account": "liability_or_asset_account",
            "payment_currency": "payment_currency",
            "project": "project",
            "default_cost_center": "default_cost_center",
            "total": "total",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields":[],
        "parentfield":None,
        "parenttype": None,
    },
    "Expenses Item": {
        "fields": {
            "company": "company",
            "account": "account",
            "qty": "qty",
            "rate": "rate",
            "description": "description",
            "project": "project",
            "cost_center": "cost_center",
            "account_currency": "account_currency",
            "amount": "amount",
            "party_type": "party_type",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields": ["parent"],
        "parentfield": "expenses_item",
        "parenttype": "Expenses Entry",
    },
    "Meter Reading": {
        "fields": {
            "company": "company",
            "posting_date": "posting_date",
            "opening_meter_reading": "opening_meter_reading",
            "closing_meter_reading": "closing_meter_reading",
            "total": "total",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields": [],
        "parentfield": None,
        "parenttype":None,
    },
    "Damaged Bottles": {
        "fields": {
            "company": "company",
            "warehouse": "warehouse",
            "posted_by": "posted_by",
            "posting_date": "posting_date",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields":[],
        "parentfield":None,
        "parenttype": None,
        "clear_related_fields": [
        {
            "related_doctype": "Stock Entry",
            "parent_field": "damaged_bottle",
            "fields_to_clear": ["damaged_bottle", "damaged_bottle_name"]
        }
    ],
    },
    "Damaged Bottle Items": {
        "fields": {
            "company": "company",
            "bottle_type": "bottle_type",
            "item_code_name": "item_code",
            "type_of_damage": "type_of_damage",
            "qty": "qty",
            "remarks": "remarks",
            "warehouse": "warehouse",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields": ["item_code" ,"parent"],
        "parentfield": "damaged_bottle_items",
        "parenttype": "Damaged Bottles",
    },
    "Stock Entry": {
        "fields": {
            "company": "company",
            "stock_entry_type":"stock_entry_type",
            "customer_name": "customer",
            "pending_bottle_ref": "pending_bottle_ref",
            "damaged_bottle_name": "damaged_bottle",
            "type_of_damage": "type_of_damage",
            "naming_series": "naming_series",
            "purpose": "purpose",
            "from_warehouse": "from_warehouse",
            "to_warehouse":"to_warehouse",
            "posting_date": "posting_date",
            "posting_time": "posting_time",
            "remarks": "remarks",
            "supplier": "supplier",
            "supplier_name": "supplier_name",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields": ["customer" ,"damaged_bottle"],
        "parentfield": None,
        "parenttype":None
    },
     "Stock Entry Detail": {
        "fields": {
            "company": "company",
            "s_warehouse": "s_warehouse",
            "t_warehouse": "t_warehouse",
            "item_code_name": "item_code",
            "item_name": "item_name",
            "qty": "qty",
            "amount": "amount",
            "basic_rate": "basic_rate",
            "description": "description",
            "expense_account": "expense_account",
            "item_group": "item_group",
            "franchise_doctype_id": "name",
            "creation_time": "creation",
            "modified_time": "modified",
        },
        "dynamic_fields": ['parent', 'item_code'],
        "parentfield": "stock_entry_detail",
        "parenttype":"Stock Entry",
    }

}


@frappe.whitelist()
# Schedular Which Fetch Bench Wise Call Function to call data
def master_enq_pos_data():
    # Fetch all POS Benches with their names and countries
    all_benches = frappe.get_all("POS Benches", fields=["name","country"])
    # Enqueue data fetching for each POS Bench
    for bench in all_benches:
        frappe.enqueue('pos_master_app.pos_master_app.api.api.get_pos_data_site_wise', queue='short',timeout=3600, franchise_bench=bench.name)
    # Return success status
    return {"status":"sucessfull","message":"POS Bench data started importing!"}


# Bennch WIse Franchise data Import
@frappe.whitelist()
def get_pos_data_site_wise(franchise_bench=None):
    try:
        # Initialize API activity log
        api_activity_doc = frappe.new_doc("API Activity Log")
        api_activity_doc.franchise_bench = franchise_bench
        api_activity_doc.api_start_time = datetime.now()

        # Fetch all active POS Franchises for the given bench
        all_franchises = frappe.get_all(
            "POS Franchise",
            fields=[
                "name",
                "domain_name",
                "franchise_naming_series",
                "status",
                "parent",
                "api_key_secret_pair",
            ],
            filters={"status": "Live","parent": franchise_bench},
        )
        # Iterate through each franchise associated with the bench
        for franchise in all_franchises:
            try:

                # Check if domain name exists for the franchise
                if franchise.get("domain_name"):
                    franchise_name = franchise.get("domain_name")
                    naming_series = franchise.get("name")

                    # Initialize franchise-wise activity log
                    franchise_activity_log = {
                        "franchise_name": franchise_name,
                        "start_time": datetime.now(),
                        "end_time": None,
                        "error_log": "",
                    }

                    # Call franchise API to fetch data
                    url = f"{franchise_name}/api/method/pos_api_app.pos_api_app.api.api.post_pos_data"
                    headers = {
                        "Content-Type": "text/json",
                        "Authorization": f"Token {franchise.api_key_secret_pair}",
                    }
                    payload = ""
                    response = requests.get(url, json=payload, headers=headers)
                    response_data = response.json()

                    # Process response from franchise API
                    if "exception" not in response_data:
                        # Synchronize each document type for the franchise
                        synchronize_documents(
                            response_data["message"],
                            franchise_name,
                            naming_series,
                        )
                    else:
                        # Log error if exception is present in response
                        franchise_activity_log["error_log"] = str(response_data)
                        log_error_to_pos_api_error_log(franchise_name, franchise_bench, str(response_data))
                else:
                    continue
            except Exception as e:
                # Log any exceptions encountered during franchise processing
                franchise_activity_log["error_log"] = str(e)
                log_error_to_pos_api_error_log(franchise_name, franchise_bench, str(e))

            finally:
                # Update end time and log franchise activity
                franchise_activity_log["end_time"] = datetime.now()
                franchise_activity_log["api_time"] = (
                    franchise_activity_log["end_time"]
                    - franchise_activity_log["start_time"]
                )
                log = frappe.new_doc("API Franchise Wise Log")
                log.update(franchise_activity_log)
                api_activity_doc.append("franchise_wise_activity_log", log)

        # Update end time for API activity and save log
        api_activity_doc.api_end_time = datetime.now()
        api_activity_doc.save(ignore_permissions=True)
        frappe.db.commit()

        # Return success message after processing all franchises
        return {
            "status": "success",
            "message": "POS Franchises data imported successfully!",
        }

    # Log any exceptions encountered during overall process
    except Exception as ex:
        log_error_to_pos_api_error_log(franchise_name, franchise_name, str(ex))
        return {"status": "error", "message": str(ex)}
        

# Import All data of franchise and call doctype wise function
def synchronize_documents(data, franchise_name, naming_series):
    # Iterate through predefined document mappings
    for doctype, details in document_mappings.items():
        
        sync_documents(
            data.get(doctype.replace(" ", "_").lower()),
            doctype,
            details["fields"],
            details["dynamic_fields"],
            details["parentfield"],
            details["parenttype"],
            franchise_name,
            naming_series,
        )

# Doctype Wise Import data bases on given dynamic mapping
def sync_documents(
    documents,
    doctype,
    field_mappings,
    dynamic_fields,
    parentfield,
    parenttype,
    franchise_name,
    naming_series,
):
    print("\n\n      ", doctype, "started", len(documents))
    # Fetch existing documents for the given naming series

    existing_documents = frappe.get_all(
        doctype,
        filters={"franchise_code": naming_series},
        fields=["name", "franchise_doctype_id", "modified_time", "franchise_name"],
    )
    existing_documents_dict = {
        doc["franchise_doctype_id"].lower(): doc for doc in existing_documents
    }
    existing_document_names = set(existing_documents_dict.keys())

    print("         ", doctype, "start loop")
    docs_to_insert = []
    docs_to_update = []
    docs_to_delete = set(existing_document_names)

    # Process each document received from franchise API
    for document in documents:
        document_name = document["name"].lower()
        docs_to_delete.discard(document_name)

        if document_name in existing_document_names:
            # Update document if modified
            existing_document = existing_documents_dict[document_name]
            if (
                str(existing_document["modified_time"]) != str(document.get("modified"))
                or franchise_name != existing_document["franchise_name"]
            ):
                # make field_mappings wise value set in array
                fields_to_set = set_fields_to_set(
                    document,
                    field_mappings,
                    franchise_name,
                    naming_series,
                    document_name,
                    dynamic_fields,
                    parentfield,
                    parenttype,
                )
                docs_to_update.append((existing_document["name"], fields_to_set))
        else:
            # Insert new document if not already existing
            fields_to_set = set_fields_to_set(
                document,
                field_mappings,
                franchise_name,
                naming_series,
                document_name,
                dynamic_fields,
                parentfield,
                parenttype,
            )
           

            docs_to_insert.append(list(fields_to_set.values()))
    
    # Batch insert new documents
    print("         ", doctype, "bulk insert start", len(docs_to_insert))
    if docs_to_insert:
        batch_size = 100000
        fields = list(fields_to_set.keys())
        for chunk in chunker(docs_to_insert, batch_size):
            frappe.db.bulk_insert(doctype, fields, chunk)
    print("         ", doctype, "bulk insert end", len(docs_to_insert))
    
    print("         ", doctype, "bulk update start", len(docs_to_update))
    # Bulk update existing documents
    for docname, fields in docs_to_update:
        frappe.db.set_value(doctype, docname, fields)

    print("         ", doctype, "bulk update end", len(docs_to_update))

    print("         ", doctype, "end loop")

    print("         ", doctype, "delete start")
    # Delete documents that are no longer present in franchise data
    if docs_to_delete:
        for docname in docs_to_delete:
             if document_mappings.get(doctype).get("have_relating_records"):
                related_fields_to_clear = document_mappings[doctype].get("clear_related_fields", [])
                for related_field_config in related_fields_to_clear:
                    # clear related record where this docname exist in fields
                    updating_related_records(
                        related_field_config["related_doctype"],
                        related_field_config["parent_field"],
                        existing_documents_dict[docname]["name"],
                        fields_to_clear=related_field_config["fields_to_clear"]
                    )
        for docname in docs_to_delete:
            frappe.delete_doc(
                doctype,
                existing_documents_dict[docname]["name"],
                ignore_permissions=True,
            )
    # Commit changes to database
    frappe.db.commit()
    print("         ", doctype, "delete end")


def set_fields_to_set(
    document,
    field_mappings,
    franchise_name,
    naming_series,
    document_name,
    dynamic_fields,
    parentfield,
    parenttype,
):
    # Set fields to update or insert for a document.
    fields_to_set = {
        field: document.get(field_name) for field, field_name in field_mappings.items()
    }
    # Dictionary of fields to set for the document.
    fields_to_set.update(
        {
            "franchise_name": franchise_name,
            "franchise_code": naming_series,
            "name": f"{document_name}_{naming_series}",
        }
    )
    # Dictionary of parent fields to set for the document.
    if parentfield:
        fields_to_set["parentfield"] = parentfield
        fields_to_set["parenttype"] = parenttype

    # Dictionary of dynamic fields to set for the document.
    if dynamic_fields:
        fields_to_set.update(
            {
                field: (
                    None
                    if not document.get(field)
                    else document.get(field).lower() + "_" + naming_series
                )
                for field in dynamic_fields
            }
        )

    return fields_to_set


def chunker(seq, size):
    # Generator function to chunk a sequence into smaller chunks of specified size.
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


 # clear related record where given filter_value exist in fields
def updating_related_records(
    doctype,
    filter_field,
    filter_value,
    fields_to_clear=None
):
    # Update related documents by clearing specified fields.
    if fields_to_clear is None:
        fields_to_clear = []

     # Fetch documents for matching field
    docs = frappe.get_all(doctype, filters={filter_field: filter_value})

    for doc in docs:
        doc_obj = frappe.get_doc(doctype, doc.name)
        # Clear specified fields
        for field in fields_to_clear:
            setattr(doc_obj, field, None)
        doc_obj.save()
    frappe.db.commit()


# Log errors encountered during POS API Callling and importing data.
def log_error_to_pos_api_error_log(franchise_name, franchise_bench, error_log):
        # Create new POS API Error Log document
        error_log_doc = frappe.new_doc("POS API Error Log")
        error_log_doc.franchise_name = franchise_name
        error_log_doc.franchise_bench = franchise_bench
        error_log_doc.error_log = error_log
        error_log_doc.save(ignore_permissions=True)
        frappe.db.commit()



# delete franchise data on status change or delete it from benches
def delete_records_by_franchise_code(franchise_code=None):
    if franchise_code:
        doctypes = [
            'Damaged Bottle Items','Damaged Bottles','Meter Reading','Expenses Item','Expenses Entry','Stock Entry Detail','Stock Entry',
            'Packed Item','Sales Invoice Item','Sales Invoice', 'POS Invoice Item', 'POS Invoice', 'Item', 'Item Group','Customer', 'Customer Group'
        ]
        
        for doctype in doctypes:
            query = f"""
                DELETE FROM `tab{doctype}` WHERE franchise_code = '{franchise_code}';
            """
            
            try:
                frappe.db.sql(query, as_dict=1)
                frappe.db.commit()
                print(f"Deleted records from {doctype} with franchise_code = '{franchise_code}'.")
            except Exception as e:
                print(f"Error deleting records from {doctype}: {str(e)}")
    return {"status":"sucessfull","message":"POS Franchises data deleted successfully!"}
