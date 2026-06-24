import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { getAuthToken, getTenantId, logoutUser } from '../services/api';

export default function Home() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [tenantId, setTenantId] = useState<string | null>(null);
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    const token = getAuthToken();
    if (!token) {
      router.push('/login');
    } else {
      setTenantId(getTenantId());
      setRole(localStorage.getItem('lablex_role'));
      setLoading(false);
    }
  }, [router]);

  const handleLogout = () => {
    logoutUser();
    router.push('/login');
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: '#0b0c10', color: '#c5c6c7' }}>
        Loading dashboard...
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="sidebar-logo">LABLEX</div>
        <ul className="nav-menu">
          <li className="nav-item active">Dashboard</li>
          <li className="nav-item">External Tools</li>
          <li className="nav-item">Benchmarks</li>
          <li className="nav-item">Evaluation Runs</li>
          <li className="nav-item">Reports</li>
        </ul>
        <div className="user-profile">
          <div className="user-name">System Administrator</div>
          <div className="user-role">{role ? role.toUpperCase() : 'USER'}</div>
          <button className="btn-logout" onClick={handleLogout}>Log Out</button>
        </div>
      </aside>

      <main className="main-content">
        <div className="header-section">
          <h2 className="page-title">AI Evaluation Control Plane</h2>
          <span className="tenant-badge">Tenant ID: {tenantId}</span>
        </div>

        <div className="dashboard-card">
          <h3 className="card-title">Welcome to LabLex Foundation</h3>
          <p className="card-description">
            Your multi-tenant control plane skeleton is fully bootstrapped. FastAPI backend services, Next.js UI dashboard, Alembic migrations, and local Postgres, Redis, and MinIO components are configured and running.
          </p>
          <p style={{ color: '#888', fontSize: '13px', margin: 0 }}>
            No external evaluation engines or CLI adapters are active yet, as governed by the 22 Production Gates (§43).
          </p>
        </div>
      </main>
    </div>
  );
}
