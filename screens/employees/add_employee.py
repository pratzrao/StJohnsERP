import streamlit as st
from services.db_helper import (
    insert_management,
    insert_teacher,
    insert_admin
)

st.title("Add New Employee")

# Dropdown to select employee type
employee_type = st.selectbox("Select Employee Type", ["Management", "Teacher", "Admin"])

# Form for adding employee details
if employee_type == "Management":
    st.header("Management Details")
    
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    date_of_birth = st.date_input("Date of Birth")
    aadhar_number = st.text_input("Aadhar Number")
    pan_number = st.text_input("Pan Number")
    gender = st.selectbox("Gender", ["male", "female", "other"])
    mobile_number = st.text_input("Mobile Number")
    address = st.text_area("Address")
    email = st.text_input("Email")
    marital_status = st.selectbox("Marital Status", ["single", "married", "widowed", "divorced"])
    emergency_contact_name = st.text_input("Emergency Contact Name")
    emergency_contact_relationship = st.text_input("Emergency Contact Relationship")
    emergency_contact_number = st.text_input("Emergency Contact Number")
    job_title = st.text_input("Job Title")
    date_hired = st.date_input("Date Hired")
    full_time_or_part_time = st.selectbox("Full Time or Part Time", ["full time", "part time"])
    qualification = st.text_input("Qualification")
    professional_certifications = st.text_input("Professional Certifications")
    years_of_experience_in_stjohns = st.number_input("Years of Experience in St. John's", min_value=0)
    years_of_previous_experience = st.number_input("Years of Previous Experience", min_value=0)
    additional_skills = st.text_area("Additional Skills")
    languages = st.text_input("Languages Spoken")
    bank_details = st.text_input("Bank Details")
    opt_in_for_pf = st.selectbox("Opt-in for Provident Fund", ["yes", "no"])
    status = st.selectbox("Status", ['employed', 'quit', 'fired', 'retired', 'owner'])

    submit_button = st.button("Add Management Employee")

    if submit_button:
        if first_name and last_name:
            insert_management(first_name, last_name, date_of_birth, aadhar_number, pan_number, gender,
                              mobile_number, address, email, marital_status, emergency_contact_name,
                              emergency_contact_relationship, emergency_contact_number, job_title, date_hired,
                              full_time_or_part_time, qualification, professional_certifications,
                              years_of_experience_in_stjohns, years_of_previous_experience, additional_skills,
                              languages, bank_details, opt_in_for_pf, status)
            st.success(f"Management employee {first_name} {last_name} added successfully.")
        else:
            st.error("Please fill all required fields.")

elif employee_type == "Teacher":
    st.header("Teacher Details")
    
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    date_of_birth = st.date_input("Date of Birth")
    aadhar_number = st.text_input("Aadhar Number")
    pan_number = st.text_input("Pan Number")
    gender = st.selectbox("Gender", ["male", "female", "other"])
    mobile_number = st.text_input("Mobile Number")
    address = st.text_area("Address")
    email = st.text_input("Email")
    marital_status = st.selectbox("Marital Status", ["single", "married", "widowed", "divorced"])
    emergency_contact_name = st.text_input("Emergency Contact Name")
    emergency_contact_relationship = st.text_input("Emergency Contact Relationship")
    emergency_contact_number = st.text_input("Emergency Contact Number")
    job_title = st.text_input("Job Title")
    grades_taught = st.text_input("Grades Taught")
    subjects_taught = st.text_input("Subjects Taught")
    teaching_periods_per_week = st.number_input("Teaching Periods Per Week", min_value=0)
    date_hired = st.date_input("Date Hired")
    full_time_or_part_time = st.selectbox("Full Time or Part Time", ["full time", "part time"])
    qualification = st.text_input("Qualification")
    professional_certifications = st.text_input("Professional Certifications")
    years_of_experience_in_stjohns = st.number_input("Years of Experience in St. John's", min_value=0)
    years_of_previous_experience = st.number_input("Years of Previous Experience", min_value=0)
    additional_skills = st.text_area("Additional Skills")
    languages = st.text_input("Languages Spoken")
    bank_details = st.text_input("Bank Details")
    opt_in_for_pf = st.selectbox("Opt-in for Provident Fund", ["Yes", "No"])
    status = st.selectbox("Status", ["Active", "Inactive"])

    submit_button = st.button("Add Teacher Employee")

    if submit_button:
        if first_name and last_name:
            insert_teacher(first_name, last_name, date_of_birth, aadhar_number, pan_number, gender, mobile_number,
                           address, email, marital_status, emergency_contact_name,
                           emergency_contact_relationship, emergency_contact_number, job_title, grades_taught,
                           subjects_taught, teaching_periods_per_week, date_hired, full_time_or_part_time,
                           qualification, professional_certifications, years_of_experience_in_stjohns,
                           years_of_previous_experience, additional_skills, languages, bank_details, opt_in_for_pf, status)
            st.success(f"Teacher employee {first_name} {last_name} added successfully.")
        else:
            st.error("Please fill all required fields.")

elif employee_type == "Admin":
    st.header("Admin Details")
    
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    date_of_birth = st.date_input("Date of Birth")
    aadhar_number = st.text_input("Aadhar Number")
    pan_number = st.text_input("Pan Number")
    gender = st.selectbox("Gender", ["male", "female", "other"])
    mobile_number = st.text_input("Mobile Number")
    address = st.text_area("Address")
    email = st.text_input("Email")
    marital_status = st.selectbox("Marital Status", ["single", "married", "widowed", "divorced"])
    emergency_contact_name = st.text_input("Emergency Contact Name")
    emergency_contact_relationship = st.text_input("Emergency Contact Relationship")
    emergency_contact_number = st.text_input("Emergency Contact Number")
    job_title = st.text_input("Job Title")
    date_hired = st.date_input("Date Hired")
    qualification = st.text_input("Qualification")
    status = st.selectbox("Status", ["Active", "Inactive"])

    submit_button = st.button("Add Admin Employee")

    if submit_button:
        if first_name and last_name:
            insert_admin(first_name, last_name, date_of_birth, aadhar_number, pan_number, gender, mobile_number,
                         address, email, marital_status, emergency_contact_name,
                         emergency_contact_relationship, emergency_contact_number, job_title, date_hired,
                         qualification, status)
            st.success(f"Admin employee {first_name} {last_name} added successfully.")
        else:
            st.error("Please fill all required fields.")