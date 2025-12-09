import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="FEMA Disaster Relief Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("fema_sample.csv", low_memory=False)
    df["repairAmount"] = pd.to_numeric(df["repairAmount"], errors="coerce").fillna(0)
    df["tsaEligible"] = pd.to_numeric(df["tsaEligible"], errors="coerce")
    return df

df = load_data()



def main():
    st.title("FEMA Disaster Relief Dashboard")
    st.write("Exploring repair assistance and TSA eligibility for disaster survivors.")

    # Load data once, cached by Streamlit
    df = load_data()

    # -----------------------------
    # Data Preview
    # -----------------------------
    st.subheader("Data Preview")
    st.write(df.head())

    # -----------------------------
    # Histogram of Repair Amount
    # -----------------------------
    st.subheader("Histogram of Repair Amount")

    fig_hist = px.histogram(
        df,
        x="repairAmount",
        nbins=30,
        title="Distribution of Repair Amounts",
        labels={"repairAmount": "Repair Amount (USD)"}
    )

    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown(
        """
        **Insight:** Most households have low or zero repair assistance,
        with a smaller number receiving much larger amounts. This creates
        a right-skewed distribution of repair funding.
        """
    )

    # -----------------------------
    # Boxplot of Repair Amount by TSA Eligibility
    # -----------------------------
    st.subheader("Boxplot: Repair Amount by TSA Eligibility")

    # Filter to valid TSA labels (0/1)
    df_box = df[df["tsaEligible"].isin([0, 1])].copy()
    df_box["tsaEligibleLabel"] = df_box["tsaEligible"].map(
        {0: "0 - Not Eligible", 1: "1 - Eligible"}
    )

    fig_box = px.box(
        df_box,
        x="tsaEligibleLabel",
        y="repairAmount",
        title="Repair Amount by TSA Eligibility",
        labels={
            "tsaEligibleLabel": "TSA Eligible (1 = Yes, 0 = No)",
            "repairAmount": "Repair Amount (USD)"
        }
    )

    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown(
        """
        **Insight:** TSA-eligible households tend to receive higher repair
        amounts and show a wider spread of repair funding than non-eligible
        households, which matches the inferential statistics in the report.
        """
    )

    st.markdown("---")
    st.caption("INFO 450 – FEMA Disaster Relief Project")


if __name__ == "__main__":
    main()
