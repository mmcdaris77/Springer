{{
    config(
        alias='npi_endpoint_pfile'
    )
}}

{% set v_schema = this.schema %}

{% set list_of_relations = dbt_utils.get_relations_by_pattern(v_schema, 'stg_endpoint_pfile%') %}


{{
    dbt_utils.union_relations(list_of_relations)
}}
