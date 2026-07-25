import {
  Grid,
  Paper,
  Typography,
  Box,
  LinearProgress,
} from "@mui/material";

import BoltIcon from "@mui/icons-material/Bolt";
import ThermostatIcon from "@mui/icons-material/Thermostat";
import SavingsIcon from "@mui/icons-material/Savings";
import AnalyticsIcon from "@mui/icons-material/Analytics";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";

import useDashboard from "../hooks/useDashboard";
import Loading from "./Loading";

function DashboardCards() {

  const { dashboard, loading } = useDashboard();

  if (loading) {
    return <Loading />;
  }

  const cards = [
    {
      title: "Average Energy",
      value: dashboard?.average_energy_prediction ?? 0,
      unit: "kWh",
      icon: <BoltIcon sx={{ fontSize: 40 }} />,
      colour: "#2563EB",
      progress: 78,
      subtitle: "Energy Consumption",
    },
    {
      title: "Comfort Score",
      value: dashboard?.average_comfort_score ?? 0,
      unit: "%",
      icon: <ThermostatIcon sx={{ fontSize: 40 }} />,
      colour: "#22C55E",
      progress: 92,
      subtitle: "Occupant Comfort",
    },
    {
      title: "Expected Savings",
      value: dashboard?.average_expected_savings ?? 0,
      unit: "%",
      icon: <SavingsIcon sx={{ fontSize: 40 }} />,
      colour: "#F59E0B",
      progress: 66,
      subtitle: "Potential Savings",
    },
    {
      title: "Predictions",
      value: dashboard?.total_predictions ?? 0,
      unit: "",
      icon: <AnalyticsIcon sx={{ fontSize: 40 }} />,
      colour: "#8B5CF6",
      progress: 100,
      subtitle: "ML Predictions",
    },
  ];

  return (
    <Grid container spacing={3}>

      {cards.map((card) => (

        <Grid
          item
          xs={12}
          sm={6}
          xl={3}
          key={card.title}
        >

          <Paper
            elevation={0}
            sx={{
              p: 3,
              borderRadius: 5,
              height: 220,
              overflow: "hidden",
              position: "relative",

              background:
                "linear-gradient(145deg,#ffffff,#f8fafc)",

              border: "1px solid #E2E8F0",

              transition: ".35s",

              "&:hover": {

                transform: "translateY(-8px)",

                boxShadow:
                  "0 20px 45px rgba(37,99,235,.18)",

              },
            }}
          >

            <Box
              sx={{
                position: "absolute",
                right: 20,
                top: 20,
                width: 70,
                height: 70,
                borderRadius: "50%",
                bgcolor: `${card.colour}15`,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                color: card.colour,
              }}
            >
              {card.icon}
            </Box>

            <Typography
              color="text.secondary"
              fontWeight={600}
            >
              {card.title}
            </Typography>

            <Typography
              variant="h3"
              fontWeight={700}
              mt={2}
            >
              {card.value}
              <Typography
                component="span"
                variant="h6"
                color="text.secondary"
              >
                {" "}
                {card.unit}
              </Typography>
            </Typography>

            <Typography
              mt={1}
              color="text.secondary"
            >
              {card.subtitle}
            </Typography>

            <Box
              mt={3}
              display="flex"
              alignItems="center"
              justifyContent="space-between"
            >
              <Typography
                fontWeight={600}
                color={card.colour}
              >
                {card.progress}% Complete
              </Typography>

              <TrendingUpIcon
                sx={{
                  color: card.colour,
                }}
              />
            </Box>

            <LinearProgress
              variant="determinate"
              value={card.progress}
              sx={{
                mt: 1.5,
                height: 8,
                borderRadius: 20,

                "& .MuiLinearProgress-bar": {
                  background: card.colour,
                },
              }}
            />

          </Paper>

        </Grid>

      ))}

    </Grid>
  );
}

export default DashboardCards;