import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../components/Layout';
import { fetchWithAuth } from '../../services/api';

interface MetricDelta {
  val_a: number;
  val_b: number;
  delta: number | null;
  winner: string;
}

interface SampleComparison {
  sample_id: string;
  run_a: {
    status: string;
    output_text: string | null;
    latency_ms: number | null;
    metrics: Record<string, any>;
  };
  run_b: {
    status: string;
    output_text: string | null;
    latency_ms: number | null;
    metrics: Record<string, any>;
  };
  metrics_comparison: Record<string, MetricDelta>;
}

interface ComparisonDetails {
  id: string;
  name: string;
  created_at: string;
  comparison_data: {
    run_a: {
      id: string;
      created_at: string;
      runspec_components: Record<string, any>;
    };
    run_b: {
      id: string;
      created_at: string;
      runspec_components: Record<string, any>;
    };
    summary: Record<string, MetricDelta>;
    overall_winner: string;
    samples: SampleComparison[];
  };
}

export default function ComparisonDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [details, setDetails] = useState<ComparisonDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    async function loadDetails() {
      try {
        const data = await fetchWithAuth(`/api/v1/comparisons/${id}`);
        setDetails(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load comparison.');
      } finally {
        setLoading(false);
      }
    }
    loadDetails();
  }, [id]);

  if (loading) {
    return (
      <Layout activeTab="dashboard">
        <div className="loader">Loading comparison deltas...</div>
      </Layout>
    );
  }

  if (error || !details) {
    return (
      <Layout activeTab="dashboard">
        <div className="error-container">
          <h3>Error</h3>
          <p>{error || 'Comparison details not found.'}</p>
          <button onClick={() => router.push('/')} className="btn-back">Go to Dashboard</button>
        </div>
        <style jsx>{`
          .error-container {
            text-align: center;
            padding: 50px;
          }
          .btn-back {
            background: var(--accent-color);
            color: #0b0c10;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
          }
        `}</style>
      </Layout>
    );
  }

  const { name, created_at, comparison_data } = details;
  const { run_a, run_b, summary, overall_winner, samples } = comparison_data;

  // Format date helper
  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleString();
  };

  const getAPIUrl = () => {
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  };

  return (
    <Layout activeTab="dashboard">
      <div className="comparison-detail-container">
        
        {/* Header Metadata */}
        <div className="comp-header-card">
          <div className="comp-header-left">
            <h3 className="comp-name">{name}</h3>
            <p className="comp-date">Computed: {formatDate(created_at)}</p>
          </div>
          <div className="comp-actions">
            <a 
              href={`${getAPIUrl()}/api/v1/comparisons/${id}/report`} 
              target="_blank" 
              rel="noreferrer"
              className="action-btn btn-html"
            >
              View HTML Report ↗
            </a>
            <a 
              href={`${getAPIUrl()}/api/v1/comparisons/${id}/export/csv`} 
              className="action-btn btn-csv"
            >
              Export CSV ⬇
            </a>
          </div>
        </div>

        {/* Runs Comparison Cards */}
        <div className="runs-meta-grid">
          <div className="run-meta-card run-a-card">
            <span className="run-badge badge-a">Baseline (Run A)</span>
            <div className="run-id">{run_a.id}</div>
            <div className="run-date">Started: {formatDate(run_a.created_at)}</div>
            <div className="components-preview">
              <h5>Component Specs:</h5>
              <ul>
                {Object.entries(run_a.runspec_components).map(([k, v]) => (
                  <li key={k}><strong>{k}:</strong> {String(v)}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="run-meta-card run-b-card">
            <span className="run-badge badge-b">Target (Run B)</span>
            <div className="run-id">{run_b.id}</div>
            <div className="run-date">Started: {formatDate(run_b.created_at)}</div>
            <div className="components-preview">
              <h5>Component Specs:</h5>
              <ul>
                {Object.entries(run_b.runspec_components).map(([k, v]) => (
                  <li key={k}><strong>{k}:</strong> {String(v)}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Overall Winner Card */}
        <div className="winner-glowing-card">
          <div className="winner-label">OVERALL WINNER</div>
          <div className="winner-value">
            {overall_winner === 'run_a' && 'Baseline (Run A)'}
            {overall_winner === 'run_b' && 'Target (Run B)'}
            {overall_winner === 'draw' && 'DRAW (Equal Metric Weight)'}
          </div>
        </div>

        {/* Summary Table */}
        <div className="table-section">
          <h4 className="section-subtitle">Aggregate Metrics Comparison</h4>
          <div className="table-responsive">
            <table className="comp-table">
              <thead>
                <tr>
                  <th>Metric Name</th>
                  <th>Run A (Baseline)</th>
                  <th>Run B (Target)</th>
                  <th>Delta (B - A)</th>
                  <th>Winner</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(summary).map(([mname, mdata]) => (
                  <tr key={mname}>
                    <td><strong>{mname}</strong></td>
                    <td>{mdata.val_a}</td>
                    <td>{mdata.val_b}</td>
                    <td>
                      <span className={`delta-val ${mdata.winner === 'run_b' ? 'win' : mdata.winner === 'run_a' ? 'lose' : 'draw'}`}>
                        {mdata.delta !== null ? (mdata.delta > 0 ? `+${mdata.delta}` : mdata.delta) : 'N/A'}
                      </span>
                    </td>
                    <td>
                      <span className={`winner-badge ${mdata.winner}`}>
                        {mdata.winner === 'run_a' ? 'Run A' : mdata.winner === 'run_b' ? 'Run B' : 'Draw'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Sample List Table */}
        <div className="table-section" style={{ marginTop: '40px' }}>
          <h4 className="section-subtitle">Granular Sample Comparisons ({samples.length} cases)</h4>
          <div className="table-responsive">
            <table className="comp-table sample-table">
              <thead>
                <tr>
                  <th style={{ width: '10%' }}>Sample ID</th>
                  <th style={{ width: '35%' }}>Baseline Output (Run A)</th>
                  <th style={{ width: '35%' }}>Target Output (Run B)</th>
                  <th style={{ width: '20%' }}>Metrics Deltas</th>
                </tr>
              </thead>
              <tbody>
                {samples.map(sample => (
                  <tr key={sample.sample_id}>
                    <td><strong>{sample.sample_id}</strong></td>
                    
                    {/* Run A Output */}
                    <td>
                      <div className="sample-output-box">
                        {sample.run_a.status === 'completed' ? (
                          <pre>{sample.run_a.output_text}</pre>
                        ) : (
                          <span className="status-error">Error: {sample.run_a.status}</span>
                        )}
                        <span className="sample-latency">Latency: {sample.run_a.latency_ms} ms</span>
                      </div>
                    </td>

                    {/* Run B Output */}
                    <td>
                      <div className="sample-output-box">
                        {sample.run_b.status === 'completed' ? (
                          <pre>{sample.run_b.output_text}</pre>
                        ) : (
                          <span className="status-error">Error: {sample.run_b.status}</span>
                        )}
                        <span className="sample-latency">Latency: {sample.run_b.latency_ms} ms</span>
                      </div>
                    </td>

                    {/* Deltas */}
                    <td>
                      <div className="sample-deltas">
                        {Object.entries(sample.metrics_comparison).map(([mname, mdata]) => (
                          <div key={mname} className="sample-metric-delta-row">
                            <span className="metric-name">{mname}:</span>
                            <span className="metric-values">{mdata.val_a} ➔ {mdata.val_b}</span>
                            <span className={`metric-delta ${mdata.winner === 'run_b' ? 'win' : mdata.winner === 'run_a' ? 'lose' : 'draw'}`}>
                              ({mdata.delta !== null ? (mdata.delta > 0 ? `+${mdata.delta}` : mdata.delta) : 'N/A'})
                            </span>
                          </div>
                        ))}
                      </div>
                    </td>

                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <style jsx>{`
        .comparison-detail-container {
          display: flex;
          flex-direction: column;
          gap: 30px;
        }
        .comp-header-card {
          background: var(--card-bg);
          backdrop-filter: blur(10px);
          border: 1px solid var(--border-color);
          border-radius: 12px;
          padding: 24px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .comp-name {
          font-size: 20px;
          font-weight: 600;
          color: #fff;
          margin: 0 0 6px 0;
        }
        .comp-date {
          color: #888;
          font-size: 13px;
          margin: 0;
        }
        .comp-actions {
          display: flex;
          gap: 15px;
        }
        .action-btn {
          text-decoration: none;
          font-weight: 600;
          font-size: 13px;
          padding: 10px 18px;
          border-radius: 6px;
          cursor: pointer;
          transition: opacity 0.2s;
        }
        .btn-html {
          background: rgba(69, 243, 255, 0.1);
          border: 1px solid var(--accent-color);
          color: var(--accent-color);
        }
        .btn-csv {
          background: var(--accent-color);
          color: #0b0c10;
        }
        .action-btn:hover {
          opacity: 0.9;
        }
        .runs-meta-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 20px;
        }
        .run-meta-card {
          background: rgba(31, 40, 51, 0.3);
          border: 1px solid rgba(255, 255, 255, 0.05);
          border-radius: 12px;
          padding: 20px;
        }
        .run-badge {
          display: inline-block;
          font-size: 10px;
          font-weight: 700;
          text-transform: uppercase;
          padding: 3px 8px;
          border-radius: 4px;
          margin-bottom: 12px;
        }
        .badge-a {
          background: rgba(121, 40, 202, 0.2);
          color: #d3adf7;
          border: 1px solid rgba(121, 40, 202, 0.4);
        }
        .badge-b {
          background: rgba(255, 0, 128, 0.2);
          color: #ff85c0;
          border: 1px solid rgba(255, 0, 128, 0.4);
        }
        .run-id {
          font-family: monospace;
          color: #fff;
          font-size: 14px;
          margin-bottom: 6px;
        }
        .run-date {
          color: #666;
          font-size: 12px;
          margin-bottom: 15px;
        }
        .components-preview h5 {
          font-size: 11px;
          font-weight: 600;
          color: #888;
          text-transform: uppercase;
          margin: 0 0 8px 0;
        }
        .components-preview ul {
          list-style: none;
          padding: 0;
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 4px;
        }
        .components-preview li {
          font-size: 12px;
          color: #aaa;
        }
        .winner-glowing-card {
          background: linear-gradient(135deg, rgba(121, 40, 202, 0.15) 0%, rgba(255, 0, 128, 0.15) 100%);
          border: 1px solid var(--accent-color);
          border-radius: 12px;
          padding: 24px;
          text-align: center;
          box-shadow: 0 0 15px rgba(69, 243, 255, 0.15);
        }
        .winner-label {
          font-size: 11px;
          font-weight: 700;
          color: var(--accent-color);
          letter-spacing: 2px;
          margin-bottom: 8px;
        }
        .winner-value {
          font-size: 22px;
          font-weight: 700;
          color: #fff;
        }
        .section-subtitle {
          font-size: 15px;
          font-weight: 600;
          color: #fff;
          text-transform: uppercase;
          letter-spacing: 0.8px;
          margin-bottom: 15px;
          border-left: 3px solid var(--accent-color);
          padding-left: 10px;
        }
        .table-responsive {
          width: 100%;
          overflow-x: auto;
        }
        .comp-table {
          width: 100%;
          border-collapse: collapse;
          background: rgba(31, 40, 51, 0.2);
          border: 1px solid var(--border-color);
          border-radius: 8px;
          overflow: hidden;
        }
        .comp-table th, .comp-table td {
          padding: 14px 18px;
          text-align: left;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);
          font-size: 13px;
        }
        .comp-table th {
          background: rgba(11, 12, 16, 0.7);
          color: #888;
          font-weight: 600;
          text-transform: uppercase;
          font-size: 11px;
          letter-spacing: 0.5px;
        }
        .delta-val {
          font-weight: 700;
          font-family: monospace;
          font-size: 14px;
        }
        .delta-val.win {
          color: var(--success-color);
        }
        .delta-val.lose {
          color: var(--danger-color);
        }
        .delta-val.draw {
          color: #888;
        }
        .winner-badge {
          display: inline-block;
          font-size: 11px;
          font-weight: 600;
          padding: 2px 8px;
          border-radius: 4px;
        }
        .winner-badge.run_a {
          background: rgba(121, 40, 202, 0.2);
          color: #d3adf7;
        }
        .winner-badge.run_b {
          background: rgba(255, 0, 128, 0.2);
          color: #ff85c0;
        }
        .winner-badge.draw {
          background: rgba(255, 255, 255, 0.05);
          color: #888;
        }
        .sample-output-box {
          background: rgba(11, 12, 16, 0.6);
          border: 1px solid rgba(255, 255, 255, 0.05);
          border-radius: 6px;
          padding: 12px;
          position: relative;
          min-height: 80px;
        }
        .sample-output-box pre {
          margin: 0;
          white-space: pre-wrap;
          word-break: break-all;
          font-family: monospace;
          font-size: 12px;
          color: #ccc;
        }
        .sample-latency {
          display: block;
          margin-top: 8px;
          font-size: 11px;
          color: #555;
        }
        .status-error {
          color: var(--danger-color);
          font-weight: 500;
        }
        .sample-deltas {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .sample-metric-delta-row {
          font-size: 12px;
          display: flex;
          flex-direction: column;
        }
        .sample-metric-delta-row .metric-name {
          color: #888;
          font-weight: 500;
        }
        .sample-metric-delta-row .metric-values {
          color: #fff;
          font-family: monospace;
        }
        .sample-metric-delta-row .metric-delta {
          font-weight: 700;
          font-family: monospace;
        }
        .sample-metric-delta-row .metric-delta.win {
          color: var(--success-color);
        }
        .sample-metric-delta-row .metric-delta.lose {
          color: var(--danger-color);
        }
        .sample-metric-delta-row .metric-delta.draw {
          color: #888;
        }
      `}</style>
    </Layout>
  );
}
