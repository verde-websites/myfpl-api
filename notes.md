Manager Endpoints
- Separate manager logic into services - Metadata, Transfers, Live Player Data
- Use curl_cffi on the manager endpoint requests 
- Add response model to manager endpoint
- Add error catches and logging to manager controller 
- total_points * is_captain = total_points
- add gameweek_id as URI to manager endpoint and also refactor services to acknowledge dependency on gameweek

Fixtures: 
- handle fixtures that get postponed (potentially at rescheduled column in fixtures table)

DB Stuff:
- Convert player_type to int not a string containing integer