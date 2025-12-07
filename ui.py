import html as html_lib
from typing import Dict, Any

# --- Styling and helpers for UI ---
STYLE = """
<style>
body { font-family: 'Segoe UI', Tahoma, sans-serif; background:#f6f8fa; color:#222; margin:0; padding:0; }
.container { max-width:1000px; margin:36px auto; background:#fff; padding:28px; border-radius:12px; box-shadow:0 6px 24px rgba(0,0,0,0.08); }
h1 { color:#1a73e8; margin:0 0 10px 0; text-align:center;}
h2 { color:#333; margin-top:18px; border-bottom:1px solid #eee; padding-bottom:8px }
.form-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
@media(max-width:800px){ .form-grid{grid-template-columns:1fr} }
label { display:block; font-weight:600; margin-top:10px; }
input, select, textarea { width:100%; padding:10px; margin-top:6px; border-radius:8px; border:1px solid #d1d7e0; font-size:15px; }
textarea { min-height:110px; }
.checkbox-group,label.radio-group { margin-top:8px; }
button { background:#1a73e8; color:#fff; padding:12px 18px; border-radius:8px; border:none; cursor:pointer; margin-top:18px; font-weight:700; }
.progress { display:flex; gap:12px; margin-bottom:18px; justify-content:space-between; }
.step { flex:1; text-align:center; color:#a2abb8; font-weight:700; position:relative; padding:8px 6px; }
.step.active { color:#1a73e8; }
.step::before { content:'●'; display:block; font-size:20px; margin-bottom:6px; }
.step:not(:last-child)::after { content:''; position:absolute; right:-6px; top:22px; width:12px; height:4px; background:#e6e9ee; z-index:-1; }
.step.active:not(:last-child)::after { background:#1a73e8; }
.loader { border:4px solid #f3f3f3; border-top:4px solid #1a73e8; border-radius:50%; width:44px; height:44px; animation:spin 1s linear infinite; margin:28px auto; }
@keyframes spin { 0%{transform:rotate(0)}100%{transform:rotate(360deg)} }
.rfp-output { background:#fafbfd; padding:18px; border-radius:10px; white-space:pre-wrap; line-height:1.5; font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Monaco, "Roboto Mono", "Courier New", monospace; }
.download { display:inline-block; margin-top:18px; background:#22a66b; color:#fff; padding:10px 16px; border-radius:8px; text-decoration:none; }
.notice { margin-top:12px; color:#666; font-size:14px }
</style>
"""

def render_progress(step: int):
    steps = ["1. Basic Info", "2. Details & Scoring", "3. Generate RFP"]
    html = '<div class="progress">'
    for i, label in enumerate(steps, start=1):
        cls = "step active" if i <= step else "step"
        html += f'<div class="{cls}">{label}</div>'
    html += "</div>"
    return html


def generate_form_html(schema: Dict[str, Any], action="/submit", defaults: Dict[str, Any] = None):
    defaults = defaults or {}
    sections: Dict[str, list] = {}
    for field in schema.get("fields", []):
        section = field.get("section", "General")
        sections.setdefault(section, []).append(field)

    html = STYLE
    html += '<div class="container">'
    html += render_progress(1)
    html += f"<h1>{html_lib.escape(schema.get('title', 'Form'))}</h1>"
    html += f'<form method="post" action="{action}">'

    for section, fields in sections.items():
        html += f"<h2>{html_lib.escape(section)}</h2>"
        html += '<div class="form-grid">'
        for field in fields:
            name = field.get("name")
            label = field.get("label", name)
            ftype = field.get("type", "text")
            default = defaults.get(name, field.get("default", ""))

            html += "<div>"
            html += f'<label for="{html_lib.escape(name)}">{html_lib.escape(label)}</label>'

            if ftype in ("text", "email", "tel", "number"):
                val = html_lib.escape(str(default)) if default is not None else ""
                required = "required" if field.get("required", False) else ""
                html += f'<input type="{ftype}" name="{html_lib.escape(name)}" value="{val}" {required}>'
            elif ftype == "textarea":
                val = html_lib.escape(str(default)) if default is not None else ""
                html += f'<textarea name="{html_lib.escape(name)}">{val}</textarea>'
            elif ftype == "select":
                html += f'<select name="{html_lib.escape(name)}">'
                for opt in field.get("options", []):
                    sel = 'selected' if str(opt) == str(default) else ''
                    html += f'<option value="{html_lib.escape(str(opt))}" {sel}>{html_lib.escape(str(opt))}</option>'
                html += '</select>'
            elif ftype == "checkbox":
                html += '<div class="checkbox-group">'
                for opt in field.get("options", []):
                    checked = ""
                    if isinstance(default, list) and str(opt) in [str(x) for x in default]:
                        checked = "checked"
                    elif isinstance(default, str) and str(opt) in default.split(","):
                        checked = "checked"
                    html += f'<label><input type="checkbox" name="{html_lib.escape(name)}" value="{html_lib.escape(str(opt))}" {checked}> {html_lib.escape(str(opt))}</label>'
                html += '</div>'
            elif ftype == "radio":
                html += '<div class="radio-group">'
                for opt in field.get("options", []):
                    checked = "checked" if str(opt) == str(default) else ""
                    html += f'<label><input type="radio" name="{html_lib.escape(name)}" value="{html_lib.escape(str(opt))}" {checked}> {html_lib.escape(str(opt))}</label>'
                html += '</div>'
            else:
                html += f'<input type="text" name="{html_lib.escape(name)}" value="{html_lib.escape(str(default))}">'
            html += "</div>"
        html += '</div>'
    html += '<button type="submit">Continue</button></form></div>'
    return html


def loading_page(title: str, redirect_url: str, message: str = ""):
    html = STYLE
    html += '<div class="container">'
    html += f"<h1>⏳ {html_lib.escape(title)}</h1>"
    html += '<div class="loader"></div>'
    if message:
        html += f"<p class='notice'>{html_lib.escape(message)}</p>"
    html += f"""
    <script>
      setTimeout(function(){{ window.location.href = '{redirect_url}'; }}, 800);
    </script>
    """
    html += "</div>"
    return html


def result_page(title: str, content: str, download_link: str = None, download_text: str = "Download", back_link: str = None):
    html = STYLE
    html += '<div class="container">'
    html += f"<h1>{html_lib.escape(title)}</h1>"
    html += f'<div class="rfp-output">{html_lib.escape(content)}</div>'
    if download_link:
        html += f'<a class="download" href="{download_link}">{html_lib.escape(download_text)}</a>'
    if back_link:
        html += f'<p><a href="{back_link}">← Back</a></p>'
    else:
        html += '<p><a href="/">← Start New Initiative</a></p>'
    html += "</div>"
    return html


def rfp_result_page(initiative_id: int, schema_name: str, rfp_text: str):
    safe_text = html_lib.escape(rfp_text)
    html = STYLE
    html += '<div class="container">'
    html += render_progress(3)
    html += "<h1>📄 Generated RFP</h1>"
    html += f'<div class="rfp-output">{safe_text}</div>'
    html += f'<a class="download" href="/download_rfp/{initiative_id}">⬇️ Download RFP (.docx)</a>'
    html += '<p class="notice">Generated by local Mistral (Ollama). Review and edit the document as needed.</p>'
    html += f'<a class="download" style="background-color:#3367D6;" href="/find_vendors/{initiative_id}/{schema_name}">🔍 Find Vendors</a>'
    html += f'<a class="download" href="/upload_vendor_responses/{initiative_id}">⬆️ Upload Vendor Responses</a>'
    html += "</div>"
    return html


def upload_vendor_form_page(initiative_id: int):
    return STYLE + f"""
    <div class="container">
        <h1>📤 Upload Vendor Responses</h1>
        <form action="/upload_vendor_responses/{initiative_id}" method="post" enctype="multipart/form-data">
            <p>Please upload between <b>2 and 7</b> vendor response files (PDF, DOCX, or TXT).</p>
            <input type="file" name="files" multiple required accept=".pdf,.docx,.txt">
            <br><br>
            <button type="submit">Upload & Compare</button>
        </form>
        <p class="notice">Each vendor response will be analyzed and compared using AI.</p>
    </div>
    """