import uuid
import logging

def generate_guid() -> str:
    """Generates a random UUID (version 4) and returns it as a string."""
    log = logging.getLogger(__name__)
    try:
        guid = uuid.uuid4() #Creates a random uuid.
        log.debug(f"Generated guid: {guid}")
        return str(guid)
    except Exception as e:
        log.error(f"An error occurred when generating a guid. Error: {e}")
        return ""