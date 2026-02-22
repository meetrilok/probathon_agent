import { useEffect, useState } from 'react';

import { Dashboard } from './components/Dashboard';
import { IngestionForm } from './components/IngestionForm';
import { InputsChecklist } from './components/InputsChecklist';
import { ValidationPanel } from './components/ValidationPanel';
import { fetchDashboard, fetchRequiredInputs } from './services/api';
import type { DashboardResponse, RequiredInputsResponse } from './types/api';

export default function App() {
  const [inputs, setInputs] = useState<RequiredInputsResponse | null>(null);
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);

  const load = async () => {
    const [inputData, dashboardData] = await Promise.all([fetchRequiredInputs(), fetchDashboard()]);
    setInputs(inputData);
    setDashboard(dashboardData);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <main style={{ maxWidth: 900, margin: '0 auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>Use-Case Intelligence Platform</h1>
      <p>Collect, validate, and visualize enterprise use-case ideas through modular agents.</p>
      <InputsChecklist data={inputs} />
      <IngestionForm onSuccess={load} />
      <ValidationPanel />
      <Dashboard data={dashboard} />
    </main>
  );
}
