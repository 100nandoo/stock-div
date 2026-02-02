import marimo

__generated_with = "0.19.7"
app = marimo.App(width="full")


@app.cell
def _(mo):
    mo.md("""
    # Retrieve Company List
    Generate CSV file for both **Kompas 100** and **Strait Times Index**
    """)
    return


@app.cell
def _(mo):
    options = ["Kompas 100", "STI", "Both"]
    selected = mo.ui.radio(options=options)
    run_button = mo.ui.run_button(label="Run")
    mo.vstack(["Which one:", selected, run_button])
    return run_button, selected


@app.cell
def _(fetch_and_save_stock_info, kompas100, run_button, selected, sti):

    if run_button.value:
        if selected.value == "Kompas 100":
            fetch_and_save_stock_info(kompas100, "kompas100")
        elif selected.value == "STI":
            fetch_and_save_stock_info(sti, "sti")
        elif selected.value == "Both":
            fetch_and_save_stock_info(kompas100, "kompas100")
            fetch_and_save_stock_info(sti, "sti")

        else:
            print("No valid option selected.")
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd
    import yfinance as yf
    from datetime import datetime
    import io
    from tqdm import tqdm
    import os
    return mo, os, pd, tqdm, yf


@app.cell(hide_code=True)
def _():
    kompas100 = [
        "BBCA.JK", "DSSA.JK", "BBRI.JK", "TPIA.JK", "AMMN.JK", "BMRI.JK", "TLKM.JK", "ASII.JK", "BRPT.JK", "PANI.JK",
        "BBNI.JK", "FILM.JK", "BRMS.JK", "BRIS.JK", "ANTM.JK", "BUMI.JK", "HMSP.JK", "UNTR.JK", "ICBP.JK", "NCKL.JK",
        "ADMR.JK", "MDKA.JK", "MBMA.JK", "UNVR.JK", "CPIN.JK", "AMRT.JK", "ISAT.JK", "PTRO.JK", "INCO.JK", "GOTO.JK",
        "ADRO.JK", "EXCL.JK", "INDF.JK", "AADI.JK", "EMTK.JK", "KLBF.JK", "MYOR.JK", "TCPI.JK", "PGAS.JK", "INKP.JK",
        "PGEO.JK", "MTEL.JK", "BNGA.JK", "CMRY.JK", "MEDC.JK", "ENRG.JK", "MIKA.JK", "NISP.JK", "JPFA.JK", "TOWR.JK",
        "GGRM.JK", "TAPG.JK", "PTBA.JK", "AVIA.JK", "PNBN.JK", "JSMR.JK", "AKRA.JK", "ITMG.JK", "TINS.JK", "SRTG.JK",
        "ARTO.JK", "INTP.JK", "TKIM.JK", "HEAL.JK", "MAPA.JK", "MAPI.JK", "BSDE.JK", "KPIG.JK", "RAJA.JK", "PWON.JK",
        "BBTN.JK", "INDY.JK", "SMGR.JK", "SCMA.JK", "SIDO.JK", "CTRA.JK", "BUKA.JK", "DSNG.JK", "HRUM.JK", "STAA.JK",
        "AUTO.JK", "DEWA.JK", "ESSA.JK", "BFIN.JK", "CLEO.JK", "BTPS.JK", "PNLF.JK", "LSIP.JK", "SSIA.JK", "ACES.JK",
        "SMRA.JK", "ERAA.JK", "SMDR.JK", "MNCN.JK", "ELSA.JK", "BBYB.JK", "KIJA.JK", "GJTL.JK", "ASRI.JK", "PTPP.JK"
    ]

    sti = {
        "H78.SI", "S63.SI", "G13.SI", "Y92.SI", "BUOU.SI", "AJBU.SI", "N2IU.SI", "9CI.SI", "ME8U.SI", "BS6.SI",
        "5E2.SI", "O39.SI", "J36.SI", "U14.SI", "U96.SI", "D01.SI", "D05.SI", "Z74.SI", "BN4.SI", "J69U.SI",
        "M44U.SI", "F34.SI", "S58.SI", "C09.SI", "C38U.SI", "V03.SI", "A17U.SI", "U11.SI", "S68.SI", "C6L.SI"
    }
    return kompas100, sti


@app.cell
def _(os, pd, tqdm, yf):
    # Helper: convert large numbers to human-readable
    def human_readable_number(num):
        try:
            num = float(num)
        except (TypeError, ValueError):
            return "N/A"
        if num >= 1_000_000_000_000:
            return f"{num/1_000_000_000_000:.1f}T"
        elif num >= 1_000_000_000:
            return f"{num/1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return str(num)

    def fetch_and_save_stock_info(ticker_list, list_name=None):
        """
        Fetch stock info from Yahoo Finance and save to CSV.

        Args:
            ticker_list (list or set): list of tickers
            list_name (str, optional): name to use for CSV file. If None, defaults to 'custom'
        """
        all_tickers = list(ticker_list)  # in case it's a set
        tickers = yf.Tickers(all_tickers)

        company_data = []

        for ticker_symbol in tqdm(all_tickers, desc="Fetching tickers"):
            t = tickers.tickers.get(ticker_symbol)
            if t is None:
                company_data.append({
                    "Company": "Error",
                    "Ticker": ticker_symbol,
                    "Sector": "Error",
                    "Market Cap": "Error",
                    "Market Cap Raw": "Error"
                })
                continue

            info = t.info if hasattr(t, "info") else {}
            name = info.get("shortName", "N/A")
            sector = info.get("sector", "N/A")
            mcap = info.get("marketCap", "N/A")
            mcap_read = human_readable_number(mcap)

            company_data.append({
                "Company": name,
                "Ticker": ticker_symbol,
                "Sector": sector,
                "Market Cap": mcap_read,
                "Market Cap Raw": mcap
            })

        # Convert to DataFrame
        df_company = pd.DataFrame(company_data)



        # Determine filename
        if list_name is None:
            filename = "custom_stock_info.csv"
        else:
            filename = f"{list_name}_stock_info.csv"

        os.makedirs("./data", exist_ok=True)


        # Save CSV to /data folder
        filepath = f"./data/{filename}"
        df_company.to_csv(filepath, index=False)
        print(f"✅ Company, Ticker, Sector, and Market Cap saved to {filepath}")
    return (fetch_and_save_stock_info,)


@app.cell
def _(mo):
    mo.md("## Show Data")
    show_button = mo.ui.run_button(label="Show Data")
    show_button
    return (show_button,)


@app.cell
def _(mo, os, pd, show_button):

    _tables = []

    if os.path.exists("./data/kompas100_stock_info.csv"):
        pd_kompas100 = pd.read_csv("./data/kompas100_stock_info.csv")
        _tables.append(mo.md("# Kompas 100"))
        _tables.append(mo.ui.table(pd_kompas100))
    else:
        _tables.append(mo.md("⚠️ kompas100_stock_info.csv not found."))

    if os.path.exists("./data/sti_stock_info.csv"):
        pd_sti = pd.read_csv("./data/sti_stock_info.csv")
        _tables.append(mo.md("# STI"))
        _tables.append(mo.ui.table(pd_sti))
    else:
        _tables.append(mo.md("⚠️ sti_stock_info.csv not found."))


    # Stack and show tables only if there’s at least one
    mo.vstack(_tables) if show_button.value else None
    return


@app.cell(disabled=True, hide_code=True)
def _(pprint, yf):
    # Create Ticker object
    bca = yf.Ticker("BBCA.JK")

    # 1️⃣ Print all info fields (basic info, company, sector, etc.)
    pprint.pprint(bca.info)

    # 2️⃣ Print historical price data
    print("\n=== Historical Prices ===")
    print(bca.history(period="1y"))

    # 3️⃣ Dividends
    print("\n=== Dividends ===")
    print(bca.dividends)

    # 4️⃣ Stock splits
    print("\n=== Stock Splits ===")
    print(bca.splits)

    # 5️⃣ Actions (dividends + splits combined)
    print("\n=== Actions ===")
    print(bca.actions)

    # 6️⃣ Financial statements
    print("\n=== Financials ===")
    print(bca.financials)

    print("\n=== Balance Sheet ===")
    print(bca.balance_sheet)

    print("\n=== Cashflow ===")
    print(bca.cashflow)

    # 7️⃣ Sustainability info (if available)
    print("\n=== Sustainability ===")
    print(bca.sustainability)

    # 8️⃣ Recommendations / analyst info
    print("\n=== Recommendations ===")
    print(bca.recommendations)
    return


if __name__ == "__main__":
    app.run()
