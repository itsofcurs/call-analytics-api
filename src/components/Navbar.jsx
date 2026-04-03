import React, { useState, useEffect } from 'react';

const Navbar = () => {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [currentDate, setCurrentDate] = useState('');

  useEffect(() => {
    const now = new Date();
    const formatted = new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    }).format(now);
    setCurrentDate(formatted);
  }, []);

  const notifications = [
    { id: 1, text: 'Analysis #12 completed successfully', time: '2m ago' },
    { id: 2, text: 'Critical SOP breach detected in Hindi queue', time: '15m ago' },
    { id: 3, text: 'System load is stable', time: '1h ago' },
  ];

  return (
    <header className="fixed top-0 right-0 w-full lg:w-[calc(100%-16rem)] h-16 bg-surface/80 backdrop-blur-md flex justify-between items-center px-6 lg:px-8 z-40 shadow-[0_20px_50px_rgba(0,26,66,0.3)] border-b border-outline-variant/10">
      <div className="flex items-center gap-4 lg:gap-6 flex-1">
        <h2 className="text-lg font-black text-white font-headline tracking-tight uppercase">
          Ethereal intelligence
        </h2>
        <div className="relative w-64 lg:w-96 group">
          <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline group-focus-within:text-primary transition-colors text-sm">
            search
          </span>
          <input
            type="text"
            placeholder="Search analytics, agents, or transcripts..."
            className="w-full bg-surface-container-low border-none rounded-full py-2 pl-10 pr-4 text-sm focus:ring-1 focus:ring-primary-container text-on-surface placeholder:text-outline/50 transition-all font-body"
          />
        </div>
      </div>

      <div className="flex items-center gap-4 lg:gap-5">
        {/* Date Section */}
        <div className="flex items-center gap-2 bg-surface-container-low px-3 py-1.5 rounded-lg border border-outline-variant/10 shadow-sm">
          <span className="material-symbols-outlined text-tertiary text-sm">calendar_today</span>
          <span className="text-[11px] font-bold text-white uppercase tracking-wider">{currentDate}</span>
        </div>

        {/* Notifications Section */}
        <div className="relative">
          <button 
            onClick={() => { setShowNotifications(!showNotifications); setShowProfile(false); }}
            className={`relative p-2 rounded-full transition-all ${showNotifications ? 'bg-primary/20 text-white' : 'text-outline hover:text-white hover:bg-white/5'}`}
          >
            <span className="material-symbols-outlined">notifications</span>
            <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-primary rounded-full border border-surface shadow-[0_0_10px_#0f69dc]"></span>
          </button>
          
          {showNotifications && (
            <div className="absolute right-0 mt-3 w-80 glass-card rounded-xl shadow-2xl p-4 z-50 border border-outline-variant/20">
              <div className="flex justify-between items-center mb-4 border-b border-outline-variant/10 pb-2">
                <p className="text-xs font-bold text-white uppercase tracking-widest">Recent Activity</p>
                <span className="text-[10px] text-primary cursor-pointer hover:underline">Mark all read</span>
              </div>
              <div className="space-y-3">
                {notifications.map(n => (
                  <div key={n.id} className="p-2 rounded-lg hover:bg-white/5 transition-colors cursor-pointer group">
                    <p className="text-[11px] text-white font-medium group-hover:text-primary transition-colors">{n.text}</p>
                    <p className="text-[9px] text-outline mt-1">{n.time}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Settings Section */}
        <button 
          onClick={() => alert("Settings configuration is currently locked for this hackathon track.")}
          className="p-2 text-outline hover:text-white hover:bg-white/5 rounded-full transition-all"
        >
          <span className="material-symbols-outlined">settings</span>
        </button>

        <div className="hidden lg:block h-8 w-px bg-outline-variant/10" />

        {/* Profile Section */}
        <div className="relative">
          <div 
            onClick={() => { setShowProfile(!showProfile); setShowNotifications(false); }}
            className="flex items-center gap-3 cursor-pointer group p-1 rounded-full hover:bg-white/5 transition-all"
          >
            <img
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuAt6CxEcD9KBqVX74f4gvFh2WXlbVW4iXvinyaecm89723TrQDZq4UbVqrLoktQxsSph96Ug_9LosvejXh-TJjTYxs0Qp-D_dsXMtPJGks9Rysz4Y2K5_UWMAt2BhUPR6HsBEz0M04lnTwKftiSPRKJ5RpBYy3-ZXLbDFlG15jN-FHpngc4a1N9nH1ncuFo_0Uu0r_3UZDseaeJazSQDs-mHcSBmt3_mrTtqHOU4h59Qu8o821Ka7-T1ykFKhGNGN2OWMeO6sXpqmrl"
              alt="User avatar"
              className="w-8 h-8 rounded-full border border-primary-container/30 object-cover shadow-lg"
            />
          </div>

          {showProfile && (
            <div className="absolute right-0 mt-3 w-48 glass-card rounded-xl shadow-2xl overflow-hidden z-50 border border-outline-variant/20">
              <div className="p-4 border-b border-outline-variant/10">
                <p className="text-xs font-bold text-white uppercase tracking-widest">Administrator</p>
                <p className="text-[10px] text-outline truncate">admin@ethereal.ai</p>
              </div>
              <div className="p-2">
                <button className="w-full text-left p-2 text-[11px] text-white hover:bg-white/5 rounded-lg flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm">person</span> Profile
                </button>
                <button className="w-full text-left p-2 text-[11px] text-white hover:bg-white/5 rounded-lg flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm">logout</span> Logout
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
