'''
Building schemas -- this is the layer between the database
and outside

Three Schemas:

1. ShortenRequest -- what comes IN (URL string)
2. ShortenResponse -- what goes OUT after a link is created.
3. AnalyticsReponse -- what goes OUT on GET /api/analytics/{short_code}
'''

from datetime import datetime

# BaseModel inherits: check data type, rejects bad, converts data into python object
# HttpUrl: makes sure that a field muust be real URL (http or https)
from pydantic import BaseModel, HttpUrl

from typing import Optional

class ShortenRequest(BaseModel):
    url: HttpUrl
    model_config = {"from_attributes": True}
    
class ShortenResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    # Tells pydantic its allowed to read data directly from SQLalchemy model object
    model_config = {"from_attributes": True}
    
class ClickResponse(BaseModel):
    clicked_at: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]
    model_config = {"from_attributes": True}

class AnalyticsResponse(BaseModel):
    short_code: str
    total_clicks: int
    recent_clicks: list[ClickResponse]
    model_config = {"from_attributes": True}
    
    
