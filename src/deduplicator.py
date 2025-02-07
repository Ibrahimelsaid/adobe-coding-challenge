import json
from datetime import datetime

class JSONDeduplicator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = self.load_data()
        self.latest_records = {} 
        self.email_map = {}  
        self.change_history = {}  
        self.output_file_name = 'data/modified_leads.json'
        self.log_file_name = 'data/logs.json'
        self.seen_emails = set() 

    def load_data(self):
        """Load data from input JSON file."""
        with open(self.input_file, "r") as file:
            return json.load(file).get("leads", [])

    def has_field_changes(self, new_record, old_record):
        """Check if there are actual field changes between records."""
        if not old_record:
            return []
            
        changes = []
        for key in new_record:
            if new_record[key] != old_record.get(key):
                changes.append({
                    "field": key,
                    "from": old_record.get(key),
                    "to": new_record[key]
                })
        return changes

    def should_update_record(self, new_record, existing_record):
        """Determine if the new record should replace the existing record."""
        if not existing_record:
            return True
            
        new_date = datetime.fromisoformat(new_record["entryDate"])
        existing_date = datetime.fromisoformat(existing_record["entryDate"])
        
        return new_date >= existing_date

    def deduplicate(self):
        """Deduplicate records based on ID and email."""
        for record in self.data:
            record_id = record["_id"]
            record_email = record["email"]
            
            existing_by_id = self.latest_records.get(record_id)
            existing_by_email = self.email_map.get(record_email)
            
            is_new_record = record_email not in self.seen_emails
            
            if is_new_record:
                self.change_history[record_id] = {
                    "initial_record": None,
                    "final_record": record,
                    "field_changes": []  
                }
                self.seen_emails.add(record_email)
            else:
                existing_record = None
                if existing_by_id and existing_by_email:
                    id_date = datetime.fromisoformat(existing_by_id["entryDate"])
                    email_date = datetime.fromisoformat(existing_by_email["entryDate"])
                    existing_record = existing_by_id if id_date >= email_date else existing_by_email
                else:
                    existing_record = existing_by_id or existing_by_email

                if existing_record and self.should_update_record(record, existing_record):
                    changes = self.has_field_changes(record, existing_record)
                    if changes:
                        self.change_history[record_id] = {
                            "initial_record": existing_record,
                            "final_record": record,
                            "field_changes": changes
                        }

            if not existing_by_id and not existing_by_email:
                self.latest_records[record_id] = record
                self.email_map[record_email] = record
            elif self.should_update_record(record, existing_by_id or existing_by_email):
                self.latest_records[record_id] = record
                
                if existing_by_email and existing_by_email["_id"] != record_id:
                    old_id = existing_by_email["_id"]
                    if old_id in self.latest_records:
                        del self.latest_records[old_id]
                
                self.email_map[record_email] = record
                
                if existing_by_id and existing_by_id["email"] != record_email:
                    del self.email_map[existing_by_id["email"]]

    def generate_logs(self):
        """Generate logs based on change history."""
        logs = []
        
        for record_id, history in self.change_history.items():
            if history["field_changes"]:  
                log_entry = {
                    "action": "record_updated",
                    "id": record_id,
                    "email": history["final_record"]["email"],
                    "source_record": history["initial_record"],
                    "output_record": history["final_record"],
                    "field_changes": history["field_changes"]
                }
                logs.append(log_entry)
            elif history["initial_record"] is None:
                log_entry = {
                    "action": "new_record",
                    "id": record_id,
                    "email": history["final_record"]["email"],
                    "source_record": None,
                    "output_record": history["final_record"],
                    "field_changes": []  
                }
                logs.append(log_entry)

        return logs

    def save_results(self):
        """Save deduplicated records to a JSON file."""
        sorted_records = sorted(
            self.latest_records.values(),
            key=lambda r: datetime.fromisoformat(r["entryDate"])
        )
        
        with open(self.output_file_name, "w") as outfile:
            json.dump({"leads": sorted_records}, outfile, indent=4)

    def save_log(self):
        """Generate and save the log file."""
        logs = self.generate_logs()
        with open(self.log_file_name, "w") as logfile:
            json.dump(logs, logfile, indent=4)

