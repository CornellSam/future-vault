import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { AnimatePresence } from "framer-motion";
import { WagmiProvider } from "wagmi";
import { RainbowKitProvider } from "@rainbow-me/rainbowkit";
import "@rainbow-me/rainbowkit/styles.css";
import { Layout } from "./components/Layout";
import { HomePage } from "./pages/HomePage";
import { CreatePage } from "./pages/CreatePage";
import { CapsulesPage } from "./pages/CapsulesPage";
import { DashboardPage } from "./pages/DashboardPage";
import { NotFound } from "./pages/NotFound";
import { Toaster } from "./components/ui/toaster";
import { wagmiConfig, queryClient } from "./lib/wagmi";
import "./index.css";

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="create" element={<CreatePage />} />
          <Route path="capsules" element={<CapsulesPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </AnimatePresence>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <WagmiProvider config={wagmiConfig}>
        <RainbowKitProvider>
          <BrowserRouter>
            <AnimatedRoutes />
            <Toaster />
          </BrowserRouter>
        </RainbowKitProvider>
      </WagmiProvider>
    </QueryClientProvider>
  );
}

export default App;
