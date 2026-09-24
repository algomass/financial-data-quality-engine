import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

def load_data():
    """
    Connect to SQLite and retrieve both valid and error datasets.
    """
    conn = sqlite3.connect('financial_data.db')
    try:
        valid_df = pd.read_sql_query("SELECT * FROM valid_transactions", conn)
        error_df = pd.read_sql_query("SELECT * FROM dq_error_log", conn)
    except Exception as e:
        st.error(f"Database error: {e}. Please ensure previous steps were executed.")
        valid_df = pd.DataFrame()
        error_df = pd.DataFrame()
    finally:
        conn.close()
        
    return valid_df, error_df

def main():
    st.set_page_config(page_title="DQ Engine Dashboard", layout="wide")
    st.title("Financial Data Quality Engine 📊")
    st.markdown("Monitoraggio in tempo reale della qualità del dato sulle transazioni in ingresso.")
    
    # Load data from the Data Warehouse (SQLite)
    valid_df, error_df = load_data()
    
    if valid_df.empty and error_df.empty:
        st.warning("Nessun dato trovato nel database.")
        return
        
    total_records = len(valid_df) + len(error_df)
    valid_records = len(valid_df)
    error_records = len(error_df)
    
    st.markdown("---")
    
    # ---------------------------------------------------------
    # 1. Key Performance Indicators (KPIs)
    # ---------------------------------------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions Analyzed", total_records)
    col2.metric("Valid Records (Passed)", valid_records)
    col3.metric("Invalid Records (Rejected)", error_records)
    
    st.markdown("---")
    
    # ---------------------------------------------------------
    # 2. Visualizations
    # ---------------------------------------------------------
    st.subheader("Data Quality Error Distribution")
    if not error_df.empty:
        # Grouping by error_reason to count occurrences
        error_counts = error_df['error_reason'].value_counts().reset_index()
        error_counts.columns = ['Error Reason', 'Count']
        
        # We use Altair to force the x-axis labels to be horizontal (labelAngle=0)
        # while keeping the bars vertical. We also hide the axis title for a cleaner look.
        chart = alt.Chart(error_counts).mark_bar().encode(
            x=alt.X('Error Reason', axis=alt.Axis(labelAngle=0, labelOverlap=False, title=None)),
            y=alt.Y('Count', axis=alt.Axis(title='Numero di Record'))
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.success("Tutti i dati sono validi. Nessun errore rilevato!")
        
    st.markdown("---")
    
    # ---------------------------------------------------------
    # 3. Data Explorer (Tabs)
    # ---------------------------------------------------------
    st.subheader("Database Explorer")
    tab1, tab2 = st.tabs(["✅ Valid Transactions", "🚨 DQ Error Log"])
    
    with tab1:
        st.write(f"Showing **{valid_records}** clean records ready for downstream systems.")
        st.dataframe(valid_df, use_container_width=True)
        
    with tab2:
        st.write(f"Showing **{error_records}** records that failed one or more Data Quality rules.")
        st.dataframe(error_df, use_container_width=True)

if __name__ == "__main__":
    main()
