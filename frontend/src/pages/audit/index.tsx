import { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import { fetchWithAuth } from '../../services/api';

interface AuditLogItem {
  id: string;
  actor_id: string;
  action: string;
  resource_type: string;
  resource_id: string;
  details: Record<string, any>;
  timestamp: string;
}

export default function AuditLogs() {
  const [logs, setLogs] = useState<AuditLogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters state
  const [resourceType, setResourceType] = useState('');
  const [action, setAction] = useState('');
  const [actorId, setActorId] = useState('');
  
  // Pagination
  const [skip, setSkip] = useState(0);
  const [limit] = useState(25);
  const [totalCount, setTotalCount] = useState(0);

  // Modal details state
  const [activeDetails, setActiveDetails] = useState<Record<string, any> | null>(null);

  const fetchLogs = async () => {
    setLoading(true);
    setError(null);
    try {
      let queryParams = `?skip=${skip}&limit=${limit}`;
      if (resourceType) queryParams += `&resource_type=${resourceType}`;
      if (action) queryParams += `&action=${action}`;
      if (actorId) queryParams += `&actor_id=${actorId}`;

      const data = await fetchWithAuth(`/api/v1/audit-logs${queryParams}`);
      setLogs(data.items || []);
      setTotalCount(data.total_count || 0);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch audit logs.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [skip, resourceType, action, actorId]);

  const handleFilterSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSkip(0);
    fetchLogs();
  };

  const handleResetFilters = () => {
    setResourceType('');
    setAction('');
    setActorId('');
    setSkip(0);
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleString();
  };

  return (
    <Layout activeTab="dashboard">
      <div className="audit-logs-container">
        
        {/* Filter Card */}
        <div className="card glass-card">
          <h4 className="card-title-premium">Filter Tenant Activity Logs</h4>
          <form onSubmit={handleFilterSubmit} className="filters-form">
            
            <div className="filter-group">
              <label className="filter-label">Resource Type</label>
              <select 
                value={resourceType} 
                onChange={e => setResourceType(e.target.value)}
                className="filter-select"
              >
                <option value="">All Resources</option>
                <option value="run">Run</option>
                <option value="batch">Batch</option>
                <option value="comparison">Comparison</option>
                <option value="runspec">RunSpec</option>
                <option value="registry">Registry</option>
              </select>
            </div>

            <div className="filter-group">
              <label className="filter-label">Action</label>
              <input 
                type="text" 
                value={action} 
                onChange={e => setAction(e.target.value)} 
                placeholder="e.g. trigger_run"
                className="filter-input"
              />
            </div>

            <div className="filter-group">
              <label className="filter-label">Actor ID</label>
              <input 
                type="text" 
                value={actorId} 
                onChange={e => setActorId(e.target.value)} 
                placeholder="Search actor ID"
                className="filter-input"
              />
            </div>

            <div className="filter-actions">
              <button type="submit" className="btn-filter-submit">Apply</button>
              <button type="button" onClick={handleResetFilters} className="btn-filter-reset">Reset</button>
            </div>

          </form>
        </div>

        {/* Audit Log Table */}
        <div className="card glass-card list-card" style={{ marginTop: '30px' }}>
          <div className="list-header">
            <h4 className="card-title-premium" style={{ margin: 0 }}>Activity Log</h4>
            <span className="total-badge">{totalCount} total entries</span>
          </div>

          {error && <div className="error-box">{error}</div>}

          {loading ? (
            <div className="loader">Loading audit records...</div>
          ) : logs.length === 0 ? (
            <p className="empty-message">No matching activity records found.</p>
          ) : (
            <div className="table-responsive">
              <table className="audit-table">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Actor ID</th>
                    <th>Action</th>
                    <th>Resource Type</th>
                    <th>Resource ID</th>
                    <th>Details</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map(log => (
                    <tr key={log.id}>
                      <td><strong>{formatDate(log.timestamp)}</strong></td>
                      <td><span className="actor-badge">{log.actor_id}</span></td>
                      <td><span className="action-text">{log.action}</span></td>
                      <td><span className="resource-type-badge">{log.resource_type}</span></td>
                      <td><span className="resource-id-text" title={log.resource_id}>{log.resource_id.substring(0, 18)}...</span></td>
                      <td>
                        <button 
                          onClick={() => setActiveDetails(log.details)} 
                          className="btn-view-details"
                        >
                          Inspect JSON
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Pagination Controls */}
              <div className="pagination-controls">
                <button 
                  disabled={skip === 0} 
                  onClick={() => setSkip(Math.max(0, skip - limit))}
                  className="pagination-btn"
                >
                  ◀ Previous
                </button>
                <span className="pagination-info">
                  Showing {skip + 1} - {Math.min(totalCount, skip + limit)} of {totalCount}
                </span>
                <button 
                  disabled={skip + limit >= totalCount} 
                  onClick={() => setSkip(skip + limit)}
                  className="pagination-btn"
                >
                  Next ▶
                </button>
              </div>

            </div>
          )}
        </div>

        {/* Modal for Details Inspection */}
        {activeDetails && (
          <div className="details-modal-overlay" onClick={() => setActiveDetails(null)}>
            <div className="details-modal-card" onClick={e => e.stopPropagation()}>
              <div className="modal-header">
                <h4>Inspect Action Metadata</h4>
                <button onClick={() => setActiveDetails(null)} className="btn-close-modal">✕</button>
              </div>
              <div className="modal-body">
                <pre>{JSON.stringify(activeDetails, null, 2)}</pre>
              </div>
            </div>
          </div>
        )}

      </div>

      <style jsx>{`
        .audit-logs-container {
          display: flex;
          flex-direction: column;
        }
        .glass-card {
          background: var(--card-bg);
          backdrop-filter: blur(12px);
          border: 1px solid var(--border-color);
          border-radius: 16px;
          padding: 24px;
        }
        .card-title-premium {
          font-size: 16px;
          font-weight: 600;
          color: #fff;
          margin-bottom: 20px;
          border-left: 3px solid var(--accent-color);
          padding-left: 10px;
        }
        .filters-form {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) auto;
          gap: 20px;
          align-items: flex-end;
        }
        .filter-group {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .filter-label {
          font-size: 11px;
          font-weight: 600;
          color: #888;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
        .filter-select, .filter-input {
          background: rgba(11, 12, 16, 0.6);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 8px;
          color: #fff;
          padding: 10px 14px;
          font-size: 13px;
          outline: none;
          height: 42px;
          transition: border-color 0.3s;
        }
        .filter-select:focus, .filter-input:focus {
          border-color: var(--accent-color);
        }
        .filter-actions {
          display: flex;
          gap: 10px;
          height: 42px;
        }
        .btn-filter-submit {
          background: var(--accent-color);
          color: #0b0c10;
          border: none;
          font-weight: 600;
          padding: 0 20px;
          border-radius: 8px;
          cursor: pointer;
          font-size: 13px;
        }
        .btn-filter-reset {
          background: rgba(255, 255, 255, 0.05);
          color: #fff;
          border: 1px solid rgba(255, 255, 255, 0.1);
          font-weight: 600;
          padding: 0 16px;
          border-radius: 8px;
          cursor: pointer;
          font-size: 13px;
        }
        .list-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
        }
        .total-badge {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.1);
          color: #888;
          padding: 4px 10px;
          border-radius: 12px;
          font-size: 11px;
        }
        .error-box {
          color: var(--danger-color);
          background: rgba(255, 59, 48, 0.1);
          border: 1px solid rgba(255, 59, 48, 0.2);
          border-radius: 6px;
          padding: 10px;
          margin-bottom: 15px;
          font-size: 13px;
        }
        .loader {
          text-align: center;
          color: var(--accent-color);
          padding: 40px;
          font-size: 14px;
        }
        .empty-message {
          color: #555;
          text-align: center;
          padding: 40px 0;
          font-size: 13px;
        }
        .table-responsive {
          width: 100%;
          overflow-x: auto;
        }
        .audit-table {
          width: 100%;
          border-collapse: collapse;
        }
        .audit-table th, .audit-table td {
          padding: 12px 16px;
          text-align: left;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);
          font-size: 13px;
        }
        .audit-table th {
          background: rgba(11, 12, 16, 0.7);
          color: #888;
          font-weight: 600;
          text-transform: uppercase;
          font-size: 11px;
          letter-spacing: 0.5px;
        }
        .actor-badge {
          background: rgba(255, 255, 255, 0.05);
          padding: 2px 6px;
          border-radius: 4px;
          font-family: monospace;
          color: #ccc;
        }
        .action-text {
          font-weight: 600;
          color: var(--accent-color);
        }
        .resource-type-badge {
          background: rgba(69, 243, 255, 0.08);
          color: var(--accent-color);
          padding: 2px 6px;
          border-radius: 4px;
          font-size: 11px;
          font-weight: 500;
        }
        .resource-id-text {
          font-family: monospace;
          color: #666;
        }
        .btn-view-details {
          background: transparent;
          border: 1px solid rgba(255, 255, 255, 0.1);
          color: #ccc;
          padding: 4px 8px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 11px;
          transition: all 0.2s;
        }
        .btn-view-details:hover {
          border-color: var(--accent-color);
          color: var(--accent-color);
        }
        .pagination-controls {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-top: 20px;
          padding-top: 15px;
          border-top: 1px solid rgba(255, 255, 255, 0.05);
        }
        .pagination-btn {
          background: rgba(255, 255, 255, 0.05);
          color: #fff;
          border: 1px solid rgba(255, 255, 255, 0.1);
          padding: 8px 16px;
          border-radius: 6px;
          font-size: 12px;
          cursor: pointer;
        }
        .pagination-btn:disabled {
          opacity: 0.3;
          cursor: not-allowed;
        }
        .pagination-info {
          font-size: 13px;
          color: #666;
        }
        .details-modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.8);
          backdrop-filter: blur(4px);
          display: flex;
          justify-content: center;
          align-items: center;
          z-index: 1000;
        }
        .details-modal-card {
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: 12px;
          width: 90%;
          max-width: 600px;
          max-height: 80vh;
          display: flex;
          flex-direction: column;
          box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }
        .modal-header {
          padding: 16px 20px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .modal-header h4 {
          margin: 0;
          color: #fff;
        }
        .btn-close-modal {
          background: transparent;
          border: none;
          color: #888;
          font-size: 18px;
          cursor: pointer;
        }
        .btn-close-modal:hover {
          color: #fff;
        }
        .modal-body {
          padding: 20px;
          overflow-y: auto;
        }
        .modal-body pre {
          background: #000;
          padding: 15px;
          border-radius: 6px;
          font-family: monospace;
          font-size: 12px;
          color: var(--success-color);
          margin: 0;
          white-space: pre-wrap;
          word-break: break-all;
        }
      `}</style>
    </Layout>
  );
}
