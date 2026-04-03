import { Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard.jsx';
import Home from './pages/Home.jsx';
import Insights from './pages/Insights.jsx';
import Uploads from './pages/Uploads.jsx';
import Reports from './pages/Reports.jsx';

function App() {
  return (
    <div className="min-h-screen bg-background text-on-background">
      <Routes>
        <Route path="/" element={<Dashboard />}>
          <Route index element={<Home />} />
          <Route path="insights" element={<Insights />} />
          <Route path="uploads" element={<Uploads />} />
          <Route path="reports" element={<Reports />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
