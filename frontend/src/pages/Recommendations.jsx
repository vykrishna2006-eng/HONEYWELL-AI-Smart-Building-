import { useEffect, useState } from "react";
import {
  Box, Typography, Paper, Stack, Avatar,
  Chip, Divider, CircularProgress, Grid, Button,
} from "@mui/material";

import SmartToyIcon       from "@mui/icons-material/SmartToy";
import AutoAwesomeIcon    from "@mui/icons-material/AutoAwesome";
import SavingsIcon        from "@mui/icons-material/Savings";
import BoltIcon           from "@mui/icons-material/Bolt";
import TipsAndUpdatesIcon from "@mui/icons-material/TipsAndUpdates";
import RefreshIcon        from "@mui/icons-material/Refresh";
import ThermostatIcon     from "@mui/icons-material/Thermostat";

import DashboardLayout         from "../layouts/DashboardLayout";
import { getRecommendation }   from "../services/llmService";
import { getLatestRecommendation } from "../services/analyticsService";

export default function Recommendations() {
  const [llmRec,    setLlmRec]    = useState("");
  const [dbRec,     setDbRec]     = useState(null);
  const [llmLoad,   setLlmLoad]   = useState(true);
  const [dbLoad,    setDbLoad]    = useState(true);

  useEffect(() => {
    loadAll();
  }, []);

  const loadAll = () => {
    setLlmLoad(true);
    setDbLoad(true);

    getRecommendation()
      .then((r) => {
        if (typeof r === "string") setLlmRec(r);
        else setLlmRec(r?.response || r?.recommendation || r?.message || JSON.stringify(r, null, 2));
      })
      .catch(() => setLlmRec("Unable to load AI recommendation. Check Ollama connection."))
      .finally(() => setLlmLoad(false));

    getLatestRecommendation()
      .then(setDbRec)
      .catch(() => setDbRec(null))
      .finally(() => setDbLoad(false));
  };

  return (
    <DashboardLayout>
      {/* Hero */}
      <Paper
        className="fade-in"
        sx={{
          mb: 4, p: { xs:3, md:4 },
          background: "linear-gradient(135deg,#2563EB,#06B6D4)",
          color: "white",
        }}
      >
        <Stack direction={{ xs:"column", md:"row" }} spacing={3} alignItems={{ md:"center" }}>
          <Avatar sx={{ width:70, height:70, bgcolor:"rgba(255,255,255,.2)" }}>
            <SmartToyIcon sx={{ fontSize: 40 }} />
          </Avatar>
          <Box flexGrow={1}>
            <Typography variant="h4" fontWeight={800}>AI Recommendation Assistant</Typography>
            <Typography sx={{ opacity:0.85, mt:0.5 }}>
              LLM-powered intelligent building optimisation engine
            </Typography>
          </Box>
          <Button
            variant="contained"
            onClick={loadAll}
            startIcon={<RefreshIcon />}
            sx={{ bgcolor:"rgba(255,255,255,0.2)", "&:hover":{ bgcolor:"rgba(255,255,255,0.3)" } }}
          >
            Refresh
          </Button>
        </Stack>
      </Paper>

      {/* DB Recommendation Metrics */}
      {!dbLoad && dbRec && (
        <Grid container spacing={3} mb={4}>
          <Grid item xs={12} md={4}>
            <Paper className="hover-lift fade-in" sx={{ p:3, border:"1px solid #E2E8F0", textAlign:"center" }}>
              <SavingsIcon sx={{ fontSize:45, color:"#22C55E" }} />
              <Typography variant="h4" fontWeight={800} mt={1}>
                {Number(dbRec.expected_savings).toFixed(1)}%
              </Typography>
              <Typography color="text.secondary">Expected Savings</Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} md={4}>
            <Paper className="hover-lift fade-in" sx={{ p:3, border:"1px solid #E2E8F0", textAlign:"center" }}>
              <ThermostatIcon sx={{ fontSize:45, color:"#2563EB" }} />
              <Typography variant="h4" fontWeight={800} mt={1}>
                {Number(dbRec.recommended_setpoint).toFixed(1)}°C
              </Typography>
              <Typography color="text.secondary">Recommended Setpoint</Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} md={4}>
            <Paper className="hover-lift fade-in" sx={{ p:3, border:"1px solid #E2E8F0", textAlign:"center" }}>
              <AutoAwesomeIcon sx={{ fontSize:45, color:"#8B5CF6" }} />
              <Typography variant="h4" fontWeight={800} mt={1}>High</Typography>
              <Typography color="text.secondary">Optimisation Level</Typography>
            </Paper>
          </Grid>
        </Grid>
      )}

      {/* DB Recommendation Reason */}
      {!dbLoad && dbRec && (
        <Paper
          className="hover-lift fade-in"
          sx={{ p:4, border:"1px solid #E2E8F0", mb:3 }}
        >
          <Stack direction="row" spacing={2} alignItems="center" mb={2}>
            <Avatar sx={{ bgcolor:"#22C55E" }}><BoltIcon /></Avatar>
            <Box>
              <Typography variant="h6" fontWeight={700}>ML-Based Recommendation</Typography>
              <Typography variant="body2" color="text.secondary">From latest prediction record</Typography>
            </Box>
            <Box flexGrow={1} />
            <Chip label="DB Record" color="success" size="small" />
          </Stack>
          <Divider sx={{ mb:2 }} />
          <Paper elevation={0} sx={{ bgcolor:"#F0FDF4", borderLeft:"4px solid #22C55E", p:2.5, borderRadius:3 }}>
            <Stack direction="row" spacing={1.5} alignItems="flex-start">
              <TipsAndUpdatesIcon sx={{ color:"#16A34A", mt:0.3 }} />
              <Typography lineHeight={1.8}>{dbRec.reason}</Typography>
            </Stack>
          </Paper>
        </Paper>
      )}

      {/* LLM Recommendation */}
      <Paper
        className="hover-lift fade-in"
        sx={{ p:4, border:"1px solid #E2E8F0" }}
      >
        <Stack direction="row" spacing={2} alignItems="center" mb={2}>
          <Avatar sx={{ bgcolor:"#2563EB" }}><SmartToyIcon /></Avatar>
          <Box>
            <Typography variant="h6" fontWeight={700}>LLM AI Recommendation</Typography>
            <Typography variant="body2" color="text.secondary">Generated in real time via Ollama</Typography>
          </Box>
          <Box flexGrow={1} />
          <Chip
            label={
              <Stack direction="row" alignItems="center" spacing={0.5}>
                <Box sx={{ width:7, height:7, borderRadius:"50%", bgcolor:"#22C55E" }} className="pulse-dot" />
                <span>Live</span>
              </Stack>
            }
            color="success"
            size="small"
          />
        </Stack>

        <Divider sx={{ mb:3 }} />

        {llmLoad ? (
          <Box textAlign="center" py={6}>
            <CircularProgress />
            <Typography mt={2} color="text.secondary">
              LLM is analysing your building data…
            </Typography>
          </Box>
        ) : (
          <Paper elevation={0} sx={{ bgcolor:"#EFF6FF", p:3, borderRadius:4, borderLeft:"5px solid #2563EB" }}>
            <Stack direction="row" spacing={2} alignItems="flex-start">
              <TipsAndUpdatesIcon sx={{ color:"#2563EB", mt:0.5, flexShrink:0 }} />
              <Typography sx={{ whiteSpace:"pre-wrap", lineHeight:2 }}>
                {llmRec}
              </Typography>
            </Stack>
          </Paper>
        )}
      </Paper>
    </DashboardLayout>
  );
}
