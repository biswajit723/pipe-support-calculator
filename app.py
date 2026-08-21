import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Pipe Support Calculator", layout="wide")
st.title("⚙️ Bulk Pipe Support Calculator (Table 5-1 Rules)")

# Table 5-1 Span Data Matrix
span_matrix = {
    "3/4\"": {
        "G1_Liq_NI": 3.3,
        "G1_Liq_I": 2.1,
        "G1_Gas_NI": 3.8,
        "G1_Gas_I": 2.2,
        "G2_Liq_NI": 3.2,
        "G2_Liq_I": 2.0,
        "G2_Gas_NI": 3.8,
        "G2_Gas_I": 2.1,
    },
    "1\"": {
        "G1_Liq_NI": 3.3,
        "G1_Liq_I": 2.1,
        "G1_Gas_NI": 3.8,
        "G1_Gas_I": 2.2,
        "G2_Liq_NI": 3.2,
        "G2_Liq_I": 2.0,
        "G2_Gas_NI": 3.8,
        "G2_Gas_I": 2.1,
    },
    "1.1/2\"": {
        "G1_Liq_NI": 4.0,
        "G1_Liq_I": 2.8,
        "G1_Gas_NI": 4.7,
        "G1_Gas_I": 3.0,
        "G2_Liq_NI": 4.0,
        "G2_Liq_I": 2.5,
        "G2_Gas_NI": 4.8,
        "G2_Gas_I": 2.7,
    },
    "2\"": {
        "G1_Liq_NI": 4.6,
        "G1_Liq_I": 4.1,
        "G1_Gas_NI": 5.2,
        "G1_Gas_I": 4.2,
        "G2_Liq_NI": 4.5,
        "G2_Liq_I": 4.0,
        "G2_Gas_NI": 5.5,
        "G2_Gas_I": 4.6,
    },
    "3\"": {
        "G1_Liq_NI": 5.4,
        "G1_Liq_I": 5.0,
        "G1_Gas_NI": 6.5,
        "G1_Gas_I": 5.5,
        "G2_Liq_NI": 5.1,
        "G2_Liq_I": 4.8,
        "G2_Gas_NI": 6.5,
        "G2_Gas_I": 5.2,
    },
    "4\"": {
        "G1_Liq_NI": 6.1,
        "G1_Liq_I": 5.1,
        "G1_Gas_NI": 7.5,
        "G1_Gas_I": 5.5,
        "G2_Liq_NI": 5.5,
        "G2_Liq_I": 5.0,
        "G2_Gas_NI": 7.5,
        "G2_Gas_I": 5.5,
    },
    "6\"": {
        "G1_Liq_NI": 7.0,
        "G1_Liq_I": 5.8,
        "G1_Gas_NI": 9.0,
        "G1_Gas_I": 6.7,
        "G2_Liq_NI": 5.8,
        "G2_Liq_I": 4.5,
        "G2_Gas_NI": 9.2,
        "G2_Gas_I": 5.7,
    },
    "8\"": {
        "G1_Liq_NI": 7.8,
        "G1_Liq_I": 6.7,
        "G1_Gas_NI": 10.5,
        "G1_Gas_I": 8.0,
        "G2_Liq_NI": 6.5,
        "G2_Liq_I": 5.0,
        "G2_Gas_NI": 10.5,
        "G2_Gas_I": 6.5,
    },
    "10\"": {
        "G1_Liq_NI": 8.4,
        "G1_Liq_I": 7.2,
        "G1_Gas_NI": 11.5,
        "G1_Gas_I": 9.0,
        "G2_Liq_NI": 7.0,
        "G2_Liq_I": 5.5,
        "G2_Gas_NI": 12.0,
        "G2_Gas_I": 7.5,
    },
    "12\"": {
        "G1_Liq_NI": 9.0,
        "G1_Liq_I": 7.7,
        "G1_Gas_NI": 12.8,
        "G1_Gas_I": 9.7,
        "G2_Liq_NI": 7.3,
        "G2_Liq_I": 6.0,
        "G2_Gas_NI": 13.0,
        "G2_Gas_I": 8.2,
    },
    "14\"": {
        "G1_Liq_NI": 10.7,
        "G1_Liq_I": 9.2,
        "G1_Gas_NI": 15.0,
        "G1_Gas_I": 10.2,
        "G2_Liq_NI": 7.5,
        "G2_Liq_I": 6.2,
        "G2_Gas_NI": 17.5,
        "G2_Gas_I": 8.6,
    },
    "16\"": {
        "G1_Liq_NI": 11.0,
        "G1_Liq_I": 9.5,
        "G1_Gas_NI": 16.0,
        "G1_Gas_I": 11.5,
        "G2_Liq_NI": 7.7,
        "G2_Liq_I": 6.5,
        "G2_Gas_NI": 14.5,
        "G2_Gas_I": 9.5,
    },
    "18\"": {
        "G1_Liq_NI": 11.5,
        "G1_Liq_I": 10.5,
        "G1_Gas_NI": 17.0,
        "G1_Gas_I": 12.2,
        "G2_Liq_NI": 7.8,
        "G2_Liq_I": 6.7,
        "G2_Gas_NI": 15.5,
        "G2_Gas_I": 10.0,
    },
    "20\"": {
        "G1_Liq_NI": 11.5,
        "G1_Liq_I": 11.0,
        "G1_Gas_NI": 18.0,
        "G1_Gas_I": 13.0,
        "G2_Liq_NI": 8.4,
        "G2_Liq_I": 7.2,
        "G2_Gas_NI": 16.5,
        "G2_Gas_I": 11.0,
    },
    "24\"": {
        "G1_Liq_NI": 12.0,
        "G1_Liq_I": 11.0,
        "G1_Gas_NI": 19.0,
        "G1_Gas_I": 14.0,
        "G2_Liq_NI": 9.0,
        "G2_Liq_I": 8.0,
        "G2_Gas_NI": 18.0,
        "G2_Gas_I": 12.5,
    },
}


def get_span(size, group, service, insulated):
    grp = "G1" if "1" in str(group) else "G2"
    srv = "Liq" if "liquid" in str(service).lower() else "Gas"
    ins = (
        "I"
        if "yes" in str(insulated).lower() or "insulated" in str(insulated).lower()
        else "NI"
    )

    key = f"{grp}_{srv}_{ins}"
    size_str = str(size).strip()
    if not size_str.endswith('"'):
        size_str += '"'

    return span_matrix.get(size_str, {}).get(key, 6.0)


uploaded_file = st.file_uploader("Upload MTO Excel File", type=["xlsx", "csv"])

if uploaded_file:
    df = (
        pd.read_excel(uploaded_file)
        if uploaded_file.name.endswith(".xlsx")
        else pd.read_csv(uploaded_file)
    )

    if st.button("🚀 Calculate All Pipe Supports"):
        spans = []
        for _, row in df.iterrows():
            s = get_span(
                row.get("Size", '2"'),
                row.get("Group", "Group-1"),
                row.get("Service", "Liquid"),
                row.get("Insulation", "No"),
            )
            spans.append(s)

        df["Allowable_Span_m"] = spans
        df["Base_Supports"] = np.ceil(df["Length"] / df["Allowable_Span_m"]) + 1

        valves = df["Valves"] if "Valves" in df.columns else 0
        flanges = df["Flanges"] if "Flanges" in df.columns else 0

        df["Total_Supports"] = df["Base_Supports"] + valves + (flanges * 0.5)

        st.success("✅ হাজার হাজার লাইনের গণনা এক ক্লিকে সম্পন্ন হয়েছে!")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Calculated File (CSV)",
            data=csv,
            file_name="Calculated_MTO_Supports.csv",
        )
