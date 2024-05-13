import streamlit as st
import pandas as pd
import numpy as np
from data_reader import DataReader
from make_stats import MakeStats
import matplotlib.pyplot as plt
from streamlit_extras.add_vertical_space import add_vertical_space
import os
from datetime import datetime


plt.style.use('seaborn-v0_8-pastel')
st.set_page_config(
    page_title = "Trading report",
    page_icon = "📈",
    layout = "wide"
)


# Adding line to sidebar
with st.sidebar:
    st.write("")


# Title of page
st.subheader("Report Generator 📄", divider="blue")


# Container with data settings
container_input = st.container(border=True)
left_input, right_input = container_input.columns(2)


# Configuring the left input column
with left_input:
    uploaded_file = st.file_uploader("Upload file")
    
    
# Configuring the right column
with right_input:
    # DataFrame for renaming columns for user data
    header_settings = st.data_editor(
        pd.DataFrame({"System columns": ["Symbol", "Type", "Lots", "Open time", "Close time", "Net profit"],
                      "User columns": ["", "", "", "", "", ""]}),
        use_container_width=True,
        disabled=("System columns",),
        hide_index=True
    )
    # Choosing a date format in dataset
    date_format = st.selectbox("Date format", ["%d.%m.%Y %H:%M:%S", "%d.%m.%Y %H:%M",
                                               "%d-%m-%Y %H:%M:%S", "%d-%m-%Y %H:%M"])

    # Balance input
    balance = st.number_input("Balance account", min_value=0.00, placeholder="Balance")
    
   
# Button to start generating report
btn_start = st.button("Generate")

# Objects for data reader and making statistics
data_reader = DataReader()
make_stats = MakeStats()

# Generating a report
if btn_start:
    
    # Run if file was uploaded and it is a csv format
    if uploaded_file is not None:
        if os.path.splitext(uploaded_file.name)[1] != ".csv":
            st.error("Need .csv file format")
            st.stop()
        
        # Get column name for rename
        header_settings = header_settings[header_settings["User columns"] != ""]
        new_header = dict(header_settings[["User columns", "System columns"]].values)
        
        try:
            df_data = data_reader.load_file(uploaded_file)
            df_data = data_reader.rename_header(df_data, new_header)
            df_data = data_reader.format_data_frame(df_data, date_format, balance)

        except pd.errors.ParserError:
            st.error("File Reading Error")
            st.stop()

        except ValueError:
            st.error("Value Error")
            st.stop()

        except Exception as e:
            st.error("Unknown Error")
            st.stop()
            
            
        with st.spinner("Generating..."):
            st.dataframe(df_data, use_container_width=True, hide_index=True)
            add_vertical_space(3)
            st.subheader("Statistics 📊", divider="blue")
            
            profit_stats       = make_stats.get_profit_stats(df_data)
            week_data          = make_stats.score_by_week_day(df_data)
            win_rate = make_stats.get_win_rate(df_data)
            duration_time      = make_stats.get_transtions_duration(df_data)
            symbols          = make_stats.get_assets(df_data)
            transations_type = make_stats.get_operations_type(df_data)
            lots             = make_stats.get_lot_amount(df_data)
            df_size                  = make_stats.get_transations_number(df_data)
            
            # ----------------- # 
            
            # Columns for stats
            container_first = st.container()
            left_first, right_first = container_first.columns(2)
            
            # Net profit in time
            with left_first:
                st.pyplot(make_stats.plot_line(df_data["Net profit"],
                                                "Transation number", "Net profit", 
                                                "Net profit in time"))
                
            # Accumulated net profit    
            with right_first:
                st.pyplot(make_stats.plot_line(np.cumsum(df_data["Net profit"]),
                                                "Transation number", "Accumulated net profit", 
                                                "Accumulated net profit in time"))
                
            # ----------------- # 
            
            container_second = st.container()
            left_second, right_second = container_second.columns(2)
            
            # Balance in time
            with left_second:
                st.pyplot(make_stats.plot_line(df_data["Balance"],
                                                "Transation number", "Balance", 
                                                "Balance value in time"))
            
            # Profit in table
            with right_second:
                add_vertical_space(2)
                st.write("Stats - Net profit")
                st.data_editor(profit_stats, use_container_width=True, hide_index=True, disabled=True)

                add_vertical_space(0)
                st.write("Stats - Week net profit")
                st.data_editor(week_data, use_container_width=True, disabled=True)
                           
            # ----------------- # 
            
            container_third = st.container()
            left_third, right_third = container_third.columns(2)
            
            # Win rate
            with left_third:
                st.pyplot(make_stats.plot_bars(pd.Series(win_rate, index=["Win", "Loss"]),
                                                "Percent %", "Status", 
                                                "Win/Loss rate", "h"))
                
            # Profit by week day
            with right_third:
                st.pyplot(make_stats.plot_bars(week_data[["Min", "Max", "Sum"]],
                                                "Week day", "Net profit", 
                                                "Stats - Week net profit", "v"))
                
            # ----------------- #
            
            # Duration time
            fig_dur, ax_dur = plt.subplots(figsize=(12, 4), dpi=3000)
            df_data["Deltatime"].plot.bar(ax=ax_dur).grid(True, alpha=0.25)
            ax_dur.set_title("Time duration on single transation")
            ax_dur.set_ylabel("Time [minute]")
            ax_dur.set_xlabel("Transation", labelpad=10)
            
            # Make space between x ticks
            if df_size > 50:
                ax_dur.set_xticks(range(0, df_size, df_size//10))
            st.pyplot(fig_dur)
            st.data_editor(duration_time, use_container_width=True, hide_index=True, disabled=True)
            
            st.divider()
            
            # ----------------- #
            
            container_fourth = st.container()
            left_fourth, mid_fourth, right_fourth = container_fourth.columns(3)  
            
            top_value = 5
            # Symbol stats
            with left_fourth:
                st.pyplot(make_stats.plot_pie(symbols.iloc[:top_value], "Assets"))
                st.data_editor(symbols.reset_index().rename(columns={"count": "Count"}).iloc[:top_value], 
                               use_container_width=True, hide_index=True, disabled=True)
                
            # Type transation stats
            with mid_fourth:
                st.pyplot(make_stats.plot_pie(transations_type.iloc[:top_value], "Type"))
                st.data_editor(transations_type.reset_index().rename(columns={"count": "Count"}).iloc[:top_value], 
                               use_container_width=True, hide_index=True, disabled=True)
                
            # Lots stats
            with right_fourth:
                st.pyplot(make_stats.plot_pie(lots.iloc[:top_value], "Lots"))
                st.data_editor(lots.reset_index().rename(columns={"count": "Count"}).iloc[:top_value], 
                               use_container_width=True, hide_index=True, disabled=True)
                
            add_vertical_space(5)
            
    else:
        st.error("No file")