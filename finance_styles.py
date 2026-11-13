FINANCE_CSS = """
<style>
    * { box-sizing: border-box; }
    body { background:#1e1e2e; color:#cdd6f4; font-family:system-ui,sans-serif; margin:0; padding:16px; }
    .container { max-width:980px; margin:0 auto; }
    h1 { font-size:clamp(1.3rem, 4vw, 1.9rem); text-align:center; color:#89b4fa; }
    .grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(290px, 1fr)); gap:16px; }
    .card { background:#11111b; padding:20px; border-radius:14px; border:1px solid #313244; }
    input, select, button { width:100%; padding:12px; margin-top:10px; border-radius:8px; border:1px solid #45475a; background:#181825; color:white; font-size:16px; }
    button { background:#89b4fa; color:#11111b; font-weight:bold; border:none; cursor:pointer; }
    .btn-secondary { background:#313244; color:white; }
    .btn-danger { background:#f38ba8; color:#11111b; padding:6px 10px; width:auto; margin:0; font-size:14px; }
    .btn-edit { background:#f9e2af; color:#11111b; padding:6px 10px; width:auto; margin:0 6px 0 0; font-size:14px; }
    .tx-row { display:flex; justify-content:space-between; align-items:center; gap:8px; padding:10px 0; border-bottom:1px solid #313244; }
    .balance { color:#a6e3a1; font-size:1.8rem; margin:0 0 8px 0; }
    .advice { color:#f9e2af; font-weight:bold; }
    .error { color:#f38ba8; font-size:0.9rem; margin-top:8px; }
</style>
"""
