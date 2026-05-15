import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Header from './components/layout/Header';
import MobileNav from './components/layout/MobileNav';
import Footer from './components/layout/Footer';
import Home from './pages/Home';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Dashboard from './pages/Dashboard';
import Health from './pages/Health';
import Activities from './pages/Activities';
import Expenses from './pages/Expenses';
import Investments from './pages/Investments';
import Travel from './pages/Travel';
import Calendar from './pages/Calendar';
import Finance from './pages/Finance';
import Technology from './pages/Technology';
import Learning from './pages/Learning';
import Reports from './pages/Reports';
import UserManagement from './pages/admin/UserManagement';

function RequireAuth({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function RequireAdmin({ children }) {
  const { isAdmin } = useAuth();
  return isAdmin ? children : <Navigate to="/" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen bg-gray-50">
        <Header />
        <main className="flex-1 pb-20 md:pb-0">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/health" element={<Health />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/travel" element={<Travel />} />
            <Route path="/calendar" element={<Calendar />} />
            <Route path="/finance" element={<Finance />} />
            <Route path="/technology" element={<Technology />} />
            <Route path="/learning" element={<Learning />} />
            <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
            <Route path="/expenses" element={<RequireAuth><Expenses /></RequireAuth>} />
            <Route path="/investments" element={<RequireAuth><Investments /></RequireAuth>} />
            <Route path="/reports" element={<RequireAuth><Reports /></RequireAuth>} />
            <Route path="/admin/users" element={<RequireAuth><RequireAdmin><UserManagement /></RequireAdmin></RequireAuth>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <MobileNav />
        <Footer />
      </div>
    </BrowserRouter>
  );
}
