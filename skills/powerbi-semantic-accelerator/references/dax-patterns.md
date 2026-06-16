# DAX Pattern Reference

Use explicit measures only. Do not expose implicit aggregations.

## Generator-Supported Patterns

### sum

```DAX
Revenue =
SUM ( Fact_MetricSnapshot[Revenue Amount] )
```

Required: `pattern`, `table`, `column`.

### distinct_count

```DAX
Entity Count =
DISTINCTCOUNT ( Fact_MetricSnapshot[Entity Id] )
```

### count_rows

```DAX
Snapshot Row Count =
COUNTROWS ( Fact_MetricSnapshot )
```

Use only with documented table grain.

### weighted_average

```DAX
PowerScore =
DIVIDE (
    SUMX (
        Fact_MetricSnapshot,
        Fact_MetricSnapshot[Score Value] * Fact_MetricSnapshot[Entity Weight]
    ),
    SUM ( Fact_MetricSnapshot[Entity Weight] )
)
```

### delta

```DAX
Score vs Target =
[PowerScore] - [Target Score]
```

### ratio

```DAX
Score vs Target % =
DIVIDE ( [Score vs Target], [Target Score] )
```

## Metric Semantics

Classify each public self-service metric:

```text
additive          -> sum across dimension/time, e.g. Revenue
semi_additive     -> aggregate across some axes, not all time, e.g. Balance
non_additive      -> cannot sum, e.g. Unit Price
ratio             -> numerator/denominator, e.g. Margin Rate
weighted_average  -> recompute using value and weight
distinct_count    -> context-dependent count
```

Declare `time_behavior`: `flow`, `snapshot`, `period_end`, `balance`, `average_over_period`, or `point_in_time`.

## Selectors

Prefer Field Parameters for visual measure/dimension switching. Use disconnected selector + `SWITCH` only for custom semantic logic.

### selected_metric

```DAX
Selected Metric Value =
VAR MetricKey = SELECTEDVALUE ( 'Metric Selector'[Metric Key], "default" )
RETURN
    SWITCH (
        MetricKey,
        "revenue", [Revenue],
        "orders", [Order Count],
        "score", [PowerScore],
        [PowerScore]
    )
```

Rules: selector keys map only to explicit governed measures; keep base measures reusable.

### selected_metric_label

```DAX
Selected Metric Label =
SELECTEDVALUE ( 'Metric Selector'[Display Name], "PowerScore" )
```

### top_n_rank

```DAX
Entity Rank =
RANKX (
    ALLSELECTED ( Dim_Entity[Entity Name] ),
    [Selected Metric Value],
    ,
    DESC,
    Dense
)
```

### top_n_flag

```DAX
Show Top N Entity =
VAR N = SELECTEDVALUE ( 'Top N Selector'[N], 10 )
RETURN IF ( [Entity Rank] <= N, 1, 0 )
```

### score_band

```DAX
Score Band =
VAR ScoreValue = [PowerScore]
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( ScoreValue ), BLANK (),
        ScoreValue < 60, "Critical",
        ScoreValue < 80, "Warning",
        "Good"
    )
```

Use DAX bands only for simple semantic thresholds. Materialize complex band logic upstream.

### component_contribution_pct

```DAX
Component Contribution % =
DIVIDE (
    [Component Contribution],
    CALCULATE ( [Component Contribution], ALLSELECTED ( Dim_Component ) )
)
```

### dynamic_title

```DAX
Metric Explorer Title =
"Metric Explorer - " & [Selected Metric Label]
```

## Calculation Groups

For v0.1, create only one Time View group: `Current`, `Previous Period`, `YTD`, `Rolling 3M`, `Rolling 12M`. Add more groups only after explicit measures, date role, and metric semantics are stable.
