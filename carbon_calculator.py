import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

# Set up the page title and layout
st.set_page_config(page_title="Carbon Emissions Calculator", layout="centered")

# Title of the app
st.title("Impact Accounting Simulator: Monetised Emissions")

st.header("How To Use")

# Explanatory text at the top of the calculator
st.write("""
Companies create significant environmental damage through their greenhouse gas emissions (GHG).
By convention, these are broken down into three scopies, reflecting different areas of operation.
This calculator uses the value factor for the social cost of carbon of $236 (per tonne of carbon 
dioxide equivalents) suggested by the International Foundation for Valuing Impacts, which champions
the adoption of impact accounting globally.

""")

# Input field for company name
company_name = st.text_input("Enter Company Name", value="Acme Inc")

# Horizontal divider
st.markdown("---")

# Input fields for Scope 1, Scope 2, and Scope 3 emissions with helper text and precision control
st.header("Enter Emission Volumes")

st.write("""
Provide the scope 1, 2, and 3 emissions for the company whose data you are using. If you don't have one of these parameters, just leave
it blank and the calculator will still work. Make sure to select the correct reporting unit! 

""")

# Dropdown to select units (Tonnes or Millions of Tonnes)
unit = st.selectbox("Select Unit", ["Tonnes of CO2e", "Millions of Tonnes of CO2e"])

scope1 = st.number_input("Scope 1 Emissions (Quantity)", min_value=0.0, value=0.00, format="%.2f", help="Please enter the reported Scope 1 emissions.")
scope2 = st.number_input("Scope 2 Emissions (Quantity)", min_value=0.0, value=0.00, format="%.2f", help="Please enter the reported Scope 2 emissions.")
scope3 = st.number_input("Scope 3 Emissions (Quantity)", min_value=0.0, value=0.00, format="%.2f", help="Please enter the reported Scope 3 emissions.")


# Conversion factor
conversion_factor = 236

# Adjust values based on selected unit
if unit == "Millions of Tonnes of CO2e":
    scope1 *= 1_000_000
    scope2 *= 1_000_000
    scope3 *= 1_000_000

# Calculate total emissions in USD
total_scope1_usd = scope1 * conversion_factor
total_scope2_usd = scope2 * conversion_factor
total_scope3_usd = scope3 * conversion_factor

total_usd = total_scope1_usd + total_scope2_usd + total_scope3_usd

# Round total monetized emissions to nearest integer
total_usd_rounded = round(total_usd)

# Display results with rounding and additional explanation text
st.subheader(f"Total Monetized Emissions: ${total_usd_rounded:,}")
st.write("This number represents the total monetary value of emissions if they were monetized.")

# Horizontal divider before chart
st.markdown("---")

# Custom title for chart using company name
st.subheader(f"Monetised Emissions For {company_name}")

# Prepare data for grouped bar chart (separate vertical bars)
categories = ['Scope 1', 'Scope 2', 'Scope 3']
values = [total_scope1_usd, total_scope2_usd, total_scope3_usd]

# Plot grouped bar chart if there are any non-zero values
if sum(values) > 0:
    fig, ax = plt.subplots()

    # Create a grouped bar chart with separate bars for each scope category
    ax.bar(categories[0], values[0], label='Scope 1', color='blue')
    ax.bar(categories[1], values[1], label='Scope 2', color='orange')
    ax.bar(categories[2], values[2], label='Scope 3', color='green')

    # Add labels and title to the plot
    ax.set_ylabel('USD ($)')
    ax.set_title(f'Monetized Carbon Emissions Breakdown for {company_name}')
    ax.legend()

    # Display grouped bar chart in Streamlit
    st.pyplot(fig)

    # Close the figure after rendering it to avoid memory issues
    plt.close(fig)
else:
    st.write("No emissions data to display.")
