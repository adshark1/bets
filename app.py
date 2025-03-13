import streamlit as st
import pandas as pd

###############################################################################
# CONFIG & PAGE SETUP
###############################################################################
st.set_page_config(
    page_title="Adshark bets",
    layout="wide",  # you can choose "centered" if you prefer
)

st.title("Adshark bets")
st.write("Past bets/model performance below, future bets will be password protected.")

###############################################################################
# SIDEBAR INSTRUCTIONS
###############################################################################
with st.sidebar:
    st.header("Instructions")
    st.write(
        """
        1. If desired, **upload** a new CSV for each dataset to temporarily view updated data.
        2. To see **restricted columns** in the 'Future Data' tab, enter the password in the text box on that tab.
        3. Data changes made via uploads only persist **for the current session**. For permanent changes,
           update the CSV files in your GitHub repo and redeploy this app.
        """
    )
    st.info("Feel free to explore each tab above. Enjoy the data insights!")

###############################################################################
# UTILITY: FILE LOADER WITH FALLBACK
###############################################################################
def load_data(default_csv_path, upload_key):
    """
    Attempts to load data from an uploaded file widget (st.file_uploader).
    If no file is uploaded, falls back to the CSV at 'default_csv_path'.
    Returns a pandas DataFrame.
    """
    uploaded_file = st.file_uploader(
        f"Upload a CSV to override {default_csv_path}",
        type="csv",
        key=upload_key
    )
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_csv(default_csv_path)


###############################################################################
# CREATE TABS
###############################################################################
tab1, tab2, tab3, tab4 = st.tabs(["Past Games", "Future Games", "Yearly Performance", "Weekly Performance"])

###############################################################################
# TAB 1 - PAST DATA
###############################################################################
with tab1:
    st.header("Past Games")
    # Load 'past.csv'
    past_df = load_data("past.csv", "past_uploader")
    
    st.subheader("Historical Bet Results")
    st.dataframe(past_df, use_container_width=True)


###############################################################################
# TAB 2 - FUTURE DATA (WITH PASSWORD-PROTECTED COLUMNS)
###############################################################################
with tab2:
    st.header("Future Games")
    future_df = load_data("future.csv", "future_uploader")
    
    # Basic columns that are always visible
    public_cols = ["season", "week", "away_team", "home_team", "spread_line", "total_line"]
    
    # This is a sample set of restricted columns. Adjust these to match your actual dataset columns.
    # For example, maybe you want to hide "expected_value", "model_pick", "predicted_total", etc.
    restricted_cols = [col for col in future_df.columns if col not in public_cols]
    
    # Ask for password
    st.write("### Model Picks Restricted")
    password_input = st.text_input("Enter password to unlock restricted columns:", type="password")
    
    if password_input == st.secrets.get("PASSWORD"):
        st.success("Correct password! Displaying all columns.")
        st.dataframe(future_df, use_container_width=True)
    else:
        st.info(
            "Showing only public columns. "
            "Enter the correct password above to unlock restricted columns."
        )
        # Show only public columns
        st.dataframe(future_df[public_cols], use_container_width=True)


###############################################################################
# TAB 3 - MODEL PERFORMANCE SUMMARY
###############################################################################
with tab3:
    st.header("Yearly Model Performance Summary")
    perf_df = load_data("final_model_performance_summary.csv", "perf_uploader")
    
    st.subheader("Model's Performance by Year")
    st.dataframe(perf_df, use_container_width=True)


###############################################################################
# TAB 4 - BET SUMMARY BY SEASON/WEEK
###############################################################################
with tab4:
    st.header("Weekly Model Performance Summary")
    bet_df = load_data("bet_summary_by_season_week.csv", "bet_uploader")
    
    st.subheader("Model's Performance by Week")
    st.dataframe(bet_df, use_container_width=True)


###############################################################################
# END OF APP
###############################################################################
st.write("---")
