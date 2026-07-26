import { useEffect, useState } from "react";
import {
  Grid, Paper, Typography, Box, Stack, Avatar, Chip,
  Divider, LinearProgress, CircularProgress,
} from "@mui/material";

import BoltIcon          from "@mui/icons-material/Bolt";
import ThermostatIcon    from "@mui/icons-material/Thermostat";
import SavingsIcon       from "@mui/icons-material/Savings";
import QueryStatsIcon    from "@mui/icons-material/QueryStats";
import SmartToyIcon      from "@mui/icons-material/SmartToy";
import TipsAndUpdatesIcon from "@mui/icons-material/TipsAndUpdates";
import TrendingDownIcon  from "@mui/icons-material/TrendingDown";
import TrendingUpIcon    from "@mui/icons-material/TrendingUp";
import ApartmentIcon     from "@mui/icons-material/Apartment";

import DashboardLayout   from "../layouts/DashboardLayout";
import EnergyChart       from "../components/EnergyChart";
import PMVChart          from "../components/PMVChart";
import ComfortChart      from "../components/ComfortChart";
import api               from "../api/api";

// ── Stat Card ──────────────────────────────────────────────
function StatCard({ title, value, sub, icon, color, trend, progress }) {
  return (
    <Paper
      className="hover-lift fade-in"
      sx={{
        p: 3, border: "1px solid #E2E8F0",
        background: `linear-gradient(145deg,#ffffff,#f8fafc)`,
      }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
        <Box>
          <Typography variant="body2" color="text.secondary" fontWeight={500}>
            {title}
          </Typography>
          <Typography variant="h4" fontWeight={800} mt={0.5} sx={{ color }}>
            {value ?? "—"}
          </Typography>
          {sub && (
            <Typography variant="caption" color="text.secondary">{sub}</Typography>
          )}
        </Box>
        <Avatar sx={{ bgcolor: `${color}18`, width: 52, height: 52 }}>
          <Box sx={{ color }}>{icon}</Box>
        </Avatar>
      </Stack>

      {trend !== undefined && (
        <Stack direction="row" alignItems="center" spacing={0.5} mt={1.5}>
          {trend >= 0
            ? <TrendingUpIcon   sx={{ color: "#22C55E", fontSize: 16 }} />
            : <TrendingDownIcon sx={{ color: "#EF4444", fontSize: 16 }} />
          }
          <Typography variant="caption" sx={{ color: trend >= 0 ? "#22C55E" : "#EF4444", fontWeight: 600 }}>
            {Math.abs(trend).toFixed(1)}% vs. prev.
          </Typography>
        </Stack>
      )}

      {progress !== undefined && (
        <Box mt={2}>
          <LinearProgress
            variant="determinate"
            value={Math.min(progress, 100)}
            sx={{
              height: 6, borderRadius: 20,
              bgcolor: `${color}18`,
              "& .MuiLinearProgress-bar": { bgcolor: color },
            }}
          />
        </Box>
      )}
    </Paper>
  );
}

// ── Page ───────────────────────────────────────────────────
export default function Dashboard() {
  const [summary,        setSummary]        = useState(null);
  const [prediction,     setPrediction]     = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [energy,         setEnergy]         = useState(null);
  const [comfort,        setComfort]        = useState(null);
  const [current,        setCurrent]        = useState(null);
  const [loading,        setLoading]        = useState(true);

  useEffect(() => {
    Promise.allSettled([
      api.get("/analytics/dashboard"),
      api.get("/analytics/latest-prediction"),
      api.get("/analytics/latest-recommendation"),
      api.get("/analytics/energy"),
      api.get("/analytics/comfort"),
      api.get("/api/dashboard/current"),
    ]).then(([s, p, r, e, c, cur]) => {
      if (s.status   === "fulfilled") setSummary(s.value.data);
      if (p.status   === "fulfilled") setPrediction(p.value.data);
      if (r.status   === "fulfilled") setRecommendation(r.value.data);
      if (e.status   === "fulfilled") setEnergy(e.value.data);
      if (c.status   === "fulfilled") setComfort(c.value.data);
      if (cur.status === "fulfilled") setCurrent(cur.value.data);
    }).finally(() => setLoading(false));
  }, []);

  const kpis = [
    {
      title: "Total Predictions",
      value: summary?.total_predictions ?? "—",
      icon:  <QueryStatsIcon />,
      color: "#2563EB",
      progress: summary ? Math.min((summary.total_predictions / 100) * 100, 100) : 0,
    },
    {
      title: "Avg Energy Prediction",
      value: summary?.average_energy_prediction != null
        ? `${Number(summary.average_energy_prediction).toFixed(2)} kWh`
        : "—",
      sub: energy ? `Max: ${Number(energy.maximum).toFixed(2)} kWh` : undefined,
      icon:  <BoltIcon />,
      color: "#F59E0B",
    },
    {
      title: "Avg Comfort Score",
      value: summary?.average_comfort_score != null
        ? Number(summary.average_comfort_score).toFixed(3)
        : "—",
      sub: comfort ? `Min: ${Number(comfort.minimum).toFixed(3)}` : undefined,
      icon:  <ThermostatIcon />,
      color: "#22C55E",
      progress: summary ? Math.min(summary.average_comfort_score * 100, 100) : 0,
    },
    {
      title: "Avg Expected Savings",
      value: summary?.average_expected_savings != null
        ? `${Number(summary.average_expected_savings).toFixed(1)}%`
        : "—",
      icon:  <SavingsIcon />,
      color: "#8B5CF6",
      progress: summary?.average_expected_savings ?? 0,
    },
  ];

  return (
    <DashboardLayout>

      {/* Hero Banner */}
      <Paper
        className="fade-in"
        sx={{
          mb: 4, p: { xs: 3, md: 4 },
          background: "linear-gradient(135deg,#2563EB 0%,#0ea5e9 50%,#06B6D4 100%)",
          color: "white",
          overflow: "hidden",
          position: "relative",
        }}
      >
        <Box
          sx={{
            position:"absolute", right:-40, top:-40,
            width:220, height:220, borderRadius:"50%",
            bgcolor:"rgba(255,255,255,0.07)",
          }}
        />
        <Stack direction={{ xs:"column", md:"row" }} justifyContent="space-between" alignItems={{ md:"center" }} gap={2}>
          <Box>
            <Stack direction="row" alignItems="center" spacing={1.5} mb={1}>
              <ApartmentIcon sx={{ fontSize: 32 }} />
              <Typography variant="h4" fontWeight={800}>
                Building Dashboard
              </Typography>
            </Stack>
            <Typography sx={{ opacity: 0.85 }}>
              AI-powered monitoring · energy, comfort & optimization in real time
            </Typography>
          </Box>
          <Stack direction="row" spacing={2} flexWrap="wrap">
            {current && (
              <>
                <Chip label={`PMV: ${Number(current.pmv).toFixed(3)}`}
                  sx={{ bgcolor:"rgba(255,255,255,0.2)", color:"#fff", fontWeight:700 }} />
                <Chip label={`Energy: ${Number(current.energy).toFixed(3)} kWh`}
                  sx={{ bgcolor:"rgba(255,255,255,0.2)", color:"#fff", fontWeight:700 }} />
              </>
            )}
            <Chip
              label={<Stack direction="row" alignItems="center" spacing={0.5}>
                <Box sx={{ width:8, height:8, borderRadius:"50%", bgcolor:"#22C55E" }} className="pulse-dot" />
                <span>Live</span>
              </Stack>}
              sx={{ bgcolor:"rgba(255,255,255,0.2)", color:"#fff", fontWeight:700 }}
            />
          </Stack>
        </Stack>
      </Paper>

      {/* KPI Cards */}
      {loading ? (
        <Box display="flex" justifyContent="center" py={6}><CircularProgress /></Box>
      ) : (
        <Grid container spacing={3} mb={4}>
          {kpis.map((k) => (
            <Grid item xs={12} sm={6} xl={3} key={k.title}>
              <StatCard {...k} />
            </Grid>
          ))}
        </Grid>
      )}

      {/* Charts row 1 */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} lg={8}>
          <EnergyChart />
        </Grid>
        <Grid item xs={12} lg={4}>
          <ComfortChart />
        </Grid>
      </Grid>

      {/* Charts row 2 */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12}>
          <PMVChart />
        </Grid>
      </Grid>

      {/* Latest Recommendation */}
      {recommendation && (
        <Paper
          className="hover-lift fade-in"
          sx={{
            p: 4, border: "1px solid #E2E8F0",
            background: "linear-gradient(145deg,#ffffff,#f8fafc)",
          }}
        >
          <Stack direction="row" spacing={2} alignItems="center" mb={2}>
            <Avatar sx={{ bgcolor: "#2563EB", width: 48, height: 48 }}>
              <SmartToyIcon />
            </Avatar>
            <Box>
              <Typography variant="h6" fontWeight={700}>Latest AI Recommendation</Typography>
              <Typography variant="body2" color="text.secondary">
                Based on the most recent ML prediction
              </Typography>
            </Box>
            <Box flexGrow={1} />
            <Chip label="AI" color="primary" icon={<SmartToyIcon />} />
          </Stack>

          <Divider sx={{ mb: 2 }} />

          <Paper
            elevation={0}
            sx={{ bgcolor:"#EFF6FF", borderLeft:"4px solid #2563EB", p:2.5, borderRadius:3 }}
          >
            <Stack direction="row" spacing={1.5} alignItems="flex-start">
              <TipsAndUpdatesIcon sx={{ color:"#2563EB", mt:0.3 }} />
              <Typography lineHeight={1.8}>{recommendation.reason}</Typography>
            </Stack>
          </Paper>

          <Grid container spacing={2} mt={2}>
            <Grid item xs={12} sm={4}>
              <Paper elevation={0} sx={{ p:2, bgcolor:"#F0FDF4", borderRadius:3 }}>
                <Typography variant="caption" color="text.secondary">Expected Savings</Typography>
                <Typography variant="h5" fontWeight={800} color="#16A34A">
                  {Number(recommendation.expected_savings).toFixed(1)}%
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Paper elevation={0} sx={{ p:2, bgcolor:"#FFF7ED", borderRadius:3 }}>
                <Typography variant="caption" color="text.secondary">Recommended Setpoint</Typography>
                <Typography variant="h5" fontWeight={800} color="#EA580C">
                  {Number(recommendation.recommended_setpoint).toFixed(1)}°C
                </Typography>
              </Paper>
            </Grid>
            {current && (
              <Grid item xs={12} sm={4}>
                <Paper elevation={0} sx={{ p:2, bgcolor:"#F0F9FF", borderRadius:3 }}>
                  <Typography variant="caption" color="text.secondary">LLM Reason</Typography>
                  <Typography variant="body2" mt={0.5} sx={{ lineHeight:1.6, fontSize:12 }}>
                    {current.reason?.slice(0, 100) || "—"}
                  </Typography>
                </Paper>
              </Grid>
            )}
          </Grid>
        </Paper>
      )}
    </DashboardLayout>
  );
}
