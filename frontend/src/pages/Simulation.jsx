import { useState, useEffect } from "react";
import {
  Box, Paper, Typography, Grid, Button, Stack,
  Chip, LinearProgress, CircularProgress, Divider,
  Alert, AlertTitle, List, ListItem, ListItemIcon,
  ListItemText, Collapse, Tooltip,
} from "@mui/material";

import PlayArrowIcon      from "@mui/icons-material/PlayArrow";
import CheckCircleIcon    from "@mui/icons-material/CheckCircle";
import DescriptionIcon    from "@mui/icons-material/Description";
import TableRowsIcon      from "@mui/icons-material/TableRows";
import ViewColumnIcon     from "@mui/icons-material/ViewColumn";
import SmartToyIcon       from "@mui/icons-material/SmartToy";
import BoltIcon           from "@mui/icons-material/Bolt";
import ErrorOutlineIcon   from "@mui/icons-material/ErrorOutlined";
import WarningAmberIcon   from "@mui/icons-material/WarningAmber";
import CheckIcon          from "@mui/icons-material/Check";
import CloseIcon          from "@mui/icons-material/Close";
import InfoOutlinedIcon   from "@mui/icons-material/InfoOutlined";
import ContentCopyIcon    from "@mui/icons-material/ContentCopy";
import ExpandMoreIcon     from "@mui/icons-material/ExpandMore";
import ExpandLessIcon     from "@mui/icons-material/ExpandLess";
import FolderOpenIcon     from "@mui/icons-material/FolderOpen";
import TerminalIcon       from "@mui/icons-material/Terminal";

import DashboardLayout   from "../layouts/DashboardLayout";
import EnergyChart       from "../components/EnergyChart";
import PMVChart          from "../components/PMVChart";
import SetpointChart     from "../components/SetpointChart";
import OccupancyChart    from "../components/OccupancyChart";
import ClosedLoopReport  from "../components/ClosedLoopReport";
import { runSimulation } from "../services/simulationService";
import api               from "../api/api";

// ── Status badge ─────────────────────────────────────────
function StatusBadge({ ok, label, path }) {
  return (
    <ListItem dense disableGutters>
      <ListItemIcon sx={{ minWidth: 32 }}>
        {ok
          ? <CheckIcon sx={{ color: "#22C55E", fontSize: 18 }} />
          : <CloseIcon sx={{ color: "#EF4444", fontSize: 18 }} />
        }
      </ListItemIcon>
      <ListItemText
        primary={<Typography variant="body2" fontWeight={600}>{label}</Typography>}
        secondary={
          <Typography variant="caption" sx={{ color: ok ? "#64748B" : "#EF4444", fontFamily: "monospace" }}>
            {path}
          </Typography>
        }
      />
    </ListItem>
  );
}

// ── Copy-to-clipboard button ─────────────────────────────
function CopyButton({ text }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <Tooltip title={copied ? "Copied!" : "Copy"}>
      <Button
        size="small"
        onClick={copy}
        startIcon={<ContentCopyIcon sx={{ fontSize: 14 }} />}
        sx={{ fontSize: 11, py: 0.3, px: 1 }}
      >
        {copied ? "Copied" : "Copy"}
      </Button>
    </Tooltip>
  );
}

// ── Error terminal block ──────────────────────────────────
function TerminalBlock({ label, content }) {
  const [open, setOpen] = useState(false);
  if (!content?.trim()) return null;
  return (
    <Box mt={1.5}>
      <Button
        size="small"
        startIcon={open ? <ExpandLessIcon /> : <ExpandMoreIcon />}
        endIcon={<TerminalIcon sx={{ fontSize: 14 }} />}
        onClick={() => setOpen(!open)}
        sx={{ fontSize: 12, color: "#64748B" }}
      >
        {open ? "Hide" : "Show"} {label}
      </Button>
      <Collapse in={open}>
        <Box
          sx={{
            mt: 1, p: 2, bgcolor: "#0F172A", borderRadius: 2,
            fontFamily: "monospace", fontSize: 12, color: "#94A3B8",
            whiteSpace: "pre-wrap", maxHeight: 240, overflowY: "auto",
          }}
        >
          <Stack direction="row" justifyContent="flex-end" mb={1}>
            <CopyButton text={content} />
          </Stack>
          {content}
        </Box>
      </Collapse>
    </Box>
  );
}

// ── Main page ─────────────────────────────────────────────
export default function Simulation() {
  const [loading,  setLoading]  = useState(false);
  const [result,   setResult]   = useState(null);
  const [simError, setSimError] = useState(null);   // structured error from backend
  const [status,   setStatus]   = useState(null);   // /simulation/status response
  const [statusLoading, setStatusLoading] = useState(true);

  // Load EnergyPlus readiness status on mount
  useEffect(() => {
    api.get("/simulation/status")
      .then((r) => setStatus(r.data))
      .catch(() => setStatus(null))
      .finally(() => setStatusLoading(false));
  }, []);

  const startSimulation = async () => {
    setLoading(true);
    setSimError(null);
    setResult(null);

    try {
      const data = await runSimulation();

      // Backend always returns 200; check status field
      if (data?.status === "error") {
        setSimError(data);
      } else {
        setResult(data);
        // Refresh status after a successful run
        api.get("/simulation/status").then((r) => setStatus(r.data)).catch(() => {});
      }
    } catch (err) {
      // Network / 5xx error
      const detail = err?.response?.data?.detail;
      setSimError({
        status:    "error",
        code:      "NETWORK_ERROR",
        message:   detail
          ? (typeof detail === "string" ? detail : detail.message ?? JSON.stringify(detail))
          : "Cannot reach the backend. Make sure the FastAPI server is running on port 8000.",
        diagnosis: err?.message ?? "",
        stdout:    "",
        stderr:    "",
      });
    } finally {
      setLoading(false);
    }
  };

  const simResults = result?.results;
  const ready      = status?.ready_to_simulate;

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
        <Stack
          direction={{ xs:"column", md:"row" }}
          justifyContent="space-between"
          alignItems={{ md:"center" }}
          gap={2}
        >
          <Box>
            <Stack direction="row" spacing={1.5} alignItems="center" mb={0.5}>
              <BoltIcon sx={{ fontSize: 30 }} />
              <Typography variant="h4" fontWeight={800}>Building Simulation</Typography>
            </Stack>
            <Typography sx={{ opacity:0.85 }}>
              AI-powered EnergyPlus building optimisation simulation
            </Typography>
          </Box>

          <Tooltip
            title={
              !ready && !statusLoading
                ? "EnergyPlus is not ready — see the status panel below"
                : ""
            }
          >
            <span>
              <Button
                variant="contained"
                size="large"
                startIcon={
                  loading
                    ? <CircularProgress size={18} color="inherit" />
                    : <PlayArrowIcon />
                }
                onClick={startSimulation}
                disabled={loading}
                sx={{
                  bgcolor: "rgba(255,255,255,0.2)",
                  "&:hover": { bgcolor: "rgba(255,255,255,0.35)" },
                  minWidth: 180,
                }}
              >
                {loading ? "Running…" : "Start Simulation"}
              </Button>
            </span>
          </Tooltip>
        </Stack>
      </Paper>

      {/* EnergyPlus readiness status card */}
      {!statusLoading && status && (
        <Paper
          className="fade-in"
          sx={{
            p: 3, mb: 3, border: "1px solid",
            borderColor: ready ? "#BBF7D0" : "#FECACA",
            bgcolor: ready ? "#F0FDF4" : "#FEF2F2",
          }}
        >
          <Stack direction="row" spacing={1.5} alignItems="center" mb={1.5}>
            {ready
              ? <CheckCircleIcon sx={{ color:"#22C55E" }} />
              : <WarningAmberIcon sx={{ color:"#EF4444" }} />
            }
            <Typography variant="h6" fontWeight={700}
              sx={{ color: ready ? "#15803D" : "#B91C1C" }}
            >
              {ready ? "EnergyPlus is ready to simulate" : "EnergyPlus is NOT ready"}
            </Typography>
            {!ready && (
              <Chip
                label="Setup required"
                size="small"
                sx={{ bgcolor:"#FEE2E2", color:"#B91C1C", fontWeight:700 }}
              />
            )}
          </Stack>

          <List dense disablePadding>
            <StatusBadge
              ok={status.energyplus_exe.exists}
              label="EnergyPlus executable"
              path={status.energyplus_exe.path}
            />
            <StatusBadge
              ok={status.idf_file.exists}
              label="Building IDF file"
              path={status.idf_file.path}
            />
            <StatusBadge
              ok={status.weather_file.exists}
              label="Weather EPW file"
              path={status.weather_file.path}
            />
            <StatusBadge
              ok={status.report_csv.exists}
              label="Simulation report CSV (previous run)"
              path={status.report_csv.path}
            />
          </List>

          {!status.energyplus_exe.exists && (
            <Box
              mt={2} p={2}
              sx={{ bgcolor:"#FFF7ED", borderRadius:2, border:"1px solid #FED7AA" }}
            >
              <Stack direction="row" spacing={1} alignItems="flex-start">
                <InfoOutlinedIcon sx={{ color:"#EA580C", mt:0.2, flexShrink:0 }} />
                <Box>
                  <Typography variant="body2" fontWeight={700} color="#C2410C">
                    How to install EnergyPlus
                  </Typography>
                  <Typography variant="body2" color="#92400E" mt={0.5} lineHeight={1.8}>
                    1. Download from{" "}
                    <a href="https://energyplus.net/downloads" target="_blank" rel="noreferrer"
                       style={{ color:"#2563EB" }}>
                      energyplus.net/downloads
                    </a>{" "}
                    — choose <strong>Windows 64-bit</strong>, version <strong>23.1+</strong>.<br />
                    2. Install to <code style={{ background:"#FEE2E2", padding:"0 4px", borderRadius:3 }}>
                      C:\EnergyPlusV23-1-0\
                    </code> (or update the path in <code>energyplus/config.py</code>).<br />
                    3. Restart the backend server and click <strong>Start Simulation</strong> again.
                  </Typography>
                </Box>
              </Stack>
            </Box>
          )}
        </Paper>
      )}

      {/* Running progress */}
      {loading && (
        <Paper className="fade-in" sx={{ p:3, mb:3, border:"1px solid #E2E8F0" }}>
          <Stack direction="row" spacing={1.5} alignItems="center" mb={1.5}>
            <CircularProgress size={20} />
            <Typography fontWeight={600}>Running EnergyPlus simulation…</Typography>
          </Stack>
          <LinearProgress />
          <Typography variant="body2" color="text.secondary" mt={1.5}>
            This may take 30–120 seconds depending on the IDF complexity.
            Do not close the browser tab.
          </Typography>
        </Paper>
      )}

      {/* ── Structured error panel ─────────────────────── */}
      {simError && (
        <Paper
          className="fade-in"
          sx={{
            p: 3, mb: 3,
            border: "1px solid #FECACA",
            bgcolor: "#FEF2F2",
          }}
        >
          <Stack direction="row" spacing={1.5} alignItems="flex-start">
            <ErrorOutlineIcon sx={{ color:"#EF4444", mt:0.3, flexShrink:0, fontSize:28 }} />
            <Box flexGrow={1}>
              <Stack direction="row" justifyContent="space-between" alignItems="center" flexWrap="wrap" gap={1}>
                <Typography variant="h6" fontWeight={700} color="#B91C1C">
                  Simulation Failed
                </Typography>
                <Chip
                  label={simError.code ?? "ERROR"}
                  size="small"
                  sx={{ bgcolor:"#FEE2E2", color:"#B91C1C", fontWeight:700, fontFamily:"monospace" }}
                />
              </Stack>

              <Typography variant="body2" mt={1} color="#7F1D1D" lineHeight={1.8}>
                {simError.message}
              </Typography>

              {simError.diagnosis && (
                <Box mt={1.5} p={1.5} sx={{ bgcolor:"#FFF7ED", borderRadius:2, border:"1px solid #FED7AA" }}>
                  <Stack direction="row" spacing={1} alignItems="flex-start">
                    <InfoOutlinedIcon sx={{ color:"#EA580C", fontSize:18, mt:0.2, flexShrink:0 }} />
                    <Box>
                      <Typography variant="body2" color="#92400E" lineHeight={1.7}>
                        <strong>Diagnosis:</strong> {simError.diagnosis}
                      </Typography>
                      {/* Show auto-restore notice for thermostat errors */}
                      {(simError.diagnosis?.includes("THERMOSTAT ERROR") ||
                        simError.diagnosis?.includes("heating setpoint is higher")) && (
                        <Box
                          mt={1.5} p={1.5}
                          sx={{ bgcolor:"#F0FDF4", borderRadius:2, border:"1px solid #BBF7D0" }}
                        >
                          <Stack direction="row" spacing={1} alignItems="flex-start">
                            <CheckCircleIcon sx={{ color:"#22C55E", fontSize:16, mt:0.2, flexShrink:0 }} />
                            <Typography variant="body2" color="#15803D" lineHeight={1.7}>
                              <strong>Auto-fixed:</strong> The IDF file has been restored to the baseline.
                              Click <strong>Start Simulation</strong> again — it should now succeed.
                            </Typography>
                          </Stack>
                        </Box>
                      )}
                    </Box>
                  </Stack>
                </Box>
              )}

              {/* Missing files list */}
              {simError.missing?.length > 0 && (
                <Box mt={2}>
                  <Typography variant="subtitle2" fontWeight={700} color="#B91C1C" mb={1}>
                    Missing files / components:
                  </Typography>
                  {simError.missing.map((m, i) => (
                    <Box
                      key={i}
                      sx={{
                        mb: 1.5, p: 2,
                        bgcolor: "#FFF1F2",
                        border: "1px solid #FECACA",
                        borderRadius: 2,
                      }}
                    >
                      <Stack direction="row" spacing={1} alignItems="center" mb={0.5}>
                        <FolderOpenIcon sx={{ color:"#EF4444", fontSize:18 }} />
                        <Typography variant="body2" fontWeight={700} color="#991B1B">
                          {m.item}
                        </Typography>
                      </Stack>
                      <Typography
                        variant="caption"
                        sx={{ fontFamily:"monospace", color:"#6B7280", display:"block", mb:0.5 }}
                      >
                        {m.path}
                      </Typography>
                      <Typography variant="body2" color="#374151" lineHeight={1.7}>
                        ✅ Fix: {m.fix}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              )}

              {/* Terminal output */}
              <TerminalBlock label="stdout" content={simError.stdout} />
              <TerminalBlock label="stderr" content={simError.stderr} />

              {/* Quick-help for NETWORK_ERROR */}
              {simError.code === "NETWORK_ERROR" && (
                <Box mt={2} p={2} sx={{ bgcolor:"#EFF6FF", borderRadius:2, border:"1px solid #BFDBFE" }}>
                  <Typography variant="body2" fontWeight={700} color="#1E40AF" mb={0.5}>
                    Backend not reachable — quick checks:
                  </Typography>
                  <Typography variant="body2" color="#1E3A8A" lineHeight={1.9}>
                    1. Is the FastAPI server running?{" "}
                    <code style={{ background:"#DBEAFE", padding:"0 4px", borderRadius:3 }}>
                      python main.py
                    </code><br />
                    2. Is it on port <strong>8000</strong>?
                    Open{" "}
                    <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer"
                       style={{ color:"#2563EB" }}>
                      localhost:8000/docs
                    </a>{" "}
                    to verify.<br />
                    3. Check CORS — the backend allows <code>localhost:5173</code>.
                  </Typography>
                </Box>
              )}
            </Box>
          </Stack>
        </Paper>
      )}

      {/* Simulation success summary */}
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
              EnergyPlus completed a full annual simulation, producing{" "}
              {simResults.rows} hourly rows across{" "}
              {simResults.columns?.length ?? 0} output variables.
            </Typography>
          </Paper>
        </>
      )}

      {/* Charts section */}
      <Typography variant="h5" fontWeight={700} mb={1}>
        Simulation Data Charts
      </Typography>
      <Typography variant="body2" color="text.secondary" mb={3}>
        Charts read from the latest simulation CSV report in{" "}
        <code style={{ background:"#F1F5F9", padding:"2px 6px", borderRadius:4 }}>
          energyplus/reports/savings_report.csv
        </code>
      </Typography>

      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} lg={8}><EnergyChart /></Grid>
        <Grid item xs={12} lg={4}><OccupancyChart /></Grid>
      </Grid>

      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} lg={6}><PMVChart /></Grid>
        <Grid item xs={12} lg={6}><SetpointChart /></Grid>
      </Grid>

      <ClosedLoopReport />
    </DashboardLayout>
  );
}
