import streamlit as st
from services.db_helper import fetch_available_items, fetch_student_ids, insert_sale_records, fetch_latest_sale_id

st.title("Add Sale")

# Initialize session state for sale items
if "sale_items" not in st.session_state:
    st.session_state.sale_items = []

# Fetch available items and student IDs
available_items = fetch_available_items()
student_ids = fetch_student_ids()

# Dropdown for selecting student
student_id = st.selectbox("Select Student ID", student_ids)

# Dropdown for selecting item
item_names = [item["item_name"] for item in available_items]
selected_item_name = st.selectbox("Select Item", item_names, key="item_selector")

# Get selected item details
selected_item = next((item for item in available_items if item["item_name"] == selected_item_name), None)

# Input fields for quantity and payment status
quantity = st.number_input("Quantity", min_value=1, step=1, key="quantity_input")
payment_status = st.selectbox("Payment Status", ["paid", "pending", "cancelled"])

# Input field for sale date (global for all items)
sale_date = st.date_input("Sale Date").strftime("%Y-%m-%d")

# Add item button
if st.button("Add Item"):
    if selected_item and quantity > 0:
        if quantity > selected_item["quantity"]:
            st.warning(f"Warning: Quantity sold exceeds inventory for {selected_item['item_name']}.")

        # Add item to session state
        st.session_state.sale_items.append({
            "item_id": selected_item["item_id"],
            "item_name": selected_item["item_name"],
            "quantity": quantity,
            "selling_price": selected_item["selling_price"],
            "total_price": quantity * selected_item["selling_price"],
        })
        st.success(f"Added {quantity} x {selected_item['item_name']} to the sale.")

# Display current bill breakdown
if st.session_state.sale_items:
    st.write("### Bill Breakdown")
    total_price = 0
    for idx, item in enumerate(st.session_state.sale_items, start=1):
        st.write(f"{idx}. {item['quantity']} x {item['item_name']} @ {item['selling_price']} = {item['total_price']}")
        total_price += item["total_price"]
    st.write(f"**Total: {total_price}**")
else:
    st.write("No items added yet.")

# Finalize Sale button
if st.button("Finalize Sale"):
    if student_id and st.session_state.sale_items:
        # Generate base sale ID
        latest_sale_id = fetch_latest_sale_id()
        base_sale_id = (
            f"SJSSALE{str(int(latest_sale_id.replace('SJSSALE', '')) + 1).zfill(5)}"
            if latest_sale_id
            else "SJSSALE00001"
        )

        # Prepare sales data
        sales = []
        for item in st.session_state.sale_items:
            sales.append({
                "item_id": item["item_id"],
                "student_id": student_id,
                "sale_date": sale_date,
                "quantity": item["quantity"],
                "cost_per_unit": item["selling_price"],
                "selling_price": item["selling_price"],
                "payment_status": payment_status,
            })

        # Insert sale records into the database
        try:
            insert_sale_records(base_sale_id, sales)
            st.success(f"Sale finalized with Base Sale ID: {base_sale_id}")

            # Clear session state for sale items
            st.session_state.sale_items = []
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("No items added or Student ID missing.")