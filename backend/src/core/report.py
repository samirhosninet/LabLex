from jinja2 import Template
from datetime import datetime
from sqlalchemy.orm import Session
from src.models.evaluation import ToolRun
from src.core.errors import LabLexException

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LabLex Evaluation Report - {{ run_id }}</title>
    <style>
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            margin: 0;
            padding: 40px;
        }
        .container {
            max-width: 1100px;
            margin: 0 auto;
        }
        .header {
            border-bottom: 1px solid #21262d;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .header-left h1 {
            color: #58a6ff;
            margin: 0 0 10px 0;
            font-size: 2.2rem;
        }
        .meta {
            color: #8b949e;
            font-size: 0.9rem;
        }
        .logo {
            font-size: 1.5rem;
            font-weight: 800;
            color: #f0f6fc;
            background: linear-gradient(135deg, #7928ca, #ff0080);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 1px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-2px);
        }
        .card .value {
            font-size: 2rem;
            font-weight: 700;
            color: #f0f6fc;
            margin-bottom: 5px;
        }
        .card .label {
            color: #8b949e;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1.2px;
        }
        h2 {
            color: #f0f6fc;
            border-left: 4px solid #7928ca;
            padding-left: 10px;
            margin-bottom: 20px;
            font-size: 1.4rem;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 40px;
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        th, td {
            text-align: left;
            padding: 14px 16px;
            border-bottom: 1px solid #21262d;
        }
        th {
            background-color: #0d1117;
            color: #8b949e;
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        tr:hover {
            background-color: rgba(56, 139, 253, 0.05);
        }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .badge-success {
            background-color: rgba(56, 139, 253, 0.15);
            color: #58a6ff;
            border: 1px solid rgba(56, 139, 253, 0.3);
        }
        .badge-danger {
            background-color: rgba(248, 81, 73, 0.15);
            color: #ff7b72;
            border: 1px solid rgba(248, 81, 73, 0.3);
        }
        .json-preview {
            background-color: #090c10;
            border: 1px solid #21262d;
            border-radius: 6px;
            padding: 10px;
            font-family: monospace;
            font-size: 0.8rem;
            color: #8b949e;
            max-width: 300px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-left">
                <h1>Evaluation Run Report</h1>
                <div class="meta">
                    Run ID: {{ run_id }} | Generated: {{ generated_at }}
                </div>
            </div>
            <div class="logo">LABLEX AI</div>
        </div>

        <h2>Summary Dashboard</h2>
        <div class="stats-grid">
            <div class="card">
                <div class="value">{{ summary.total_samples }}</div>
                <div class="label">Total Cases</div>
            </div>
            <div class="card">
                <div class="value" style="color: #3fb950;">{{ summary.completed_count }}</div>
                <div class="label">Passed</div>
            </div>
            <div class="card">
                <div class="value" style="color: #f85149;">{{ summary.failed_count }}</div>
                <div class="label">Failed</div>
            </div>
            <div class="card">
                <div class="value" style="color: #58a6ff;">{{ summary.average_latency_ms }} ms</div>
                <div class="label">Avg Latency</div>
            </div>
        </div>

        <h2>Granular Metrics Table</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 15%">Sample ID</th>
                    <th style="width: 30%">Prompt Input</th>
                    <th style="width: 25%">Model Output / Error</th>
                    <th style="width: 10%">Latency</th>
                    <th style="width: 10%">Metrics</th>
                    <th style="width: 10%">Status</th>
                </tr>
            </thead>
            <tbody>
                {% for sample in samples %}
                <tr>
                    <td><strong>{{ sample.sample_id }}</strong></td>
                    <td><div class="json-preview" title="{{ sample.input_text }}">{{ sample.input_text }}</div></td>
                    <td>
                        {% if sample.status == 'completed' %}
                        <div class="json-preview" title="{{ sample.output_text }}">{{ sample.output_text }}</div>
                        {% else %}
                        <span style="color: #ff7b72; font-size: 0.85rem;">{{ sample.error_message }}</span>
                        {% endif %}
                    </td>
                    <td>{{ sample.latency_ms or 0 }} ms</td>
                    <td>
                        {% for k, v in sample.metrics.items() %}
                        <span style="font-size: 0.8rem; color: #8b949e;">{{ k }}:</span> <strong>{{ v }}</strong><br>
                        {% endfor %}
                    </td>
                    <td>
                        {% if sample.status == 'completed' %}
                        <span class="badge badge-success">PASSED</span>
                        {% else %}
                        <span class="badge badge-danger">FAILED</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

def generate_run_report(run_id: str, db: Session) -> str:
    """
    Generates Jinja2 HTML report content for a completed ToolRun.
    """
    run = db.query(ToolRun).filter(ToolRun.id == run_id).first()
    if not run:
        raise LabLexException(
            code="NOT_FOUND",
            message="ToolRun not found.",
            status_code=404
        )
        
    if run.status not in ("completed", "failed", "normalization_failed"):
        raise LabLexException(
            code="INVALID_STATE",
            message="Reports can only be generated for runs that are in a terminal state.",
            status_code=400
        )
        
    norm_res = run.normalized_results[0] if run.normalized_results else None
    if not norm_res:
        raise LabLexException(
            code="REPORT_ERROR",
            message="No normalized results found for this run, report cannot be built.",
            status_code=400
        )
        
    samples_data = [
        {
            "sample_id": s.sample_id,
            "input_text": s.input_text or "N/A",
            "expected_output": s.expected_output or "N/A",
            "output_text": s.output_text,
            "error_message": s.error_message,
            "latency_ms": s.latency_ms,
            "metrics": s.metrics,
            "status": s.status
        } for s in norm_res.samples
    ]
    
    template = Template(HTML_TEMPLATE)
    html_output = template.render(
        run_id=run.id,
        generated_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        summary=norm_res.metrics_summary,
        samples=samples_data
    )
    
    return html_output


COMPARISON_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LabLex AI Comparison Report</title>
    <style>
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            margin: 0;
            padding: 40px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            border-bottom: 1px solid #21262d;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .header-left h1 {
            color: #58a6ff;
            margin: 0 0 10px 0;
            font-size: 2.2rem;
        }
        .meta {
            color: #8b949e;
            font-size: 0.9rem;
        }
        .logo {
            font-size: 1.5rem;
            font-weight: 800;
            color: #f0f6fc;
            background: linear-gradient(135deg, #7928ca, #ff0080);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 1px;
        }
        .summary-box {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .card .value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #f0f6fc;
            margin-bottom: 5px;
        }
        .card .label {
            color: #8b949e;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1.2px;
        }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-a {
            background-color: rgba(121, 40, 202, 0.2);
            color: #d3adf7;
            border: 1px solid rgba(121, 40, 202, 0.4);
        }
        .badge-b {
            background-color: rgba(255, 0, 128, 0.2);
            color: #ff85c0;
            border: 1px solid rgba(255, 0, 128, 0.4);
        }
        .badge-draw {
            background-color: rgba(139, 148, 158, 0.2);
            color: #c9d1d9;
            border: 1px solid rgba(139, 148, 158, 0.4);
        }
        .text-win {
            color: #3fb950;
            font-weight: 600;
        }
        .text-lose {
            color: #f85149;
            font-weight: 600;
        }
        h2 {
            color: #f0f6fc;
            border-left: 4px solid #7928ca;
            padding-left: 10px;
            margin-bottom: 20px;
            font-size: 1.4rem;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 40px;
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            overflow: hidden;
        }
        th, td {
            text-align: left;
            padding: 14px 16px;
            border-bottom: 1px solid #21262d;
        }
        th {
            background-color: #0d1117;
            color: #8b949e;
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
        }
        .json-preview {
            background-color: #090c10;
            border: 1px solid #21262d;
            border-radius: 6px;
            padding: 10px;
            font-family: monospace;
            font-size: 0.8rem;
            color: #8b949e;
            max-width: 260px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-left">
                <h1>AI Evaluation Comparison Report</h1>
                <div class="meta">
                    Baseline Run: {{ comp.run_a.id }} | Target Run: {{ comp.run_b.id }}
                </div>
            </div>
            <div class="logo">LABLEX AI</div>
        </div>

        <h2>Summary Comparisons</h2>
        <div class="summary-box">
            <div class="card">
                <div class="value">
                    {% if comp.overall_winner == 'run_a' %}
                    Baseline (Run A)
                    {% elif comp.overall_winner == 'run_b' %}
                    Target (Run B)
                    {% else %}
                    DRAW
                    {% endif %}
                </div>
                <div class="label">Overall Winner</div>
            </div>
            {% for skey, sdata in comp.summary.items() %}
            <div class="card">
                <div class="value">
                    {{ sdata.val_a }} vs {{ sdata.val_b }}
                    <span style="font-size: 0.9rem; font-weight: 400; display: block; margin-top: 5px;">
                        Delta: {{ sdata.delta }} ({{ sdata.winner }} wins)
                    </span>
                </div>
                <div class="label">{{ skey }}</div>
            </div>
            {% endfor %}
        </div>

        <h2>Sample Level Comparisons</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 10%">Sample ID</th>
                    <th style="width: 35%">Baseline Output (Run A)</th>
                    <th style="width: 35%">Target Output (Run B)</th>
                    <th style="width: 20%">Metrics Delta & Winner</th>
                </tr>
            </thead>
            <tbody>
                {% for sample in comp.samples %}
                <tr>
                    <td><strong>{{ sample.sample_id }}</strong></td>
                    <td>
                        <div class="json-preview" title="{{ sample.run_a.output_text or '' }}">{{ sample.run_a.output_text or 'N/A' }}</div>
                        <span style="font-size: 0.75rem; color: #8b949e;">Latency: {{ sample.run_a.latency_ms or 0 }} ms</span>
                    </td>
                    <td>
                        <div class="json-preview" title="{{ sample.run_b.output_text or '' }}">{{ sample.run_b.output_text or 'N/A' }}</div>
                        <span style="font-size: 0.75rem; color: #8b949e;">Latency: {{ sample.run_b.latency_ms or 0 }} ms</span>
                    </td>
                    <td>
                        {% for mkey, mdata in sample.metrics_comparison.items() %}
                        <span style="font-size: 0.8rem; color: #8b949e;">{{ mkey }}:</span> 
                        <strong>{{ mdata.val_a }} ➔ {{ mdata.val_b }}</strong>
                        <span style="font-size: 0.8rem; display: block;">
                            Delta: <span class="{% if mdata.winner == 'run_b' %}text-win{% elif mdata.winner == 'run_a' %}text-lose{% endif %}">
                                {{ mdata.delta if mdata.delta is not none else 'N/A' }}
                            </span>
                            <span class="badge {% if mdata.winner == 'run_a' %}badge-a{% elif mdata.winner == 'run_b' %}badge-b{% else %}badge-draw{% endif %}" style="font-size: 0.65rem; padding: 1px 4px;">
                                {{ mdata.winner }}
                            </span>
                        </span>
                        {% endfor %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

def generate_comparison_report(comparison_id: str, db: Session) -> str:
    """
    Generates Jinja2 HTML report content for side-by-side run comparisons.
    """
    from src.models.evaluation import Comparison
    from src.core.comparison_engine import calculate_comparison

    comp_rec = db.query(Comparison).filter(Comparison.id == comparison_id).first()
    if not comp_rec:
        raise LabLexException(
            code="NOT_FOUND",
            message="Comparison not found.",
            status_code=404
        )

    # Resolve runs
    run_ids = [item.run_id for item in comp_rec.items]
    if len(run_ids) != 2:
        raise LabLexException(
            code="REPORT_ERROR",
            message="Comparison must contain exactly two runs to build a report.",
            status_code=400
        )

    compared_data = calculate_comparison(run_ids[0], run_ids[1], db)

    template = Template(COMPARISON_HTML_TEMPLATE)
    html_output = template.render(
        comp=compared_data
    )
    return html_output


def generate_run_csv(run_id: str, db: Session) -> str:
    """
    Generates CSV string export of normalized results for a completed ToolRun.
    """
    import csv
    import io
    
    run = db.query(ToolRun).filter(ToolRun.id == run_id).first()
    if not run or not run.normalized_results:
        return ""

    norm_res = run.normalized_results[0]
    output = io.StringIO()
    writer = csv.writer(output)

    # Collect all unique metric keys
    metric_keys = set()
    for sample in norm_res.samples:
        metric_keys.update(sample.metrics.keys())
    metric_keys = sorted(list(metric_keys))

    # Header
    header = ["Sample ID", "Input Text", "Expected Output", "Output Text", "Status", "Latency MS"] + metric_keys
    writer.writerow(header)

    # Rows
    for sample in norm_res.samples:
        row = [
            sample.sample_id,
            sample.input_text or "",
            sample.expected_output or "",
            sample.output_text or "",
            sample.status,
            sample.latency_ms or 0
        ]
        for mkey in metric_keys:
            row.append(sample.metrics.get(mkey, ""))
        writer.writerow(row)

    return output.getvalue()


def generate_comparison_csv(comparison_id: str, db: Session) -> str:
    """
    Generates CSV string export of side-by-side run comparisons.
    """
    import csv
    import io
    from src.models.evaluation import Comparison
    from src.core.comparison_engine import calculate_comparison

    comp_rec = db.query(Comparison).filter(Comparison.id == comparison_id).first()
    if not comp_rec:
        return ""

    run_ids = [item.run_id for item in comp_rec.items]
    if len(run_ids) != 2:
        return ""

    comp_data = calculate_comparison(run_ids[0], run_ids[1], db)
    
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(["Comparison Summary", f"Baseline (Run A): {run_ids[0]}", f"Target (Run B): {run_ids[1]}", "Winner"])
    for skey, sval in comp_data.get("summary", {}).items():
        writer.writerow([skey, sval["val_a"], sval["val_b"], sval["winner"]])

    writer.writerow([])
    writer.writerow(["Sample Comparison"])

    # Columns
    writer.writerow([
        "Sample ID",
        "Run A Output", "Run A Latency",
        "Run B Output", "Run B Latency",
        "Metric Name", "Run A Metric", "Run B Metric", "Metric Delta", "Metric Winner"
    ])

    for sample in comp_data.get("samples", []):
        for idx, (mkey, mdata) in enumerate(sample["metrics_comparison"].items()):
            row = []
            if idx == 0:
                row = [
                    sample["sample_id"],
                    sample["run_a"]["output_text"] or "",
                    sample["run_a"]["latency_ms"] or "",
                    sample["run_b"]["output_text"] or "",
                    sample["run_b"]["latency_ms"] or ""
                ]
            else:
                row = ["", "", "", "", ""]

            row += [
                mkey,
                mdata["val_a"],
                mdata["val_b"],
                mdata["delta"] if mdata["delta"] is not None else "",
                mdata["winner"]
            ]
            writer.writerow(row)

    return output.getvalue()
