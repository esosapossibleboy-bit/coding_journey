from fpdf import FPDF

def build_statement_pdf(user_name: str, summary: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    safe_title = f"Private Budget Statement - {summary.get('month_year', '')}".encode("latin-1", "replace").decode("latin-1")
    pdf.cell(0, 10, safe_title, ln=True)

    pdf.set_font("Helvetica", "", 11)
    safe_user = f"Account Holder: {user_name}".encode("latin-1", "replace").decode("latin-1")
    pdf.cell(0, 8, safe_user, ln=True)
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
            when = tx.get("created_at") or tx.get("month_year") or ""
            raw_line = f"[{when}] {tx['title']} ({tx['category']}) : {sign}${tx['amount']:.2f}"
            safe_line = raw_line.encode("latin-1", "replace").decode("latin-1")
            pdf.cell(0, 7, safe_line, ln=True)

    return bytes(pdf.output())
