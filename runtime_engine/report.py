from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

class Report:
    def __init__(self) -> None:
        self.alerts = [["Model element", "Description", "Triggered rule", "Criticality"]]
        self.obsoletes = [["Model element", "Description", "Triggered rule", "Criticality"]]

    @property
    def alerts(self):
        return self.__alerts

    @alerts.setter
    def alerts(self, alerts):
        self.__alerts = alerts

    def add_alert(self, alert):
        self.alerts.append(alert)

    @property
    def obsoletes(self):
        return self.__obsoletes

    @obsoletes.setter
    def obsoletes(self, obsoletes):
        self.__obsoletes = obsoletes

    def add_obsolete(self, obsolete):
        self.obsoletes.append(obsolete)
    
    def generate_report(self, file_name, model_name, date):
        doc = SimpleDocTemplate(file_name, pagesize=letter)
        
        # PDF content
        elements = []
        
        # Tittle
        styles = getSampleStyleSheet()
        title = Paragraph("Obsolescence Report <br/><br/>", styles['Title'])
        elements.append(title)
        
        # Description
        model = Paragraph("<b>Model:</b> " + model_name, styles['Normal'])
        elements.append(model)
        datetime_str = date.strftime("%B %d, %Y - %H:%M:%S")
        date = Paragraph("<b>Date:</b> " + datetime_str +"<br/><br/>", styles['Normal'])
        elements.append(date)
        
        # Create table with elements obsoletes
        legendT1 = Paragraph("<u>Obsolete Model elements</u>:<br/><br/>", styles['Normal'])
        elements.append(legendT1)
        table_obsolete = Table(self.obsoletes)
        elements.append(table_obsolete)
        
        
        # Create table with elements gaining obsolescence
        legendT2 = Paragraph("<br/><br/>Model elements experiencing obsolescence:<br/><br/>", styles['Normal'])
        elements.append(legendT2)
        table_alerts = Table(self.alerts)
        elements.append(table_alerts)

        # Table style
        style = TableStyle([('BACKGROUND', (0,0), (-1,0), colors.Color(0.16, 0.43, 0.51)),
                            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0,0), (-1,0), 12),
                            ('BACKGROUND', (0,1), (-1,-1), colors.Color(0.87, 0.92, 0.92)),
                            ('GRID', (0,0), (-1,-1), 1, colors.transparent),
                            ('LINEABOVE', (0,1), (-1,-1), 0, colors.white)])
        
        table_obsolete.setStyle(style)
        table_obsolete._argW = [100, 230, 80, 70]
        table_alerts.setStyle(style)
        table_alerts._argW = [100, 230, 80, 70]

        # Generate PDF
        doc.build(elements)