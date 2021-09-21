with earliest_date as (
    select user_id,
           date_trunc('week', min(created)) as reg_week,
           date_trunc('day', min(created))  as reg_day
    from tab1

    group by user_id
    order by reg_date
),
     date_of_purchase as (
         select user_id,
                sum_rub,
                created,
                extract(isodow from created) - 1 as day_of_week
         from tab2
     )
select ed.reg_week                                                              as week_start,
       dp.day_of_week                                                           as day_after,
       (sum(sum_rub))/(count(distinct ed.user_id))                              as ltv
from date_of_purchase dp
         left join earliest_date ed on dp.user_id = ed.user_id
where trunc(date_part('day', dp.created::timestamp - ed.reg_week::timestamp)/7) = 0
group by week_start, day after
order by week_start;
