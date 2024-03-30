/*
    PostgreSQL: 
    get some drugs/routes/units from omop vocab to use as patterns
*/
-- drug names 
select distinct 'drug' as src, lower(a.concept_name) as pat_text
from omop.concept a
where lower(a.vocabulary_id) = 'rxnorm'
	and lower(a.concept_class_id) = 'ingredient'
	and nullif(trim(a.invalid_reason), '') is null

union all
	
-- routes 
select 'route' as src, route
from (
	select distinct trim(replace(lower(a.concept_name), ' route', '')) as pat_text
	from omop.concept a
	where lower(a.domain_id) = 'route'
		and nullif(trim(a.invalid_reason), '') is null
		and not a.concept_name ilike 'route of admin%'
	
	union all
	
	select trim(g) as route
	from string_to_table('iv', ',') g
) x

union all 

-- unit 
select distinct 'unit' as src, trim(lower(a.concept_name)) as pat_text
from omop.concept a
where lower(a.domain_id) = 'unit'
	and nullif(trim(a.invalid_reason), '') is null
; 


-- FRQ qualifier 
select distinct 'frq', trim(lower(a.concept_name)) as pat_text
from omop.concept a
where lower(a.domain_id) = 'meas value'
    and lower(a.concept_class_id) = 'qualifier value'
    and nullif(trim(a.invalid_reason), '') is null
    and a.concept_name ilike any(array['%week%','%day%','%month%','%year%','%hour%'])
 
;
