with county_year as (

    select * from {{ ref('avg_price_by_county_year') }}

),

regions as (

    select * from {{ ref('county_region') }}

),

joined as (

    select
        regions.region,
        county_year.sale_year,
        county_year.number_of_sales,
        county_year.average_price
    from county_year
    inner join regions
        on county_year.county = regions.county

),

by_region_year as (

    select
        region,
        sale_year,
        sum(number_of_sales)                                          as total_sales,
        round(sum(average_price * number_of_sales) / sum(number_of_sales)) as avg_price
    from joined
    group by region, sale_year

)

select * from by_region_year
order by region, sale_year