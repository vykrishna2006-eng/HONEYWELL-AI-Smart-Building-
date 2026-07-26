import { Box, Toolbar, Container } from "@mui/material";
import Navbar from "../components/Navbar";
import Sidebar, { DRAWER_WIDTH } from "../components/Sidebar";

function DashboardLayout({ children }) {
  return (
    <Box sx={{ display: "flex", minHeight: "100vh", bgcolor: "background.default" }}>
      <Navbar />
      <Sidebar />

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          ml: `${DRAWER_WIDTH}px`,
          width: `calc(100% - ${DRAWER_WIDTH}px)`,
          minHeight: "100vh",
        }}
      >
        <Toolbar />
        <Container maxWidth={false} sx={{ py: 4, px: { xs: 2, md: 4 } }}>
          {children}
        </Container>
      </Box>
    </Box>
  );
}

export default DashboardLayout;
