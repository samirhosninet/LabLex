import { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import { fetchWithAuth } from '../../services/api';

interface ManifestItem {
  id: string;
  manifest_id: string;
  kind: string;
  name: string;
  schema_version: string;
  manifest_version: string;
  deprecated: boolean;
  content: any;
  created_at: string;
}

const COMPONENT_KINDS = [
  { value: '', label: 'All Categories' },
  { value: 'external_tool', label: 'External Tools' },
  { value: 'target', label: 'Targets' },
  { value: 'model', label: 'Models' },
  { value: 'benchmark', label: 'Benchmarks' },
  { value: 'adapter', label: 'Adapters' },
  { value: 'result_schema', label: 'Result Schemas' },
  { value: 'metric_profile', label: 'Metric Profiles' },
  { value: 'model_provider', label: 'Model Providers' },
  { value: 'report_template', label: 'Report Templates' },
];

export default function RegistryIndex() {
  const [manifests, setManifests] = useState<ManifestItem[]>([]);
  const [selectedKind, setSelectedKind] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Registration Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [rawJson, setRawJson] = useState('');
  const [registerError, setRegisterError] = useState<string | null>(null);
  const [registerSuccess, setRegisterSuccess] = useState(false);

  const loadManifests = async () => {
    setLoading(true);
    setError(null);
    try {
      const endpoint = `/api/v1/manifests?limit=50${selectedKind ? `&kind=${selectedKind}` : ''}`;
      const data = await fetchWithAuth(endpoint);
      setManifests(data.items || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load registry components.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadManifests();
  }, [selectedKind]);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setRegisterError(null);
    setRegisterSuccess(false);
    
    try {
      let parsedPayload;
      try {
        parsedPayload = JSON.parse(rawJson);
      } catch (jsonErr) {
        throw new Error('Invalid JSON format. Please check syntax.');
      }
      
      await fetchWithAuth('/api/v1/manifests', {
        method: 'POST',
        body: JSON.stringify(parsedPayload)
      });
      
      setRegisterSuccess(true);
      setRawJson('');
      setTimeout(() => {
        setIsModalOpen(false);
        setRegisterSuccess(false);
        loadManifests();
      }, 1500);
      
    } catch (err: any) {
      setRegisterError(err.message || 'Registration failed.');
    }
  };

  return (
    <Layout activeTab="registry">
      <div className="registry-actions" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px', alignItems: 'center' }}>
        <div className="filters" style={{ display: 'flex', gap: '10px', overflowX: 'auto', paddingBottom: '10px' }}>
          {COMPONENT_KINDS.map((kind) => (
            <button
              key={kind.value}
              className={`filter-tab ${selectedKind === kind.value ? 'active' : ''}`}
              onClick={() => setSelectedKind(kind.value)}
              style={{
                background: selectedKind === kind.value ? 'rgba(69, 243, 255, 0.15)' : 'rgba(31, 40, 51, 0.45)',
                border: `1px solid ${selectedKind === kind.value ? '#45f3ff' : 'rgba(69, 243, 255, 0.15)'}`,
                color: selectedKind === kind.value ? '#45f3ff' : '#c5c6c7',
                padding: '8px 16px',
                borderRadius: '20px',
                cursor: 'pointer',
                fontWeight: 500,
                whiteSpace: 'nowrap',
                transition: 'all 0.3s ease'
              }}
            >
              {kind.label}
            </button>
          ))}
        </div>
        
        <button
          className="btn-register"
          onClick={() => setIsModalOpen(true)}
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
          Register Manifest
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: '#888' }}>Loading registry...</div>
      ) : manifests.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '60px', border: '1px dashed rgba(255,255,255,0.1)', borderRadius: '12px', background: 'rgba(31, 40, 51, 0.2)' }}>
          <h4 style={{ margin: '0 0 10px 0', fontSize: '18px', color: '#fff' }}>No Components Registered</h4>
          <p style={{ color: '#888', margin: '0 0 20px 0', fontSize: '14px' }}>Get started by registering a new JSON manifest payload.</p>
          <button className="btn-primary" style={{ maxWidth: '200px' }} onClick={() => setIsModalOpen(true)}>Register First Manifest</button>
        </div>
      ) : (
        <div className="manifest-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
          {manifests.map((m) => (
            <div
              key={m.id}
              className="manifest-card"
              style={{
                background: 'rgba(31, 40, 51, 0.45)',
                border: '1px solid rgba(69, 243, 255, 0.1)',
                borderRadius: '12px',
                padding: '20px',
                transition: 'all 0.3s ease',
                cursor: 'pointer',
                position: 'relative'
              }}
              onClick={() => router.push(`/registry/${m.id}`)}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = '#45f3ff';
                e.currentTarget.style.boxShadow = '0 0 12px rgba(69, 243, 255, 0.1)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'rgba(69, 243, 255, 0.1)';
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              <span
                style={{
                  fontSize: '10px',
                  textTransform: 'uppercase',
                  fontWeight: 700,
                  color: '#66fcf1',
                  background: 'rgba(102, 252, 241, 0.1)',
                  padding: '4px 8px',
                  borderRadius: '10px',
                  display: 'inline-block',
                  marginBottom: '10px'
                }}
              >
                {m.kind.replace('_', ' ')}
              </span>
              <h3 style={{ margin: '0 0 5px 0', fontSize: '18px', color: '#fff' }}>{m.name}</h3>
              <div style={{ fontSize: '12px', color: '#888', marginBottom: '15px' }}>
                ID: <code style={{ color: '#45f3ff' }}>{m.manifest_id}</code> | Version: {m.manifest_version}
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: '#555' }}>
                <span>Created: {new Date(m.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Register Manifest Modal */}
      {isModalOpen && (
        <div
          className="modal-overlay"
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0,0,0,0.85)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000,
            padding: '20px'
          }}
        >
          <div
            className="modal-content"
            style={{
              background: '#1f2833',
              border: '1px solid #45f3ff',
              borderRadius: '16px',
              width: '100%',
              maxWidth: '650px',
              padding: '30px',
              boxShadow: '0 0 24px rgba(69, 243, 255, 0.15)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h3 style={{ margin: 0, color: '#fff', fontSize: '20px' }}>Register Component Manifest</h3>
              <button
                onClick={() => setIsModalOpen(false)}
                style={{ background: 'transparent', border: 'none', color: '#888', fontSize: '20px', cursor: 'pointer' }}
              >
                &times;
              </button>
            </div>
            
            <form onSubmit={handleRegister}>
              <div className="form-group">
                <label className="form-label">Paste Manifest JSON Payload</label>
                <textarea
                  value={rawJson}
                  onChange={(e) => setRawJson(e.target.value)}
                  placeholder={`{\n  "kind": "external_tool",\n  "id": "mock_tool_v1",\n  "name": "My Mock Tool",\n  "schema_version": "1.0",\n  "manifest_version": "1.0.0",\n  "endpoint": "http://localhost:8080/eval",\n  "compatible_adapters": ["mock_adapter_v1"]\n}`}
                  required
                  style={{
                    width: '100%',
                    height: '280px',
                    background: '#0b0c10',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '8px',
                    color: '#a9f5f2',
                    fontFamily: 'monospace',
                    fontSize: '13px',
                    padding: '15px',
                    outline: 'none',
                    resize: 'none'
                  }}
                />
              </div>
              
              {registerError && <div className="error-message" style={{ marginBottom: '15px' }}>{registerError}</div>}
              {registerSuccess && (
                <div style={{ color: '#34c759', background: 'rgba(52, 199, 89, 0.1)', padding: '10px', borderRadius: '6px', border: '1px solid rgba(52, 199, 89, 0.2)', marginBottom: '15px', fontSize: '13px' }}>
                  Component successfully registered!
                </div>
              )}
              
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  style={{
                    background: 'transparent',
                    border: '1px solid rgba(255,255,255,0.1)',
                    color: '#c5c6c7',
                    padding: '10px 20px',
                    borderRadius: '8px',
                    cursor: 'pointer'
                  }}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary" style={{ maxWidth: '160px', marginTop: 0 }}>
                  Submit
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </Layout>
  );
}
