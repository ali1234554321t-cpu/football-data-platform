select
    date_key,
    full_date,
    day_number,
    month_number,
    month_name,
    quarter_number,
    year_number,
    day_name,
    week_number,
    is_weekend
from {{ source('football_warehouse', 'dim_date') }}