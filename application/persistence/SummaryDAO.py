import logging
from application.configuration.firebase_config import db
from application.automation.Summary import Summary
from datetime import datetime
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
    def find_or_create(self, month_and_year):
        doc_ref = self.db.collection("summary").document(f"{month_and_year}")
        doc = doc_ref.get()
        if doc.exists:
            return Summary.from_dict(month_and_year, doc.to_dict())
        else:
            return self.save(Summary(month_and_year))

    def update_summary(self, summary):
        try:
            doc_ref = self.db.collection("summary").document(f"{summary.get_month_and_year()}")
            doc_ref.update({
                "total": summary.get_total(),
                "last_total": summary.get_last_total(),
                "last_months_total": summary.get_last_months_total(),
                "last_months_total_today": summary.get_last_months_total_today(), 
                "last_report_date" : summary.get_last_report_date(),
                "message_last_months_total" : summary.get_message_last_months_total(),
                "message_last_months_total_today" : summary.get_message_last_months_total_today()
            })
            return doc_ref.get().to_dict()
        except Exception as e:
            print(f"Error al actualizar el documento: {e}")
            raise 

    def save(self, summary):
        doc_ref = self.db.collection("summary").document(f"{summary.get_month_and_year()}")
        new_summary = summary.to_summary_dict()
        doc_ref.set(new_summary)
        return summary



    # devuelve el objeto como un JSON evitando crear una instancia de Summary
    def get_json(self, month_and_year):
        doc_ref = self.db.collection("summary").document(f"{month_and_year}")
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return {"message": "Ocurrio un error al recuperar la info"}
    
    # devuelven o updatean casos en especifico
    
    def get(self, month_and_year, field):
        doc_ref = self.db.collection("summary").document(f"{month_and_year}")
        doc = doc_ref.get()    
        if doc.exists:
            data = doc.to_dict()
            return data.get(field, f"No existe el campo: {field}")
        return None 
    
    def update(self, month_and_year, field, value):
        doc_ref = self.db.collection("summary").document(f"{month_and_year}")
        doc_ref.update({field: value})
    


   