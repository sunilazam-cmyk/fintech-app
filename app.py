import streamlit as st
import plotly.graph_objects as go
from calculators import calculate_sip, calculate_emi, calculate_compound_interest, compare_loans
from database import init_db, log_calculator_activity, get_calculator_history

init_db()

st.set_page_config(page_title="FinTech Calculator Suite", layout="wide")

st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Select Module", ["SIP Calculator", "EMI Calculator", "Compound Interest", "Loan Comparison", "Calculation History"])

st.title("FinTech Calculator Suite")

if app_mode == "SIP Calculator":
    st.header("SIP Calculator")
    c1, c2 = st.columns([1, 2])
    with c1:
        p = st.number_input("Monthly Investment (Rs)", min_value=100, value=5000, step=500)
        r = st.slider("Expected Return (% p.a.)", 1.0, 30.0, 12.0)
        t = st.slider("Tenure (Years)", 1, 30, 10)
        if st.button("Calculate SIP"):
            res = calculate_sip(p, r, t)
            log_calculator_activity("SIP", f"P=Rs{p}, R={r}%, T={t}Y", f"Maturity=Rs{res['maturity_value']:,}")
            st.metric("Total Invested", f"Rs {res['total_invested']:,}")
            st.metric("Est. Returns", f"Rs {res['estimated_returns']:,}")
            st.metric("Maturity Value", f"Rs {res['maturity_value']:,}")
    with c2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=res["months"] if 'res' in locals() else [], y=res["invested_series"] if 'res' in locals() else [], name="Invested Amount", fill='tozeroy'))
        fig.add_trace(go.Scatter(x=res["months"] if 'res' in locals() else [], y=res["wealth_series"] if 'res' in locals() else [], name="Total Wealth", fill='tonexty'))
        fig.update_layout(title="Wealth Growth Projection", xaxis_title="Months", yaxis_title="Amount (Rs)")
        st.plotly_chart(fig, use_container_width=True)

elif app_mode == "EMI Calculator":
    st.header("Loan EMI Calculator")
    c1, c2 = st.columns([1, 2])
    with c1:
        p = st.number_input("Loan Principal (Rs)", min_value=10000, value=500000, step=10000)
        r = st.slider("Interest Rate (% p.a.)", 1.0, 25.0, 10.5)
        t = st.slider("Tenure (Years)", 1, 30, 5)
        if st.button("Calculate EMI"):
            res = calculate_emi(p, r, t)
            log_calculator_activity("EMI", f"Principal=Rs{p}, R={r}%, T={t}Y", f"EMI=Rs{res['monthly_emi']:,}")
            st.metric("Monthly EMI", f"Rs {res['monthly_emi']:,}")
            st.metric("Total Interest", f"Rs {res['total_interest']:,}")
            st.metric("Total Payment", f"Rs {res['total_payment']:,}")
    with c2:
        if 'res' in locals():
            fig = go.Figure(data=[go.Pie(labels=['Principal Amount', 'Total Interest'], values=[p, res['total_interest']], hole=.4)])
        else:
            fig = go.Figure(data=[go.Pie(labels=['Principal Amount', 'Total Interest'], values=[p, 0], hole=.4)])
        fig.update_layout(title="Payment Breakdown")
        st.plotly_chart(fig, use_container_width=True)

elif app_mode == "Compound Interest":
    st.header("Compound Interest Calculator")
    c1, c2 = st.columns([1, 2])
    with c1:
        p = st.number_input("Principal Amount (Rs)", min_value=1000, value=100000, step=5000)
        r = st.slider("Annual Interest Rate (%)", 1.0, 25.0, 8.0)
        t = st.slider("Tenure (Years)", 1, 30, 5)
        freq = st.selectbox("Compounding Frequency", [12, 4, 1], format_func=lambda x: "Monthly" if x == 12 else ("Quarterly" if x == 4 else "Annually"))
        if st.button("Calculate Growth"):
            res = calculate_compound_interest(p, r, t, freq)
            log_calculator_activity("Compound Interest", f"P=Rs{p}, R={r}%, T={t}Y", f"Final=Rs{res['final_amount']:,}")
            st.metric("Principal Amount", f"Rs {res['principal']:,}")
            st.metric("Interest Earned", f"Rs {res['interest_earned']:,}")
            st.metric("Final Amount", f"Rs {res['final_amount']:,}")
    with c2:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=res["years"] if 'res' in locals() else [], y=res["yearly_amounts"] if 'res' in locals() else [], name="Compounded Value"))
        fig.update_layout(title="Yearly Balance Growth", xaxis_title="Years", yaxis_title="Amount (Rs)")
        st.plotly_chart(fig, use_container_width=True)

elif app_mode == "Loan Comparison":
    st.header("Loan Comparison Engine")
    p = st.number_input("Common Principal Amount (Rs)", min_value=10000, value=1000000, step=50000)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Option 1")
        r1 = st.number_input("Rate Option 1 (%)", value=8.5)
        t1 = st.number_input("Tenure Option 1 (Yrs)", value=15)
    with col2:
        st.subheader("Option 2")
        r2 = st.number_input("Rate Option 2 (%)", value=9.0)
        t2 = st.number_input("Tenure Option 2 (Yrs)", value=20)
    if st.button("Compare Loans"):
        res = compare_loans(p, r1, int(t1), r2, int(t2))
        log_calculator_activity("Loan Comparison", f"P=Rs{p}", f"Opt1 EMI=Rs{res['Option 1']['monthly_emi']}, Opt2 EMI=Rs{res['Option 2']['monthly_emi']}")
        c1, c2 = st.columns(2)
        with c1:
            st.info("Option 1 Metrics")
            st.write(f"**Monthly EMI:** Rs {res['Option 1']['monthly_emi']:,}")
            st.write(f"**Total Interest:** Rs {res['Option 1']['total_interest']:,}")
            st.write(f"**Total Cost:** Rs {res['Option 1']['total_payment']:,}")
        with c2:
            st.info("Option 2 Metrics")
            st.write(f"**Monthly EMI:** Rs {res['Option 2']['monthly_emi']:,}")
            st.write(f"**Total Interest:** Rs {res['Option 2']['total_interest']:,}")
            st.write(f"**Total Cost:** Rs {res['Option 2']['total_payment']:,}")

elif app_mode == "Calculation History":
    st.header("Saved Activity History (SQLite Database)")
    st.dataframe(get_calculator_history(), use_container_width=True)
