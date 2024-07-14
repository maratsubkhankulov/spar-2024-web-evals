import re
from copy import deepcopy
from typing import Any, cast

from inspect_ai._util.registry import (
    registry_info,
    registry_log_name,
    registry_params,
    registry_unqualified_name,
)
from inspect_ai.log import (
    EvalMetric,
    EvalResults,
    EvalScore,
)
from inspect_ai.scorer import Metric, Score, Scorer
from inspect_ai.scorer._scorer import SCORER_METRICS, scorer_metrics


def eval_results(
    scores: list[dict[str, Score]],
    scorers: list[Scorer] | None,
    metrics: list[Metric] = [],
) -> EvalResults:
    # record scorer
    results = EvalResults()
    if scorers:
        result_scores = []
        for scorer in scorers:
            # extract non-metrics metadata
            metadata = deepcopy(registry_info(scorer).metadata)
            del metadata[SCORER_METRICS]

            # this scorer
            scorer_name = registry_log_name(scorer)

            # scores for this scorer
            resolved_scores = [
                score[scorer_name] for score in scores if scorer_name in score
            ]

            # Compute metrics for this scorer
            targets = target_metrics(scorer, metrics)
            if isinstance(targets, list):
                # If there is a simple list of metrics
                # just compute the metrics for this scorer
                result_scores.extend(
                    scorer_for_metrics(
                        scorer_name=scorer_name,
                        scorer=scorer,
                        metadata=metadata,
                        scores=resolved_scores,
                        metrics=targets,
                    )
                )
            else:
                # If there is a dictionary of metrics, apply
                # the metrics to the values within the scores
                # (corresponding by key) and emit an EvalScorer for
                # each key (which effectively creates multiple scorers
                # by expanding a dictionary score value into multiple
                # results with metrics)
                result_scores.extend(
                    scorers_from_metric_dict(
                        scorer_name=scorer_name,
                        scorer=scorer,
                        metadata=metadata,
                        scores=resolved_scores,
                        metrics=targets,
                    )
                )
        # build results
        results.scores = result_scores

    return results


def scorer_for_metrics(
    scorer_name: str,
    scorer: Scorer,
    metadata: dict[str, Any],
    scores: list[Score],
    metrics: list[Metric],
) -> list[EvalScore]:
    results: list[EvalScore] = []
    # we want to use simple names for metrics in the metrics dict
    # (i.e. without package prefixes). we do this by getting the
    # unqualified name, then appending a suffix if there are duplicates
    # this keeps the code straightforward and intuitive for users
    # programming against the log (e.g. metrics["accuracy"]) vs.
    # metrics["pkgname/accuracy"])
    list_metrics: dict[str, EvalMetric] = {}
    for metric in metrics:
        key = metrics_unique_key(
            registry_unqualified_name(metric), list(list_metrics.keys())
        )

        list_metrics[key] = EvalMetric(
            name=registry_log_name(metric),
            value=cast(float, metric(scores)),
        )

    # build results
    results.append(
        EvalScore(
            scorer=scorer_name,
            name=scorer_name,
            params=registry_params(scorer),
            metadata=metadata if len(metadata.keys()) > 0 else None,
            metrics=list_metrics,
        )
    )
    return results


def scorers_from_metric_dict(
    scorer_name: str,
    scorer: Scorer,
    metadata: dict[str, Any],
    scores: list[Score],
    metrics: dict[str, list[Metric]],
) -> list[EvalScore]:
    results: list[EvalScore] = []
    for metric_key, metric_list in metrics.items():
        # filter scores to a list of scalars with the value of the metric name
        metric_scores: list[Score] = []
        for score in scores:
            if isinstance(score.value, dict):
                if metric_key in score.value:
                    # Convert the score into a simple scalar value to apply metrics
                    metric_score = deepcopy(score)
                    metric_score.value = cast(float, score.value[metric_key])
                    metric_scores.append(metric_score)
                else:
                    raise TypeError(
                        f"key '{metric_key}' isn't present in the score value dictionary"
                    )
            else:
                raise TypeError(
                    "dictionary of metrics specific for a non-dictionary score"
                )

        result_metrics: dict[str, EvalMetric] = {}
        for target_metric in metric_list:
            # compute the metric value
            metric_name = registry_log_name(target_metric)
            result_metrics[metric_name] = EvalMetric(
                name=metric_name,
                value=cast(float, target_metric(metric_scores)),
            )

        # create a scorer result for this metric
        # TODO: What is there is separate simple scorer which has a name collision with
        # a score created by this scorer
        results.append(
            EvalScore(
                scorer=scorer_name,
                name=metric_key,
                params=registry_params(scorer),
                metadata=metadata if len(metadata.keys()) > 0 else None,
                metrics=result_metrics,
            )
        )
    return results


def metrics_unique_key(key: str, existing: list[str]) -> str:
    if key not in existing:
        return key
    else:
        key_index = 2
        pattern = re.compile(f"{re.escape(key)}(\\d+)")
        for existing_key in existing:
            match = pattern.match(existing_key)
            index = int(match.group(1)) if match else None
            if index and (index >= key_index):
                key_index = index + 1
        return f"{key}{key_index}"


# build a list of metrics (scorer built-in metrics + de-duplicated additional metrics)
def target_metrics(
    scorer: Scorer, metrics: list[Metric]
) -> list[Metric] | dict[str, list[Metric]]:
    output_metrics = scorer_metrics(scorer)

    if isinstance(output_metrics, dict):
        if isinstance(metrics, dict):
            output_metrics.update(metrics)
        return output_metrics
    else:
        output_metrics_names = [registry_log_name(metric) for metric in output_metrics]
        if isinstance(metrics, list):
            output_metrics.extend(
                [
                    metric
                    for metric in metrics
                    if registry_log_name(metric) not in output_metrics_names
                ]
            )
        return output_metrics
