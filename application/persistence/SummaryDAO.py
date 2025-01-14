from application.configuration.firebase_config import db
from application.models.Summary import Summary
import logging

class SummaryDAO:

    def __init__(self):
        self.initialize_logging()
        self.db = db

    def initialize_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='summary_dao.log',
            filemode='a'
        )

    def update_summary(self, summary):
        try:
            doc_ref = self.db.collection("summary").document(f"{summary.get_month_and_year()}")
            
            doc_ref.update({
                "total": summary.get_total(),
                "last_total": summary.get_last_total(),
                "last_months_total": summary.get_last_months_total(),
                "last_months_total_today": summary.get_last_months_total_today(), 
                "last_report_date" : summary.get_last_report_date()
            })
            return doc_ref.get().to_dict()
        except Exception as e:
            print(f"Error al actualizar el documento: {e}")
            raise 

    def save(self, summary):
        doc_ref = self.db.collection("summary").document(f"{summary.get_month_and_year()}")
        summary_dict = summary.to_summary_dict()
        doc_ref.set(summary_dict)
        return summary

    # devuelve el objeto summary con el month_and_year dado
    def find(self, month_and_year):
        doc_ref = self.db.collection("summary").document(f"{month_and_year}")
        doc = doc_ref.get()
        if doc.exists:
            return Summary.from_dict(month_and_year, doc.to_dict())
        return None 
    
    # devuelve el objeto como un JSON evitando crear una instancia de Summary
    def get_json(self, month_and_year):
        doc_ref = self.db.collection("summary").document(f"{month_and_year}")
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return {"message": "Ocurrio un error al recuperar la info"}
    

    


   