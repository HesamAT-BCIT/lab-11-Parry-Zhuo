import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, "user_id"):
            log_record["user_id"] = record.user_id
        if hasattr(record, "endpoint"):
            log_record["endpoint"] = record.endpoint
        if hasattr(record, "method"):
            log_record["method"] = record.method

        return json.dumps(log_record)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers = [handler]