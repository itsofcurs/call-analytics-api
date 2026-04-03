import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar.jsx';

const navItems = [
  { label: 'Dashboard', to: '/', icon: 'dashboard' },
  { label: 'Insights', to: '/insights', icon: 'analytics' },
  { label: 'Uploads', to: '/uploads', icon: 'cloud_upload' },
  { label: 'Reports', to: '/reports', icon: 'assessment' },
];

const Dashboard = () => (
  <div className="flex min-h-screen">
    <aside className="hidden lg:flex h-screen w-64 fixed left-0 top-0 bg-surface-variant/40 backdrop-blur-xl flex-col py-6 px-4 z-50">
      <div className="flex items-center gap-3 mb-10 px-2">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-container to-secondary-container flex items-center justify-center shadow-lg ai-glow">
          <span className="material-symbols-outlined text-white" style={{ fontVariationSettings: "'FILL' 1" }}>
            psychology
          </span>
        </div>
        <div>
          <h1 className="text-xl font-bold tracking-tight text-white font-headline">Ethereal AI</h1>
          <p className="text-[10px] uppercase tracking-widest text-primary font-bold">Predictive Prism</p>
        </div>
      </div>
      <nav className="flex-1 space-y-2 overflow-y-auto custom-scrollbar">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 font-semibold ${
                isActive
                  ? 'text-white bg-primary-container/30 shadow-[0_0_15px_rgba(15,105,220,0.3)] border-r-2 border-[#0f69dc]'
                  : 'text-slate-400 hover:text-white hover:bg-white/10'
              }`
            }
          >
            <span className="material-symbols-outlined text-primary">{item.icon}</span>
            <span className="font-label">{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="mt-auto px-2">
        <div className="p-4 rounded-xl bg-surface-container-low/50 border border-outline-variant/10">
          <p className="text-xs text-outline mb-2">System Status</p>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-tertiary animate-pulse shadow-[0_0_8px_#4cd7f6]" />
            <span className="text-xs font-medium text-on-surface">Neural Engine Live</span>
          </div>
        </div>
      </div>
    </aside>

    <div className="flex-1 lg:ml-64 bg-background min-h-screen">
      <Navbar />
      <main className="pt-24 pb-12 px-4 lg:px-8 space-y-8">
        <Outlet />
      </main>
    </div>
  </div>
);

export default Dashboard;
