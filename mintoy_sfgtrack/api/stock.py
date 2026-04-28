import frappe
from frappe.utils import today
from frappe.defaults import get_defaults
from erpnext.stock.report.stock_balance.stock_balance import execute as execute_stock_balance

@frappe.whitelist()
def get_stock(item_code, item_group):
    item_data = {
        'total_qty': 0,
        'description': {}
    }

    default_company = frappe.defaults.get_user_default("Company")

    item_list = frappe.db.get_list("Item", {"item_group": item_group, "name": ['like', f'%{item_code}%']}, ["name", "item_name"])

    for item in item_list:
        filters = frappe._dict({
            "company": default_company,
            "from_date": today(),
            "to_date": today(),
            "item_group": item_group,
            "item_code": [item.name],
            "warehouse": None,
            "warehouse_type": None,
            "valuation_field_type": "Currency",
            "include_uom": None,
        })

        column, data = execute_stock_balance(filters)

        for d in data:
            if item.name not in item_data['description']:
                item_data['description'][item.name] = 0
            item_data['description'][item.name] += d["bal_qty"]
            item_data['total_qty'] += d["bal_qty"]

    return item_data
