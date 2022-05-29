{% macro sqlite_drop_tables_by_pattern(v_pattern, v_log_only=true) %}

    {% set q_tables %}  
        select 'drop table if exists ' || name || ';'
        from sqlite_master 
        where type = 'table' 
        and name like '{{ v_pattern }}'
        order by name;
    {% endset %}


    {% if execute %}

        {{ log(q_tables, info=true) }}

        {%set results = run_query(q_tables) %}

        {% if results %}
            {% for str_drop in results.columns[0] %}
                {% if not v_log_only %}
                    {% do run_query(str_drop) %}
                {% endif %}
                {{ log(str_drop, info=true) }}
            {% endfor %}
        {% endif %}
        
    {% endif %}

{% endmacro %}