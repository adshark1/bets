import streamlit as st
import pandas as pd

###############################################################################
# CONFIG & PAGE SETUP
###############################################################################
st.set_page_config(
    page_title="adshark bets",
    layout="centered",  # you can choose "centered" if you prefer
)

st.title("adshark bets")
st.write("Created by @adshark_. Past bets/model performance below, future bets are password protected.")

###############################################################################
# UTILITY: FILE LOADER WITHOUT UPLOADER
###############################################################################
def load_data(csv_path):
    """
    Loads data from the specified CSV path and returns a pandas DataFrame.
    """
    return pd.read_csv(csv_path)

###############################################################################
# CREATE TABS (now includes a 'Home' tab)
###############################################################################
tab_home, tab1, tab2, tab3, tab4 = st.tabs([
    "Home",
    "Past Games",
    "Future Games",
    "Yearly Performance",
    "Weekly Performance"
])

###############################################################################
# HOME TAB - WELCOME MESSAGE
###############################################################################
with tab_home:
    st.header("Welcome to adshark's NFL Model Dashboard!")
    st.write(
        """
        All model stats and historical game picks are available to freely look through,
        but future game predictions are password protected. I'll be sharing the password 
        on my Twitter @adshark_ for the first couple weeks, so come check it out. 
        See you in Week 1!  
        
        **Last season's performance:**  
        - 58.3% ATS (56-40-3 +12u)
        - 70.2% on totals (198-84-3 +105.6u)
        - 67.2% overall (254-124-6 +117.6u)
        """
    )

###############################################################################
# TAB 1 - PAST DATA
###############################################################################
with tab1:
    st.header("Past Games")
    # Load 'past.csv'
    past_df = load_data("past.csv")
    
    st.subheader("Historical Bet Results")
    st.dataframe(past_df, use_container_width=True)

###############################################################################
# TAB 2 - FUTURE DATA (WITH PASSWORD-PROTECTED COLUMNS)
###############################################################################
with tab2:
    st.header("Future Games")
    future_df = load_data("future.csv")
    
    # Basic columns that are always visible
    public_cols = ["season", "week", "away_team", "home_team", "spread_line", "total_line"]
    
    # Example restricted columns
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
    perf_df = load_data("final_model_performance_summary.csv")
    
    st.subheader("Model's Performance by Year")
    st.dataframe(perf_df, use_container_width=True)

###############################################################################
# TAB 4 - BET SUMMARY BY SEASON/WEEK
###############################################################################
with tab4:
    st.header("Weekly Model Performance Summary")
    bet_df = load_data("bet_summary_by_season_week.csv")
    
    st.subheader("Model's Performance by Week")
    st.dataframe(bet_df, use_container_width=True)

###############################################################################
# END OF APP
###############################################################################
st.write("---")
