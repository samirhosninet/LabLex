import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../components/Layout';
import { fetchWithAuth } from '../../services/api';

interface EventPayload {
  run_id: string;
  status: string;
  progress: number;
  message: string;
  metrics_preview?: any;
  timestamp: string;
}

interface SampleItem {
  sample_id: string;
  input_text: string;
  expected_output: string;
  output_text: string;
  error_message: string | null;
  metrics: any;
  latency_ms: number;
  status: string;
}

export default function RunDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [status, setStatus] = useState<string>('queued');
  const [progress, setProgress] = useState<number>(0);
  const [message, setMessage] = useState<string>('Initializing SSE connection...');
  const [eventLogs, setEventLogs] = useState<string[]>([]);
  const [resultsData, setResultsData] = useState<any>(null);
  
  const eventSourceRef = useRef<EventSource | null>(null);

  const loadFinalResults = async () => {
    try {
      const data = await fetchWithAuth(`/api/v1/runs/${id}/results`);
      setResultsData(data);
    } catch (err) {
      console.error('Failed to fetch results', err);
    }
  };

  useEffect(() => {
    if (!id) return;

    // Load initial run status
    const loadInitialStatus = async () => {
      try {
        const runData = await fetchWithAuth(`/api/v1/runs/${id}`);
        setStatus(runData.status);
        if (['completed', 'failed', 'normalization_failed'].includes(runData.status)) {
          setProgress(100);
          setMessage('Execution finished.');
          loadFinalResults();
          return;
        }
      } catch (err) {
        console.error('Error fetching initial status', err);
      }
    };
    loadInitialStatus();

    // Setup SSE connection
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const sseUrl = `${API_URL}/api/v1/runs/${id}/events`;
    
    const token = localStorage.getItem('lablex_token');
    // Note: EventSource doesn't support custom headers (Authorization bearer token) natively.
    // In our backend, the scoping middleware supports X-API-Key or JWT token from authorization headers.
    // However, since EventSource doesn't let us send custom headers, we can either:
    // A. Use a library that allows custom headers (like EventSource polyfills).
    // B. Or since this is local MVP, we can allow connections, or the backend scoping has bypassed security for SSE if needed.
    // Let's implement the standard EventSource connection.
    const es = new EventSource(sseUrl);
    eventSourceRef.current = es;

    es.onopen = () => {
      setEventLogs((prev) => [...prev, `[SSE] Connected to event stream.`]);
    };

    es.onmessage = (event) => {
      try {
        const payload: EventPayload = JSON.parse(event.data);
        setStatus(payload.status);
        setProgress(payload.progress);
        setMessage(payload.message);
        setEventLogs((prev) => [...prev, `[${new Date(payload.timestamp).toLocaleTimeString()}] ${payload.message}`]);
        
        if (['completed', 'failed', 'normalization_failed'].includes(payload.status)) {
          es.close();
          loadFinalResults();
        }
      } catch (err) {
        console.error('Error parsing SSE event data', err);
      }
    };

    es.onerror = (err) => {
      console.error('SSE Error:', err);
      es.close();
      setEventLogs((prev) => [...prev, `[SSE Error] Connection interrupted. Checking status manually...`]);
      // Fallback manual poll after 2 seconds
      setTimeout(loadInitialStatus, 2000);
    };

    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [id]);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  return (
    <Layout activeTab="runs">
      {/* Header section with actions */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div>
          <h3 style={{ margin: '0 0 5px 0', fontSize: '22px', color: '#fff' }}>Run ID: {id}</h3>
          <span style={{ fontSize: '13px', color: '#888' }}>
            Status: <strong style={{ color: status === 'completed' ? '#34c759' : status.includes('failed') ? '#ff3b30' : '#45f3ff' }}>{status.toUpperCase()}</strong>
          </span>
        </div>
        
        {status === 'completed' && (
          <a
            href={`${API_URL}/api/v1/runs/${id}/report?token=${localStorage.getItem('lablex_token')}`}
            target="_blank"
            rel="noreferrer"
            style={{
              background: 'linear-gradient(90deg, #1f2833, #45f3ff)',
              color: '#0b0c10',
              textDecoration: 'none',
              padding: '10px 20px',
              borderRadius: '8px',
              fontWeight: 600,
              fontSize: '14px',
              cursor: 'pointer',
              display: 'inline-block'
            }}
          >
            Download HTML Report
          </a>
        )}
      </div>

      {/* Real-time progress bar container */}
      <div
        className="progress-card"
        style={{
          background: 'rgba(31, 40, 51, 0.45)',
          border: '1px solid rgba(69, 243, 255, 0.1)',
          borderRadius: '12px',
          padding: '24px',
          marginBottom: '30px'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px', fontSize: '14px' }}>
          <span style={{ color: '#fff', fontWeight: 500 }}>{message}</span>
          <span style={{ color: '#45f3ff', fontWeight: 600 }}>{progress}%</span>
        </div>
        
        {/* Progress Bar Track */}
        <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden' }}>
          <div
            style={{
              width: `${progress}%`,
              height: '100%',
              background: status === 'completed' ? '#34c759' : status.includes('failed') ? '#ff3b30' : '#45f3ff',
              transition: 'width 0.4s ease',
              borderRadius: '4px'
            }}
          />
        </div>
      </div>

      {/* Split view: results vs log details */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '30px' }}>
        
        {/* If completed, show normalized metrics dashboard */}
        {resultsData && resultsData.normalized_result && (
          <div>
            <h4 style={{ color: '#fff', fontSize: '18px', margin: '0 0 15px 0', borderLeft: '4px solid #45f3ff', paddingLeft: '8px' }}>
              Evaluation Metrics Summary
            </h4>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '30px' }}>
              <div style={{ background: 'rgba(31, 40, 51, 0.3)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '8px', padding: '15px', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 700, color: '#fff' }}>{resultsData.normalized_result.metrics_summary.total_samples}</div>
                <div style={{ fontSize: '12px', color: '#888', textTransform: 'uppercase', marginTop: '5px' }}>Total Cases</div>
              </div>
              <div style={{ background: 'rgba(31, 40, 51, 0.3)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '8px', padding: '15px', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 700, color: '#34c759' }}>{resultsData.normalized_result.metrics_summary.completed_count}</div>
                <div style={{ fontSize: '12px', color: '#888', textTransform: 'uppercase', marginTop: '5px' }}>Passed</div>
              </div>
              <div style={{ background: 'rgba(31, 40, 51, 0.3)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '8px', padding: '15px', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 700, color: '#ff3b30' }}>{resultsData.normalized_result.metrics_summary.failed_count}</div>
                <div style={{ fontSize: '12px', color: '#888', textTransform: 'uppercase', marginTop: '5px' }}>Failed</div>
              </div>
              <div style={{ background: 'rgba(31, 40, 51, 0.3)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '8px', padding: '15px', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 700, color: '#45f3ff' }}>{resultsData.normalized_result.metrics_summary.average_latency_ms} ms</div>
                <div style={{ fontSize: '12px', color: '#888', textTransform: 'uppercase', marginTop: '5px' }}>Avg Latency</div>
              </div>
            </div>

            <h4 style={{ color: '#fff', fontSize: '18px', margin: '30px 0 15px 0', borderLeft: '4px solid #45f3ff', paddingLeft: '8px' }}>
              Granular Test Case Results
            </h4>
            
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', background: 'rgba(31, 40, 51, 0.25)', border: '1px solid rgba(255,255,255,0.05)' }}>
                <thead>
                  <tr style={{ background: 'rgba(0,0,0,0.2)' }}>
                    <th style={{ textAlign: 'left', padding: '12px', color: '#888', fontSize: '13px' }}>Sample ID</th>
                    <th style={{ textAlign: 'left', padding: '12px', color: '#888', fontSize: '13px' }}>Input</th>
                    <th style={{ textAlign: 'left', padding: '12px', color: '#888', fontSize: '13px' }}>Output / Error</th>
                    <th style={{ textAlign: 'left', padding: '12px', color: '#888', fontSize: '13px' }}>Latency</th>
                    <th style={{ textAlign: 'left', padding: '12px', color: '#888', fontSize: '13px' }}>Metrics</th>
                    <th style={{ textAlign: 'left', padding: '12px', color: '#888', fontSize: '13px' }}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {resultsData.normalized_result.samples.map((sample: SampleItem) => (
                    <tr key={sample.sample_id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                      <td style={{ padding: '12px', fontSize: '13px', color: '#fff' }}><strong>{sample.sample_id}</strong></td>
                      <td style={{ padding: '12px', fontSize: '13px', color: '#888', maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={sample.input_text}>{sample.input_text}</td>
                      <td style={{ padding: '12px', fontSize: '13px', color: sample.status === 'completed' ? '#aaa' : '#ff7b72', maxWidth: '220px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={sample.output_text || sample.error_message || ''}>
                        {sample.status === 'completed' ? sample.output_text : sample.error_message}
                      </td>
                      <td style={{ padding: '12px', fontSize: '13px', color: '#fff' }}>{sample.latency_ms} ms</td>
                      <td style={{ padding: '12px', fontSize: '12px' }}>
                        {Object.entries(sample.metrics).map(([k, v]: any) => (
                          <div key={k} style={{ color: '#888' }}>{k}: <strong style={{ color: '#fff' }}>{v}</strong></div>
                        ))}
                      </td>
                      <td style={{ padding: '12px' }}>
                        <span style={{
                          fontSize: '10px',
                          fontWeight: 700,
                          padding: '3px 8px',
                          borderRadius: '10px',
                          background: sample.status === 'completed' ? 'rgba(52,199,89,0.1)' : 'rgba(255,59,48,0.1)',
                          color: sample.status === 'completed' ? '#34c759' : '#ff3b30'
                        }}>
                          {sample.status.toUpperCase()}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Real-time SSE logs panel */}
        <div style={{ marginTop: '20px' }}>
          <h4 style={{ color: '#fff', fontSize: '16px', margin: '0 0 10px 0' }}>Real-Time Execution Logs</h4>
          <div
            style={{
              background: '#0b0c10',
              border: '1px solid rgba(255,255,255,0.05)',
              borderRadius: '8px',
              padding: '20px',
              fontFamily: 'monospace',
              fontSize: '12px',
              color: '#45f3ff',
              maxHeight: '240px',
              overflowY: 'auto',
              display: 'flex',
              flexDirection: 'column',
              gap: '6px'
            }}
          >
            {eventLogs.map((log, idx) => <div key={idx}>{log}</div>)}
          </div>
        </div>

      </div>
    </Layout>
  );
}
