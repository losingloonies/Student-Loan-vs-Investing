import pandas as pd
import matplotlib.pyplot as plt

student_loan = -117687
savings_account = 75000
monthly_loan_payment = 622
worst_return = 20  # years


def find_worst_return(filepath="spy.csv", worse_return=worst_return):
    df = pd.read_csv(filepath)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    worst_val = None
    worst_date = None

    for i in range(len(df)):
        start_date = df.loc[i, "Date"]
        start_value = df.loc[i, "Value"]

        target_date = start_date + pd.DateOffset(years=worse_return)
        future_data = df[df["Date"] >= target_date]

        if not future_data.empty:
            end_value = future_data.iloc[0]["Value"]
            ret = (end_value - start_value) / start_value

            if (worst_val is None) or (ret < worst_val):
                worst_val = ret
                worst_date = start_date

    if worst_val is not None:
        print(f"Worst return found:")
        print(f"Start Date: {worst_date.date()}  |  Return: {worst_val:.2%} over {worse_return} years")
        return worst_date
    else:
        print("Not enough data to compute the return.")
        return None


def simulate_networth(filepath="spy.csv"):
    df = pd.read_csv(filepath)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    last_date = df["Date"].iloc[-1]
    start_date = last_date - pd.DateOffset(years=worst_return)
    spy_window = df[df["Date"] >= start_date].reset_index(drop=True)

    loan = student_loan + savings_account
    savings_total = 0.0

    networth_history = []
    loan_history = []
    savings_history = []

    contributions = []

    for i in range(len(spy_window)):
        current_date = spy_window.loc[i, "Date"]
        current_spy = spy_window.loc[i, "Value"]

        if i > 0 and current_date.month != spy_window.loc[i - 1, "Date"].month:
            if loan < 0:
                loan += monthly_loan_payment
                if loan > 0:
                    savings_total += loan
                    contributions.append((current_date, current_spy))
                    loan = 0
            else:
                contributions.append((current_date, current_spy))

        contrib_growth = 0
        for contrib_date, contrib_spy in contributions:
            contrib_growth += monthly_loan_payment * (current_spy / contrib_spy)
        savings_total = contrib_growth

        networth_history.append(savings_total + loan)
        loan_history.append(loan)
        savings_history.append(savings_total)

    # --- SQUARE SAVINGS PLOT (minimal, high quality, upper portion black) ---
    plt.figure(figsize=(8, 8), facecolor="none", dpi=300)
    ax = plt.gca()
    ax.plot(spy_window["Date"], savings_history, color="#00FF00", linewidth=4)  # coding green

    # Remove axes, ticks, spines
    ax.set_facecolor("none")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Fill above the line with black
    x = spy_window["Date"]
    y = savings_history
    ax.fill_between(x, y, ax.get_ylim()[1], color="black", alpha=1)

    plt.tight_layout(pad=0)
    plt.savefig("savings_square.png", transparent=True)
    plt.close()


def main():
    simulate_networth("spy.csv")


if __name__ == "__main__":
    main()
