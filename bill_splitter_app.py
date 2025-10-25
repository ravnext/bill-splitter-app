import streamlit as st
import pandas as pd

st.title("💸 Fair Bill Splitter")

st.markdown("""
Enter how much each person paid, and this tool will calculate  
who owes whom — with the *fewest possible transactions*.
""")

# Input table
st.subheader("Enter Payments")
data = st.data_editor(
    pd.DataFrame({"Name": ["Alice", "Bob", "Charlie"], "Paid": [0.0, 0.0, 0.0]}),
    num_rows="dynamic"
)

if st.button("Calculate Fair Settlement"):
    names = data["Name"].tolist()
    paid = data["Paid"].tolist()
    n = len(names)
    if n == 0:
        st.warning("Please add at least one person.")
    else:
        avg = sum(paid) / n
        balances = {names[i]: round(paid[i] - avg, 2) for i in range(n)}

        # Minimal cash flow algorithm
        def minCashFlow(balances):
            people = list(balances.keys())
            net = list(balances.values())
            transactions = []

            def getMaxCreditIndex():
                return max(range(len(net)), key=lambda i: net[i])

            def getMaxDebitIndex():
                return min(range(len(net)), key=lambda i: net[i])

            def settle():
                mxCredit = getMaxCreditIndex()
                mxDebit = getMaxDebitIndex()
                if abs(net[mxCredit]) < 1e-9 and abs(net[mxDebit]) < 1e-9:
                    return

                min_val = min(-net[mxDebit], net[mxCredit])
                net[mxCredit] -= min_val
                net[mxDebit] += min_val

                transactions.append(
                    (people[mxDebit], people[mxCredit], round(min_val, 2))
                )
                settle()

            settle()
            return transactions

        results = minCashFlow(balances)

        st.subheader("💰 Settlements")
        if not results:
            st.success("All settled up! No payments needed.")
        else:
            for d, c, amt in results:
                st.write(f"**{d} ➜ {c}: ${amt:.2f}**")

        st.divider()
        st.subheader("Balances")
        st.dataframe(pd.DataFrame(list(balances.items()), columns=["Name", "Net Balance"]))
