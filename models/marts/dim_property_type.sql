with property_types as (

    select distinct property_type as property_type_code
    from {{ ref('stg_price_paid') }}

),

labelled as (

    select
        property_type_code,
        case property_type_code
            when 'D' then 'Detached'
            when 'S' then 'Semi-Detached'
            when 'T' then 'Terraced'
            when 'F' then 'Flat / Maisonette'
            when 'O' then 'Other'
            else 'Unknown'
        end as property_type_name
    from property_types

)

select * from labelled