{{
    config(
        alias='npi_pl_pfile'
    )
}}
{% set v_schema = this.schema %}

{% set list_of_relations = dbt_utils.get_relations_by_pattern(v_schema, 'stg_pl_pfile%') %}


{{
    dbt_utils.union_relations(list_of_relations)
}}
