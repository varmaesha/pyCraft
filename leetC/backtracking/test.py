from jinja2 import Template
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

# --- Read the Template from file ---
with open(r"c:\Users\esha.varma\OneDrive - Fractal Analytics Pvt. Ltd\Desktop\test\pyCraft\leetC\backtracking\resoultion.txt", "r", encoding="utf-8") as f:
    resolution_template = f.read()

# --- Dynamic Data ---
data =[ {
    "company_name": "Costa Coral Hospitality Private Limited",
    "company_address": "SF-45, Samvet Shikhar, Rajbandha Maidan, Raipur, Chhattisgarh 492001",
    "contact_number": "+919552720000",
    "email": "costaboss@gmail.com",
    "meeting_date": "02nd day of May, 2025",
    "meeting_time": "11:00am",
    "director_name": "Tripti Bajel",
    "director_din": "11082550",
    "signed_by": "Amit Kumar Sharma",
    "signed_by_din": "07973333",
    "resolution_date": datetime.now().strftime("%B %d, %Y"),
    "resolution_place": "Raipur, Chhattisgarh 492001",
},
 {
    "company_name": "qwertyui",
    "company_address": "SF-45, Samvet Shikhar, Rajbandha Maidan, Raipur, Chhattisgarh 492001",
    "contact_number": "+919552720000",
    "email": "costaboss@gmail.com",
    "meeting_date": "02nd day of May, 2025",
    "meeting_time": "11:00am",
    "director_name": "Tripti Bajel",
    "director_din": "11082550",
    "signed_by": "Amit Kumar Sharma",
    "signed_by_din": "07973333",
    "resolution_date": datetime.now().strftime("%B %d, %Y"),
    "resolution_place": "Raipur, Chhattisgarh 492001",
},
 {
    "company_name": "asdfghjk",
    "company_address": "SF-45, Samvet Shikhar, Rajbandha Maidan, Raipur, Chhattisgarh 492001",
    "contact_number": "+919552720000",
    "email": "costaboss@gmail.com",
    "meeting_date": "02nd day of May, 2025",
    "meeting_time": "11:00am",
    "director_name": "Tripti Bajel",
    "director_din": "11082550",
    "signed_by": "Amit Kumar Sharma",
    "signed_by_din": "07973333",
    "resolution_date": datetime.now().strftime("%B %d, %Y"),
    "resolution_place": "Raipur, Chhattisgarh 492001",
}]

# --- Render the Document ---
template = Template(resolution_template)

# --- Generate PDF for each company ---
def create_pdf(text, output_filename):
    c = canvas.Canvas(output_filename, pagesize=A4)
    width, height = A4
    margin = 50
    text_object = c.beginText(margin, height - margin)
    text_object.setFont("Times-Roman", 12)
    
    for line in text.split("\n"):
        line = line.strip()
        while len(line) > 90:
            text_object.textLine(line[:90])
            line = line[90:]
        if line:
            text_object.textLine(line)
    
    c.drawText(text_object)
    c.showPage()
    c.save()

for item in data:
    rendered_text = template.render(**item)
    output_pdf = f"{item['company_name'].replace(' ', '_')}_resolution.pdf"
    create_pdf(rendered_text, output_pdf)
    print(f"PDF generated successfully: {output_pdf}")
