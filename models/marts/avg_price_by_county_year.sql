with sales as (

    select * from {{ ref('fct_sales') }}

),

by_county_year as (

    select
        county,
        year(transfer_date)       as sale_year,
        count(*)                  as number_of_sales,
        round(avg(price))         as average_price,
        round(median(price))      as median_price
    from sales
    group by county, year(transfer_date)

)

select * from by_county_year
order by county, sale_year