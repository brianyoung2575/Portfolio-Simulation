import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

st.title("Portfolio Simulation")
st.sidebar.header("Parameters")
st.subheader("How this simulation works")
st.markdown("""
**Market:** Represents market exposure (e.g. S&P 500)

**Satellite:** Represents higher-risk investments with higher return potential but more volatility

Both components are combined to form the portfolio with your chosen allocation
""")

#Parameters
log_scale = st.sidebar.checkbox("Log Y-Axis Scale")
years = st.sidebar.slider("Years", 1, 40, 5)
simulations = st.sidebar.slider("Simulations", 25, 2000, 250, step=25)

initial_capital = st.sidebar.number_input("Initial Capital", value=10000)

mu = st.sidebar.slider("Average Market Return (μ)", 0.0, 0.2, 0.10)
sigma = st.sidebar.slider("Market Standard Deviation (σ)", 0.01, 0.8, 0.16)

satellite_mu = st.sidebar.slider("Average Satellite Return (μ)", 0.0, 0.5, 0.20)
satellite_sigma = st.sidebar.slider("Satellite Standard Deviation (σ)", 0.01, 1.0, 0.30)

satellite_allocation = st.sidebar.slider("Satellite Allocation", 0.0, 1.0, 0.1)
market_allocation = 1 - satellite_allocation

market_leverage = st.sidebar.slider("Market Leverage", 1.0, 3.0, 1.0)
satellite_leverage = st.sidebar.slider("Satellite Leverage", 1.0, 3.0, 1.0)

#Simulation
final_values = []
all_paths = []

for i in range(simulations):
    market_value = 1.0
    satellite_value = 1.0
    portfolio_path = [initial_capital]

    for i in range(years):
        market_r = np.random.normal(mu, sigma)
        satellite_r = np.random.normal(satellite_mu, satellite_sigma)
        market_value *= np.exp(market_r)
        satellite_value *= np.exp(satellite_r)
        portfolio_value = (market_allocation * market_leverage * market_value + satellite_allocation * satellite_value * satellite_leverage) * initial_capital
        portfolio_path.append(portfolio_value)
    
    all_paths.append(portfolio_path)
    final_values.append(portfolio_path[-1])

final_values = np.array(final_values)

#Statistics
st.subheader("Statistics")
mean_gain_pct = ((np.mean(final_values)-initial_capital)/initial_capital)*100
median_gain_pct = ((np.median(final_values)-initial_capital)/initial_capital)*100
st.markdown(f"**Mean:** ${np.mean(final_values):,.2f} ({mean_gain_pct:+.2f}%)")
st.markdown(f"**Median:** ${np.median(final_values):,.2f} ({median_gain_pct:+.2f}%)")
st.markdown(f"**Probability of losing:** {np.mean(final_values < initial_capital)*100:.2f}%")

#Plots
def format_dollars(x, pos):
    return f'${x:,.0f}'

fig, ax = plt.subplots()
for path in all_paths:
    ax.plot(path, alpha=0.3)
ax.set_title("Portfolio Simulation Paths")
ax.set_xlabel("Year")
ax.set_ylabel("Value ($) (Log Scale)")
if log_scale:
    ax.set_yscale("log")
ax.yaxis.set_major_formatter(FuncFormatter(format_dollars))
ax.grid()
st.pyplot(fig)

fig2, ax2 = plt.subplots()
ax2.hist(final_values, bins=50)
ax2.set_title("Distribution of Final Portfolio Values")
ax2.set_xlabel("Final Value ($)")
ax2.set_ylabel("Frequency")
ax2.xaxis.set_major_formatter(FuncFormatter(format_dollars))
ax2.grid()
plt.tight_layout()
st.pyplot(fig2)