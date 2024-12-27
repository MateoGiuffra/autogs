import logging
from application.configuration.firebase_config import db

class SummaryDAO:

    def __init__(self):
        self.initialize_logging()
        self.db = db
    

    def initialize_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='webdriver_errors.log',
            filemode='a'
        )

    def update(self, current_month, field, value):
        doc_ref = self.db.collection("summary").document(f"{current_month}")
        doc_ref.update({field: value})

    def create_new_summary(self, current_month):
        doc_ref = self.db.collection("summary").document(f"{current_month}")
        empty_summary = {"total": 0,
                         "last_total": 0,
                         "last_months_total":0,
                         "last_months_total_today ":0}
        doc_ref.set(empty_summary)

    def get(self, current_month, field):
        doc_ref = self.db.collection("summary").document(f"{current_month}")
        doc = doc_ref.get()    
        if doc.exists:
            data = doc.to_dict()
            return data.get(field, f"No existe el campo: {field}")
        return None 
    
# def main():
#     dao = SummaryDAO()
#     dao.create_new_summary(12)
#     dao.update(12,"total",1100000)
#     total = dao.get(12,"total")
#     noexiste = dao.get(12,"totala")
#     tiene0 = dao.get(12,"last_total")
#     print(total)
#     print(noexiste)
#     print(tiene0)

# main()     


   