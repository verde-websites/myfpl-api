Manager Endpoints
- Use curl_cffi on the manager endpoint requests and create pydantic models for the FPL response

Fixtures: 
- handle fixtures that get postponed (potentially at rescheduled column in fixtures table)

DB Stuff:
- Convert player_type to int not a string containing integer

General:
- Add versioning to endpoints
- Add more data validation to FPL schemas for FPL API endpoints