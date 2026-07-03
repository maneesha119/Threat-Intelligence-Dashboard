import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf(ip, threat, score, geo, vt):
    
    output_dir = "reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_path = os.path.join(output_dir, f"threat_report_{ip}.pdf")
    
    # PDF Document Setup (Margins 40)
    doc = SimpleDocTemplate(file_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    # Styles Setup
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'PDFTitle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor("#1e3a8a"), spaceAfter=0, spaceBefore=0
    )
    
    date_style = ParagraphStyle(
        'PDFDate', parent=styles['Normal'], fontSize=9, leading=12, textColor=colors.HexColor("#64748b"), alignment=2
    )
    
    section_style = ParagraphStyle(
        'PDFSection', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#2563eb"), spaceBefore=15, spaceAfter=10
    )
    text_style = ParagraphStyle(
        'PDFText', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor("#1f2937")
    )
    bold_text = ParagraphStyle(
        'PDFTextBold', parent=text_style, fontName="Helvetica-Bold"
    )

    # 🛠️ HEADER SECTION 
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    header_table_data = [
        [Paragraph("Threat Intelligence Report", title_style), Paragraph(f"Generated On:<br/>{timestamp}", date_style)]
    ]
    
    
    header_table = Table(header_table_data, colWidths=[352, 180])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'), 
        ('PADDING', (0,0), (-1,-1), 0),      
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 15)) 
    
    # Table Styling Template
    table_style = TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VERTICALALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ])

    # Section 1: General Info
    story.append(Paragraph("1. Target & Threat Summary", section_style))
    summary_data = [
        [Paragraph("Metric", bold_text), Paragraph("Value", bold_text)],
        [Paragraph("IP Address", text_style), Paragraph(str(ip), text_style)],
        [Paragraph("Threat Level", text_style), Paragraph(str(threat), text_style)],
        [Paragraph("Abuse Confidence Score", text_style), Paragraph(f"{score}%", text_style)]
    ]
    t1 = Table(summary_data, colWidths=[180, 320])
    t1.setStyle(table_style)
    story.append(t1)
    
    # Section 2: VirusTotal
    story.append(Paragraph("2. VirusTotal Detection Statistics", section_style))
    vt_malicious = "0"
    vt_suspicious = "0"
    vt_harmless = "0"
    vt_undetected = "0"
    
    if vt and "data" in vt:
        stats = vt["data"]["attributes"]["last_analysis_stats"]
        vt_malicious = str(stats.get("malicious", 0))
        vt_suspicious = str(stats.get("suspicious", 0))
        vt_harmless = str(stats.get("harmless", 0))
        vt_undetected = str(stats.get("undetected", 0))
        
    vt_data = [
        [Paragraph("Analysis", bold_text), Paragraph("Count", bold_text)],
        [Paragraph("Malicious", text_style), Paragraph(vt_malicious, text_style)],
        [Paragraph("Suspicious", text_style), Paragraph(vt_suspicious, text_style)],
        [Paragraph("Harmless", text_style), Paragraph(vt_harmless, text_style)],
        [Paragraph("Undetected", text_style), Paragraph(vt_undetected, text_style)]
    ]
    t2 = Table(vt_data, colWidths=[180, 320])
    t2.setStyle(table_style)
    story.append(t2)

    # Section 3: Geolocation
    story.append(Paragraph("3. Geolocation Intelligence", section_style))
    country = geo.get("country", "Unknown") if geo else "Unknown"
    city = geo.get("city", "Unknown") if geo else "Unknown"
    region = geo.get("regionName", "Unknown") if geo else "Unknown"
    
    geo_data = [
        [Paragraph("Location Detail", bold_text), Paragraph("Value", bold_text)],
        [Paragraph("Country", text_style), Paragraph(str(country), text_style)],
        [Paragraph("City", text_style), Paragraph(str(city), text_style)],
        [Paragraph("Region", text_style), Paragraph(str(region), text_style)]
    ]
    t3 = Table(geo_data, colWidths=[180, 320])
    t3.setStyle(table_style)
    story.append(t3)

    doc.build(story)
    return file_path