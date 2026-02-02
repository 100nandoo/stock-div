import marimo

__generated_with = "0.19.7"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md("""
    # Fetch A Single Company Dividend History 💰
    """)
    return


@app.cell
def _():
    import marimo as mo
    import yfinance as yf
    import pandas as pd
    return mo, yf


@app.cell
def _(mo):
    input = mo.ui.text(placeholder="D05.SI", label="Enter yahoo finance ticker:")
    search_button = mo.ui.run_button(label="Search")
    return input, search_button


@app.cell
def _(input, mo, search_button):
    mo.hstack([input, search_button]) 
    return


@app.cell
def _(input, mo, save_annual_dividend_history, search_button):
    search_button
    result = None
    hist = None
    ticker = None
    with mo.status.spinner(title="Loading...") as _spinner:
        if search_button.value and input.value.strip():
            result, hist, ticker = save_annual_dividend_history(input.value)

    mo.md("Ticker can't be empty⚠️") if not input.value.strip() else None
    return hist, result, ticker


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Function") if mo.app_meta().mode == "edit" else None
    return


@app.cell(hide_code=True)
def _(yf):
    def save_annual_dividend_history(symbol):
        """
        Fetches all dividend history for a symbol, sums by year,
        calculates yield based on current price, and saves to CSV.
        """
        try:
            ticker = yf.Ticker(symbol)

            # 1. Get current price
            # Using fast_info or history to get the latest close
            hist = ticker.history(period="1d")
            if hist.empty:
                print(f"Could not fetch price for {symbol}")
                return
            current_price = hist['Close'].iloc[-1]

            # 2. Get dividends
            divs = ticker.dividends
            if divs.empty:
                print(f"No dividend history found for {symbol}")
                return

            # 3. Process data into a DataFrame
            df = divs.to_frame().reset_index()
            df['Year'] = df['Date'].dt.year

            # 4. Group by year and sum (combines multiple payouts)
            annual_df = df.groupby('Year')['Dividends'].sum().reset_index()

            # 5. Calculate yield % based on current price
            annual_df['Yield_%'] = (annual_df['Dividends'] / current_price) * 100

            # 6. Formatting: If Payout > 1000, remove decimals
            def format_payout(val):
                if val > 1000:
                    return int(round(val))
                return round(val, 2) 

            annual_df['Dividends'] = annual_df['Dividends'].apply(format_payout)
            annual_df['Yield_%'] = annual_df['Yield_%'].map('{:.2f}'.format)

            # 7. Save to CSV
            filename = f"./data/{symbol.replace('.', '_')}_annual_dividends.csv"
            annual_df.to_csv(filename, index=False)

            print(f"✅ Success! File saved as: {filename}")
            print(f"Current Price used: {current_price:.2f}")
            return annual_df, hist, ticker
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None, None
    return (save_annual_dividend_history,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("## UI for Result") if mo.app_meta().mode == "edit" else None
    return


@app.cell(hide_code=True)
def _(hist, input, mo, result, ticker):
    result
    vheader = None
    if result is not None:
        current_price = hist['Close'].iloc[-1]
        currency = ticker.info.get('currency', '')
        header = mo.md(f"## {input.value}")
        price = mo.md(f"#### {currency} {current_price:.2f}")
        vheader = mo.vstack([header, price])

    vheader
    return


@app.cell(hide_code=True)
def _(mo, result):
    table = mo.ui.table(
        data=result, 
        pagination=False, 
        show_column_summaries=False, 
        show_data_types=False
    )

    table if result is not None else None
    return


if __name__ == "__main__":
    app.run()
