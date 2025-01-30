from application.configuration.firebase_config import db
from application.models.Summary import Summary
import logging
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta

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
                "last_report_date" : summary.get_last_report_date(),
                "date_of_lmtt" : summary.get_date_of_lmtt(),
                "date_of_lmt" : summary.get_date_of_lmt()
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
    
    # devuelve el campo dado por parametro 
    def get_field_of(self, month_and_year, field):
        doc_ref = self.db.collection("summary").document(f"{month_and_year}")
        doc = doc_ref.get([field])  

        if doc.exists:
            return doc.to_dict().get(field)
        return None

    
    # devuelve el campo dado por parametro 
    def update_field_of(self, month_and_year, field, value):
        doc_ref = self.db.collection("summary").document(f"{month_and_year}")
        doc_ref.update({field: value}) 

    
# if __name__ == "__main__":
#     dao = SummaryDAO()
#     dao.update_field_of("1-2025", "date_of_lmt", (datetime.now(pytz.timezone("America/Argentina/Buenos_Aires")) - relativedelta(months=1) ))


   