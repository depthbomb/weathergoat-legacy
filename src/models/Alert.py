from typing import Literal, Optional
from pydantic import Field, BaseModel


class Alert(BaseModel):
    id: str
    area_description: str = Field(alias="areaDesc")
    sent: str
    effective: str
    expires: str
    status: Literal["Actual", "Exercise", "System", "Test", "Draft"]
    message_type: Literal["Alert", "Update", "Cancel", "Ack", "Error"] = Field(alias="messageType")
    severity: Literal["Extreme", "Severe", "Moderate", "Minor", "Unknown"]
    certainty: Literal["Observed", "Likely", "Possible", "Unlikely", "Unknown"]
    urgency: Literal["Immediate", "Expected", "Future", "Past", "Unknown"]
    event: str
    sender_name: str = Field(alias="senderName")
    headline: str
    description: str
    instruction: Optional[str]
    response: Literal["Shelter", "Evacuate", "Prepare", "Execute", "Avoid", "Monitor", "Assess", "AllClear", "None"]
