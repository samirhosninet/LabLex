import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Layout from '../components/Layout';
import { fetchWithAuth } from '../services/api';

interface QuotaData {
  max_concurrent_runs: number;
  current_concurrent_runs: number;
  max_monthly_runs: number;
  current_monthly_runs: number;
  rate_limit_per_minute: number;
}

interface RunItem {
  id: string;
  runspec_id: string;
  status: string;
  created_at: string;
}

interface ComparisonItem {
  id: string;
  name: string;
  created_at: string;
  runs: string[];
}

export default function Home() {
  const router = useRouter();
  const [quota, setQuota] = useState<QuotaData | null>(null);
  const [runs, setRuns] = useState<RunItem[]>([]);
  const [comparisons, setComparisons] = useState<ComparisonItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [submittingComp, setSubmittingComp] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Comparison form state
  const [runA, setRunA] = useState('');
  const [runB, setRunB] = useState('');
  const [compName, setCompName] = useState('');

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const [quotaData, runsData, compData] = await Promise.all([
          fetchWithAuth('/api/v1/runs/quota'),
          fetchWithAuth('/api/v1/runs?limit=20'),
          fetchWithAuth('/api/v1/comparisons?limit=10')
        ]);
        setQuota(quotaData);
        setRuns(runsData.items || []);
        setComparisons(compData.items || []);
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard data.');
      } finally {
        setLoading(false);
      }
    }
    loadDashboardData();
  }, []);

  const handleCreateComparison = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!runA || !runB) {
      setError('Please select two completed runs to compare.');
      return;
    }
    if (runA === runB) {
      setError('Baseline and Target runs must be different.');
      return;
    }

    setSubmittingComp(true);
    setError(null);

    try {
      const result = await fetchWithAuth('/api/v1/comparisons', {
        method: 'POST',
        body: JSON.stringify({
          run_id_a: runA,
          run_id_b: runB,
          name: compName || undefined
        })
      });
      router.push(`/comparisons/${result.id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to trigger comparison.');
      setSubmittingComp(false);
    }
  };

  const completedRuns = runs.filter(r => r.status === 'completed');

  if (loading) {
    return (
      <Layout activeTab="dashboard">
        <div className="loader">Loading Dashboard analytics...</div>
        <style jsx>{`
          .loader {
            color: var(--accent-color);
            text-align: center;
            padding: 50px;
            font-size: 16px;
            font-weight: 500;
          }
        `}</style>
      </Layout>
    );
  }

  return (
    <Layout activeTab="dashboard">
      <div className="dashboard-grid">
        
        {/* Row 1: Quotas & Gauges */}
        <section className="dashboard-section full-width">
          <h3 className="section-title">Operational Quotas & Resource Usage</h3>
          <div className="quota-cards">
            
            {/* Concurrent Runs Gauge */}
            <div className="quota-card">
              <div className="gauge-value">
                {quota?.current_concurrent_runs} <span className="slash">/</span> {quota?.max_concurrent_runs}
              </div>
              <div className="quota-bar-container">
                <div 
                  className="quota-bar active-bar" 
                  style={{ width: `${Math.min(100, ((quota?.current_concurrent_runs || 0) / (quota?.max_concurrent_runs || 5)) * 100)}%` }}
                />
              </div>
              <div className="quota-label">Active Concurrent Runs</div>
            </div>

            {/* Monthly Limit Quota */}
            <div className="quota-card">
              <div className="gauge-value">
                {quota?.current_monthly_runs} <span className="slash">/</span> {quota?.max_monthly_runs}
              </div>
              <div className="quota-bar-container">
                <div 
                  className="quota-bar monthly-bar" 
                  style={{ width: `${Math.min(100, ((quota?.current_monthly_runs || 0) / (quota?.max_monthly_runs || 100)) * 100)}%` }}
                />
              </div>
              <div className="quota-label">Monthly Runs Consumed</div>
            </div>

            {/* Rate Limiting info */}
            <div className="quota-card">
              <div className="gauge-value">
                {quota?.rate_limit_per_minute} <span className="unit">req/m</span>
              </div>
              <div className="rate-circle-indicator">
                <div className="rate-ping" />
              </div>
              <div className="quota-label">API Rate Limit Per Tenant</div>
            </div>

          </div>
        </section>

        {/* Row 2: Left column (Compare Wizard), Right column (Runs/Comparisons lists) */}
        
        {/* Wizard Card */}
        <div className="grid-col">
          <div className="card glass-card">
            <h4 className="card-title-premium">Compare Runs Side-by-Side</h4>
            <p className="card-subtitle-premium">Select baseline and target runs to analyze deltas and find the winner.</p>
            
            {error && <div className="dashboard-error">{error}</div>}

            <form onSubmit={handleCreateComparison} className="wizard-form">
              <div className="form-group-premium">
                <label className="form-label-premium">Baseline Run (A)</label>
                <select 
                  className="form-select-premium"
                  value={runA} 
                  onChange={e => setRunA(e.target.value)}
                  required
                >
                  <option value="">-- Choose Completed Run --</option>
                  {completedRuns.map(r => (
                    <option key={r.id} value={r.id}>
                      {r.id.substring(0, 8)} ({new Date(r.created_at).toLocaleDateString()})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group-premium">
                <label className="form-label-premium">Target Run (B)</label>
                <select 
                  className="form-select-premium"
                  value={runB} 
                  onChange={e => setRunB(e.target.value)}
                  required
                >
                  <option value="">-- Choose Completed Run --</option>
                  {completedRuns.map(r => (
                    <option key={r.id} value={r.id}>
                      {r.id.substring(0, 8)} ({new Date(r.created_at).toLocaleDateString()})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group-premium">
                <label className="form-label-premium">Comparison Name (Optional)</label>
                <input 
                  type="text" 
                  className="form-input-premium" 
                  placeholder="e.g. Model V2 vs Baseline"
                  value={compName}
                  onChange={e => setCompName(e.target.value)}
                />
              </div>

              <button 
                type="submit" 
                className="btn-premium-action" 
                disabled={submittingComp || completedRuns.length < 2}
              >
                {submittingComp ? 'Calculating Deltas...' : 'Run Metric Comparison'}
              </button>

              {completedRuns.length < 2 && (
                <p className="warning-text">You need at least 2 completed runs to trigger a comparison.</p>
              )}
            </form>
          </div>

          <div className="card glass-card links-card">
            <h4 className="card-title-premium" style={{ marginBottom: '15px' }}>Compliance & Logs</h4>
            <div className="log-links">
              <Link href="/audit" className="log-link-btn">
                <span>Browse Tenant Audit Logs</span>
                <span className="arrow">➔</span>
              </Link>
            </div>
          </div>
        </div>

        {/* Lists Column */}
        <div className="grid-col">
          
          {/* Recent Comparisons List */}
          <div className="card glass-card list-card">
            <h4 className="card-title-premium">Recent Comparisons</h4>
            {comparisons.length === 0 ? (
              <p className="empty-message">No comparisons computed yet.</p>
            ) : (
              <div className="items-list">
                {comparisons.map(comp => (
                  <div key={comp.id} className="item-row">
                    <div className="item-info">
                      <div className="item-name">{comp.name}</div>
                      <div className="item-date">{new Date(comp.created_at).toLocaleString()}</div>
                    </div>
                    <Link href={`/comparisons/${comp.id}`} className="item-action-link">
                      View Report
                    </Link>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Recent Runs List */}
          <div className="card glass-card list-card">
            <h4 className="card-title-premium">Recent Runs Status</h4>
            {runs.length === 0 ? (
              <p className="empty-message">No runs triggered yet.</p>
            ) : (
              <div className="items-list">
                {runs.slice(0, 5).map(run => (
                  <div key={run.id} className="item-row">
                    <div className="item-info">
                      <div className="item-name">Run ID: {run.id.substring(0, 8)}...</div>
                      <div className="item-date">{new Date(run.created_at).toLocaleString()}</div>
                    </div>
                    <div className="item-right">
                      <span className={`status-badge status-${run.status}`}>{run.status}</span>
                      <Link href={`/runs/${run.id}`} className="view-run-link" style={{ marginLeft: '10px' }}>
                        Details
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>

      </div>

      <style jsx>{`
        .dashboard-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 30px;
          margin-top: 10px;
        }
        .full-width {
          grid-column: 1 / span 2;
        }
        .grid-col {
          display: flex;
          flex-direction: column;
          gap: 30px;
        }
        .section-title {
          font-size: 16px;
          font-weight: 600;
          color: #fff;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 20px;
          border-left: 3px solid var(--accent-color);
          padding-left: 10px;
        }
        .quota-cards {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 20px;
        }
        .quota-card {
          background: rgba(31, 40, 51, 0.4);
          border: 1px solid var(--border-color);
          border-radius: 12px;
          padding: 24px;
          text-align: center;
          position: relative;
          overflow: hidden;
        }
        .gauge-value {
          font-size: 28px;
          font-weight: 700;
          color: #fff;
          margin-bottom: 12px;
          font-family: monospace;
        }
        .gauge-value .slash {
          color: #444;
          font-weight: 300;
        }
        .gauge-value .unit {
          font-size: 14px;
          color: #888;
          font-weight: 500;
        }
        .quota-bar-container {
          width: 100%;
          height: 6px;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 3px;
          margin-bottom: 15px;
          overflow: hidden;
        }
        .quota-bar {
          height: 100%;
          border-radius: 3px;
          transition: width 0.5s ease-in-out;
        }
        .active-bar {
          background: linear-gradient(90deg, #7928ca, var(--accent-color));
        }
        .monthly-bar {
          background: linear-gradient(90deg, #ff0080, #7928ca);
        }
        .rate-circle-indicator {
          height: 6px;
          display: flex;
          justify-content: center;
          align-items: center;
          margin-bottom: 15px;
        }
        .rate-ping {
          width: 8px;
          height: 8px;
          background-color: var(--success-color);
          border-radius: 50%;
          box-shadow: 0 0 8px var(--success-color);
        }
        .quota-label {
          font-size: 11px;
          font-weight: 600;
          color: #888;
          text-transform: uppercase;
          letter-spacing: 0.8px;
        }
        .glass-card {
          background: var(--card-bg);
          backdrop-filter: blur(12px);
          border: 1px solid var(--border-color);
          border-radius: 16px;
          padding: 30px;
          box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        }
        .card-title-premium {
          font-size: 18px;
          font-weight: 600;
          color: #fff;
          margin: 0 0 8px 0;
        }
        .card-subtitle-premium {
          color: #888;
          font-size: 13px;
          margin: 0 0 24px 0;
          line-height: 1.5;
        }
        .dashboard-error {
          color: var(--danger-color);
          background: rgba(255, 59, 48, 0.08);
          border: 1px solid rgba(255, 59, 48, 0.2);
          border-radius: 8px;
          padding: 12px;
          font-size: 13px;
          margin-bottom: 20px;
        }
        .wizard-form {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }
        .form-group-premium {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .form-label-premium {
          font-size: 11px;
          font-weight: 600;
          color: #888;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
        .form-select-premium, .form-input-premium {
          width: 100%;
          background: rgba(11, 12, 16, 0.6);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 8px;
          color: #fff;
          padding: 12px 14px;
          font-size: 13px;
          outline: none;
          transition: border-color 0.3s ease;
        }
        .form-select-premium:focus, .form-input-premium:focus {
          border-color: var(--accent-color);
        }
        .btn-premium-action {
          width: 100%;
          background: linear-gradient(90deg, #03dac6, var(--accent-color));
          color: #0b0c10;
          border: none;
          border-radius: 8px;
          padding: 14px;
          font-weight: 600;
          font-size: 13px;
          cursor: pointer;
          transition: opacity 0.2s, transform 0.2s;
        }
        .btn-premium-action:hover {
          opacity: 0.95;
          transform: translateY(-1px);
        }
        .btn-premium-action:disabled {
          background: #333;
          color: #777;
          cursor: not-allowed;
          transform: none;
        }
        .warning-text {
          font-size: 12px;
          color: #ff9f0a;
          margin: 10px 0 0 0;
          text-align: center;
        }
        .links-card {
          padding: 20px 30px;
        }
        .log-links {
          display: flex;
          flex-direction: column;
        }
        .log-link-btn {
          display: flex;
          justify-content: space-between;
          align-items: center;
          color: var(--accent-color);
          text-decoration: none;
          font-weight: 600;
          font-size: 13px;
          padding: 10px 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);
          transition: padding-left 0.2s ease;
        }
        .log-link-btn:hover {
          padding-left: 5px;
        }
        .log-link-btn .arrow {
          font-size: 14px;
        }
        .list-card {
          flex-grow: 1;
        }
        .empty-message {
          color: #555;
          font-size: 13px;
          text-align: center;
          padding: 40px 0;
        }
        .items-list {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }
        .item-row {
          background: rgba(11, 12, 16, 0.4);
          border: 1px solid rgba(255, 255, 255, 0.03);
          border-radius: 8px;
          padding: 12px 16px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          transition: border-color 0.3s;
        }
        .item-row:hover {
          border-color: rgba(69, 243, 255, 0.1);
        }
        .item-info {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }
        .item-name {
          font-size: 13px;
          font-weight: 500;
          color: #fff;
        }
        .item-date {
          font-size: 11px;
          color: #666;
        }
        .item-action-link {
          font-size: 12px;
          color: var(--accent-color);
          text-decoration: none;
          font-weight: 600;
        }
        .item-action-link:hover {
          text-decoration: underline;
        }
        .status-badge {
          font-size: 10px;
          font-weight: 700;
          text-transform: uppercase;
          padding: 3px 8px;
          border-radius: 10px;
          letter-spacing: 0.5px;
        }
        .status-completed {
          background: rgba(52, 199, 89, 0.15);
          color: var(--success-color);
          border: 1px solid rgba(52, 199, 89, 0.3);
        }
        .status-running {
          background: rgba(0, 122, 255, 0.15);
          color: #007aff;
          border: 1px solid rgba(0, 122, 255, 0.3);
        }
        .status-queued {
          background: rgba(255, 159, 10, 0.15);
          color: #ff9f0a;
          border: 1px solid rgba(255, 159, 10, 0.3);
        }
        .status-failed, .status-normalization_failed {
          background: rgba(255, 59, 48, 0.15);
          color: var(--danger-color);
          border: 1px solid rgba(255, 59, 48, 0.3);
        }
        .view-run-link {
          font-size: 12px;
          color: #888;
          text-decoration: none;
        }
        .view-run-link:hover {
          color: #fff;
        }
      `}</style>
    </Layout>
  );
}
