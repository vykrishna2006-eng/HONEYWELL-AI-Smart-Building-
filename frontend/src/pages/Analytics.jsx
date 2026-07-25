import {
  Box,
  Grid,
  Paper,
  Typography,
  Stack,
  Chip,
  LinearProgress,
} from "@mui/material";

import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import BoltIcon from "@mui/icons-material/Bolt";
import ThermostatIcon from "@mui/icons-material/Thermostat";
import SavingsIcon from "@mui/icons-material/Savings";
import AnalyticsIcon from "@mui/icons-material/Analytics";

import DashboardLayout from "../layouts/DashboardLayout";

import EnergyChart from "../components/EnergyChart";
import ComfortChart from "../components/ComfortChart";

function Analytics() {

  const analytics = [
    {
      title: "Energy Efficiency",
      value: "91%",
      icon: <BoltIcon sx={{ fontSize: 42 }} />,
      color: "#2563EB",
      progress: 91,
    },
    {
      title: "Comfort Index",
      value: "94%",
      icon: <ThermostatIcon sx={{ fontSize: 42 }} />,
      color: "#22C55E",
      progress: 94,
    },
    {
      title: "Energy Savings",
      value: "18%",
      icon: <SavingsIcon sx={{ fontSize: 42 }} />,
      color: "#F59E0B",
      progress: 18,
    },
    {
      title: "System Accuracy",
      value: "97%",
      icon: <AnalyticsIcon sx={{ fontSize: 42 }} />,
      color: "#8B5CF6",
      progress: 97,
    },
  ];

  return (

    <DashboardLayout>

      {/* Header */}

      <Box mb={4}>

        <Typography
          variant="h4"
          fontWeight={700}
        >
          Analytics Dashboard
        </Typography>

        <Typography
          color="text.secondary"
          mt={1}
        >
          Monitor building performance,
          energy efficiency and AI insights.
        </Typography>

      </Box>

      {/* KPI Cards */}

      <Grid container spacing={3}>

        {analytics.map((item) => (

          <Grid
            item
            xs={12}
            md={6}
            xl={3}
            key={item.title}
          >

            <Paper
              elevation={0}
              sx={{
                p: 3,
                borderRadius: 5,
                border: "1px solid #E2E8F0",
                background:
                  "linear-gradient(145deg,#ffffff,#f8fafc)",
              }}
            >

              <Stack
                direction="row"
                justifyContent="space-between"
                alignItems="center"
              >

                <Box>

                  <Typography
                    color="text.secondary"
                  >
                    {item.title}
                  </Typography>

                  <Typography
                    variant="h3"
                    fontWeight={700}
                    mt={1}
                  >
                    {item.value}
                  </Typography>

                </Box>

                <Box
                  sx={{
                    color: item.color,
                  }}
                >
                  {item.icon}
                </Box>

              </Stack>

              <Box mt={3}>

                <LinearProgress
                  variant="determinate"
                  value={item.progress}
                  sx={{
                    height: 8,
                    borderRadius: 20,

                    "& .MuiLinearProgress-bar": {
                      backgroundColor: item.color,
                    },
                  }}
                />

              </Box>

            </Paper>

          </Grid>

        ))}

      </Grid>

      {/* Charts */}

      <Grid
        container
        spacing={3}
        mt={2}
      >

        <Grid item xs={12} lg={7}>
          <EnergyChart />
        </Grid>

        <Grid item xs={12} lg={5}>
          <ComfortChart />
        </Grid>

      </Grid>

      {/* AI Insights */}

      <Paper
        elevation={0}
        sx={{
          mt: 4,
          p: 4,
          borderRadius: 5,
          border: "1px solid #E2E8F0",
          background:
            "linear-gradient(145deg,#ffffff,#f8fafc)",
        }}
      >

        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >

          <Typography
            variant="h5"
            fontWeight={700}
          >
            AI Performance Insights
          </Typography>

          <Chip
            icon={<TrendingUpIcon />}
            label="Excellent"
            color="success"
          />

        </Stack>

        <Typography
          mt={3}
          color="text.secondary"
          lineHeight={2}
        >
          The AI prediction engine indicates that the building is
          operating with high efficiency. Energy consumption remains
          stable while occupant comfort stays above the desired
          threshold. Current optimisation strategies are expected to
          reduce overall HVAC energy usage by approximately 18% without
          affecting indoor comfort.
        </Typography>

      </Paper>

    </DashboardLayout>

  );

}

export default Analytics;