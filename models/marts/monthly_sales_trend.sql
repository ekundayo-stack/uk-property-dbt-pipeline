with sales as (

    select * from {{ ref('stg_price_paid') }}

),

by_month as (

    select
        date_trunc('month', transfer_date) as sales_month,
        count(*)                           as number_of_sales,
        round(avg(price))                  as average_price
    from sales
    group by date_trunc('month', transfer_date)

)

select * from by_month
order by sales_month