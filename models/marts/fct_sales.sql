with sales as (

    select * from {{ ref('stg_price_paid') }}

),

property_types as (

    select * from {{ ref('dim_property_type') }}

),

final as (

    select
        sales.transaction_id,
        cast(sales.transfer_date as date) as transfer_date,
        sales.property_type               as property_type_code,
        property_types.property_type_name,
        sales.price,
        sales.postcode,
        sales.town_city,
        sales.district,
        sales.county
    from sales
    left join property_types
        on sales.property_type = property_types.property_type_code

)

select * from final