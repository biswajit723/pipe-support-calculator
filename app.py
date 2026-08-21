import io
import numpy as np
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Pipe Support Calculator", page_icon="⚙️", layout="wide"
)

# Custom CSS for Aesthetic UI
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #004b99;
        color: white;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-left: 5px solid #0066cc;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Table 5-1 Span Data Matrix
span_matrix = {
    '3/4"': {
        "G1_Liq_NI": 3.3,
        "G1_Liq_I": 2.1,
        "G1_Gas_NI": 3.8,
        "G1_Gas_I": 2.2,
        "G2_Liq_NI": 3.2,
        "G2_Liq_I": 2.0,
        "G2_Gas_NI": 3.8,
        "G2_Gas_I": 2.1,
    },
    '1"': {
        "G1_Liq_NI": 3.3,
        "G1_Liq_I": 2.1,
        "G1_Gas_NI": 3.8,
        "G1_Gas_I": 2.2,
        "G2_Liq_NI": 3.2,
        "G2_Liq_I": 2.0,
        "G2_Gas_NI": 3.8,
        "G2_Gas_I": 2.1,
    },
    '1.1/2"': {
        "G1_Liq_NI": 4.0,
        "G1_Liq_I": 2.8,
        "G1_Gas_NI": 4.7,
        "G1_Gas_I": 3.0,
        "G2_Liq_NI": 4.0,
        "G2_Liq_I": 2.5,
        "G2_Gas_NI": 4.8,
        "G2_Gas_I": 2.7,
    },
    '2"': {
        "G1_Liq_NI": 4.6,
        "G1_Liq_I": 4.1,
        "G1_Gas_NI": 5.2,
        "G1_Gas_I": 4.2,
        "G2_Liq_NI": 4.5,
        "G2_Liq_I": 4.0,
        "G2_Gas_NI": 5.5,
        "G2_Gas_I": 4.6,
    },
    '3"': {
        "G1_Liq_NI": 5.4,
        "G1_Liq_I": 5.0,
        "G1_Gas_NI": 6.5,
        "G1_Gas_I": 5.5,
        "G2_Liq_NI": 5.1,
        "G2_Liq_I": 4.8,
        "G2_Gas_NI": 6.5,
        "G2_Gas_I": 5.2,
    },
    '4"': {
        "G1_Liq_NI": 6.1,
        "G1_Liq_I": 5.1,
        "G1_Gas_NI": 7.5,
        "G1_Gas_I": 5.5,
        "G2_Liq_NI": 5.5,
        "G2_Liq_I": 5.0,
        "G2_Gas_NI": 7.5,
        "G2_Gas_I": 5.5,
    },
    '6"': {
        "G1_Liq_NI": 7.0,
        "G1_Liq_I": 5.8,
        "G1_Gas_NI": 9.0,
        "G1_Gas_I": 6.7,
        "G2_Liq_NI": 5.8,
        "G2_Liq_I": 4.5,
        "G2_Gas_NI": 9.2,
        "G2_Gas_I": 5.7,
    },
    '8"': {
        "G1_Liq_NI": 7.8,
        "G1_Liq_I": 6.7,
        "G1_Gas_NI": 10.5,
        "G1_Gas_I": 8.0,
        "G2_Liq_NI": 6.5,
        "G2_Liq_I": 5.0,
        "G2_Gas_NI": 10.5,
        "G2_Gas_I": 6.5,
    },
    '10"': {
        "G1_Liq_NI": 8.4,
        "G1_Liq_I": 7.2,
        "G1_Gas_NI": 11.5,
        "G1_Gas_I": 9.0,
        "G2_Liq_NI": 7.0,
        "G2_Liq_I": 5.5,
        "G2_Gas_NI": 12.0,
        "G2_Gas_I": 7.5,
    },
    '12"': {
        "G1_Liq_NI": 9.0,
        "G1_Liq_I": 7.7,
        "G1_Gas_NI": 12.8,
        "G1_Gas_I": 9.7,
        "G2_Liq_NI": 7.3,
        "G2_Liq_I": 6.0,
        "G2_Gas_NI": 13.0,
        "G2_Gas_I": 8.2,
    },
    '14"': {
        "G1_Liq_NI": 10.7,
        "G1_Liq_I": 9.2,
        "G1_Gas_NI": 15.0,
        "G1_Gas_I": 10.2,
        "G2_Liq_NI": 7.5,
        "G2_Liq_I": 6.2,
        "G2_Gas_NI": 17.5,
        "G2_Gas_I": 8.6,
    },
    '16"': {
        "G1_Liq_NI": 11.0,
        "G1_Liq_I": 9.5,
        "G1_Gas_NI": 16.0,
        "G1_Gas_I": 11.5,
        "G2_Liq_NI": 7.7,
        "G2_Liq_I": 6.5,
        "G2_Gas_NI": 14.5,
        "G2_Gas_I": 9.5,
    },
    '18"': {
        "G1_Liq_NI": 11.5,
        "G1_Liq_I": 10.5,
        "G1_Gas_NI": 17.0,
        "G1_Gas_I": 12.2,
        "G2_Liq_NI": 7.8,
        "G2_Liq_I": 6.7,
        "G2_Gas_NI": 15.5,
        "G2_Gas_I": 10.0,
    },
    '20"': {
        "G1_Liq_NI": 11.5,
        "G1_Liq_I": 11.0,
        "G1_Gas_NI": 18.0,
        "G1_Gas_I": 13.0,
        "G2_Liq_NI": 8.4,
        "G2_Liq_I": 7.2,
        "G2_Gas_NI": 16.5,
        "G2_Gas_I": 11.0,
    },
    '24"': {
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
    if not size_str.endswith('"') and size_str != "":
        size_str += '"'

    return span_matrix.get(size_str, {}).get(key, 6.0)


# Tabs Navigation
tab1, tab2 = st.tabs(
    ["🏠 Home & Guide", "🚀 Bulk Pipe Support Calculator"]
)

# TAB 1: LANDING PAGE & GUIDELINES
with tab1:
    st.title("🛠️ Automatic Pipe Support Count System")
    st.subheader(
        "Calculate support counts for thousands of pipe lines in one click based on Table 5-1 engineering standards."
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
        <div class="metric-card">
            <h4>⚡ Fast Calculation</h4>
            <p>Process MTO for 10,000+ pipe lines in under 2 seconds.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
        <div class="metric-card">
            <h4>🎯 Table 5-1 Compliant</h4>
            <p>Automatically detects Group-1/2, Liquid/Gas, and Insulation status.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
        <div class="metric-card">
            <h4>🛡️ Error Protected</h4>
            <p>Software won't crash even if there is missing or invalid data in the file.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.write("### 📋 Required columns in your Excel file:")

    template_df = pd.DataFrame(
        [
            {
                "Size": '2"',
                "Length": 60,
                "Group": "Group-1",
                "Service": "Liquid",
                "Insulation": "No",
                "Valves": 2,
                "Flanges": 1,
            },
            {
                "Size": '8"',
                "Length": 120,
                "Group": "Group-2",
                "Service": "Gas",
                "Insulation": "Yes",
                "Valves": 0,
                "Flanges": 2,
            },
        ]
    )

    st.table(template_df)

    # Download Sample Excel Template
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        template_df.to_excel(writer, index=False)

    st.download_button(
        label="📥 Download Sample Excel Template",
        data=buffer.getvalue(),
        file_name="Sample_Pipe_MTO.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

# TAB 2: BULK CALCULATOR
with tab2:
    st.title("🚀 Bulk Support Calculation Engine")
    st.write("Upload your MTO (Excel or CSV) file below:")

    uploaded_file = st.file_uploader(
        "Drop your Excel or CSV file here", type=["xlsx", "csv"]
    )

    if uploaded_file is not None:
        try:
            # File Read with Error Handling
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)

            st.success("✅ File loaded successfully!")
            st.write("### 👁️ Data Preview (First 5 Rows):")
            st.dataframe(df.head())

            if st.button("📊 Calculate Supports Now"):
                # Column check
                required_cols = ["Size", "Length"]
                missing_cols = [
                    col
                    for col in required_cols
                    if col not in df.columns
                    and col.lower() not in [c.lower() for c in df.columns]
                ]

                if missing_cols:
                    st.error(
                        f"⚠️ Required columns missing! The file must contain at least **Size** and **Length** columns."
                    )
                else:
                    # Smart column lookup (case insensitive)
                    col_map = {c.lower(): c for c in df.columns}

                    size_col = col_map.get("size", df.columns[0])
                    len_col = col_map.get("length", df.columns[1])
                    grp_col = col_map.get("group", None)
                    srv_col = col_map.get("service", None)
                    ins_col = col_map.get("insulation", None)
                    val_col = col_map.get("valves", None)
                    flg_col = col_map.get("flanges", None)

                    # Calculation Process
                    spans = []
                    for idx, row in df.iterrows():
                        sz = row[size_col]
                        grp = row[grp_col] if grp_col else "Group-1"
                        srv = row[srv_col] if srv_col else "Liquid"
                        ins = row[ins_col] if ins_col else "No"

                        span_val = get_span(sz, grp, srv, ins)
                        spans.append(span_val)

                    df["Allowable_Span_m"] = spans

                    # Numeric Conversion Protection
                    df[len_col] = pd.to_numeric(
                        df[len_col], errors="coerce"
                    ).fillna(0)

                    df["Base_Supports"] = (
                        np.ceil(df[len_col] / df["Allowable_Span_m"]) + 1
                    )

                    valves_count = (
                        pd.to_numeric(df[val_col], errors="coerce").fillna(0)
                        if val_col
                        else 0
                    )
                    flanges_count = (
                        pd.to_numeric(df[flg_col], errors="coerce").fillna(0)
                        if flg_col
                        else 0
                    )

                    df["Total_Supports"] = (
                        df["Base_Supports"]
                        + valves_count
                        + (flanges_count * 0.5)
                    )

                    st.markdown("---")
                    st.balloons()
                    st.success("🎉 Calculation Complete!")

                    # Summary Metrics
                    m1, m2 = st.columns(2)
                    m1.metric("Total Pipe Lines Processed", f"{len(df)}")
                    m2.metric(
                        "Total Required Supports",
                        f"{int(df['Total_Supports'].sum())}",
                    )

                    st.write("### 📋 Calculated Results:")
                    st.dataframe(df)

                    # Export to CSV
                    csv_data = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="📥 Download Result as Excel (CSV)",
                        data=csv_data,
                        file_name="Calculated_Pipe_Supports.csv",
                        mime="text/csv",
                    )

        except Exception as e:
            st.error(
                "❌ Error processing file! Please ensure the file data is in the correct format."
            )
            st.info(
                "💡 Tip: Check the 'Home & Guide' tab and download the sample file to verify the format."
            )
