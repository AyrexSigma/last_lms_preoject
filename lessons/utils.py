from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.http import HttpResponse
from io import BytesIO


def generate_certificate_pdf(user, course):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    story = []
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='CertificateTitle', fontSize=48, leading=58, alignment=1,
                              textColor=colors.HexColor('#b8860b'), spaceAfter=30))
    styles.add(ParagraphStyle(name='Name', fontSize=56, leading=66, alignment=1, textColor=colors.HexColor('#1e3d59'),
                              spaceBefore=40, spaceAfter=40))
    styles.add(ParagraphStyle(name='Course', fontSize=36, leading=46, alignment=1, spaceBefore=30, spaceAfter=60))
    styles.add(ParagraphStyle(name='Date', fontSize=24, leading=34, alignment=1, textColor=colors.grey))

    story.append(Paragraph("СЕРТИФІКАТ", styles['CertificateTitle']))
    story.append(Paragraph("цього підтверджує, що", styles['Normal']))
    story.append(Paragraph(f"{user.get_full_name() or user.username}", styles['Name']))
    story.append(Paragraph("успішно завершив(ла) курс", styles['Normal']))
    story.append(Paragraph(course.title, styles['Course']))
    story.append(Paragraph(f"Дата завершення: {course.created_at.strftime('%d.%m.%Y')}", styles['Date']))
    story.append(Spacer(1, 60))
    story.append(Paragraph("LMS — Система управління навчанням", styles['Normal']))

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{course.title[:20]}_{user.username}.pdf"'
    return response