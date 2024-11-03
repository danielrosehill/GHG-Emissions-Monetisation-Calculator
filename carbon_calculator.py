import streamlit as st
import plotly.express as px

# Set up the page title and layout
st.set_page_config(page_title="Carbon Emissions Calculator", layout="centered")

# Title of the app
st.title("Impact Accounting Simulator: Monetised Emissions")

# Add an expander for "How To Use"
with st.expander("How To Use"):
    st.write("""
    Companies create significant environmental damage through their greenhouse gas emissions (GHG).
    These emissions are broken down into three scopes, reflecting different areas of operation.
    This calculator uses a monetization rate of **$236 per tonne of CO2e**, based on the social cost of carbon 
    suggested by the International Foundation for Valuing Impacts.
    """)

# Input field for company name
company_name = st.text_input("Enter Company Name", value="Acme Inc")

# Horizontal divider
st.markdown("---")

# Use tabs to separate input and results
tab1, tab2 = st.tabs(["Input Emissions Data", "Results"])

with tab1:
    # Input fields for Scope 1, Scope 2, and Scope 3 emissions with helper text and precision control
    st.header("Enter Emission Volumes")
    st.write("""
    Provide the scope 1, 2, and 3 emissions for the company whose data you are using. If you don't have one of these parameters, just leave it blank.
    Make sure to select the correct reporting unit!
    """)

    # Dropdown to select units (Tonnes or Millions of Tonnes)
    unit = st.selectbox("Select Unit", ["Tonnes of CO2e", "Millions of Tonnes of CO2e"])

    # Number inputs for Scope 1, Scope 2, and Scope 3 emissions
    scope1 = st.number_input("Scope 1 Emissions (Quantity)", min_value=0.0, value=0.00, format="%.2f",
                             help="Please enter the reported Scope 1 emissions.")
    scope2 = st.number_input("Scope 2 Emissions (Quantity)", min_value=0.0, value=0.00, format="%.2f",
                             help="Please enter the reported Scope 2 emissions.")
    scope3 = st.number_input("Scope 3 Emissions (Quantity)", min_value=0.0, value=0.00, format="%.2f",
                             help="Please enter the reported Scope 3 emissions.")

with tab2:
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

    # Display results with bold text and additional explanation text using HTML for better control over formatting
    st.subheader(f"**Total Monetized Emissions: ${total_usd_rounded:,}**")

    # Dynamic explanation for how the cost is calculated (without LaTeX)

    st.markdown("""
        <div style='font-size:18px'>
        The total monetary value is calculated by multiplying each emission type by $236 per tonne:
        </div>
        """, unsafe_allow_html=True)

    # Display individual calculations with escaped dollar signs in plain text and larger text size using HTML
    st.markdown(f"""
        <div style='font-size:18px'>
        - Scope 1: {scope1:.2f} tonnes * $236/tonne = ${total_scope1_usd:,.2f}<br>
        - Scope 2: {scope2:.2f} tonnes * $236/tonne = ${total_scope2_usd:,.2f}<br>
        - Scope 3: {scope3:.2f} tonnes * $236/tonne = ${total_scope3_usd:,.2f}
        </div>
        """, unsafe_allow_html=True)

    # Horizontal divider before chart
    st.markdown("---")


    # Prepare data for grouped bar chart (separate vertical bars)
    categories = ['Scope 1', 'Scope 2', 'Scope 3']
    values = [total_scope1_usd, total_scope2_usd, total_scope3_usd]

    # Plot interactive bar chart using Plotly if there are any non-zero values
    if sum(values) > 0:
        fig = px.bar(x=categories, y=values,
                     labels={'x': 'Emission Scopes', 'y': 'USD ($)'},
                     title=f'Monetized Carbon Emissions Breakdown for {company_name}',
                     color=categories)
        st.plotly_chart(fig)

        # Show percentage breakdowns as well (optional)
        total_emissions = sum(values)
        if total_emissions > 0:
            percentages = [v / total_emissions * 100 for v in values]
            st.write(f"Percentage Breakdown:")
            st.write(f"- Scope 1**: {percentages[0]:.2f}%")
            st.write(f"- **Scope 2**: {percentages[1]:.2f}%")
            st.write(f"- **Scope 3**: {percentages[2]:.2f}%")

    else:
        st.write("No emissions data to display.")
