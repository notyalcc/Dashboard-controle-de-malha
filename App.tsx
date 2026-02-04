import React, { useState, useEffect, useCallback, createContext } from 'react';
import { HashRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import { User, Submission, Notification, BroadcastMessage } from './types';
import { supabase } from './services/supabaseClient';
import { LOGO_URL, LOGO_SVG_BACKUP } from './constants';

import LoginScreen from './screens/LoginScreen';
import DashboardScreen from './screens/DashboardScreen';
import HistoryScreen from './screens/HistoryScreen';
import HistoryDetailScreen from './screens/HistoryDetailScreen';
import ProfileScreen from './screens/ProfileScreen';
import AboutScreen from './screens/AboutScreen';
import AdminPanelScreen from './screens/AdminPanelScreen';
import DefensePlanScreen from './screens/DefensePlanScreen';

export const ThemeContext = createContext({ isDark: false, toggleTheme: () => {} });

const App: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [syncing, setSyncing] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [activeAlert, setActiveAlert] = useState<BroadcastMessage | null>(null);
  const [isDark, setIsDark] = useState(() => localStorage.getItem('theme') !== 'light');

  useEffect(() => {
    const root = window.document.documentElement;
    if (isDark) {
      root.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDark]);

  const toggleTheme = () => setIsDark(!isDark);

  const addNotification = useCallback((message: string, type: Notification['type'] = 'info') => {
    const id = Math.random().toString(36).substring(7);
    setNotifications(prev => [...prev, { id, message, type }]);
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== id));
    }, 4000);
  }, []);

  const fetchActiveAlerts = useCallback(async () => {
    try {
      const { data, error } = await supabase
        .from('messages')
        .select('*')
        .eq('is_active', true)
        .order('created_at', { ascending: false })
        .limit(1);

      if (!error && data && data.length > 0) {
        setActiveAlert(data[0]);
      } else {
        setActiveAlert(null);
      }
    } catch (err) {
      console.error("Erro alertas:", err);
    }
  }, []);

  const fetchSubmissions = useCallback(async () => {
    setSyncing(true);
    try {
      const { data, error } = await supabase
        .from('checklists')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(30);

      if (error) throw error;
      if (data) {
        setSubmissions(data.map(item => ({
          ...item,
          id: String(item.id),
          itens: JSON.parse(item.itens_json || '{}'),
          tipo_registro: 'ENTRADA'
        })));
      }
    } catch (err: any) {
      console.error("Erro sinc:", err);
    } finally {
      setSyncing(false);
    }
  }, []);

  useEffect(() => {
    const savedUser = localStorage.getItem('vigilancia_user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
      fetchSubmissions();
      fetchActiveAlerts();
    }
    const interval = setInterval(() => {
      if (localStorage.getItem('vigilancia_user')) {
        fetchActiveAlerts();
      }
    }, 60000);
    return () => clearInterval(interval);
  }, [fetchSubmissions, fetchActiveAlerts]);

  const handleLogin = (userData: User) => {
    setUser(userData);
    localStorage.setItem('vigilancia_user', JSON.stringify(userData));
    addNotification(`Acesso autorizado: ${userData.name}`, "success");
    fetchSubmissions();
    fetchActiveAlerts();
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('vigilancia_user');
    setSubmissions([]);
    setActiveAlert(null);
    addNotification("Sessão finalizada.", "info");
  };

  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      <Router>
        <div className={`min-h-screen transition-colors duration-500 ${isDark ? 'dark bg-[#020617]' : 'bg-slate-50'}`}>
          {user && (
            <TopBar 
              user={user} 
              syncing={syncing} 
              onRefresh={() => { fetchSubmissions(); fetchActiveAlerts(); }} 
              toggleTheme={toggleTheme} 
              isDark={isDark} 
              onLogout={handleLogout}
            />
          )}

          {user && activeAlert && (
            <div className="max-w-3xl mx-auto px-4 mt-4">
              <div className={`p-5 rounded-4xl border-2 shadow-2xl flex items-start gap-4 transition-all animate-in slide-in-from-top duration-500 ${
                activeAlert.message_type === 'error' ? 'bg-red-600 border-red-400 text-white animate-pulse' :
                activeAlert.message_type === 'warning' ? 'bg-orange-500 border-orange-400 text-white' :
                'bg-blue-700 border-blue-500 text-white'
              }`}>
                <div className="w-12 h-12 rounded-2xl bg-white/20 flex items-center justify-center shrink-0 shadow-inner">
                  <i className={`fas ${activeAlert.message_type === 'error' ? 'fa-triangle-exclamation' : 'fa-bullhorn'} text-xl`}></i>
                </div>
                <div className="flex-1">
                  <p className="text-[9px] font-black uppercase tracking-[0.2em] opacity-80 mb-1">COMUNICADO OFICIAL</p>
                  <p className="text-sm font-bold leading-tight">{activeAlert.content}</p>
                </div>
              </div>
            </div>
          )}
          
          <main className="max-w-3xl mx-auto px-4 pb-32 pt-6">
            <Routes>
              <Route path="/login" element={!user ? <LoginScreen onLogin={handleLogin} /> : <Navigate to="/" />} />
              <Route path="/" element={user ? <DashboardScreen user={user} onAddSubmission={fetchSubmissions} notify={addNotification} /> : <Navigate to="/login" />} />
              <Route path="/history" element={user ? <HistoryScreen submissions={submissions} /> : <Navigate to="/login" />} />
              <Route path="/history/:id" element={user ? <HistoryDetailScreen submissions={submissions} /> : <Navigate to="/login" />} />
              <Route path="/defense-plan" element={user ? <DefensePlanScreen /> : <Navigate to="/login" />} />
              <Route path="/profile" element={user ? <ProfileScreen user={user} setUser={setUser} notify={addNotification} onLogout={handleLogout} /> : <Navigate to="/login" />} />
              <Route path="/about" element={user ? <AboutScreen /> : <Navigate to="/login" />} />
              <Route path="/admin" element={user && (user.role === 'admin' || user.role === 'supervisor') ? <AdminPanelScreen notify={addNotification} /> : <Navigate to="/" />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </main>

          {user && <FloatingNav userRole={user.role} />}

          <div className="fixed top-24 left-4 right-4 z-[100] space-y-3 pointer-events-none">
            {notifications.map(n => (
              <div key={n.id} className={`max-w-sm mx-auto p-4 rounded-3xl shadow-2xl glass border flex items-center gap-4 animate-in slide-in-from-top-4 duration-500 pointer-events-auto ${
                n.type === 'success' ? 'text-green-600 dark:text-green-400 border-green-200/50' :
                n.type === 'error' ? 'text-red-600 dark:text-red-400 border-red-200/50' :
                'text-blue-600 dark:text-blue-400 border-blue-200/50'
              }`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  n.type === 'success' ? 'bg-green-100 dark:bg-green-900/30' : 
                  n.type === 'error' ? 'bg-red-100 dark:bg-red-900/30' : 
                  'bg-blue-100 dark:bg-blue-900/30'
                }`}>
                  <i className={`fas ${n.type === 'success' ? 'fa-check' : n.type === 'error' ? 'fa-xmark' : 'fa-info'} text-xs`}></i>
                </div>
                <span className="text-[10px] font-black uppercase tracking-tight">{n.message}</span>
              </div>
            ))}
          </div>
        </div>
      </Router>
    </ThemeContext.Provider>
  );
};

const TopBar: React.FC<{ user: User; syncing: boolean; onRefresh: () => void; toggleTheme: () => void; isDark: boolean; onLogout: () => void }> = ({ user, syncing, onRefresh, toggleTheme, isDark, onLogout }) => {
  return (
    <header className="sticky top-0 z-50 glass border-b border-slate-200/10 backdrop-blur-xl">
      <div className="max-w-3xl mx-auto px-6 h-20 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white dark:bg-slate-800 rounded-2xl flex items-center justify-center shadow-lg p-1.5 border border-slate-100 dark:border-slate-700 overflow-hidden">
            <img src={LOGO_URL} className="w-full h-full object-contain" onError={(e:any) => e.target.src = LOGO_SVG_BACKUP} />
          </div>
          <div>
            <h1 className="text-[10px] font-black tracking-[0.2em] text-slate-400 dark:text-slate-500 uppercase leading-none">Grupo Macor</h1>
            <p className="text-sm font-extrabold text-[#1D3B6B] dark:text-blue-400 tracking-tight">Material Pro</p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <button onClick={toggleTheme} className="w-10 h-10 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 flex items-center justify-center transition-all active:scale-90 shadow-sm">
            <i className={`fas ${isDark ? 'fa-sun text-amber-500' : 'fa-moon text-blue-600'}`}></i>
          </button>
          <button onClick={onRefresh} className={`w-10 h-10 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 flex items-center justify-center transition-all active:scale-90 ${syncing ? 'animate-spin' : ''}`}>
            <i className="fas fa-sync-alt text-xs"></i>
          </button>
          <button onClick={onLogout} className="w-10 h-10 rounded-2xl bg-red-50 dark:bg-red-900/30 text-red-500 flex items-center justify-center transition-all active:scale-90 border border-red-100 dark:border-red-900/50">
            <i className="fas fa-power-off text-xs"></i>
          </button>
        </div>
      </div>
    </header>
  );
};

const FloatingNav: React.FC<{ userRole: string }> = ({ userRole }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path;
  const isAdmin = userRole === 'admin' || userRole === 'supervisor';

  return (
    <div className="fixed bottom-8 left-0 right-0 z-50 px-6">
      <nav className="max-w-md mx-auto glass border shadow-2xl rounded-5xl h-20 flex items-center justify-around px-2">
        <NavButton active={isActive('/')} icon="fa-clipboard-list" label="Inspeção" onClick={() => navigate('/')} />
        <NavButton active={isActive('/history')} icon="fa-clock-rotate-left" label="Relatórios" onClick={() => navigate('/history')} />
        <NavButton active={isActive('/defense-plan')} icon="fa-shield-halved" label="Plano" onClick={() => navigate('/defense-plan')} />
        {isAdmin && <NavButton active={isActive('/admin')} icon="fa-user-tie" label="Gestão" onClick={() => navigate('/admin')} />}
        <NavButton active={isActive('/about')} icon="fa-circle-info" label="Sistema" onClick={() => navigate('/about')} />
      </nav>
    </div>
  );
};

const NavButton: React.FC<{ active: boolean; icon: string; label: string; onClick: () => void }> = ({ active, icon, label, onClick }) => (
  <button onClick={onClick} className="flex flex-col items-center gap-1 group relative flex-1">
    <div className={`w-14 h-12 rounded-3xl flex items-center justify-center transition-all duration-300 mx-auto ${
      active ? 'bg-[#1D3B6B] dark:bg-blue-600 text-white shadow-xl -translate-y-2' : 'text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300'
    }`}>
      <i className={`fas ${icon} ${active ? 'text-lg' : 'text-xl'}`}></i>
    </div>
    {!active && <span className="text-[7px] font-black uppercase tracking-widest">{label}</span>}
    {active && <div className="absolute -bottom-1 w-1.5 h-1.5 bg-[#1D3B6B] dark:bg-blue-400 rounded-full animate-pulse"></div>}
  </button>
);

export default App;