import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Clock, Lock, Unlock, Shield, Sparkles, ArrowRight } from "lucide-react";
import { PageTransition, FadeIn, StaggerContainer, StaggerItem } from "../components/PageTransition";

const features = [
  {
    icon: Lock,
    title: "Time-Locked Security",
    description: "Your messages remain encrypted until the specified unlock date arrives.",
  },
  {
    icon: Shield,
    title: "FHE Encryption",
    description: "Fully Homomorphic Encryption ensures your data stays private on-chain.",
  },
  {
    icon: Unlock,
    title: "Guaranteed Reveal",
    description: "Messages automatically become decryptable when the time comes.",
  },
];

export function HomePage() {
  return (
    <PageTransition>
      <div className="relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-500/20 rounded-full blur-3xl animate-pulse delay-1000" />
        </div>

        {/* Hero Section */}
        <section className="container mx-auto px-4 py-20 md:py-32">
          <div className="max-w-4xl mx-auto text-center">
            <FadeIn>
              <motion.div
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-8"
                whileHover={{ scale: 1.02 }}
              >
                <Sparkles className="w-4 h-4 text-primary" />
                <span className="text-sm text-primary font-medium">
                  Powered by Zama FHEVM
                </span>
              </motion.div>
            </FadeIn>

            <FadeIn delay={0.1}>
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6">
                <span className="text-gradient">Future Vault</span>
              </h1>
            </FadeIn>

            <FadeIn delay={0.2}>
              <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-2xl mx-auto">
                Create encrypted time capsules that reveal their secrets only when the time is right.
              </p>
            </FadeIn>

            <FadeIn delay={0.3}>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Link to="/create">
                  <motion.button
                    className="flex items-center gap-2 px-8 py-4 rounded-xl bg-primary text-primary-foreground font-semibold text-lg glow-primary"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Clock className="w-5 h-5" />
                    Create Capsule
                    <ArrowRight className="w-5 h-5" />
                  </motion.button>
                </Link>
                <Link to="/capsules">
                  <motion.button
                    className="flex items-center gap-2 px-8 py-4 rounded-xl bg-secondary text-foreground font-semibold text-lg border border-border"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    View Capsules
                  </motion.button>
                </Link>
              </div>
            </FadeIn>
          </div>

          {/* Animated Vault Icon */}
          <FadeIn delay={0.4}>
            <div className="mt-16 flex justify-center">
              <motion.div
                className="relative w-48 h-48 md:w-64 md:h-64"
                animate={{ y: [0, -10, 0] }}
                transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
              >
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-purple-500/30 to-pink-500/30 blur-2xl" />
                <div className="relative w-full h-full rounded-3xl bg-card border border-border/50 flex items-center justify-center glow-primary">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 20, ease: "linear" }}
                  >
                    <Clock className="w-20 h-20 md:w-28 md:h-28 text-primary" />
                  </motion.div>
                </div>
              </motion.div>
            </div>
          </FadeIn>
        </section>

        {/* Features Section */}
        <section className="container mx-auto px-4 py-20">
          <FadeIn>
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
              How It Works
            </h2>
          </FadeIn>

          <StaggerContainer className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {features.map((feature, index) => (
              <StaggerItem key={index}>
                <motion.div
                  className="glass-card rounded-2xl p-8 text-center h-full"
                  whileHover={{ y: -5, scale: 1.02 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <motion.div
                    className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-6"
                    whileHover={{ rotate: 10 }}
                  >
                    <feature.icon className="w-8 h-8 text-primary" />
                  </motion.div>
                  <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </motion.div>
              </StaggerItem>
            ))}
          </StaggerContainer>
        </section>

        {/* CTA Section */}
        <section className="container mx-auto px-4 py-20">
          <FadeIn>
            <motion.div
              className="glass-card rounded-3xl p-12 text-center max-w-3xl mx-auto"
              whileHover={{ scale: 1.01 }}
            >
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Ready to Lock Your Message?
              </h2>
              <p className="text-muted-foreground mb-8 text-lg">
                Create your first time capsule and experience the power of FHE encryption.
              </p>
              <Link to="/create">
                <motion.button
                  className="px-8 py-4 rounded-xl bg-primary text-primary-foreground font-semibold text-lg glow-primary"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Get Started
                </motion.button>
              </Link>
            </motion.div>
          </FadeIn>
        </section>
      </div>
    </PageTransition>
  );
}
