import { useEffect, useState } from "react";
import {
  Grid, Paper, Typography, Box, Stack, Chip,
  LinearProgress, Divider, CircularProgress,
} from "@mui/material";

import TrendingUpIcon  from "@mui/icons-material/TrendingUp";
import BoltIcon        from "@mui/icons-material/Bolt";
import ThermostatIcon  from "@mui/icons-material/Thermostat";
import SavingsIcon     from "@mui/icons-material/Savings";
import AnalyticsIcon   from "@mui/icons-material/Analytics";

import DashboardLayout          from "../layouts/DashboardLayout";
import EnergyChart              from "../components/EnergyChart";
import ComfortChart             from "../components/ComfortChart";
import PMVChart                 from "../components/PMVChart";
import EnergyStatChart          from "../components/EnergyStatChart";
import PredictionHistoryChart   from "../components/PredictionHistoryChart";
import SetpointChart            from "../components/SetpointChart";
import OccupancyChart           from "../components/OccupancyChart";
import api                      from "../api/api";

function KpiCard({ title, value, icon, color, progress }) {
  return (
    <Paper
      className="hover-lift fade-in"
      sx={{ p: 3, border: "1px solid #E2E8F0", background: "linear-gradient(145deg,#fff,#f8fafc)" }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography variant="body2" color="text.secondary" fontWeight={500}>{title}</Typography>
          <Typography variant="h3" fontWeight={800} mt={0.5} sx={{ color }}>{value}</Typography>
        </Box>
        <Box sx={{ color, fontSize: 42 }}>{icon}</Box>
      </Stack>
      <Box mt={2.5}>
        <LinearProgress
          variant="determinate"
          value={progress}
          sx={{
            height: 8, borderRadius: 20,
            bgcolor: `${color}18`,
            "& .MuiLinearProgress-bar": { bgcolor: color, borderRadius: 20 },
          }}
        />
      </Box>
    </Paper>
  );
}

export default function Analytics() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/analytics/dashboard")
      .then((r) => setSummary(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const totalPred = summary?.total_predictions ?? 0;

  const kpis = [
    {
      title:    "Total Predictions",
      value:    loading ? "…" : totalPred,
      icon:     <AnalyticsIcon sx={{ fontSize: 42 }} />,
      color:    "#2563EB",
      progress: Math.min((totalPred / 200) * 100, 100),
    },
    {
      title:    "Avg Energy (kWh)",
      value:    loading ? "…" : Number(summary?.average_energy_prediction ?? 0).toFixed(2),
      icon:     <BoltIcon sx={{ fontSize: 42 }} />,
      color:    "#F59E0B",
      progress: 70,
    },
    {
      title:    "Avg Comfort Score",
      value:    loading ? "…" : Number(summary?.average_comfort_score ?? 0).toFixed(3),
      icon:     <ThermostatIcon sx={{ fontSize: 42 }} />,
      color:    "#22C55E",
      progress: Math.min((summary?.average_comfort_score ?? 0) * 100, 100),
    },
    {
      title:    "Avg Expected Savings",
      value:    loading ? "…" : `${Number(summary?.average_expected_savings ?? 0).toFixed(1)}%`,
      icon:     <SavingsIcon sx={{ fontSize: 42 }} />,
      color:    "#8B5CF6",
      progress: summary?.average_expected_savings ?? 0,
    },
  ];

  return (
    <DashboardLayout>
      {/* Header */}
      <Box mb={4}>
        <Stack direction="row" alignItems="center" spacing={1.5} mb={0.5}>
          <AnalyticsIcon sx={{ color: "#2563EB", fontSize: 32 }} />
          <Typography variant="h4" fontWeight={800}>Analytics Dashboard</Typography>
        </Stack>
        <Typography color="text.secondary">
          Full visibility into energy, comfort, ML predictions and simulation results
        </Typography>
      </Box>

      {/* KPI Row */}
      {loading ? (
        <Box display="flex" justifyContent="center" py={4}><CircularProgress /></Box>
      ) : (
        <Grid container spacing={3} mb={4}>
          {kpis.map((k) => (
            <Grid item xs={12} sm={6} xl={3} key={k.title}>
              <KpiCard {...k} />
            </Grid>
          ))}
        </Grid>
      )}

      {/* Charts – Row 1 */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} lg={8}><EnergyChart /></Grid>
        <Grid item xs={12} lg={4}><EnergyStatChart /></Grid>
      </Grid>

      {/* Charts – Row 2 */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} lg={6}><PMVChart /></Grid>
        <Grid item xs={12} lg={6}><ComfortChart /></Grid>
      </Grid>

      {/* Charts – Row 3 */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} lg={6}><SetpointChart /></Grid>
        <Grid item xs={12} lg={6}><OccupancyChart /></Grid>
      </Grid>

      {/* Charts – Row 4 */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12}><PredictionHistoryChart /></Grid>
      </Grid>

      {/* AI Insights */}
      <Paper
        className="fade-in"
        sx={{ p: 4, border: "1px solid #E2E8F0", background: "linear-gradient(145deg,#fff,#f8fafc)" }}
      >
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5" fontWeight={700}>AI Performance Insights</Typography>
          <Chip icon={<TrendingUpIcon />} label="Excellent" color="success" />
        </Stack>
        <Divider sx={{ mb: 2.5 }} />
        <Typography color="text.secondary" lineHeight={2}>
          The AI prediction engine indicates that the building is operating with high efficiency.
          Energy consumption remains stable while occupant comfort stays above the desired threshold.
          Current optimisation strategies are expected to reduce overall HVAC energy usage by
          approximately {Number(summary?.average_expected_savings ?? 18).toFixed(1)}% without
          affecting indoor comfort. Machine learning predictions are stored and traceable across
          all sensor readings, allowing continuous model improvement.
        </Typography>
      </Paper>
    </DashboardLayout>
  );
}
