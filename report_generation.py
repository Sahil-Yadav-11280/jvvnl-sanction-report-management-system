from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter


pdfmetrics.registerFont(TTFont('Arial-Black', 'C:\\Windows\\Fonts\\ariblk.ttf'))


def generate_report(data: list, filename):
    # 1. Set up the document layout and margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    book_no = data[0]
    serial_no = data[1]
    office = data[2]
    to_jen = data[3]
    date = data[4]
    estimate_no = data[5]
    estimate_date = data[6]
    description = data[7]
    allocation = data[8]
    acc_no = data[9]
    cons_name_add = data[10]
    mobile_no = data[11]
    service_no = data[12]
    consumer_no = data[13]
    Story = []

    # 2. Define all Text Styles used in the document
    title_style = ParagraphStyle('TitleStyle', fontName='Arial-Black', fontSize=18, alignment=TA_CENTER,
                                 spaceAfter=12)
    office_style = ParagraphStyle('OfficeStyle', fontName='Helvetica', fontSize=12, alignment=TA_CENTER, spaceAfter=24)
    order_style = ParagraphStyle('OrderStyle', fontName='Times-Bold', fontSize=14, alignment=TA_CENTER, spaceAfter=24)

    body_style = ParagraphStyle('BodyStyle', fontName='Times-Roman', fontSize=12, alignment=TA_LEFT, spaceAfter=12)
    body_style_no_space = ParagraphStyle('BodyStyleNoSpace', fontName='Times-Roman', fontSize=12, alignment=TA_LEFT)

    center_text_style = ParagraphStyle('CenterText', fontName='Times-Roman', fontSize=12, alignment=TA_CENTER,
                                       spaceAfter=12)
    bold_center_style = ParagraphStyle('BoldCenter', fontName='Times-Bold', fontSize=12, alignment=TA_CENTER,
                                       spaceAfter=12)

    right_bold_style = ParagraphStyle('RightBold', fontName='Times-Bold', fontSize=12, alignment=TA_RIGHT, spaceAfter=8)

    # Calculate exactly half the page width for the two-column layouts
    usable_width = doc.width
    col_width = usable_width / 3.0

    # --- TOP SECTION ---
    Story.append(Paragraph("Jaipur Vidhyut Vitaan Nigam Limited", title_style))
    Story.append(Paragraph(f"<b>Office</b> - {office}", office_style))
    Story.append(Paragraph("SUNDRY JOB ORDER", order_style))

    # --- FIRST DATA TABLE (Top Fields) ---
    table_data_1 = [
        [
            Paragraph(f"<b>Book No:</b> {book_no}", body_style_no_space),
            '',
            Paragraph(f"<b>Serial No:</b> {serial_no}", body_style_no_space)
        ],
        [
            Paragraph(f"<b>To:</b> {to_jen}", body_style_no_space),
            '',
            Paragraph(f"<b>Date:</b> {date}", body_style_no_space)
        ],
        [
            Paragraph(f"<b>Estimate no:</b> {estimate_no}", body_style_no_space),
            '',
            Paragraph(f"<b>Estimate date:</b> {estimate_date}", body_style_no_space)
        ]
    ]
    t1 = Table(table_data_1, colWidths=[col_width, col_width])
    t1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15)
    ]))
    Story.append(t1)

    # Add some space before the description
    Story.append(Spacer(1, 30))

    # --- MIDDLE SECTION (Work Description) ---
    Story.append(Paragraph("Please execute the following work and on completion report as under: -", center_text_style))
    Story.append(Paragraph("DESCRIPTION OF WORK", bold_center_style))
    Story.append(Paragraph(f"{description}", center_text_style))

    # Large vertical space to simulate the empty area for writing/data
    Story.append(Spacer(1, 80))

    # --- LOWER FIELDS ---
    Story.append(Paragraph(f"<b>Allocation:</b> {allocation}", body_style))
    Story.append(Paragraph(f"<b>Account Number:</b> {acc_no}", body_style))
    Story.append(Paragraph(f"<b>Consumer name and address:</b> {cons_name_add}", body_style))
    Story.append(Paragraph(f"<b>Consumer Mobile Number:</b> {mobile_no}", body_style))

    # --- SECOND DATA TABLE (Bottom Fields) ---
    table_data_2 = [
        [
            Paragraph(f"<b>Service no:</b> {service_no}", body_style_no_space),
            '',
            Paragraph(f"<b>Consumer no:</b> {consumer_no}", body_style_no_space)
        ]
    ]
    t2 = Table(table_data_2, colWidths=[col_width, col_width])
    t2.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    Story.append(t2)

    # Large space to push the signature block to the bottom of the page
    Story.append(Spacer(1, 100))

    # --- SIGNATURE BLOCK ---
    Story.append(Paragraph("Assistant Engineer (O&M)", right_bold_style))
    Story.append(Paragraph("JVVNL Behror Rural", right_bold_style))

    # 3. Build and save the document
    doc.build(Story)
    print(f"File created successfully at {filename}")
    return filename
