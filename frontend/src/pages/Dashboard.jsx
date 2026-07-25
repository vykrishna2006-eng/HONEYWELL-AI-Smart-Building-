import {
  Box,
  Grid,
  Typography,
  Paper,
  Stack,
  Chip,
} from "@mui/material";

import WavingHandIcon from "@mui/icons-material/WavingHand";
import BusinessIcon from "@mui/icons-material/Business";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";

import DashboardLayout from "../layouts/DashboardLayout";
import DashboardCards from "../components/DashboardCards";
import EnergyChart from "../components/EnergyChart";
import ComfortChart from "../components/ComfortChart";
import RecommendationCard from "../components/RecommendationCard";
import PredictionTable from "../components/PredictionTable";

function Dashboard() {

  const today = new Date().toLocaleDateString("en-GB", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <DashboardLayout>

      {/* ---------------- Hero Section ---------------- */}

      <Paper
        elevation={0}
        sx={{
          mb: 4,
          p: 4,
          borderRadius: 5,
          background:
            "linear-gradient(135deg,#2563EB,#06B6D4)",
          color: "white",
          overflow: "hidden",
          position: "relative",
        }}
      >
        <Stack
          direction={{
            xs: "column",
            md: "row",
          }}
          justifyContent="space-between"
          alignItems={{
            xs: "flex-start",
            md: "center",
          }}
          spacing={3}
        >
          <Box>

            <Stack
              direction="row"
              spacing={1}
              alignItems="center"
              mb={2}
            >
              <WavingHandIcon />

              <Typography
                variant="h4"
                fontWeight={700}
              >
                Welcome Back
              </Typography>
            </Stack>

            <Typography
              variant="h6"
              sx={{
                opacity: .95,
              }}
            >
              AI Smart Building Optimization System
            </Typography>

            <Typography
              mt={1}
              sx={{
                opacity: .85,
              }}
            >
              Monitor energy usage, comfort levels,
              predictions and AI recommendations
              in real time.
            </Typography>

          </Box>

          <Stack spacing={2}>

            <Chip
              icon={<CalendarMonthIcon />}
              label={today}
              sx={{
                bgcolor: "rgba(255,255,255,.18)",
                color: "white",
                fontWeight: 600,
              }}
            />

            <Chip
              icon={<BusinessIcon />}
              label="Building Status : Online"
              sx={{
                bgcolor: "#22C55E",
                color: "white",
                fontWeight: 700,
              }}
            />

          </Stack>

        </Stack>
      </Paper>

      {/* ---------------- KPI Cards ---------------- */}

      <DashboardCards />

      {/* ---------------- Charts ---------------- */}

      <Grid container spacing={3} mt={1}>

        <Grid item xs={12} lg={7}>
          <EnergyChart />
        </Grid>

        <Grid item xs={12} lg={5}>
          <ComfortChart />
        </Grid>

      </Grid>

      {/* ---------------- AI Recommendation ---------------- */}

      <Box mt={4}>

        <Typography
          variant="h5"
          fontWeight={700}
          mb={2}
        >
          AI Recommendation
        </Typography>

        <RecommendationCard />

      </Box>

      {/* ---------------- Prediction Table ---------------- */}

      <Box mt={4}>

        <Typography
          variant="h5"
          fontWeight={700}
          mb={2}
        >
          Recent Predictions
        </Typography>

        <PredictionTable />

      </Box>

    </DashboardLayout>
  );
}

export default Dashboard;