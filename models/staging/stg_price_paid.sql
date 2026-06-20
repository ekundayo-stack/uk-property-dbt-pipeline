with source as (

    select * from {{ source('land_registry', 'price_paid') }}

),

renamed as (

    select
        column00               as transaction_id,
        column01               as price,
        cast(column02 as date) as transfer_date,
        column03               as postcode,
        column04               as property_type,
        column05               as old_or_new,
        column06               as tenure_duration,
        column07               as paon,
        column08               as saon,
        column09               as street,
        column10               as locality,
        column11               as town_city,
        column12               as district,
        column13               as county,
        column14               as ppd_category_type,
        column15               as record_status
    from source

)

select * from renamed