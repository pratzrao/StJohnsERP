import streamlit as st
from services.db_helper import insert_sales_inventory, insert_school_inventory, fetch_latest_inventory_id

st.title("Add New Inventory Item")

# Dropdown to select inventory type
inventory_type = st.selectbox("Select Inventory Type", ["Sales Inventory", "School Inventory"])

# Generate the next inventory ID based on the selected type
latest_inventory_id = fetch_latest_inventory_id(inventory_type)

if inventory_type == "Sales Inventory":
    next_item_id = f"SJSSI{str(int(latest_inventory_id.replace('SJSSI', '')) + 1).zfill(5)}" if latest_inventory_id else "SJSSI00001"
elif inventory_type == "School Inventory":
    next_item_id = f"SJSSCI{str(int(latest_inventory_id.replace('SJSSCI', '')) + 1).zfill(5)}" if latest_inventory_id else "SJSSCI00001"

st.write(f"Generated Item ID: **{next_item_id}**")

# Common fields for both inventory types
item_name = st.text_input("Item Name *")
description = st.text_area("Description")
item_category = st.text_input("Category (e.g., Books, Uniforms, Accessories)")
quantity = st.number_input("Quantity", min_value=0, step=1)
cost_per_unit = st.number_input("Cost per Unit (INR)", min_value=0.0, step=0.01)

if inventory_type == "Sales Inventory":
    st.header("Sales Inventory Details")
    selling_price = st.number_input("Selling Price (INR)", min_value=0.0, step=0.01)
    status = st.selectbox("Status", ["available", "out of stock", "discontinued"])
    submit_button = st.button("Add Sales Inventory Item")

    if submit_button:
        if item_name:
            insert_sales_inventory(next_item_id, item_name, description, item_category, quantity, cost_per_unit, selling_price, status)
            st.success(f"Sales Inventory item '{item_name}' added successfully.")
        else:
            st.error("Item Name is required.")

elif inventory_type == "School Inventory":
    st.header("School Inventory Details")
    date_of_purchase = st.date_input("Date of Purchase")
    date_of_removal = st.date_input("Date of Removal (Optional)", value=None)
    status = st.selectbox("Status", ["in use", "archived", "disposed"])
    submit_button = st.button("Add School Inventory Item")

    if submit_button:
        if item_name:
            insert_school_inventory(next_item_id, item_name, description, item_category, quantity, cost_per_unit, date_of_purchase, date_of_removal, status)
            st.success(f"School Inventory item '{item_name}' added successfully.")
        else:
            st.error("Item Name is required.")