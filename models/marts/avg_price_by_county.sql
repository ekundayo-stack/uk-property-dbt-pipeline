with sales as (

    select * from {{ ref('stg_price_paid') }}

),

by_county as (

    select
        county,
        count(*)                  as number_of_sales,
        round(avg(price))         as average_price,
        round(median(price))      as median_price
    from sales
    group by county

)

select * from by_county
order by number_of_sales desc