import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="GeoThermal Power PLC Dashboard", layout="wide")

# Dashboard title
st.title("⚡ GeoThermal Power PLC Dashboard")
st.markdown("#### Geothermal Energy Production & Operational Analytics | 2023 – 2025")
st.markdown("---")

# Load data - Power generation data
@st.cache_data
def load_generation_data():
    np.random.seed(42)
    
    # Power plants
    plants = [
        "Olkaria I Geothermal Plant", "Olkaria II Geothermal Plant", "Olkaria III Geothermal Plant",
        "Olkaria IV Geothermal Plant", "Olkaria V Geothermal Plant", "Menengai Geothermal Plant",
        "Suswa Geothermal Plant", "Baringo-Silali Geothermal Plant", "Eburru Geothermal Plant",
        "Longonot Geothermal Plant", "Akiira Geothermal Project", "Paka Geothermal Field"
    ]
    
    years = [2023, 2024, 2025]
    months = list(range(1, 13))
    
    data = []
    
    for year in years:
        growth = 1 + (year - 2023) * 0.18  # 18% annual growth
        
        for plant in plants:
            # Base capacity (MW)
            if "Olkaria" in plant:
                base_capacity = np.random.uniform(70, 140)
            elif plant in ["Menengai Geothermal Plant", "Suswa Geothermal Plant"]:
                base_capacity = np.random.uniform(35, 80)
            else:
                base_capacity = np.random.uniform(20, 50)
            
            for month in months:
                # Seasonal variation (higher production in dry months)
                seasonal_factor = 1 + 0.15 * np.sin(np.radians((month - 3) * 30))
                
                # Capacity factor (utilization rate)
                capacity_factor = np.random.uniform(0.75, 0.92) * growth * seasonal_factor
                capacity_factor = min(capacity_factor, 0.96)
                
                # Actual generation (MW)
                generation_mw = base_capacity * capacity_factor
                
                # Maintenance downtime (%)
                if month in [2, 9]:  # Maintenance months
                    downtime = np.random.uniform(3, 8)
                else:
                    downtime = np.random.uniform(0.5, 2)
                
                # Energy produced (MWh) - 24 hours * days in month
                days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]
                if year == 2024:
                    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]
                
                energy_mwh = generation_mw * 24 * days_in_month * (1 - downtime/100)
                
                # Steam temperature (°C)
                steam_temp = np.random.uniform(180, 220) + (year - 2023) * 2
                
                # Wellhead pressure (bar)
                pressure_bar = np.random.uniform(8, 14) + (year - 2023) * 0.3
                
                data.append({
                    "Year": year,
                    "Month": month,
                    "Month_Name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][month-1],
                    "Plant": plant,
                    "Installed_Capacity_MW": round(base_capacity, 1),
                    "Actual_Generation_MW": round(generation_mw, 1),
                    "Capacity_Factor": round(capacity_factor * 100, 1),
                    "Downtime_Percentage": round(downtime, 1),
                    "Energy_Produced_MWh": round(energy_mwh, 0),
                    "Steam_Temperature_C": round(steam_temp, 1),
                    "Wellhead_Pressure_Bar": round(pressure_bar, 1),
                    "CO2_Saved_Tons": round(energy_mwh * 0.4, 0)  # 0.4 tons CO2 saved per MWh vs fossil fuels
                })
    
    return pd.DataFrame(data)

# Financial data
@st.cache_data
def load_financial_data():
    years = [2023, 2024, 2025]
    
    financial_data = []
    
    for year in years:
        growth = 1 + (year - 2023) * 0.18
        
        # Revenue streams (KES Millions)
        energy_sales = 4500 * growth * np.random.uniform(0.95, 1.05)
        carbon_credits = 350 * growth * np.random.uniform(0.9, 1.1)
        government_subsidies = 200 * growth * np.random.uniform(0.9, 1.1)
        other_income = 150 * growth * np.random.uniform(0.9, 1.1)
        
        total_revenue = energy_sales + carbon_credits + government_subsidies + other_income
        
        # Expenses (KES Millions)
        operations_maintenance = 1200 * growth * np.random.uniform(0.95, 1.05)
        well_drilling = 800 * growth * np.random.uniform(0.9, 1.1)
        salaries = 600 * growth * np.random.uniform(0.95, 1.05)
        infrastructure = 400 * growth * np.random.uniform(0.9, 1.1)
        research_development = 250 * growth * np.random.uniform(0.9, 1.1)
        environmental = 150 * growth * np.random.uniform(0.95, 1.05)
        
        total_expenses = operations_maintenance + well_drilling + salaries + infrastructure + research_development + environmental
        profit = total_revenue - total_expenses
        
        financial_data.append({
            "Year": year,
            "Energy_Sales": round(energy_sales, 1),
            "Carbon_Credits": round(carbon_credits, 1),
            "Government_Subsidies": round(government_subsidies, 1),
            "Other_Income": round(other_income, 1),
            "Total_Revenue": round(total_revenue, 1),
            "Operations_Maintenance": round(operations_maintenance, 1),
            "Well_Drilling": round(well_drilling, 1),
            "Salaries": round(salaries, 1),
            "Infrastructure": round(infrastructure, 1),
            "Research_Development": round(research_development, 1),
            "Environmental": round(environmental, 1),
            "Total_Expenses": round(total_expenses, 1),
            "Net_Profit": round(profit, 1)
        })
    
    return pd.DataFrame(financial_data)

# Load data
df_gen = load_generation_data()
df_finance = load_financial_data()

# Aggregate yearly data for key metrics
df_yearly = df_gen.groupby("Year").agg({
    "Energy_Produced_MWh": "sum",
    "Installed_Capacity_MW": "sum",
    "Actual_Generation_MW": "mean",
    "Capacity_Factor": "mean",
    "CO2_Saved_Tons": "sum"
}).reset_index()

# Sidebar Filters
st.sidebar.header("🔍 Filter Dashboard")

years = st.sidebar.multiselect("Select Year(s)", df_gen["Year"].unique(), default=[2023, 2024, 2025])
df_filtered = df_gen[df_gen["Year"].isin(years)]

plants = st.sidebar.multiselect("Select Power Plant(s)", df_gen["Plant"].unique(), default=df_gen["Plant"].unique()[:6])
df_filtered = df_filtered[df_filtered["Plant"].isin(plants)]

months = st.sidebar.multiselect("Select Month(s)", df_gen["Month_Name"].unique(), default=["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
df_filtered = df_filtered[df_filtered["Month_Name"].isin(months)]

# Key Metrics
st.header("📊 Energy Production Overview")

col1, col2, col3, col4, col5 = st.columns(5)

total_energy = df_filtered["Energy_Produced_MWh"].sum()
total_capacity = df_filtered["Installed_Capacity_MW"].iloc[0] if len(df_filtered) > 0 else 0
avg_capacity_factor = df_filtered["Capacity_Factor"].mean()
total_co2_saved = df_filtered["CO2_Saved_Tons"].sum()
total_revenue = df_finance[df_finance["Year"].isin(years)]["Total_Revenue"].sum()

with col1:
    st.metric("⚡ Total Energy Produced", f"{total_energy/1e6:.2f} GWh")
with col2:
    st.metric("🏭 Installed Capacity", f"{total_capacity:,.0f} MW")
with col3:
    st.metric("📈 Avg Capacity Factor", f"{avg_capacity_factor:.1f}%")
with col4:
    st.metric("🌍 CO₂ Emissions Saved", f"{total_co2_saved/1e6:.2f}M tons")
with col5:
    st.metric("💰 Total Revenue", f"KES {total_revenue:.0f}M")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚡ Power Generation", "🌡️ Plant Performance", "💰 Finance", "🌍 Environmental Impact", "📊 Insights"])

# TAB 1: Power Generation
with tab1:
    st.subheader("Monthly Energy Production Trend")
    
    monthly_data = df_filtered.groupby(["Year", "Month", "Month_Name"])["Energy_Produced_MWh"].sum().reset_index()
    monthly_data = monthly_data.sort_values(["Year", "Month"])
    
    fig1 = px.line(
        monthly_data,
        x="Month_Name",
        y="Energy_Produced_MWh",
        color="Year",
        title="Monthly Energy Production (MWh)",
        markers=True,
        line_shape="spline"
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    st.subheader("Energy Production by Plant")
    plant_energy = df_filtered.groupby(["Year", "Plant"])["Energy_Produced_MWh"].sum().reset_index()
    
    fig2 = px.bar(
        plant_energy,
        x="Plant",
        y="Energy_Produced_MWh",
        color="Year",
        title="Total Energy Production by Plant (MWh)",
        barmode="group"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("Generation Capacity vs Actual Output")
    capacity_data = df_filtered.groupby("Year")[["Installed_Capacity_MW", "Actual_Generation_MW"]].mean().reset_index()
    capacity_melt = capacity_data.melt(id_vars=["Year"], var_name="Metric", value_name="MW")
    
    fig3 = px.bar(
        capacity_melt,
        x="Year",
        y="MW",
        color="Metric",
        title="Installed Capacity vs Actual Generation (MW)",
        barmode="group"
    )
    st.plotly_chart(fig3, use_container_width=True)

# TAB 2: Plant Performance
with tab2:
    st.subheader("Plant Capacity Factors")
    
    capacity_factor_data = df_filtered.groupby(["Year", "Plant"])["Capacity_Factor"].mean().reset_index()
    
    fig4 = px.bar(
        capacity_factor_data,
        x="Plant",
        y="Capacity_Factor",
        color="Year",
        title="Capacity Factor by Plant (%)",
        barmode="group"
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Downtime Analysis")
        downtime_data = df_filtered.groupby(["Year", "Plant"])["Downtime_Percentage"].mean().reset_index()
        
        fig5 = px.bar(
            downtime_data,
            x="Plant",
            y="Downtime_Percentage",
            color="Year",
            title="Downtime Percentage by Plant (%)",
            barmode="group"
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        st.subheader("Steam Temperature Trends")
        temp_data = df_filtered.groupby(["Year", "Month", "Month_Name"])["Steam_Temperature_C"].mean().reset_index()
        temp_data = temp_data.sort_values(["Year", "Month"])
        
        fig6 = px.line(
            temp_data,
            x="Month_Name",
            y="Steam_Temperature_C",
            color="Year",
            title="Average Steam Temperature (°C)",
            markers=True
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    st.subheader("Wellhead Pressure Monitoring")
    pressure_data = df_filtered.groupby("Plant")["Wellhead_Pressure_Bar"].mean().reset_index()
    
    fig7 = px.bar(
        pressure_data,
        x="Plant",
        y="Wellhead_Pressure_Bar",
        title="Average Wellhead Pressure by Plant (Bar)",
        color="Wellhead_Pressure_Bar",
        color_continuous_scale="RdYlGn"
    )
    st.plotly_chart(fig7, use_container_width=True)

# TAB 3: Finance
with tab3:
    st.subheader("Revenue & Expense Trends")
    
    finance_year = df_finance[df_finance["Year"].isin(years)]
    finance_melt = finance_year.melt(id_vars=["Year"], value_vars=["Total_Revenue", "Total_Expenses", "Net_Profit"], var_name="Category", value_name="KES_Millions")
    
    fig8 = px.line(
        finance_melt,
        x="Year",
        y="KES_Millions",
        color="Category",
        title="Revenue, Expenses & Profit (KES Millions)",
        markers=True
    )
    st.plotly_chart(fig8, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue breakdown
        rev_2025 = finance_year[finance_year["Year"] == 2025].iloc[0]
        revenue_data = pd.DataFrame({
            "Source": ["Energy Sales", "Carbon Credits", "Government Subsidies", "Other Income"],
            "Amount": [rev_2025["Energy_Sales"], rev_2025["Carbon_Credits"], rev_2025["Government_Subsidies"], rev_2025["Other_Income"]]
        })
        
        fig9 = px.pie(
            revenue_data,
            values="Amount",
            names="Source",
            title=f"Revenue Breakdown (2025)",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig9, use_container_width=True)
    
    with col2:
        # Expense breakdown
        expense_data = pd.DataFrame({
            "Expense": ["O&M", "Well Drilling", "Salaries", "Infrastructure", "R&D", "Environmental"],
            "Amount": [rev_2025["Operations_Maintenance"], rev_2025["Well_Drilling"], rev_2025["Salaries"],
                      rev_2025["Infrastructure"], rev_2025["Research_Development"], rev_2025["Environmental"]]
        })
        
        fig10 = px.pie(
            expense_data,
            values="Amount",
            names="Expense",
            title=f"Expense Breakdown (2025)",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig10, use_container_width=True)
    
    # Financial metrics
    st.subheader("Financial Health Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        profit_margin = (rev_2025["Net_Profit"] / rev_2025["Total_Revenue"]) * 100
        st.metric("Profit Margin", f"{profit_margin:.1f}%", delta="+3.2%")
    
    with col2:
        rev_growth = ((finance_year[finance_year["Year"] == 2025]["Total_Revenue"].values[0] - 
                       finance_year[finance_year["Year"] == 2023]["Total_Revenue"].values[0]) / 
                      finance_year[finance_year["Year"] == 2023]["Total_Revenue"].values[0]) * 100
        st.metric("Revenue Growth (3yr)", f"{rev_growth:.1f}%", delta="+5.8%")
    
    with col3:
        ope_ratio = (rev_2025["Operations_Maintenance"] / rev_2025["Total_Revenue"]) * 100
        st.metric("O&M Ratio", f"{ope_ratio:.1f}%", delta="-1.5%")
    
    with col4:
        r_d_investment = (rev_2025["Research_Development"] / rev_2025["Total_Revenue"]) * 100
        st.metric("R&D Investment", f"{r_d_investment:.1f}%", delta="+0.8%")

# TAB 4: Environmental Impact
with tab4:
    st.subheader("CO₂ Emissions Saved vs Fossil Fuels")
    
    co2_data = df_filtered.groupby("Year")["CO2_Saved_Tons"].sum().reset_index()
    
    fig11 = px.bar(
        co2_data,
        x="Year",
        y="CO2_Saved_Tons",
        title="Annual CO₂ Emissions Saved (Tons)",
        color="CO2_Saved_Tons",
        color_continuous_scale="Greens",
        text="CO2_Saved_Tons"
    )
    fig11.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    st.plotly_chart(fig11, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Environmental Impact Metrics")
        
        total_co2 = df_filtered["CO2_Saved_Tons"].sum()
        trees_equivalent = total_co2 / 0.021  # 21kg CO2 absorbed per tree per year
        cars_equivalent = total_co2 / 4.6  # 4.6 tons CO2 per car per year
        
        st.metric("🌳 Trees Equivalent", f"{trees_equivalent/1000:.0f}K")
        st.metric("🚗 Cars Removed from Road", f"{cars_equivalent:.0f}")
        st.metric("🏠 Homes Powered", f"{df_filtered['Energy_Produced_MWh'].sum() / 10:.0f}")
    
    with col2:
        st.subheader("Renewable Energy Mix Contribution")
        total_renewable = df_filtered["Energy_Produced_MWh"].sum()
        
        fig12 = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = (total_renewable / 5000000) * 100,
            title = {"text": "National Grid Contribution (%)"},
            delta = {"reference": 40},
            gauge = {
                "axis": {"range": [None, 100]},
                "bar": {"color": "darkgreen"},
                "steps": [
                    {"range": [0, 30], "color": "lightgray"},
                    {"range": [30, 60], "color": "gray"},
                    {"range": [60, 100], "color": "darkgray"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 70
                }
            }
        ))
        st.plotly_chart(fig12, use_container_width=True)
    
    st.subheader("Monthly Environmental Impact")
    monthly_impact = df_filtered.groupby(["Year", "Month_Name"])["CO2_Saved_Tons"].sum().reset_index()
    
    fig13 = px.line(
        monthly_impact,
        x="Month_Name",
        y="CO2_Saved_Tons",
        color="Year",
        title="Monthly CO₂ Savings (Tons)",
        markers=True
    )
    st.plotly_chart(fig13, use_container_width=True)

# TAB 5: Insights
with tab5:
    st.subheader("Key Operational Insights")
    
    # Plant ranking
    st.markdown("### 🏆 Plant Performance Ranking (2025)")
    plant_2025 = df_filtered[df_filtered["Year"] == 2025].groupby("Plant").agg({
        "Capacity_Factor": "mean",
        "Energy_Produced_MWh": "sum",
        "Downtime_Percentage": "mean",
        "Steam_Temperature_C": "mean"
    }).reset_index()
    plant_2025 = plant_2025.sort_values("Capacity_Factor", ascending=False)
    plant_2025["Rank"] = range(1, len(plant_2025) + 1)
    
    st.dataframe(plant_2025, use_container_width=True)
    
    # Strategic recommendations
    st.markdown("### 🎯 Strategic Recommendations for Growth")
    
    recommendations = [
        "**🔋 Capacity Expansion** - Add 150MW of new geothermal capacity by 2026 through Olkaria VI development",
        "**🌡️ Efficiency Optimization** - Implement advanced wellhead technology to increase capacity factor to 95%",
        "**🌍 Carbon Credit Monetization** - Expand carbon credit trading partnerships with European markets",
        "**🔬 R&D Investment** - Increase geothermal exploration budget to discover new steam fields",
        "**🔄 Binary Cycle Technology** - Retrofit existing plants with binary cycle units for 15% efficiency gain",
        "**💧 Reinjection Optimization** - Improve water reinjection systems to extend reservoir life by 10 years",
        "**🤝 Strategic Partnerships** - Form JVs with international geothermal technology providers",
        "**📊 Digital Twin Implementation** - Deploy AI-powered predictive maintenance across all plants"
    ]
    
    for rec in recommendations:
        st.info(rec)
    
    # Performance scatter plot
    st.markdown("### 📊 Capacity Factor vs Downtime Analysis")
    scatter_data = df_filtered.groupby("Plant")[["Capacity_Factor", "Downtime_Percentage"]].mean().reset_index()
    
    fig14 = px.scatter(
        scatter_data,
        x="Downtime_Percentage",
        y="Capacity_Factor",
        text="Plant",
        title="Plant Efficiency: Capacity Factor vs Downtime",
        size="Capacity_Factor",
        color="Capacity_Factor",
        color_continuous_scale="RdYlGn"
    )
    fig14.update_traces(textposition="top center")
    st.plotly_chart(fig14, use_container_width=True)
    
    # Growth indicators
    st.markdown("### 📈 Key Performance Indicators (2025 YoY)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        energy_growth = ((df_yearly[df_yearly["Year"] == 2025]["Energy_Produced_MWh"].values[0] - 
                         df_yearly[df_yearly["Year"] == 2024]["Energy_Produced_MWh"].values[0]) / 
                        df_yearly[df_yearly["Year"] == 2024]["Energy_Produced_MWh"].values[0]) * 100
        st.metric("Energy Production Growth", f"{energy_growth:.1f}%", delta="+4.2%")
        st.metric("New Wells Drilled", "12", delta="+3")
    
    with col2:
        cf_growth = plant_2025["Capacity_Factor"].mean() - 78.5
        st.metric("Avg Capacity Factor", f"{plant_2025['Capacity_Factor'].mean():.1f}%", delta=f"{cf_growth:.1f}%")
        st.metric("Geothermal Reservoirs", "8", delta="+2")
    
    with col3:
        st.metric("Operational Efficiency", "91.2%", delta="+2.3%")
        st.metric("Employee Count", "3,450", delta="+280")

# Data Download
st.markdown("---")
st.subheader("📎 Download Data")

col1, col2 = st.columns(2)
with col1:
    csv = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button("⚡ Download Generation Data as CSV", csv, "geothermal_power_generation_data.csv", "text/csv")

with col2:
    csv_finance = df_finance[df_finance["Year"].isin(years)].to_csv(index=False).encode("utf-8")
    st.download_button("💰 Download Financial Data as CSV", csv_finance, "geothermal_power_financial_data.csv", "text/csv")

with st.expander("View Raw Generation Data"):
    st.dataframe(df_filtered, use_container_width=True)

with st.expander("View Raw Financial Data"):
    st.dataframe(df_finance[df_finance["Year"].isin(years)], use_container_width=True)

# Footer
st.markdown("---")
st.markdown("### 🌋 GeoThermal Power PLC - Powering Kenya's Future with Clean, Renewable Geothermal Energy")
st.caption("📌 GeoThermal Power Dashboard | 2023-2025 | Sustainable Energy Analytics")
