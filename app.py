import io
import numpy as np
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Toyomodec OFS India - Pipe Support Calculator",
    page_icon="⚙️",
    layout="wide",
)

# Custom CSS
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #0066cc !important;
        color: #ffffff !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #004b99 !important;
        color: #ffffff !important;
    }
    .metric-card {
        background-color: #1e293b;
        color: #f8fafc;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3b82f6;
        margin-bottom: 10px;
    }
    .metric-card h4 {
        color: #60a5fa !important;
        margin-bottom: 8px !important;
        font-size: 1.1rem !important;
    }
    .metric-card p {
        color: #cbd5e1 !important;
        margin: 0 !important;
        font-size: 0.95rem !important;
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


def get_span(size, material_or_group, service, insulated):
    mat_str = str(material_or_group).lower()
    if any(
        keyword in mat_str
        for keyword in ["ss", "stainless", "sdss", "dss", "group-2", "g2"]
    ):
        grp = "G2"
    else:
        grp = "G1"

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


# Header
st.sidebar.markdown("## 🏢 **Toyomodec OFS India**")
st.sidebar.markdown("---")
st.sidebar.info(
    "Engineering Automation Tool for Pipe Support Calculation (Table 5-1 & Fig 5-1)"
)

tab1, tab2 = st.tabs(
    ["🏠 Home & Guide", "🚀 Bulk Pipe Support Calculator"]
)

with tab1:
    st.title("⚙️ Toyomodec OFS India - Automatic Pipe Support System")
    st.subheader(
        "Calculate support counts based on Table 5-1 and Figure 5-1 Direction Change standards."
    )

    st.markdown("---")
    st.write("### 📋 Required columns in your Excel file:")

    template_df = pd.DataFrame(
        [
            {
                "Size": '2"',
                "Length": 60,
                "Material": "CS",
                "Service": "Liquid",
                "Insulation": "No",
                "Valves": 2,
                "Flanges": 1,
                "Elbows": 3,
                "Tees": 0,
            },
            {
                "Size": '8"',
                "Length": 120,
                "Material": "SDSS",
                "Service": "Gas",
                "Insulation": "Yes",
                "Valves": 0,
                "Flanges": 2,
                "Elbows": 5,
                "Tees": 0,
            },
        ]
    )

    st.table(template_df)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        template_df.to_excel(writer, index=False)

    st.download_button(
        label="📥 Download Sample Excel Template",
        data=buffer.getvalue(),
        file_name="Toyomodec_Sample_Pipe_MTO.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

with tab2:
    st.title("🚀 Bulk Pipe Support Calculator")
    uploaded_file = st.file_uploader(
        "Upload MTO File (.xlsx / .csv)", type=["xlsx", "csv"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)

            st.success("✅ File loaded successfully!")

            if st.button("📊 Calculate Supports Now"):
                col_map = {c.lower(): c for c in df.columns}

                size_col = col_map.get("size", df.columns[0])
                len_col = col_map.get("length", df.columns[1])
                mat_col = col_map.get("material", col_map.get("group", None))
                srv_col = col_map.get("service", None)
                ins_col = col_map.get("insulation", None)
                val_col = col_map.get("valves", None)
                flg_col = col_map.get("flanges", None)
                elb_col = col_map.get("elbows", col_map.get("elbow", None))
                tee_col = col_map.get("tees", col_map.get("tee", None))

                base_spans = []
                eff_spans = []
                base_supports_list = []
                total_supports_list = []

                for idx, row in df.iterrows():
                    sz = row[size_col]
                    mat = row[mat_col] if mat_col else "CS"
                    srv = row[srv_col] if srv_col else "Liquid"
                    ins = row[ins_col] if ins_col else "No"
                    length = float(pd.to_numeric(row[len_col], errors="coerce") or 0)

                    valves = float(pd.to_numeric(row[val_col] if val_col else 0, errors="coerce") or 0)
                    flanges = float(pd.to_numeric(row[flg_col] if flg_col else 0, errors="coerce") or 0)
                    elbows = float(pd.to_numeric(row[elb_col] if elb_col else 0, errors="coerce") or 0)
                    tees = float(pd.to_numeric(row[tee_col] if tee_col else 0, errors="coerce") or 0)

                    # 1. Base Span from Table 5-1
                    L = get_span(sz, mat, srv, ins)
                    base_spans.append(L)

                    # Estimated base count for reduction calculation
                    est_base_count = np.ceil(length / L) if L > 0 else 1

                    # 2. Figure 5-1 Adjustment (Effective Span)
                    if est_base_count > 0:
                        elbow_ratio = min(elbows / est_base_count, 1.0)
                        tee_ratio = min(tees / est_base_count, 1.0)
                        red_factor = 1.0 - (0.25 * elbow_ratio) - (0.30 * tee_ratio)
                        red_factor = max(red_factor, 0.70)
                    else:
                        red_factor = 1.0

                    effective_span = round(L * red_factor, 2)
                    eff_spans.append(effective_span)

                    # 3. Base Supports Count (Straight Pipe run without Valve/Flange)
                    base_sup = (np.ceil(length / effective_span) + 1) if effective_span > 0 else 0
                    base_supports_list.append(int(base_sup))

                    # 4. Total Supports Count (Including Valves & Flanges)
                    total_sup = base_sup + valves + (flanges * 0.5)
                    total_supports_list.append(total_sup)

                df["Base_Span_m"] = base_spans
                df["Effective_Span_m"] = eff_spans
                df["Base_Supports"] = base_supports_list
                df["Total_Supports"] = total_supports_list

                st.balloons()
                st.success("🎉 Calculation Complete with Base Supports & Total Supports!")

                # Summary
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Pipe Lines Processed", f"{len(df)}")
                m2.metric("Total Base Supports (Straight)", f"{int(df['Base_Supports'].sum())}")
                m3.metric("Total Supports (Final)", f"{int(df['Total_Supports'].sum())}")

                st.write("### 📋 Results Table:")
                st.dataframe(df)

                csv_data = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Calculated Result",
                    data=csv_data,
                    file_name="Toyomodec_Complete_Pipe_Supports.csv",
                    mime="text/csv",
                )

        except Exception as e:
            st.error(f"❌ Error in calculation: {e}")
