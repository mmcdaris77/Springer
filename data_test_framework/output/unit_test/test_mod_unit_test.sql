WITH dtf__cte__1706098338224 AS (
  SELECT
    100 AS id,
    'grr' AS value
  UNION ALL
  SELECT
    103 AS id,
    'fur' AS value
), dtf__cte__1706098336816 AS (
  SELECT
    1 AS id,
    1 AS col_a,
    2 AS col_b,
    NULL AS col_c,
    NULL AS bol
  UNION ALL
  SELECT
    2 AS id,
    3 AS col_a,
    4.55 AS col_b,
    'a' AS col_c,
    TRUE AS bol
  UNION ALL
  SELECT
    3 AS id,
    1 AS col_a,
    2 AS col_b,
    NULL AS col_c,
    FALSE AS bol
), cte_zero AS (
  SELECT
    0 AS zero
), dtf__cte__expected_values_1706098807232 AS (
  SELECT
    1 AS col_a,
    0 AS case_col
  UNION ALL
  SELECT
    2 AS col_a,
    1 AS case_col
), dtf__cte___final_1706082660112 AS (
  SELECT
    a.col_a,
    b.col_b /* test col[s] for expected values */,
    CASE WHEN a.col_a % 2 = 0 THEN 1 ELSE 0 END AS case_col
  FROM dtf__cte__1706098336816 AS a
  JOIN tbl_z AS b /* we don't want test data for this table. we'll call it static metadata used for a filter or something */
    ON a.id = b.id
)
SELECT
  *
FROM dtf__cte___final_1706082660112
LEFT JOIN dtf__cte__expected_values_1706098807232
  ON dtf__cte___final_1706082660112.col_a = dtf__cte__expected_values_1706098807232.col_a
  AND dtf__cte___final_1706082660112.case_col = dtf__cte__expected_values_1706098807232.case_col
WHERE
  dtf__cte__expected_values_1706098807232.col_a IS NULL
  OR dtf__cte__expected_values_1706098807232.case_col IS NULL