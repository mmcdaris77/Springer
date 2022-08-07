{{
    config(
        alias='populations_by_zip_code'
    )
}}
{% set v_schema = this.schema %}

{% set list_of_relations = dbt_utils.get_relations_by_pattern(v_schema, 'stg__Census_Populations_by_Zip_Code%') %}


{{
    dbt_utils.union_relations(list_of_relations)
}}


