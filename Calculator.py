import streamlit as st
import pandas as pd
import math

# Load preset databases
flange_df = pd.read_csv("FlangeWidth_LipLength_converter.csv")
gauge_df = pd.read_csv("gauge_thickness_converter.csv")

# Title
st.title("Galvanized Steel Calculator")

# Create 2 columns
col1, spacer, col2 = st.columns([1, 0.1, 1])

# --- User Inputs ---
with col1:
	st.header("Inputs")
	shape = st.selectbox("Shape", ["C Stud/C Joist", "U Stud/Track"])
	member_depth = st.number_input("Member Depth (inches)", min_value=0.0, step=0.1, value=6.0)
	flange_width = st.selectbox("Flange Width (inches)", sorted(flange_df['Flange Width'].unique()))
	gauge = st.selectbox("Gauge (ga)", sorted(gauge_df['Gauge'].unique()))
	outside_diameter = st.number_input("Outside Diameter (inches)", min_value=0.0, step=1.0, value=50)
	st.markdown("Inside Diameter: 20.0 inches (fixed)")
	cwt_price = st.number_input("CWT Price (USD)", min_value=0.0, step=0.01, value=50)

# --- Lookups ---
# Lip Length
if shape == "C Stud/C Joist":
    lip_length = float(flange_df.loc[flange_df['Flange Width'] == flange_width, 'Lip Length'].values[0])
else:
    lip_length = 0.0
# Thickness
thickness = float(gauge_df.loc[gauge_df['Gauge'] == gauge, 'Thickness'].values[0])

# --- Calculations ---
if shape == "C Stud/C Joist":
    coil_width = member_depth + 2 * flange_width + 2 * lip_length - 8 * thickness
else:
    coil_width = member_depth + 2 * flange_width - 4 * thickness

material_length = math.pi * ((outside_diameter ** 2 - 20 ** 2)) / 48 / thickness  # feet

area = material_length * thickness / 12  # sq feet

piw = 467.26 / (50 ** 2 - 20 ** 2) * (outside_diameter ** 2 - 20 ** 2)  # lbs

weight = piw * coil_width  # lbs

price_per_coil = cwt_price * weight / 100  # USD

price_per_linear_ft = price_per_coil / material_length if material_length else 0.0  # USD

price_per_sqft = price_per_linear_ft / coil_width * 12 if coil_width else 0.0  # USD

# --- Display Outputs ---
with col2:
	st.header("Outputs")
	st.write(f"**Lip Length:** {lip_length:.3f} in")
	st.write(f"**Thickness:** {thickness:.4f} in")
	st.write(f"**Coil Width:** {coil_width:.3f} in")
	st.write(f"**Material Length:** {material_length:.2f} ft")
	st.write(f"**Area:** {area:.2f} sq ft")
	st.write(f"**PIW:** {piw:.2f} lbs")
	st.write(f"**Weight:** {weight:.2f} lbs")
	st.write(f"**Price/Coil:** ${price_per_coil:.2f}")
	st.write(f"**Price/Linear Ft:** ${price_per_linear_ft:.4f}")
	st.write(f"**Price/Sqft:** ${price_per_sqft:.4f}")
