import streamlit as st
from services.db_helper import (
    fetch_latest_inventory_id,
    insert_sales_inventory,
    insert_school_inventory
)

st.title("Add Inventory Item")

# Select inventory type
inventory_type = st.selectbox("Select Inventory Type", ["Sales Inventory", "School Inventory"])

# Determine correct prefix & table
if inventory_type == "Sales Inventory":
    prefix = "SJSSI"
    table_name = "sale_inventory"
elif inventory_type == "School Inventory":
    prefix = "SJSSCI"
    table_name = "school_inventory"

# Generate new inventory ID
latest_id = fetch_latest_inventory_id(table_name, prefix)
if latest_id:
    new_id = f"{prefix}{str(int(latest_id.replace(prefix, '')) + 1).zfill(5)}"
else:
    new_id = f"{prefix}00001"

st.write(f"New Inventory ID: **{new_id}**")

# Common fields for both inventory types
item_name = st.text_input("Item Name")
description = st.text_area("Description")
item_category = st.text_input("Category")
quantity = st.number_input("Quantity", min_value=0, step=1)
cost_per_unit = st.number_input("Cost Per Unit", min_value=0.0, step=0.01)
status = st.selectbox("Status", ["available", "out of stock", "discontinued"])

# Sales Inventory Fields
if inventory_type == "Sales Inventory":
    selling_price = st.number_input("Selling Price", min_value=0.0, step=0.01)

# School Inventory Fields
elif inventory_type == "School Inventory":
    date_of_purchase = st.date_input("Date of Purchase").strftime("%Y-%m-%d")
    date_of_removal = st.date_input("Date of Removal (Optional)", value=None)
    date_of_removal = date_of_removal.strftime("%Y-%m-%d") if date_of_removal else None

# Submit Button
if st.button("Add Item"):
    if item_name and quantity > 0 and cost_per_unit > 0:
        if inventory_type == "Sales Inventory":
            insert_sales_inventory(new_id, item_name, description, item_category, quantity, cost_per_unit, selling_price, status)
            st.success(f"Sales Inventory item **{item_name}** added successfully!")
        elif inventory_type == "School Inventory":
            insert_school_inventory(new_id, item_name, description, item_category, quantity, cost_per_unit, date_of_purchase, date_of_removal, status)
            st.success(f"School Inventory item **{item_name}** added successfully!")
    else:
        st.error("Please fill all required fields correctly.")