from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def format_description_text(description_list):
    formatted_description = ""
    for heading, content in description_list:
        formatted_description += f"<b>{heading}</b><br/>{content}<br/><br/>"
    return formatted_description

def create_pdf(file_name, title_text, description_list, table_data):
    # Create a document with a given filename and page size
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    elements = []

    # Define custom styles
    styles = getSampleStyleSheet()

    # Title style: bold, larger font
    title_style = ParagraphStyle(
        name='Title',
        fontSize=16,
        leading=20,  # Space between lines
        alignment=1,  # Center alignment
        spaceAfter=12,  # Space after the title
        fontName='Helvetica-Bold'
    )

    # Body text style: normal font with line spacing
    body_style = ParagraphStyle(
        name='Body',
        fontSize=12,
        leading=15,  # Space between lines
        spaceAfter=12  # Space after each paragraph
    )

    # Add the title
    title = Paragraph(title_text, title_style)
    elements.append(title)

    # Create a paragraph with spacing between paragraphs and bold elements
    description_text = format_description_text(description_list)
    description_paragraph = Paragraph(description_text, body_style)
    elements.append(description_paragraph)

    # Add some space before the table
    elements.append(Spacer(1, 0.2 * inch))

    # Create table from the data
    data = [table_data.columns.to_list()] + table_data.values.tolist()

    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    elements.append(table)

    # Build the PDF
    doc.build(elements)