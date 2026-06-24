import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../components/Layout';
import { fetchWithAuth } from '../../services/api';

interface ManifestDetail {
  id: string;
  manifest_id: string;
  kind: string;
  name: string;
  schema_version: string;
  manifest_version: string;
  deprecated: boolean;
  content: any;
  created_at: string;
  updated_at: string;
}

export default function RegistryDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [manifest, setManifest] = useState<ManifestDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deprecateLoading, setDeprecateLoading] = useState(false);

  const loadManifest = async () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      // First fetch the manifest content
      const data = await fetchWithAuth(`/api/v1/manifests/${id}`);
      
      // We wrap the raw JSON into our display object
      setManifest({
        id: id as string,
        manifest_id: data.id,
        kind: data.kind,
        name: data.name,
        schema_version: data.schema_version,
        manifest_version: data.manifest_version,
        deprecated: data.deprecated || false,
        content: data,
        created_at: data.created_at || new Date().toISOString(),
        updated_at: data.updated_at || new Date().toISOString()
      });
    } catch (err: any) {
      setError(err.message || 'Failed to load component details.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (router.isReady) {
      loadManifest();
    }
  }, [id, router.isReady]);

  const handleDeprecate = async () => {
    if (!confirm('Are you sure you want to deprecate this component? Locked RunSpecs will still be able to use its snapshot, but new runs cannot select it.')) {
      return;
    }
    
    setDeprecateLoading(true);
    try {
      await fetchWithAuth(`/api/v1/manifests/${id}`, {
        method: 'DELETE'
      });
      loadManifest(); // reload status
    } catch (err: any) {
      alert(err.message || 'Failed to deprecate manifest.');
    } finally {
      setDeprecateLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout activeTab="registry">
        <div style={{ textAlign: 'center', padding: '40px', color: '#888' }}>Loading component details...</div>
      </Layout>
    );
  }

  if (error || !manifest) {
    return (
      <Layout activeTab="registry">
        <div className="error-message" style={{ marginBottom: '20px' }}>{error || 'Component not found.'}</div>
        <button className="btn-logout" style={{ maxWidth: '150px' }} onClick={() => router.push('/registry')}>Back to Registry</button>
      </Layout>
    );
  }

  return (
    <Layout activeTab="registry">
      <div style={{ marginBottom: '20px' }}>
        <button
          onClick={() => router.push('/registry')}
          style={{
            background: 'transparent',
            border: 'none',
            color: '#66fcf1',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: 500,
            display: 'flex',
            alignItems: 'center',
            gap: '5px',
            padding: 0,
            marginBottom: '20px'
          }}
        >
          &larr; Back to Component Registry
        </button>
      </div>

      <div
        className="detail-header"
        style={{
          background: 'rgba(31, 40, 51, 0.45)',
          border: '1px solid rgba(69, 243, 255, 0.1)',
          borderRadius: '12px',
          padding: '24px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '30px'
        }}
      >
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
            <span
              style={{
                fontSize: '10px',
                textTransform: 'uppercase',
                fontWeight: 700,
                color: '#66fcf1',
                background: 'rgba(102, 252, 241, 0.1)',
                padding: '4px 8px',
                borderRadius: '10px'
              }}
            >
              {manifest.kind.replace('_', ' ')}
            </span>
            {manifest.deprecated ? (
              <span style={{ fontSize: '10px', fontWeight: 700, color: '#ff3b30', background: 'rgba(255,59,48,0.1)', padding: '4px 8px', borderRadius: '10px', border: '1px solid rgba(255,59,48,0.2)' }}>
                DEPRECATED
              </span>
            ) : (
              <span style={{ fontSize: '10px', fontWeight: 700, color: '#34c759', background: 'rgba(52,199,89,0.1)', padding: '4px 8px', borderRadius: '10px', border: '1px solid rgba(52,199,89,0.2)' }}>
                ACTIVE
              </span>
            )}
          </div>
          <h3 style={{ margin: '0 0 8px 0', fontSize: '24px', color: '#fff' }}>{manifest.name}</h3>
          <div style={{ fontSize: '13px', color: '#888' }}>
            Internal ID: <code style={{ color: '#45f3ff' }}>{manifest.manifest_id}</code> | Schema: {manifest.schema_version} | Version: {manifest.manifest_version}
          </div>
        </div>

        {!manifest.deprecated && (
          <button
            onClick={handleDeprecate}
            disabled={deprecateLoading}
            style={{
              background: 'rgba(255, 59, 48, 0.1)',
              color: '#ff3b30',
              border: '1px solid rgba(255, 59, 48, 0.3)',
              borderRadius: '8px',
              padding: '10px 20px',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.3s'
            }}
            onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 59, 48, 0.2)'}
            onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255, 59, 48, 0.1)'}
          >
            {deprecateLoading ? 'Deprecating...' : 'Deprecate Component'}
          </button>
        )}
      </div>

      <div className="json-viewer-section">
        <h4 style={{ color: '#fff', fontSize: '16px', margin: '0 0 15px 0' }}>Manifest Specification (JSON)</h4>
        <pre
          style={{
            background: '#0b0c10',
            border: '1px solid rgba(255, 255, 255, 0.05)',
            borderRadius: '12px',
            padding: '24px',
            overflowX: 'auto',
            fontFamily: 'monospace',
            fontSize: '13px',
            color: '#a9f5f2',
            lineHeight: '1.6',
            boxShadow: 'inset 0 4px 12px rgba(0,0,0,0.5)'
          }}
        >
          {JSON.stringify(manifest.content, null, 2)}
        </pre>
      </div>
    </Layout>
  );
}
