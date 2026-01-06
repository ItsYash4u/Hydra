import React from 'react';
import { Home, Activity, Droplets, Settings, Bell, Search, User } from 'lucide-react';

const SidebarItem = ({ icon: Icon, label, active }) => (
    <div className={`flex items-center p-3 mb-2 rounded-xl cursor-pointer transition-all ${active ? 'bg-agri-primary text-white shadow-lg shadow-agri-primary/30' : 'text-gray-500 hover:bg-white hover:text-agri-primary'}`}>
        <Icon size={20} />
        <span className="ml-3 font-medium">{label}</span>
    </div>
);

const Layout = ({ children }) => {
    return (
        <div className="flex h-screen bg-agri-bg overflow-hidden">
            {/* Sidebar */}
            <aside className="w-64 bg-white m-4 rounded-2xl shadow-sm flex flex-col p-6">
                <div className="flex items-center mb-10">
                    <div className="w-10 h-10 bg-agri-primary rounded-xl flex items-center justify-center text-white mr-3 shadow-lg shadow-agri-primary/30">
                        <Droplets size={24} />
                    </div>
                    <span className="font-bold text-xl text-gray-800">Greenhouse</span>
                </div>

                <nav className="flex-1">
                    <SidebarItem icon={Home} label="Dashboard" active />
                    <SidebarItem icon={Activity} label="Analytics" />
                    <SidebarItem icon={Droplets} label="Irrigation" />
                    <SidebarItem icon={Settings} label="Settings" />
                </nav>

                <div className="mt-auto pt-6 border-t border-gray-100">
                    <div className="flex items-center p-2 rounded-xl bg-agri-bg/50">
                        <div className="w-8 h-8 rounded-full bg-agri-secondary text-white flex items-center justify-center text-xs font-bold">
                            JD
                        </div>
                        <div className="ml-3">
                            <p className="text-sm font-bold text-gray-800">John Doe</p>
                            <p className="text-xs text-gray-500">Farm Operator</p>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col overflow-hidden">
                {/* Header */}
                <header className="h-20 flex items-center justify-between px-8">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-800">Greenhouse Alpha</h1>
                        <p className="text-sm text-gray-500">Real-time monitoring & automation</p>
                    </div>

                    <div className="flex items-center space-x-4">
                        <div className="bg-white p-2 rounded-full shadow-sm text-gray-400 hover:text-agri-primary cursor-pointer transition-colors">
                            <Search size={20} />
                        </div>
                        <div className="bg-white p-2 rounded-full shadow-sm text-gray-400 hover:text-agri-primary cursor-pointer transition-colors relative">
                            <Bell size={20} />
                            <span className="absolute top-0 right-0 w-2.5 h-2.5 bg-agri-alert rounded-full border-2 border-white"></span>
                        </div>
                        <div className="bg-white p-2 rounded-full shadow-sm text-agri-primary font-bold cursor-pointer">
                            JD
                        </div>
                    </div>
                </header>

                {/* Scrollable Content */}
                <div className="flex-1 overflow-y-auto px-8 pb-8">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;
