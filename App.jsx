import React, { useState, useEffect, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Analyze from './pages/Analyze';
import HistoryPage from './pages/HistoryPage';
import ModelPage from './pages/ModelPage';
import { fetchDashboardData, fetchHistory, analyzeEmail, analyzeEml } from './services/api';

export default function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState(null);
  const [historyRows, setHistoryRows] = useState([]);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [emailForm, setEmailForm] = useState({ sender: '', subject: '', body: '' });
  const [loading, setLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(true);

  const loadData = useCallback(async () => {
    try {
      const [dash, hist] = await Promise.all([fetchDashboardData(), fetchHistory()]);
      setDashboardData(dash);
      setHistoryRows(hist);
      setIsConnected(true);
    } catch (err) {
      console.error('API connection failed:', err);
      setIsConnected(false);
      setDashboardData({ error: 'Cannot connect to backend server' });
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const result = await analyzeEmail(emailForm);
      setAnalysisResult(result);
      await loadData();
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      alert(`Analysis error: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadEml = async (file) => {
    setLoading(true);
    try {
      const result = await analyzeEml(file);
      setAnalysisResult(result);
      await loadData();
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      alert(`Upload error: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar currentPage={currentPage} onSelectPage={setCurrentPage} />
      <main className="main-content">
        <Header currentPage={currentPage} isConnected={isConnected} />
        <div className="page-body">
          {currentPage === 'dashboard' && (
            <Dashboard data={dashboardData} onNavigateToAnalyze={() => setCurrentPage('analyze')} />
          )}
          {currentPage === 'analyze' && (
            <Analyze
              form={emailForm}
              setForm={setEmailForm}
              onAnalyze={handleAnalyze}
              onUploadEml={handleUploadEml}
              loading={loading}
              result={analysisResult}
            />
          )}
          {currentPage === 'history' && <HistoryPage rows={historyRows} />}
          {currentPage === 'model' && <ModelPage />}
        </div>
      </main>
    </div>
  );
}
