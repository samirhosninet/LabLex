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
