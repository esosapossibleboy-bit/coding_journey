from fpdf import FPDF

def build_statement_pdf(user_name: str, summary: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Private Budget Statement - {summary['month_year']}", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Account Holder: {user_name}", ln=True)
    pdf.cell(
        0,
        8,
        f"Income: ${summary['income']:.2f}   |   Expenses: ${summary['expenses']:.2f}   |   Balance: ${summary['balance']:.2f}",
        ln=True,
    )
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Transaction History:", ln=True)
    pdf.set_font("Helvetica", "", 10)

    if not summary["transactions"]:
        pdf.cell(0, 8, "No transactions recorded for this month.", ln=True)
    else:
        for tx in summary["transactions"]:
            sign = "+" if tx["kind"] == "income" else "-"
            safe_line = (
                f"[{tx['created_at']}] {tx['title']} ({tx['category']}) : {sign}${tx['amount']:.2f}"
            ).encode("latin-1", "replace").decode("latin-1")
            pdf.cell(0, 7, safe_line, ln=True)

    return bytes(pdf.output())
