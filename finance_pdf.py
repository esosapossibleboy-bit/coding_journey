from fpdf import FPDF, XPos, YPos

PDF_CURRENCY_LABELS = {"€": "EUR ", "£": "GBP ", "₦": "NGN ", "¥": "JPY ", "₹": "INR "}

def clean_latin1(text: str) -> str:
    return str(text).encode("latin-1", "replace").decode("latin-1")

def build_statement_pdf(user_name: str, summary: dict, currency: str = "$") -> bytes:
    cur = PDF_CURRENCY_LABELS.get(currency, currency or "$")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, clean_latin1(f"Private Budget Statement - {summary.get('month_year', '')}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, clean_latin1(f"Account Holder: {user_name}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    totals = f"Income: {cur}{summary['income']:.2f}   |   Expenses: {cur}{summary['expenses']:.2f}   |   Balance: {cur}{summary['balance']:.2f}"
    pdf.cell(0, 8, clean_latin1(totals), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Transaction History:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)

    if not summary["transactions"]:
        pdf.cell(0, 8, "No transactions recorded for this month.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    else:
        for tx in summary["transactions"]:
            sign = "+" if tx["kind"] == "income" else "-"
            when = tx.get("created_at") or tx.get("month_year") or ""
            raw_line = f"[{when}] {tx['title']} ({tx['category']}) : {sign}{cur}{tx['amount']:.2f}"
            pdf.cell(0, 7, clean_latin1(raw_line), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    raw_out = pdf.output()
    return raw_out.encode("latin-1") if isinstance(raw_out, str) else bytes(raw_out)
