import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../components/Layout';
import { fetchWithAuth } from '../../services/api';

interface RunItem {
  id: string;
  runspec_id: string;
  status: string;
  created_at: string;
}

export default function RunsIndex() {
  const router = useRouter();
  const [runs, setRuns] = useState<RunItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadRuns = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchWithAuth('/api/v1/runs?limit=50');
      setRuns(data.items || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load evaluation runs.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRuns();
  }, []);

  return (
    <Layout activeTab="runs">
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px', alignItems: 'center' }}>
        <h3 style={{ margin: 0, color: '#fff', fontSize: '18px' }}>Execution History</h3>
        
        <button
          className="btn-register"
          onClick={() => router.push('/runs/create')}
          style={{
            background: 'linear-gradient(90deg, #1f2833, #66fcf1)',
            color: '#0b0c10',
            border: 'none',
            borderRadius: '20px',
            padding: '10px 20px',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'all 0.3s'
          }}
        >
          Launch New Run
        </button>
      </div>

      {error && <div className="error-message" style={{ marginBottom: '20px' }}>{error}</div>}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: '#888' }}>Loading execution history...</div>
      ) : runs.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '60px', border: '1px dashed rgba(255,255,255,0.1)', borderRadius: '12px', background: 'rgba(31, 40, 51, 0.2)' }}>
          <h4 style={{ margin: '0 0 10px 0', fontSize: '18px', color: '#fff' }}>No Runs Launched Yet</h4>
          <p style={{ color: '#888', margin: '0 0 20px 0', fontSize: '14px' }}>Launch a new evaluation run spec to observe SSE progress tracking.</p>
          <button className="btn-primary" style={{ maxWidth: '200px' }} onClick={() => router.push('/runs/create')}>Start First Run</button>
        </div>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', background: 'rgba(31, 40, 51, 0.25)', border: '1px solid rgba(69, 243, 255, 0.1)', borderRadius: '8px' }}>
            <thead>
              <tr style={{ background: 'rgba(0,0,0,0.2)' }}>
                <th style={{ textAlign: 'left', padding: '14px 16px', color: '#888', fontSize: '13px' }}>Run ID</th>
                <th style={{ textAlign: 'left', padding: '14px 16px', color: '#888', fontSize: '13px' }}>RunSpec ID</th>
                <th style={{ textAlign: 'left', padding: '14px 16px', color: '#888', fontSize: '13px' }}>Status</th>
                <th style={{ textAlign: 'left', padding: '14px 16px', color: '#888', fontSize: '13px' }}>Started Date</th>
                <th style={{ textAlign: 'left', padding: '14px 16px', color: '#888', fontSize: '13px' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {runs.map((run) => (
                <tr key={run.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <td style={{ padding: '14px 16px', fontSize: '13px', color: '#fff' }}><strong>{run.id}</strong></td>
                  <td style={{ padding: '14px 16px', fontSize: '13px', color: '#888' }}>{run.runspec_id}</td>
                  <td style={{ padding: '14px 16px', fontSize: '13px' }}>
                    <span style={{
                      fontSize: '11px',
                      fontWeight: 700,
                      padding: '4px 10px',
                      borderRadius: '12px',
                      background: run.status === 'completed' ? 'rgba(52,199,89,0.1)' : run.status.includes('failed') ? 'rgba(255,59,48,0.1)' : 'rgba(69,243,255,0.1)',
                      color: run.status === 'completed' ? '#34c759' : run.status.includes('failed') ? '#ff3b30' : '#45f3ff'
                    }}>
                      {run.status.toUpperCase()}
                    </span>
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: '13px', color: '#888' }}>{new Date(run.created_at).toLocaleString()}</td>
                  <td style={{ padding: '14px 16px', fontSize: '13px' }}>
                    <button
                      onClick={() => router.push(`/runs/${run.id}`)}
                      style={{
                        background: 'transparent',
                        border: '1px solid var(--accent-color)',
                        color: 'var(--accent-color)',
                        borderRadius: '6px',
                        padding: '6px 12px',
                        cursor: 'pointer',
                        fontSize: '12px',
                        fontWeight: 500
                      }}
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Layout>
  );
}
