from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(filename, transcript, summary, output_path):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(output_path)

    story = []

    story.append(Paragraph("<b>AI Meeting Assistant</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Meeting:</b> {filename}", styles["Heading2"]))

    story.append(Paragraph("<br/><b>Transcript</b>", styles["Heading2"]))
    story.append(Paragraph(transcript.replace("\n", "<br/>"), styles["BodyText"]))

    story.append(Paragraph("<br/><b>Summary</b>", styles["Heading2"]))
    story.append(Paragraph(summary.replace("\n", "<br/>"), styles["BodyText"]))

    pdf.build(story)