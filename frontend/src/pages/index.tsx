import Layout from '../components/Layout';

export default function Home() {
  return (
    <Layout activeTab="dashboard">
      <div className="dashboard-card">
        <h3 className="card-title">Welcome to LabLex AI Control Plane</h3>
        <p className="card-description">
          Your multi-tenant control plane is fully operational. FastAPI backend services, Next.js UI dashboard, Alembic migrations, and local PostgreSQL, Redis, and MinIO components are configured.
        </p>
        <p style={{ color: '#888', fontSize: '13px', margin: 0, lineHeight: '1.6' }}>
          Registered components and evaluation runs can be composed and executed dynamically via the Component Registry and Create Run Wizard.
        </p>
      </div>
    </Layout>
  );
}
