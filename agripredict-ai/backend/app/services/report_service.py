"""Report generation service - PDF and CSV."""

import csv
import io
from datetime import datetime
from typing import Dict, Any, Optional

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        HRFlowable
    )
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


def generate_pdf_report(analysis_data: Dict[str, Any], output_path: str) -> str:
    """Generate a PDF report from analysis data."""
    if not HAS_REPORTLAB:
        raise ImportError("reportlab is required for PDF generation")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Title'],
        fontSize=20, textColor=HexColor('#1a5d1a'),
        spaceAfter=20,
    )
    heading_style = ParagraphStyle(
        'CustomHeading', parent=styles['Heading2'],
        textColor=HexColor('#2d6a2e'),
        spaceAfter=10, spaceBefore=15,
    )
    body_style = styles['Normal']
    small_style = ParagraphStyle(
        'SmallText', parent=styles['Normal'],
        fontSize=8, textColor=HexColor('#666666'),
    )

    elements = []

    # Title
    elements.append(Paragraph("🌾 AgriPredict AI — Farm Analysis Report", title_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}", small_style))
    elements.append(Spacer(1, 15))
    elements.append(HRFlowable(width="100%", color=HexColor('#1a5d1a'), thickness=2))
    elements.append(Spacer(1, 15))

    # Farm Details
    farm = analysis_data.get("farm", {})
    if farm:
        elements.append(Paragraph("Farm Details", heading_style))
        farm_data = [
            ["District", farm.get("district", "N/A")],
            ["State", farm.get("state", "Andhra Pradesh")],
            ["Land Area", f"{farm.get('land_area', 'N/A')} {farm.get('land_unit', 'acres')}"],
            ["Soil Type", farm.get("soil_type", "N/A")],
            ["Irrigation", farm.get("irrigation_type", "N/A")],
            ["Season", farm.get("farming_season", "N/A")],
        ]
        table = Table(farm_data, colWidths=[150, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#e8f5e9')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 15))

    # Weather Summary
    weather = analysis_data.get("weather", {})
    if weather:
        elements.append(Paragraph("Historical Weather Summary", heading_style))
        annual = weather.get("annual_rainfall", {})
        for year, rain in sorted(annual.items()):
            elements.append(Paragraph(f"• {year}: {rain}mm annual rainfall", body_style))
        elements.append(Paragraph(f"Data source: {weather.get('data_source', 'N/A')}", small_style))
        elements.append(Spacer(1, 10))

    # Crop Recommendations
    crops = analysis_data.get("crops", [])
    if crops:
        elements.append(Paragraph("Crop Recommendations", heading_style))
        crop_data = [["Rank", "Crop", "Score", "Season", "Water Need"]]
        for c in crops[:5]:
            crop_data.append([
                str(c.get("rank", "")),
                c.get("crop_name", ""),
                f"{c.get('suitability_score', 0)}/100",
                c.get("season", ""),
                c.get("water_requirement", ""),
            ])
        table = Table(crop_data, colWidths=[40, 130, 60, 100, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a5d1a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f5f5f5')]),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 10))

    # Risk Assessment
    risk = analysis_data.get("risk", {})
    if risk:
        elements.append(Paragraph("Weather Risk Assessment", heading_style))
        elements.append(Paragraph(f"Overall Risk Level: {risk.get('overall_risk', 'N/A')}", body_style))
        for r in risk.get("risks", []):
            elements.append(Paragraph(
                f"• {r.get('category', '')}: {r.get('level', '')} — {r.get('explanation', '')}",
                body_style
            ))
        elements.append(Spacer(1, 10))

    # Financial Summary
    finance = analysis_data.get("finance", {})
    if finance:
        elements.append(Paragraph("Financial Estimate", heading_style))
        fin_data = [
            ["Total Cultivation Cost", f"₹{finance.get('total_cultivation_cost', 0):,.2f}"],
            ["Expected Gross Revenue", f"₹{finance.get('expected_gross_revenue', 0):,.2f}"],
            ["Estimated Net Return", f"₹{finance.get('estimated_net_return', 0):,.2f}"],
            ["Break-Even Price", f"₹{finance.get('break_even_price', 0):,.2f}/quintal"],
            ["Return Per Acre", f"₹{finance.get('return_per_acre', 0):,.2f}"],
        ]
        table = Table(fin_data, colWidths=[200, 250])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#fff3e0')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 10))

    # Disclaimer
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", color=colors.grey, thickness=0.5))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(
        "DISCLAIMER: All predictions, recommendations, and financial estimates in this report "
        "are approximate and based on available historical data, weather forecasts, and analytical models. "
        "Actual agricultural outcomes depend on crop management, local conditions, weather events, "
        "and market dynamics. This report is intended to support decision-making and does not guarantee outcomes.",
        small_style
    ))
    elements.append(Paragraph("Generated by AgriPredict AI — agripredict.ai", small_style))

    doc.build(elements)
    return output_path


def generate_csv_report(analysis_data: Dict[str, Any]) -> str:
    """Generate a CSV string from analysis data."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(["AgriPredict AI — Farm Analysis Report"])
    writer.writerow([f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}"])
    writer.writerow([])

    # Farm details
    farm = analysis_data.get("farm", {})
    writer.writerow(["=== Farm Details ==="])
    for key, val in farm.items():
        writer.writerow([key, val])
    writer.writerow([])

    # Weather
    weather = analysis_data.get("weather", {})
    writer.writerow(["=== Historical Rainfall (mm) ==="])
    for year, rain in sorted(weather.get("annual_rainfall", {}).items()):
        writer.writerow([year, rain])
    writer.writerow([])

    # Crops
    crops = analysis_data.get("crops", [])
    writer.writerow(["=== Crop Recommendations ==="])
    writer.writerow(["Rank", "Crop", "Score", "Season", "Water", "Reason"])
    for c in crops:
        writer.writerow([
            c.get("rank"), c.get("crop_name"), c.get("suitability_score"),
            c.get("season"), c.get("water_requirement"), c.get("reason"),
        ])
    writer.writerow([])

    # Risks
    risk = analysis_data.get("risk", {})
    writer.writerow(["=== Risk Assessment ==="])
    writer.writerow(["Category", "Level", "Explanation"])
    for r in risk.get("risks", []):
        writer.writerow([r.get("category"), r.get("level"), r.get("explanation")])
    writer.writerow([])

    # Finance
    finance = analysis_data.get("finance", {})
    writer.writerow(["=== Financial Estimate ==="])
    for key in ["total_cultivation_cost", "expected_gross_revenue", "estimated_net_return",
                 "break_even_price", "return_per_acre", "financial_risk_level"]:
        writer.writerow([key, finance.get(key, "N/A")])
    writer.writerow([])

    # Disclaimer
    writer.writerow(["DISCLAIMER: All values are estimates. Actual results may vary."])

    return output.getvalue()
