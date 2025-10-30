import pandas as pd
import matplotlib.pyplot as plt

student_loan = -117687
savings_account = 75000
monthly_loan_payment = 622
worst_return = 20  # years


def simulate_networth(filepath="spy.csv"):
    df = pd.read_csv(filepath)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    # Start simulation worst_return years before last date
    last_date = df["Date"].iloc[-1]
    start_date = last_date - pd.DateOffset(years=worst_return)
    spy_window = df[df["Date"] >= start_date].reset_index(drop=True)

    # Initial savings tracking SPY
    start_value = spy_window.loc[0, "Value"]
    savings_base = savings_account * (spy_window["Value"] / start_value)

    loan = student_loan
    networth_history = []
    loan_history = []
    savings_history = []

    # Track contributions after loan payoff
    contributions = []  # list of (date, invested_spy_value)

    for i in range(len(spy_window)):
        current_date = spy_window.loc[i, "Date"]
        current_spy = spy_window.loc[i, "Value"]

        # Check if loan is still active
        if i > 0 and current_date.month != spy_window.loc[i - 1, "Date"].month:
            if loan < 0:
                # Still paying loan
                loan += monthly_loan_payment
            else:
                # Loan paid off → start investing payments
                contributions.append((current_date, current_spy))

        # Base savings growth
        savings_total = savings_base.iloc[i]

        # Add contributions growth
        for contrib_date, contrib_spy in contributions:
            growth = monthly_loan_payment * (current_spy / contrib_spy)
            savings_total += growth

        # Record histories
        networth_history.append(savings_total + loan)
        loan_history.append(loan)
        savings_history.append(savings_total)

    # --- PLOT ---
    fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True, facecolor="black")

    # Net worth subplot
    axes[0].plot(spy_window["Date"], networth_history, color="white", linewidth=2)
    axes[0].set_title("Net Worth Evolution (Investment Made {} Years Ago)".format(worst_return), color="white", fontsize=16)
    axes[0].set_ylabel("Net Worth ($)", color="white")
    axes[0].grid(True, linestyle="--", alpha=0.3, color="white")
    axes[0].set_facecolor("black")
    axes[0].tick_params(colors="white")

    # Loan balance subplot
    axes[1].plot(spy_window["Date"], loan_history, color="red", linewidth=2)
    axes[1].set_title("Student Loan Balance Over Time", color="white", fontsize=16)
    axes[1].set_ylabel("Loan Balance ($)", color="white")
    axes[1].grid(True, linestyle="--", alpha=0.3, color="white")
    axes[1].set_facecolor("black")
    axes[1].tick_params(colors="white")

    # Savings subplot
    axes[2].plot(spy_window["Date"], savings_history, color="green", linewidth=2)
    axes[2].set_title("Savings Account Value Over Time", color="white", fontsize=16)
    axes[2].set_xlabel("Date", color="white")
    axes[2].set_ylabel("Savings ($)", color="white")
    axes[2].grid(True, linestyle="--", alpha=0.3, color="white")
    axes[2].set_facecolor("black")
    axes[2].tick_params(colors="white")

    plt.tight_layout()
    plt.show()


def main():
    simulate_networth("spy.csv")


if __name__ == "__main__":
    main()
