import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { Menu, X, Clock, LayoutDashboard, PlusCircle, Archive } from "lucide-react";
import { ConnectButton } from "@rainbow-me/rainbowkit";
import { cn } from "../lib/utils";

const navItems = [
  { path: "/", label: "Home", icon: Clock },
  { path: "/create", label: "Create", icon: PlusCircle },
  { path: "/capsules", label: "Capsules", icon: Archive },
  { path: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
];

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  return (
    <header className="sticky top-0 z-50 glass-card border-b border-border/50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <motion.div
              className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center"
              whileHover={{ scale: 1.05, rotate: 5 }}
              whileTap={{ scale: 0.95 }}
            >
              <Clock className="w-6 h-6 text-white" />
            </motion.div>
            <span className="text-xl font-bold text-gradient hidden sm:block">
              Future Vault
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path;
              const Icon = item.icon;
              
              return (
                <Link key={item.path} to={item.path}>
                  <motion.div
                    className={cn(
                      "flex items-center gap-2 px-4 py-2 rounded-lg transition-colors relative",
                      isActive
                        ? "text-primary"
                        : "text-muted-foreground hover:text-foreground"
                    )}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="font-medium">{item.label}</span>
                    {isActive && (
                      <motion.div
                        className="absolute inset-0 bg-primary/10 rounded-lg -z-10"
                        layoutId="activeNav"
                        transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                      />
                    )}
                  </motion.div>
                </Link>
              );
            })}
          </nav>

          {/* Wallet Button */}
          <div className="flex items-center gap-4">
            <ConnectButton />

            {/* Mobile Menu Button */}
            <button
              className="md:hidden p-2 rounded-lg hover:bg-secondary"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <AnimatedMobileMenu
          isOpen={mobileMenuOpen}
          items={navItems}
          currentPath={location.pathname}
          onClose={() => setMobileMenuOpen(false)}
        />
      </div>
    </header>
  );
}

function AnimatedMobileMenu({
  isOpen,
  items,
  currentPath,
  onClose,
}: {
  isOpen: boolean;
  items: typeof navItems;
  currentPath: string;
  onClose: () => void;
}) {
  return (
    <motion.div
      initial={false}
      animate={isOpen ? { height: "auto", opacity: 1 } : { height: 0, opacity: 0 }}
      transition={{ duration: 0.3, ease: "easeInOut" }}
      className="md:hidden overflow-hidden"
    >
      <nav className="py-4 space-y-2">
        {items.map((item, index) => {
          const isActive = currentPath === item.path;
          const Icon = item.icon;
          
          return (
            <motion.div
              key={item.path}
              initial={{ x: -20, opacity: 0 }}
              animate={isOpen ? { x: 0, opacity: 1 } : { x: -20, opacity: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Link
                to={item.path}
                onClick={onClose}
                className={cn(
                  "flex items-center gap-3 px-4 py-3 rounded-lg transition-colors",
                  isActive
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-secondary"
                )}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            </motion.div>
          );
        })}
      </nav>
    </motion.div>
  );
}
