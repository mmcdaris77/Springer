
/*
    OHDSI V5.0 (https://athena.ohdsi.org/search-terms/start)
    postgresql v16
    assumes that the CSV files are in dir: C:\_data\omop_vocabulary
*/

drop table if exists omop.concept_relationship;
drop table if exists omop.concept;

create table omop.concept (
    concept_id int primary key
    ,concept_name text
    ,domain_id text
    ,vocabulary_id text
    ,concept_class_id text
    ,standard_concept text
    ,concept_code text
    ,valid_start_date date
    ,valid_end_date date
    ,invalid_reason text
    ,rn serial
);

COPY omop.concept(    
	 concept_id 
    ,concept_name
    ,domain_id
    ,vocabulary_id
    ,concept_class_id
    ,standard_concept
    ,concept_code
    ,valid_start_date
    ,valid_end_date
    ,invalid_reason)
FROM 'C:\_data\omop_vocabulary\CONCEPT.csv'
DELIMITER E'\t'
QUOTE '~'
ENCODING 'UTF8'
CSV HEADER;


create table if not exists omop.concept_relationship (
    concept_id_1 int 
    ,concept_id_2 int 
    ,relationship_id text
    ,valid_start_date date
    ,valid_end_date date
    ,invalid_reason text
    ,rn serial
    --,primary key(concept_id_1,concept_id_2,relationship_id)
);

COPY omop.concept_relationship(    
    concept_id_1
    ,concept_id_2
    ,relationship_id
    ,valid_start_date
    ,valid_end_date
    ,invalid_reason)
FROM 'C:\_data\omop_vocabulary\CONCEPT_RELATIONSHIP.csv'
DELIMITER E'\t'
QUOTE '~'
ENCODING 'UTF8'
CSV HEADER;


-- remove relationship recs that do not have a concept 
delete from omop.concept_relationship a 
where not exists (
	select 1 
	from omop.concept b 
	where b.concept_id = a.concept_id_1 
)
;

delete from omop.concept_relationship a 
where not exists (
	select 1 
	from omop.concept b 
	where b.concept_id = a.concept_id_2 
)
;

-- add keys
alter table omop.concept_relationship
add constraint omop_con_rel_PK primary key(concept_id_1,concept_id_2,relationship_id);

alter table omop.concept_relationship
add constraint omop_con1_rel_FK_con foreign key(concept_id_1) references omop.concept(concept_id);
alter table omop.concept_relationship
add constraint omop_con2_rel_FK_con foreign key(concept_id_2) references omop.concept(concept_id);

create index if not exists idx_dom_con_cls on omop.concept(vocabulary_id, concept_class_id)
;
create index if not exists idx_dom on omop.concept(domain_id)
;