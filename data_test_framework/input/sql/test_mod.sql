-- make a cte to see what sqlglot will do ;)
with cte_zero as (
    select 0 as zero
) 
select 
    a.col_a
    ,b.col_b 
    -- test col[s] for expected values
    ,case when a.col_a % 2 = 0 then 1 else 0 end as case_col
from dbx.schemax.tbl_x  a 
join tbl_z b -- we don't want test data for this table. we'll call it static metadata used for a filter or something
    on a.id = b.id