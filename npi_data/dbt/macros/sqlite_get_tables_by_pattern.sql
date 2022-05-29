

{% macro sqlite_get_tables_by_pattern(p_schema, p_table_pattern) %}

    {% set v_database = target.database %}

    {% set sqlite_sql %}
        select name as table_name
        from sqlite_master
        where type = 'table'
        and name like '{{ p_table_pattern }}'
    {% endset %}

    {% if execute %}
        {% set results = run_query(sqlite_sql) %}
        {% set tbl_relations = [] %}

        {% if results %}
            {% for row in results %}

                {% set tbl_relation = api.Relation.create(
                    database=v_database,
                    schema=p_schema,
                    identifier=row.table_name,
                    type='table'
                ) %}
                {% do tbl_relations.append(tbl_relation) %}
            {% endfor %}
        {% endif %}
        {{ return(tbl_relations) }}
    {% endif %}

{% endmacro %}
