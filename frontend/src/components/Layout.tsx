import { useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { getAuthToken, getTenantId, logoutUser } from '../services/api';

interface LayoutProps {
  children: ReactNode;
  activeTab: 'dashboard' | 'registry' | 'create-run' | 'runs' | 'reports';
}

export default function Layout({ children, activeTab }: LayoutProps) {
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
        Loading LabLex...
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="sidebar-logo">LABLEX</div>
        
        <ul className="nav-menu">
          <li className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}>
            <Link href="/">Dashboard</Link>
          </li>
          <li className={`nav-item ${activeTab === 'registry' ? 'active' : ''}`}>
            <Link href="/registry">Registry</Link>
          </li>
          <li className={`nav-item ${activeTab === 'create-run' ? 'active' : ''}`}>
            <Link href="/runs/create">Create Run</Link>
          </li>
          <li className={`nav-item ${activeTab === 'runs' ? 'active' : ''}`}>
            <Link href="/runs">Runs List</Link>
          </li>
        </ul>
        
        <div className="user-profile">
          <div className="user-name">System Administrator</div>
          <div className="user-role">{role ? role.toUpperCase() : 'USER'}</div>
          <button className="btn-logout" onClick={handleLogout}>Log Out</button>
        </div>
      </aside>

      <main className="main-content">
        <div className="header-section">
          <h2 className="page-title">
            {activeTab === 'dashboard' && 'AI Evaluation Control Plane'}
            {activeTab === 'registry' && 'Component Registry'}
            {activeTab === 'create-run' && 'Compose Evaluation Run'}
            {activeTab === 'runs' && 'Evaluation Runs'}
            {activeTab === 'reports' && 'Evaluation Report'}
          </h2>
          <span className="tenant-badge">Tenant ID: {tenantId}</span>
        </div>
        
        {children}
      </main>
      
      <style jsx global>{`
        .nav-item a {
          color: inherit;
          text-decoration: none;
          display: block;
          width: 100%;
          height: 100%;
        }
      `}</style>
    </div>
  );
}
