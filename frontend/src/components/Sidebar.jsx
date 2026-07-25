import {
  Drawer,
  Toolbar,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";

import DashboardIcon from "@mui/icons-material/Dashboard";
import AnalyticsIcon from "@mui/icons-material/Analytics";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import SettingsIcon from "@mui/icons-material/Settings";
import QueryStatsIcon from "@mui/icons-material/QueryStats";
import BoltIcon from "@mui/icons-material/Bolt";

import { NavLink } from "react-router-dom";

const drawerWidth = 250;

const menus = [
  {
    text: "Dashboard",
    icon: <DashboardIcon />,
    path: "/",
  },
  {
    text: "Predictions",
    icon: <QueryStatsIcon />,
    path: "/predictions",
  },
  {
    text: "Analytics",
    icon: <AnalyticsIcon />,
    path: "/analytics",
  },
  {
    text: "Recommendations",
    icon: <SmartToyIcon />,
    path: "/recommendations",
  },
  {
    text: "Simulation",
    icon: <BoltIcon />,
    path: "/simulation",
  },
  {
    text: "Settings",
    icon: <SettingsIcon />,
    path: "/settings",
  },
];

function Sidebar() {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,

        "& .MuiDrawer-paper": {
          width: drawerWidth,
          bgcolor: "#0F172A",
          color: "white",
          borderRight: "none",
        },
      }}
    >
      <Toolbar />

      <List sx={{ mt: 2 }}>
        {menus.map((menu) => (
          <ListItemButton
            key={menu.text}
            component={NavLink}
            to={menu.path}
            sx={{
              mx: 1,
              mb: 1,
              borderRadius: 3,

              "&.active": {
                bgcolor: "#2563EB",
              },

              "&:hover": {
                bgcolor: "#1E293B",
              },
            }}
          >
            <ListItemIcon
              sx={{
                color: "white",
              }}
            >
              {menu.icon}
            </ListItemIcon>

            <ListItemText primary={menu.text} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
}

export default Sidebar;