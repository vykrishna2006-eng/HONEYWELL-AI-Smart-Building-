import {
  Drawer, Toolbar, List, ListItemButton,
  ListItemIcon, ListItemText, Box, Typography, Divider,
} from "@mui/material";

import DashboardIcon    from "@mui/icons-material/Dashboard";
import AnalyticsIcon    from "@mui/icons-material/Analytics";
import SmartToyIcon     from "@mui/icons-material/SmartToy";
import SettingsIcon     from "@mui/icons-material/Settings";
import QueryStatsIcon   from "@mui/icons-material/QueryStats";
import BoltIcon         from "@mui/icons-material/Bolt";
import ApartmentIcon    from "@mui/icons-material/Apartment";

import { NavLink } from "react-router-dom";

export const DRAWER_WIDTH = 256;

const menus = [
  { text: "Dashboard",       icon: <DashboardIcon  />, path: "/" },
  { text: "Predictions",     icon: <QueryStatsIcon />, path: "/predictions" },
  { text: "Analytics",       icon: <AnalyticsIcon  />, path: "/analytics" },
  { text: "Recommendations", icon: <SmartToyIcon   />, path: "/recommendations" },
  { text: "Simulation",      icon: <BoltIcon       />, path: "/simulation" },
  { text: "Settings",        icon: <SettingsIcon   />, path: "/settings" },
];

function Sidebar() {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: DRAWER_WIDTH,
          background: "linear-gradient(180deg,#0F172A 0%,#1A2540 100%)",
          color: "white",
          borderRight: "none",
          overflowX: "hidden",
        },
      }}
    >
      {/* Brand */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1.5,
          px: 3,
          py: 2.5,
          background: "rgba(37,99,235,0.15)",
        }}
      >
        <ApartmentIcon sx={{ color: "#06B6D4", fontSize: 28 }} />
        <Box>
          <Typography
            variant="caption"
            sx={{ color: "#94A3B8", letterSpacing: 1.5, textTransform: "uppercase", fontSize: 10 }}
          >
            AI System
          </Typography>
          <Typography variant="subtitle2" sx={{ fontWeight: 700, lineHeight: 1.2 }}>
            Smart Building
          </Typography>
        </Box>
      </Box>

      <Toolbar sx={{ minHeight: "8px !important" }} />

      <Box sx={{ px: 2 }}>
        <Typography
          variant="caption"
          sx={{ color: "#475569", px: 1, letterSpacing: 1.5, textTransform: "uppercase", fontSize: 10 }}
        >
          Navigation
        </Typography>
      </Box>

      <List sx={{ mt: 1, px: 2 }}>
        {menus.map((menu) => (
          <ListItemButton
            key={menu.text}
            component={NavLink}
            to={menu.path}
            end={menu.path === "/"}
            sx={{
              mb: 0.5,
              borderRadius: 3,
              transition: "all 0.2s",
              "&.active": {
                background: "linear-gradient(135deg,#2563EB,#1d4ed8)",
                boxShadow: "0 4px 15px rgba(37,99,235,0.35)",
                "& .MuiListItemIcon-root": { color: "#fff" },
                "& .MuiListItemText-primary": { color: "#fff", fontWeight: 700 },
              },
              "&:not(.active):hover": {
                background: "rgba(255,255,255,0.06)",
              },
            }}
          >
            <ListItemIcon sx={{ color: "#64748B", minWidth: 40 }}>
              {menu.icon}
            </ListItemIcon>
            <ListItemText
              primary={menu.text}
              primaryTypographyProps={{ fontSize: 14, fontWeight: 500, color: "#94A3B8" }}
            />
          </ListItemButton>
        ))}
      </List>

      <Box sx={{ flexGrow: 1 }} />

      <Divider sx={{ borderColor: "rgba(255,255,255,0.06)", mx: 2 }} />

      <Box sx={{ p: 2.5, display: "flex", alignItems: "center", gap: 1 }}>
        <Box
          sx={{
            width: 8, height: 8, borderRadius: "50%",
            bgcolor: "#22C55E", flexShrink: 0,
          }}
          className="pulse-dot"
        />
        <Typography variant="caption" sx={{ color: "#64748B", fontSize: 12 }}>
          System Online
        </Typography>
      </Box>
    </Drawer>
  );
}

export default Sidebar;
