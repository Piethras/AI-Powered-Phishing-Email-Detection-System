import { Shield, Mail, History, ListChecks, MessageSquare, Settings } from "lucide-react";

export const API_BASE = "http://127.0.0.1:5000/api";

export const NAV_ITEMS = [
  { key: "dashboard", label: "Dashboard", icon: Shield },
  { key: "scan", label: "Scan Email", icon: Mail },
  { key: "history", label: "Email History", icon: History },
  { key: "whitelist", label: "Whitelist", icon: ListChecks },
  { key: "feedback", label: "Feedback", icon: MessageSquare },
  { key: "settings", label: "Settings", icon: Settings },
];