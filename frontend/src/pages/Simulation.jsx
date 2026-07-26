import { useState } from "react";
import {
  Box, Paper, Typography, Grid, Button, Stack,
  Chip, LinearProgress, CircularProgress, Divider,
  Alert,
} from "@mui/material";

import PlayArrowIcon   from "@mui/icons-material/PlayArrow";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import DescriptionIcon from "@mui/icons-material/Description";
import TableRowsIcon   from "@mui/icons-material/TableRows";
import ViewColumnIcon  from "@mui/icons-material/ViewColumn";
import SmartToyIcon    from "@mui/icons-material/SmartToy";
import BoltIcon        from "@mui/icons-material/Bolt";

import DashboardLayout  from "../layouts/DashboardLayout";
import EnergyChart      from "../components/EnergyChart";
import PMVChart         from "../components/PMVChart";
import SetpointChart    from "../components/SetpointChart";
import OccupancyChart   from "../components/OccupancyChart";
import ClosedLoopReport from "../components/ClosedLoopReport";
import { runSimulation } from "../services/simulationService";

export default function Simulation() {
  const [loading, setLoading] = useState(false);
  const [result,  setResult]  = useState(null);
  const [error,   setError]   = useState("");

  const startSimulation = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await runSimulation();
      setResult(data);
    } catch (err) {
      setError("Simulation failed. Make sure EnergyPlus is configured.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const simResults = result?.results;

  return (
    <DashboardLayout>
      {/* Hero */}
      <Paper
        className="fade-in"
        sx={{
          p: { xs:3, md:4 }, mb:4,
          background: "linear-gradient(135deg,#2563EB,#06B6D4)",
          color: "white",
        }}
      >
        <Stack direction={{ xs:"column", md:"row" }} justifyContent="space-between" alignItems={{ md:"center" }} gap={2}>
          <Box>
            <Stack direction="row" spacing={1.5} alignItems="center" mb={0.5}>
              <BoltIcon sx={{ fontSize: 30 }} />
              <Typography variant="h4" fontWeight={800}>Building Simulation</Typography>
            </Stack>
            <Typography sx={{ opacity:0.85 }}>
              Run AI-powered EnergyPlus building optimisation simulations
            </Typography>
          </Box>
          <Button
            variant="contained"
            size="large"
            startIcon={loading ? <CircularProgress size={18} color="inherit" /> : <PlayArrowIcon />}
            onClick={startSimulation}
            disabled={loading}
            sx={{ bgcolor:"rgba(255,255,255,0.2)", "&:hover":{ bgcolor:"rgba(255,255,255,0.35)" }, minWidth:180 }}
          >
            {loading ? "Running…" : "Start Simulation"}
          </Button>
        </Stack>
      </Paper>

      {/* Progress */}
      {loading && (
        <Paper className="fade-in" sx={{ p:3, mb:3, border:"1px solid #E2E8F0" }}>
          <Typography fontWeight={600} mb={1}>Running EnergyPlus simulation…</Typography>
          <LinearProgress />
          <Typography variant="body2" color="text.secondary" mt={1}>
            This may take a moment. The AI is processing building conditions.
          </Typography>
        </Paper>
      )}

      {error && (
        <Alert severity="error" sx={{ mb:3, borderRadius:3 }}>{error}</Alert>
      )}

      {/* Simulation results */}
      {simResults && (
        <>
          <Grid container spacing={3} mb={3}>
            <Grid item xs={12} md={4}>
              <Paper className="hover-lift fade-in" sx={{ p:3, border:"1px solid #E2E8F0", textAlign:"center" }}>
                <DescriptionIcon sx={{ fontSize:45, color:"#2563EB" }} />
                <Typography variant="h6" fontWeight={700} mt={2} noWrap>{simResults.file}</Typography>
                <Typography color="text.secondary">Output File</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              <Paper className="hover-lift fade-in" sx={{ p:3, border:"1px solid #E2E8F0", textAlign:"center" }}>
                <TableRowsIcon sx={{ fontSize:45, color:"#22C55E" }} />
                <Typography variant="h4" fontWeight={800} mt={2}>{simResults.rows}</Typography>
                <Typography color="text.secondary">Rows Simulated</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              <Paper className="hover-lift fade-in" sx={{ p:3, border:"1px solid #E2E8F0", textAlign:"center" }}>
                <ViewColumnIcon sx={{ fontSize:45, color:"#F59E0B" }} />
                <Typography variant="h4" fontWeight={800} mt={2}>
                  {simResults.columns?.length ?? 0}
                </Typography>
                <Typography color="text.secondary">Output Variables</Typography>
              </Paper>
            </Grid>
          </Grid>

          <Paper className="fade-in" sx={{ p:4, mb:4, border:"1px solid #E2E8F0" }}>
            <Stack direction="row" spacing={2} alignItems="center">
              <SmartToyIcon color="primary" />
              <Typography variant="h5" fontWeight={700}>Simulation Summary</Typography>
              <Box flexGrow={1} />
              <Chip icon={<CheckCircleIcon />} label="Completed" color="success" />
            </Stack>
            <Divider sx={{ my:2 }} />
            <Typography lineHeight={2} color="text.secondary">
              EnergyPlus completed a full annual simulation, producing {simResults.rows} hourly
              rows across {simResults.columns?.length ?? 0} output variables.
            </Typography>
          </Paper>
        </>
      )}

      {/* Live Charts from CSV data */}
      <Typography variant="h5" fontWeight={700} mb={2}>
        Simulation Data Charts
      </Typography>
      <Typography variant="body2" color="text.secondary" mb={3}>
        All charts below read from the latest simulation CSV report.
      </Typography>

      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} lg={8}><EnergyChart /></Grid>
        <Grid item xs={12} lg={4}><OccupancyChart /></Grid>
      </Grid>

      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} lg={6}><PMVChart /></Grid>
        <Grid item xs={12} lg={6}><SetpointChart /></Grid>
      </Grid>

      {/* Closed Loop Report */}
      <ClosedLoopReport />
    </DashboardLayout>
  );
}
