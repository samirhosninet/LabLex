import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../components/Layout';
import { fetchWithAuth } from '../../services/api';

interface ManifestSummary {
  id: string;
  manifest_id: string;
  kind: string;
  name: string;
}

export default function CreateRunWizard() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(true);
  
  // Available registry components
  const [tools, setTools] = useState<ManifestSummary[]>([]);
  const [adapters, setAdapters] = useState<ManifestSummary[]>([]);
  const [schemas, setSchemas] = useState<ManifestSummary[]>([]);
  const [benchmarks, setBenchmarks] = useState<ManifestSummary[]>([]);
  const [targets, setTargets] = useState<ManifestSummary[]>([]);
  const [models, setModels] = useState<ManifestSummary[]>([]);
  
  // Selected component IDs
  const [selectedTool, setSelectedTool] = useState('');
  const [selectedAdapter, setSelectedAdapter] = useState('');
  const [selectedSchema, setSelectedSchema] = useState('');
  const [selectedBenchmark, setSelectedBenchmark] = useState('');
  const [selectedTarget, setSelectedTarget] = useState('');
  const [selectedModel, setSelectedModel] = useState('');

  // Execution states
  const [composedRunSpecId, setComposedRunSpecId] = useState<string | null>(null);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);
  const [isValidated, setIsValidated] = useState(false);
  const [dryRunReport, setDryRunReport] = useState<any>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    // Pre-load all registered components
    const loadRegistryData = async () => {
      try {
        const data = await fetchWithAuth('/api/v1/manifests?limit=100');
        const items = data.items || [];
        
        setTools(items.filter((item: any) => item.kind === 'external_tool'));
        setAdapters(items.filter((item: any) => item.kind === 'adapter'));
        setSchemas(items.filter((item: any) => item.kind === 'result_schema'));
        setBenchmarks(items.filter((item: any) => item.kind === 'benchmark'));
        setTargets(items.filter((item: any) => item.kind === 'target'));
        setModels(items.filter((item: any) => item.kind === 'model'));
      } catch (err) {
        console.error('Failed to load components.', err);
      } finally {
        setLoading(false);
      }
    };
    loadRegistryData();
  }, []);

  const handleComposeAndValidate = async () => {
    setLoading(true);
    setValidationErrors([]);
    setIsValidated(false);
    
    try {
      // Compose RunSpec
      const composeRes = await fetchWithAuth('/api/v1/runspecs/compose', {
        method: 'POST',
        body: JSON.stringify({
          components: {
            external_tool: selectedTool,
            adapter: selectedAdapter,
            result_schema: selectedSchema,
            benchmark: selectedBenchmark,
            target: selectedTarget,
            model: selectedModel
          }
        })
      });
      
      const runspecId = composeRes.id;
      setComposedRunSpecId(runspecId);
      
      // Validate RunSpec compatibility & connections
      const validateRes = await fetchWithAuth(`/api/v1/runspecs/${runspecId}/validate`, {
        method: 'POST'
      });
      
      setIsValidated(true);
      
      // Run pre-flight dry-run stats
      const dryRunRes = await fetchWithAuth(`/api/v1/runspecs/${runspecId}/dry-run`, {
        method: 'POST'
      });
      setDryRunReport(dryRunRes.preflight_audit);
      setStep(6);
      
    } catch (err: any) {
      if (err.message && err.message.includes('compatibility')) {
        // Detailed errors returned by backend
        setValidationErrors(err.details?.errors || [err.message]);
      } else {
        setValidationErrors([err.message || 'Validation failed.']);
      }
      setStep(6); // Show errors in validation step
    } finally {
      setLoading(false);
    }
  };

  const handleLockAndStartRun = async () => {
    if (!composedRunSpecId) return;
    setIsSubmitting(true);
    setSubmitError(null);
    
    try {
      // 1. Lock RunSpec to freeze snapshot configuration
      await fetchWithAuth(`/api/v1/runspecs/${composedRunSpecId}/lock`, {
        method: 'POST'
      });
      
      // 2. Trigger background execution
      const runRes = await fetchWithAuth('/api/v1/runs', {
        method: 'POST',
        body: JSON.stringify({
          runspec_id: composedRunSpecId
        })
      });
      
      // Redirect to runs detail page
      router.push(`/runs/${runRes.id}`);
      
    } catch (err: any) {
      setSubmitError(err.message || 'Failed to start evaluation run.');
      setIsSubmitting(false);
    }
  };

  return (
    <Layout activeTab="create-run">
      {/* Step Progress Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '40px', background: 'rgba(31,40,51,0.2)', padding: '15px', borderRadius: '10px' }}>
        {[1, 2, 3, 4, 5, 6, 7].map((s) => (
          <div key={s} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span
              style={{
                width: '30px',
                height: '30px',
                borderRadius: '50%',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                background: step === s ? '#45f3ff' : step > s ? '#34c759' : 'rgba(255,255,255,0.05)',
                color: step >= s ? '#0b0c10' : '#888',
                fontWeight: 600,
                fontSize: '14px',
                border: step === s ? '2px solid #45f3ff' : 'none'
              }}
            >
              {s}
            </span>
            <span style={{ fontSize: '12px', color: step === s ? '#fff' : '#888', fontWeight: step === s ? 600 : 400 }}>
              {s === 1 && 'Mode'}
              {s === 2 && 'Tool & Adapter'}
              {s === 3 && 'Schema'}
              {s === 4 && 'Benchmark'}
              {s === 5 && 'Target & Model'}
              {s === 6 && 'Compatibility'}
              {s === 7 && 'Execute'}
            </span>
          </div>
        ))}
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: '#888' }}>Initializing wizard step...</div>
      ) : (
        <div className="wizard-step-container" style={{ background: 'rgba(31, 40, 51, 0.45)', border: '1px solid rgba(69, 243, 255, 0.1)', borderRadius: '12px', padding: '40px' }}>
          
          {/* STEP 1: Evaluation Mode */}
          {step === 1 && (
            <div>
              <h3 style={{ color: '#fff', fontSize: '20px', margin: '0 0 15px 0' }}>Step 1: Choose Evaluation Mode</h3>
              <p style={{ color: '#888', fontSize: '14px', marginBottom: '30px' }}>
                Define the model testing layout. Requirements are derived dynamically from this mode.
              </p>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '20px', marginBottom: '40px' }}>
                <div
                  style={{ background: 'rgba(11, 12, 16, 0.6)', border: '1px solid #45f3ff', padding: '24px', borderRadius: '12px', cursor: 'pointer' }}
                  onClick={() => setStep(2)}
                >
                  <h4 style={{ margin: '0 0 10px 0', color: '#fff', fontSize: '18px' }}>Standard Run</h4>
                  <p style={{ color: '#888', fontSize: '13px', margin: 0, lineHeight: '1.5' }}>
                    Select an external tool, adapter, model, and benchmark target to run simulated metrics normalization.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* STEP 2: Tool & Adapter */}
          {step === 2 && (
            <div>
              <h3 style={{ color: '#fff', fontSize: '20px', margin: '0 0 20px 0' }}>Step 2: Select External Tool & Adapter</h3>
              
              <div className="form-group">
                <label className="form-label">External Tool Manifest</label>
                <select
                  value={selectedTool}
                  onChange={(e) => setSelectedTool(e.target.value)}
                  className="form-input"
                  style={{ width: '100%', height: '45px', padding: '10px' }}
                >
                  <option value="">-- Choose Tool --</option>
                  {tools.map((t) => <option key={t.id} value={t.manifest_id}>{t.name} ({t.manifest_id})</option>)}
                </select>
              </div>

              <div className="form-group" style={{ marginTop: '20px' }}>
                <label className="form-label">Adapter Manifest</label>
                <select
                  value={selectedAdapter}
                  onChange={(e) => setSelectedAdapter(e.target.value)}
                  className="form-input"
                  style={{ width: '100%', height: '45px', padding: '10px' }}
                >
                  <option value="">-- Choose Adapter --</option>
                  {adapters.map((a) => <option key={a.id} value={a.manifest_id}>{a.name} ({a.manifest_id})</option>)}
                </select>
              </div>

              <div style={{ display: 'flex', gap: '10px', marginTop: '40px' }}>
                <button className="btn-logout" style={{ maxWidth: '120px' }} onClick={() => setStep(1)}>Back</button>
                <button className="btn-primary" style={{ maxWidth: '160px', marginTop: 0 }} disabled={!selectedTool || !selectedAdapter} onClick={() => setStep(3)}>Next</button>
              </div>
            </div>
          )}

          {/* STEP 3: Result Schema */}
          {step === 3 && (
            <div>
              <h3 style={{ color: '#fff', fontSize: '20px', margin: '0 0 20px 0' }}>Step 3: Select Result Normalization Schema</h3>
              
              <div className="form-group">
                <label className="form-label">Result Schema Manifest</label>
                <select
                  value={selectedSchema}
                  onChange={(e) => setSelectedSchema(e.target.value)}
                  className="form-input"
                  style={{ width: '100%', height: '45px', padding: '10px' }}
                >
                  <option value="">-- Choose Result Schema --</option>
                  {schemas.map((s) => <option key={s.id} value={s.manifest_id}>{s.name} ({s.manifest_id})</option>)}
                </select>
              </div>

              <div style={{ display: 'flex', gap: '10px', marginTop: '40px' }}>
                <button className="btn-logout" style={{ maxWidth: '120px' }} onClick={() => setStep(2)}>Back</button>
                <button className="btn-primary" style={{ maxWidth: '160px', marginTop: 0 }} disabled={!selectedSchema} onClick={() => setStep(4)}>Next</button>
              </div>
            </div>
          )}

          {/* STEP 4: Benchmark */}
          {step === 4 && (
            <div>
              <h3 style={{ color: '#fff', fontSize: '20px', margin: '0 0 20px 0' }}>Step 4: Select Evaluation Benchmark</h3>
              
              <div className="form-group">
                <label className="form-label">Benchmark Manifest</label>
                <select
                  value={selectedBenchmark}
                  onChange={(e) => setSelectedBenchmark(e.target.value)}
                  className="form-input"
                  style={{ width: '100%', height: '45px', padding: '10px' }}
                >
                  <option value="">-- Choose Benchmark --</option>
                  {benchmarks.map((b) => <option key={b.id} value={b.manifest_id}>{b.name} ({b.manifest_id})</option>)}
                </select>
              </div>

              <div style={{ display: 'flex', gap: '10px', marginTop: '40px' }}>
                <button className="btn-logout" style={{ maxWidth: '120px' }} onClick={() => setStep(3)}>Back</button>
                <button className="btn-primary" style={{ maxWidth: '160px', marginTop: 0 }} disabled={!selectedBenchmark} onClick={() => setStep(5)}>Next</button>
              </div>
            </div>
          )}

          {/* STEP 5: Target & Model */}
          {step === 5 && (
            <div>
              <h3 style={{ color: '#fff', fontSize: '20px', margin: '0 0 20px 0' }}>Step 5: Select Evaluation Target & Model</h3>
              
              <div className="form-group">
                <label className="form-label">Target Endpoint Manifest</label>
                <select
                  value={selectedTarget}
                  onChange={(e) => setSelectedTarget(e.target.value)}
                  className="form-input"
                  style={{ width: '100%', height: '45px', padding: '10px' }}
                >
                  <option value="">-- Choose Target --</option>
                  {targets.map((t) => <option key={t.id} value={t.manifest_id}>{t.name} ({t.manifest_id})</option>)}
                </select>
              </div>

              <div className="form-group" style={{ marginTop: '20px' }}>
                <label className="form-label">Model Manifest</label>
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  className="form-input"
                  style={{ width: '100%', height: '45px', padding: '10px' }}
                >
                  <option value="">-- Choose Model --</option>
                  {models.map((m) => <option key={m.id} value={m.manifest_id}>{m.name} ({m.manifest_id})</option>)}
                </select>
              </div>

              <div style={{ display: 'flex', gap: '10px', marginTop: '40px' }}>
                <button className="btn-logout" style={{ maxWidth: '120px' }} onClick={() => setStep(4)}>Back</button>
                <button className="btn-primary" style={{ maxWidth: '240px', marginTop: 0 }} disabled={!selectedTarget || !selectedModel} onClick={handleComposeAndValidate}>
                  Compose & Validate
                </button>
              </div>
            </div>
          )}

          {/* STEP 6: Compatibility & Dry-Run validation results */}
          {step === 6 && (
            <div>
              <h3 style={{ color: '#fff', fontSize: '20px', margin: '0 0 20px 0' }}>Step 6: Compatibility Check Audit</h3>
              
              {validationErrors.length > 0 ? (
                <div>
                  <div style={{ color: '#ff3b30', background: 'rgba(255,59,48,0.1)', padding: '15px', borderRadius: '8px', border: '1px solid rgba(255,59,48,0.2)', marginBottom: '30px' }}>
                    <h4 style={{ margin: '0 0 10px 0', fontSize: '15px' }}>Compatibility Violations Detected:</h4>
                    <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '13px', lineHeight: '1.6' }}>
                      {validationErrors.map((err, i) => <li key={i}>{err}</li>)}
                    </ul>
                  </div>
                  
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <button className="btn-logout" style={{ maxWidth: '180px' }} onClick={() => setStep(5)}>Adjust Selections</button>
                  </div>
                </div>
              ) : (
                <div>
                  <div style={{ color: '#34c759', background: 'rgba(52,199,89,0.1)', padding: '15px', borderRadius: '8px', border: '1px solid rgba(52,199,89,0.2)', marginBottom: '30px', fontSize: '14px' }}>
                    ✔ RunSpec is fully compatible and validated! Preflight connection checks are green.
                  </div>
                  
                  {dryRunReport && (
                    <div style={{ background: '#0b0c10', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '8px', padding: '20px', marginBottom: '40px' }}>
                      <h4 style={{ color: '#fff', margin: '0 0 15px 0', fontSize: '15px' }}>Preflight Dry-Run Parameters:</h4>
                      <table style={{ width: '100%', fontSize: '13px', borderCollapse: 'collapse' }}>
                        <tbody>
                          <tr>
                            <td style={{ color: '#888', borderBottom: '1px solid #1f2833', padding: '10px 0' }}>Expected Test Cases:</td>
                            <td style={{ color: '#fff', borderBottom: '1px solid #1f2833', padding: '10px 0' }}><strong>{dryRunReport.expected_samples}</strong></td>
                          </tr>
                          <tr>
                            <td style={{ color: '#888', borderBottom: '1px solid #1f2833', padding: '10px 0' }}>Estimated Duration:</td>
                            <td style={{ color: '#fff', borderBottom: '1px solid #1f2833', padding: '10px 0' }}><strong>{dryRunReport.estimated_duration_seconds} seconds</strong></td>
                          </tr>
                          <tr>
                            <td style={{ color: '#888', padding: '10px 0' }}>Metrics to Extract:</td>
                            <td style={{ color: '#66fcf1', padding: '10px 0' }}><strong>{dryRunReport.metrics_to_extract?.join(', ')}</strong></td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  )}
                  
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <button className="btn-logout" style={{ maxWidth: '120px' }} onClick={() => setStep(5)}>Back</button>
                    <button className="btn-primary" style={{ maxWidth: '240px', marginTop: 0 }} onClick={() => setStep(7)}>Continue to Execution</button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* STEP 7: Lock & Run */}
          {step === 7 && (
            <div>
              <h3 style={{ color: '#fff', fontSize: '20px', margin: '0 0 15px 0' }}>Step 7: Freeze Configuration & Start Run</h3>
              <p style={{ color: '#888', fontSize: '14px', marginBottom: '30px', lineHeight: '1.6' }}>
                Locking the RunSpec freezes and saves immutable snapshots of all manifests in the database. Any future modifications to component files will not affect this run, assuring reproducibility.
              </p>
              
              {submitError && <div className="error-message" style={{ marginBottom: '20px' }}>{submitError}</div>}
              
              <div style={{ display: 'flex', gap: '10px' }}>
                <button className="btn-logout" style={{ maxWidth: '120px' }} disabled={isSubmitting} onClick={() => setStep(6)}>Back</button>
                <button className="btn-primary" style={{ maxWidth: '240px', marginTop: 0 }} disabled={isSubmitting} onClick={handleLockAndStartRun}>
                  {isSubmitting ? 'Launching Run...' : 'Lock Spec & Launch Run'}
                </button>
              </div>
            </div>
          )}

        </div>
      )}
    </Layout>
  );
}
