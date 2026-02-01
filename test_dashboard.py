import yfinance as yf
import pandas as pd

# Exemple : ticker Nvidia
stock = yf.Ticker("NVDA")

try:
    # --- 1. Historique annuel ---
    fin = stock.financials
    bs = stock.balance_sheet

    if not fin.empty and not bs.empty:
        cols = [c for c in fin.columns if c in bs.columns]
        fin = fin[cols]
        bs = bs[cols]

        def get_row(df, possible_names, fill=0):
            for name in possible_names:
                if name in df.index:
                    return df.loc[name]
            return pd.Series(fill, index=df.columns)

        # EBIT pour approximatif NOPAT
        ebit = get_row(fin, ['EBIT', 'Operating Income', 'OperatingIncome'], fill=0)
        income_tax_expense = get_row(fin, ['Income Tax Expense', 'IncomeTaxExpense', 'Provision for Income Taxes'], fill=0)
        tax_rate = income_tax_expense / (get_row(fin, ['Income Before Tax', 'Pre-Tax Income'], fill=1))
        nopat = ebit * (1 - tax_rate)

        # Capital investi : Total Assets - Current Liabilities
        total_assets = get_row(bs, ['Total Assets', 'Assets'], fill=1)
        current_liabilities = get_row(bs, ['Current Liabilities'], fill=0)
        invested_capital = total_assets - current_liabilities

        roic_hist = nopat / invested_capital

        # DataFrame final
        df_hist = pd.DataFrame({
            "ROIC": roic_hist
        })

        # Transposition pour lisibilité
        df_final = df_hist.T
        df_final = df_final.iloc[:, :5]
        df_final.columns = [d.strftime('%Y') for d in df_final.columns]

        print("\n📅 Historique annuel ROIC sur 5 ans :")
        print(df_final.applymap(lambda x: f"{x:.1%}"))

        # Commentaire automatique
        last_roic = df_final.loc['ROIC'].iloc[0]
        old_roic = df_final.loc['ROIC'].iloc[-1]
        if last_roic > old_roic:
            print("📈 Tendance Positive : Le ROIC s'est amélioré sur la période.")
        else:
            print("📉 Attention : Le ROIC a diminué par rapport à il y a 5 ans.")

    else:
        print("Historique détaillé annuel non disponible pour cet actif.")

    # --- 2. Derniers trimestres (TTM) ---
    q_fin = stock.quarterly_financials
    q_bs = stock.quarterly_balance_sheet

    if not q_fin.empty and not q_bs.empty:
        cols_q = q_fin.columns[:4]
        q_fin = q_fin[cols_q]
        q_bs = q_bs[cols_q]

        ebit_q = get_row(q_fin, ['EBIT', 'Operating Income', 'OperatingIncome'], fill=0)
        income_tax_expense_q = get_row(q_fin, ['Income Tax Expense', 'IncomeTaxExpense', 'Provision for Income Taxes'], fill=0)
        tax_rate_q = income_tax_expense_q / (get_row(q_fin, ['Income Before Tax', 'Pre-Tax Income'], fill=1))
        nopat_q = ebit_q * (1 - tax_rate_q)

        total_assets_q = get_row(q_bs, ['Total Assets', 'Assets'], fill=1)
        current_liabilities_q = get_row(q_bs, ['Current Liabilities'], fill=0)
        invested_capital_q = total_assets_q - current_liabilities_q

        roic_q = nopat_q / invested_capital_q

        df_q = pd.DataFrame({
            "ROIC": roic_q
        })
        df_q = df_q.T
        df_q.columns = [d.strftime('%Y-%m') for d in df_q.columns]

        print("\n📊 Derniers trimestres (TTM) ROIC :")
        print(df_q.applymap(lambda x: f"{x:.1%}"))

    else:
        print("Données trimestrielles non disponibles, essayez les semestres ou annuel.")

except Exception as e:
    print(f"Impossible de reconstituer l'historique ROIC ({e})")
