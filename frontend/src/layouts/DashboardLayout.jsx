import { Box, Toolbar, Container } from "@mui/material";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

const drawerWidth = 250;

function DashboardLayout({ children }) {
  return (
    <Box
      sx={{
        display: "flex",
        minHeight: "100vh",
        bgcolor:"background.default",
      }}
    >
      {/* Top Navigation */}
      <Navbar />

      {/* Left Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          ml: `${drawerWidth}px`,
          width: `calc(100% - ${drawerWidth}px)`,
          transition: "all 0.3s ease",
        }}
      >
        {/* Space below AppBar */}
        <Toolbar />

        <Container
          maxWidth={false}
          sx={{
            py: 4,
            px: {
              xs: 2,
              md: 4,
            },
          }}
        >
          {children}
        </Container>
      </Box>
    </Box>
  );
}

export default DashboardLayout;