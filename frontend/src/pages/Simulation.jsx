import { useState, useEffect } from "react";
import {
  Box, Paper, Typography, Grid, Button, Stack,
  Chip, LinearProgress, CircularProgress, Divider,
  Alert, List, ListItem, ListItemIcon, ListItemText,
  Collapse, Tooltip, Tab, Tabs,
} from "@mui/material";

import PlayArrowIcon      from "@mui/icons-material/PlayArrow";
import AutoModeIcon       from "@mui/icons-material/AutoMode";
import CheckCircleIcon    from "@mui/icons-material/CheckCircle";
import DescriptionIcon    from "@mui/icons-material/Description";
import TableRowsIcon      from "@mui/icons-material/TableRows";
import ViewColumnIcon     from "@mui/icons-material/ViewColumn";
import SmartToyIcon       from "@mui/icons-material/SmartToy";
import BoltIcon           from "@mui/icons-material/Bolt";
import ErrorOutlinedIcon  from "@mui/icons-material/ErrorOutlined";
import WarningAmberIcon   from "@mui/icons-material/WarningAmber";
import CheckIcon          from "@mui/icons-material/Check";
import CloseIcon          from "@mui/icons-material/Close";
import InfoOutlinedIcon   from "@mui/icons-material/InfoOutlined";
import ContentCopyIcon    from "@mui/icons-material/ContentCopy";
import ExpandMoreIcon     from "@mui/icons-material/ExpandMore";
import ExpandLessIcon     from "@mui/icons-material/ExpandLess";
import FolderOpenIcon     from "@mui/icons-material/FolderOpen";
import TerminalIcon       from "@mui/icons-material/Terminal";
import ThermostatIcon     from "@mui/icons-material/Thermostat";
import Co2Icon            from "@mui/icons-material/Co2";
import PeopleIcon         from "@mui/icons-material/People";
import LeafIcon           from "@mui/icons-material/EnergySavingsLeaf";

import DashboardLayout   from "../layouts/DashboardLayout";
import EnergyChart       from "../components/EnergyChart";
import PMVChart          from "../components/PMVChart";
import SetpointChart     from "../components/SetpointChart";
import OccupancyChart    from "../components/OccupancyChart";
import ClosedLoopReport  from "../components/ClosedLoopReport";
import {
  runSimulation, runClosedLoop,
  getLiveMetrics, evaluatePerformance,
} from "../services/simulationService";
import api from "../api/api";

// ── helpers ──────────────────────────────────────────────
function StatusBadge({ ok, label, path }) {
  return (
    <ListItem dense disableGutters>
      <ListItemIcon sx={{ minWidth: 32 }}>
        {ok ? <CheckIcon sx={{ color:"#22C55E", fontSize:18 }} />
            : <CloseIcon sx={{ color:"#EF4444", fontSize:18 }} />}
      </ListItemIcon>
      <ListItemText
        primary={<Typography variant="body2" fontWeight={600}>{label}</Typography>}
        secondary={<Typography variant="caption" sx={{ fontFamily:"monospace", color: ok?"#64748B":"#EF4444" }}>{path}</Typography>}
      />
    </ListItem>
  );
}

function CopyBtn({ text }) {
  const [c, setC] = useState(false);
  return (
    <Tooltip title={c ? "Copied!" : "Copy"}>
      <Button size="small" onClick={() => { navigator.clipboard.writeText(text); setC(true); setTimeout(()=>setC(false),2000); }}
        startIcon={<ContentCopyIcon sx={{fontSize:14}}/>} sx={{fontSize:11,py:0.3,px:1}}>
        {c ? "Copied" : "Copy"}
      </Button>
    </Tooltip>
  );
}

function TermBlock({ label, content }) {
  const [open, setOpen] = useState(false);
  if (!content?.trim()) return null;
  return (
    <Box mt={1.5}>
      <Button size="small" startIcon={open?<ExpandLessIcon/>:<ExpandMoreIcon/>}
        endIcon={<TerminalIcon sx={{fontSize:14}}/>}
        onClick={()=>setOpen(!open)} sx={{fontSize:12,color:"#64748B"}}>
        {open?"Hide":"Show"} {label}
      </Button>
      <Collapse in={open}>
        <Box sx={{ mt:1, p:2, bgcolor:"#0F172A", borderRadius:2, fontFamily:"monospace",
          fontSize:12, color:"#94A3B8", whiteSpace:"pre-wrap", maxHeight:240, overflowY:"auto" }}>
          <Stack direction="row" justifyContent="flex-end" mb={1}><CopyBtn text={content}/></Stack>
          {content}
        </Box>
      </Collapse>
    </Box>
  );
}

// ── Metric chip ───────────────────────────────────────────
function MetricChip({ icon, label, value, color = "#2563EB" }) {
  return (
    <Paper elevation={0} sx={{ p:1.5, border:"1px solid #E2E8F0", borderRadius:3, minWidth:110 }}>
      <Stack direction="row" spacing={1} alignItems="center">
        <Box sx={{ color }}>{icon}</Box>
        <Box>
          <Typography variant="caption" color="text.secondary" display="block">{label}</Typography>
          <Typography variant="subtitle2" fontWeight={700}>{value ?? "—"}</Typography>
        </Box>
      </Stack>
    </Paper>
  );
}

// ── Page ─────────────────────────────────────────────────
export default function Simulation() {
  const [loading,     setLoading]     = useState(false);
  const [clLoading,   setClLoading]   = useState(false);
  const [result,      setResult]      = useState(null);
  const [clResult,    setClResult]    = useState(null);
  const [simError,    setSimError]    = useState(null);
  const [status,      setStatus]      = useState(null);
  const [statusLoad,  setStatusLoad]  = useState(true);
  const [metrics,     setMetrics]     = useState(null);
  const [flags,       setFlags]       = useState(null);
  const [tab,         setTab]         = useState(0);

  useEffect(() => {
    api.get("/simulation/status")
      .then(r => setStatus(r.data)).catch(()=>{})
      .finally(()=>setStatusLoad(false));

    // Load live metrics & performance flags
    getLiveMetrics().then(setMetrics).catch(()=>{});
    evaluatePerformance().then(setFlags).catch(()=>{});
  }, []);

  const refreshMetrics = () => {
    getLiveMetrics().then(setMetrics).catch(()=>{});
    evaluatePerformance().then(setFlags).catch(()=>{});
  };

  const startSingle = async () => {
    setLoading(true); setSimError(null); setResult(null);
    try {
      const d = await runSimulation();
      if (d?.status === "error") setSimError(d);
      else { setResult(d); refreshMetrics(); }
    } catch (err) {
      setSimError({
        status:"error", code:"NETWORK_ERROR",
        message: err?.response?.data?.detail
          ? (typeof err.response.data.detail==="string" ? err.response.data.detail : JSON.stringify(err.response.data.detail))
          : "Cannot reach the backend — is the FastAPI server running on port 8000?",
      });
    } finally { setLoading(false); }
  };

  const startClosedLoop = async () => {
    setClLoading(true); setSimError(null); setClResult(null);
    try {
      const d = await runClosedLoop(2);
      if (d?.status === "error") setSimError(d);
      else { setClResult(d); refreshMetrics();
        // reload charts
        api.get("/simulation/status").then(r=>setStatus(r.data)).catch(()=>{});
      }
    } catch (err) {
      setSimError({
        status:"error", code:"NETWORK_ERROR",
        message:"Closed-loop request failed — see console for details.",
      });
    } finally { setClLoading(false); }
  };

  const ready = status?.ready_to_simulate;
  const simResults = result?.results;

  return (
    <DashboardLayout>
      {/* Hero */}
      <Paper className="fade-in" sx={{ p:{xs:3,md:4}, mb:4,
        background:"linear-gradient(135deg,#2563EB,#06B6D4)", color:"white" }}>
        <Stack direction={{xs:"column",md:"row"}} justifyContent="space-between"
          alignItems={{md:"center"}} gap={2}>
          <Box>
            <Stack direction="row" spacing={1.5} alignItems="center" mb={0.5}>
              <BoltIcon sx={{fontSize:30}}/>
              <Typography variant="h4" fontWeight={800}>Building Simulation</Typography>
            </Stack>
            <Typography sx={{opacity:0.85}}>
              Req 1: EnergyPlus engine &nbsp;·&nbsp;
              Req 2: MCP + OSS LLM &nbsp;·&nbsp;
              Req 3: AI Closed-Loop Optimisation
            </Typography>
          </Box>
          <Stack direction="row" spacing={2} flexWrap="wrap">
            <Button variant="contained" size="large"
              startIcon={loading?<CircularProgress size={18} color="inherit"/>:<PlayArrowIcon/>}
              onClick={startSingle} disabled={loading||clLoading}
              sx={{bgcolor:"rgba(255,255,255,0.2)","&:hover":{bgcolor:"rgba(255,255,255,0.35)"},minWidth:160}}>
              {loading ? "Running…" : "Single Run"}
            </Button>
            <Button variant="contained" size="large"
              startIcon={clLoading?<CircularProgress size={18} color="inherit"/>:<AutoModeIcon/>}
              onClick={startClosedLoop} disabled={loading||clLoading}
              sx={{bgcolor:"rgba(255,255,255,0.3)","&:hover":{bgcolor:"rgba(255,255,255,0.45)"},minWidth:180}}>
              {clLoading ? "Optimising…" : "Run Closed Loop (AI)"}
            </Button>
          </Stack>
        </Stack>
      </Paper>

      {/* Requirement badges */}
      <Stack direction="row" spacing={1.5} mb={3} flexWrap="wrap" gap={1}>
        <Chip label="Req 1 — EnergyPlus Engine" color="primary"  size="small" icon={<BoltIcon/>}/>
        <Chip label="Req 2 — OSS LLM + MCP Server" color="secondary" size="small" icon={<SmartToyIcon/>}/>
        <Chip label="Req 3 — Closed-Loop: Feedback → Reasoning → ECMs → Injection"
          color="success" size="small" icon={<AutoModeIcon/>}/>
      </Stack>

      {/* Status panel */}
      {!statusLoad && status && (
        <Paper className="fade-in" sx={{ p:3, mb:3, border:"1px solid",
          borderColor: ready?"#BBF7D0":"#FECACA", bgcolor: ready?"#F0FDF4":"#FEF2F2" }}>
          <Stack direction="row" spacing={1.5} alignItems="center" mb={1.5}>
            {ready ? <CheckCircleIcon sx={{color:"#22C55E"}}/>
                   : <WarningAmberIcon sx={{color:"#EF4444"}}/>}
            <Typography variant="h6" fontWeight={700}
              sx={{color: ready?"#15803D":"#B91C1C"}}>
              {ready ? "EnergyPlus is ready" : "EnergyPlus is NOT ready — setup required"}
            </Typography>
          </Stack>
          <List dense disablePadding>
            <StatusBadge ok={status.energyplus_exe.exists}  label="EnergyPlus executable" path={status.energyplus_exe.path}/>
            <StatusBadge ok={status.idf_file.exists}        label="Building IDF file"      path={status.idf_file.path}/>
            <StatusBadge ok={status.weather_file.exists}    label="Weather EPW file"       path={status.weather_file.path}/>
            <StatusBadge ok={status.report_csv.exists}      label="Simulation CSV report"  path={status.report_csv.path}/>
          </List>
          {!status.energyplus_exe.exists && (
            <Box mt={2} p={2} sx={{bgcolor:"#FFF7ED",borderRadius:2,border:"1px solid #FED7AA"}}>
              <Stack direction="row" spacing={1} alignItems="flex-start">
                <InfoOutlinedIcon sx={{color:"#EA580C",mt:0.2,flexShrink:0}}/>
                <Box>
                  <Typography variant="body2" fontWeight={700} color="#C2410C">How to install EnergyPlus</Typography>
                  <Typography variant="body2" color="#92400E" mt={0.5} lineHeight={1.8}>
                    1. Download from{" "}
                    <a href="https://energyplus.net/downloads" target="_blank" rel="noreferrer" style={{color:"#2563EB"}}>
                      energyplus.net/downloads
                    </a>{" "}— Windows 64-bit, version 23.1+<br/>
                    2. Install to <code style={{background:"#FEE2E2",padding:"0 4px",borderRadius:3}}>C:\EnergyPlusV23-1-0\</code>{" "}
                    (or update <code>energyplus/config.py</code>)<br/>
                    3. Restart the backend and click <strong>Single Run</strong>.
                  </Typography>
                </Box>
              </Stack>
            </Box>
          )}
        </Paper>
      )}

      {/* Progress bars */}
      {(loading||clLoading) && (
        <Paper className="fade-in" sx={{p:3,mb:3,border:"1px solid #E2E8F0"}}>
          <Stack direction="row" spacing={1.5} alignItems="center" mb={1.5}>
            <CircularProgress size={20}/>
            <Typography fontWeight={600}>
              {clLoading ? "Running AI closed-loop optimisation (EnergyPlus → LLM → ECMs → IDF)…"
                         : "Running EnergyPlus simulation…"}
            </Typography>
          </Stack>
          <LinearProgress/>
          {clLoading && (
            <Typography variant="body2" color="text.secondary" mt={1.5}>
              Req 3 in progress: EnergyPlus runs → metrics extracted → LLM evaluates
              comfort/energy/carbon targets → optimal ECMs computed → setpoints injected
              back into IDF for next iteration. This may take 1–3 minutes.
            </Typography>
          )}
        </Paper>
      )}

      {/* Error panel */}
      {simError && (
        <Paper className="fade-in" sx={{p:3,mb:3,border:"1px solid #FECACA",bgcolor:"#FEF2F2"}}>
          <Stack direction="row" spacing={1.5} alignItems="flex-start">
            <ErrorOutlinedIcon sx={{color:"#EF4444",mt:0.3,flexShrink:0,fontSize:28}}/>
            <Box flexGrow={1}>
              <Stack direction="row" justifyContent="space-between" alignItems="center" flexWrap="wrap" gap={1}>
                <Typography variant="h6" fontWeight={700} color="#B91C1C">Simulation Failed</Typography>
                <Chip label={simError.code??"ERROR"} size="small"
                  sx={{bgcolor:"#FEE2E2",color:"#B91C1C",fontWeight:700,fontFamily:"monospace"}}/>
              </Stack>
              <Typography variant="body2" mt={1} color="#7F1D1D" lineHeight={1.8}>{simError.message}</Typography>
              {simError.diagnosis && (
                <Box mt={1.5} p={1.5} sx={{bgcolor:"#FFF7ED",borderRadius:2,border:"1px solid #FED7AA"}}>
                  <Stack direction="row" spacing={1} alignItems="flex-start">
                    <InfoOutlinedIcon sx={{color:"#EA580C",fontSize:18,mt:0.2,flexShrink:0}}/>
                    <Box>
                      <Typography variant="body2" color="#92400E" lineHeight={1.7}>
                        <strong>Diagnosis:</strong> {simError.diagnosis}
                      </Typography>
                      {(simError.diagnosis?.includes("THERMOSTAT") || simError.diagnosis?.includes("heating setpoint")) && (
                        <Box mt={1.5} p={1.5} sx={{bgcolor:"#F0FDF4",borderRadius:2,border:"1px solid #BBF7D0"}}>
                          <Stack direction="row" spacing={1} alignItems="flex-start">
                            <CheckCircleIcon sx={{color:"#22C55E",fontSize:16,mt:0.2,flexShrink:0}}/>
                            <Typography variant="body2" color="#15803D" lineHeight={1.7}>
                              <strong>Auto-fixed:</strong> IDF restored from baseline. Click <strong>Single Run</strong> again.
                            </Typography>
                          </Stack>
                        </Box>
                      )}
                    </Box>
                  </Stack>
                </Box>
              )}
              {simError.missing?.map((m,i) => (
                <Box key={i} sx={{mt:1.5,p:2,bgcolor:"#FFF1F2",border:"1px solid #FECACA",borderRadius:2}}>
                  <Stack direction="row" spacing={1} alignItems="center" mb={0.5}>
                    <FolderOpenIcon sx={{color:"#EF4444",fontSize:18}}/>
                    <Typography variant="body2" fontWeight={700} color="#991B1B">{m.item}</Typography>
                  </Stack>
                  <Typography variant="caption" sx={{fontFamily:"monospace",color:"#6B7280",display:"block",mb:0.5}}>{m.path}</Typography>
                  <Typography variant="body2" color="#374151">✅ {m.fix}</Typography>
                </Box>
              ))}
              <TermBlock label="stdout" content={simError.stdout}/>
              <TermBlock label="stderr" content={simError.stderr}/>
            </Box>
          </Stack>
        </Paper>
      )}

      {/* Closed-loop success summary */}
      {clResult && (
        <Paper className="fade-in" sx={{p:4,mb:4,border:"1px solid #BBF7D0",bgcolor:"#F0FDF4"}}>
          <Stack direction="row" spacing={2} alignItems="center">
            <CheckCircleIcon sx={{color:"#22C55E",fontSize:32}}/>
            <Box>
              <Typography variant="h6" fontWeight={700} color="#15803D">
                AI Closed-Loop Optimisation Complete
              </Typography>
              <Typography variant="body2" color="#166534">
                {clResult.iterations} iteration{clResult.iterations!==1?"s":""} completed —
                EnergyPlus → metrics → LLM ECMs → IDF forward injection
              </Typography>
            </Box>
            <Box flexGrow={1}/>
            <Chip label={`${clResult.iterations} Iterations`} color="success" icon={<AutoModeIcon/>}/>
          </Stack>
        </Paper>
      )}

      {/* Single run success */}
      {simResults && (
        <Grid container spacing={3} mb={3}>
          {[
            {icon:<DescriptionIcon sx={{fontSize:45,color:"#2563EB"}}/>, val:simResults.file,             label:"Output File"},
            {icon:<TableRowsIcon   sx={{fontSize:45,color:"#22C55E"}}/>, val:simResults.rows,             label:"Rows Simulated"},
            {icon:<ViewColumnIcon  sx={{fontSize:45,color:"#F59E0B"}}/>, val:simResults.columns?.length??0, label:"Output Variables"},
          ].map((c,i)=>(
            <Grid item xs={12} md={4} key={i}>
              <Paper className="hover-lift fade-in" sx={{p:3,border:"1px solid #E2E8F0",textAlign:"center"}}>
                {c.icon}
                <Typography variant={typeof c.val==="string"?"h6":"h4"} fontWeight={800} mt={2} noWrap={typeof c.val==="string"}>{c.val}</Typography>
                <Typography color="text.secondary">{c.label}</Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Live Metrics row (Req 3 — Feedback) */}
      {metrics && (
        <Paper className="fade-in" sx={{p:3,mb:3,border:"1px solid #E2E8F0"}}>
          <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="h6" fontWeight={700}>Live Building Metrics (Req 3 — Continuous Feedback)</Typography>
            {flags && (
              <Chip
                label={flags.all_targets_met ? "All Targets Met" : `${flags.issues?.length} Issues`}
                color={flags.all_targets_met ? "success" : "warning"}
                size="small"
              />
            )}
          </Stack>
          <Stack direction="row" spacing={2} flexWrap="wrap" gap={2}>
            <MetricChip icon={<ThermostatIcon/>} label="Indoor Temp" value={metrics.indoor_temperature!=null?`${metrics.indoor_temperature}°C`:null} color="#2563EB"/>
            <MetricChip icon={<ThermostatIcon/>} label="PMV" value={metrics.pmv} color={Math.abs(metrics.pmv||0)<=0.5?"#22C55E":"#EF4444"}/>
            <MetricChip icon={<ThermostatIcon/>} label="PPD" value={metrics.ppd!=null?`${metrics.ppd}%`:null} color={(metrics.ppd||0)<=10?"#22C55E":"#EF4444"}/>
            <MetricChip icon={<Co2Icon/>}        label="CO₂ (ppm)" value={metrics.co2} color={(metrics.co2||0)<=1000?"#22C55E":"#EF4444"}/>
            <MetricChip icon={<PeopleIcon/>}     label="Occupancy" value={metrics.occupancy!=null?`${metrics.occupancy}%`:null} color="#F59E0B"/>
            <MetricChip icon={<BoltIcon/>}       label="Total Energy" value={metrics.total_energy!=null?`${metrics.total_energy} kWh`:null} color="#2563EB"/>
            <MetricChip icon={<LeafIcon/>}       label="Carbon" value={metrics.carbon_intensity!=null?`${metrics.carbon_intensity} gCO₂/kWh`:null} color="#22C55E"/>
          </Stack>
          {flags?.issues?.length > 0 && (
            <Box mt={2} p={2} sx={{bgcolor:"#FFF7ED",borderRadius:2,border:"1px solid #FED7AA"}}>
              <Typography variant="subtitle2" fontWeight={700} color="#92400E" mb={1}>
                Performance Issues (Req 3 — Reasoning targets):
              </Typography>
              {flags.issues.map((issue,i)=>(
                <Typography key={i} variant="body2" color="#92400E">• {issue}</Typography>
              ))}
            </Box>
          )}
        </Paper>
      )}

      {/* Tabs: Charts | Closed-Loop */}
      <Box sx={{borderBottom:"1px solid #E2E8F0", mb:3}}>
        <Tabs value={tab} onChange={(_,v)=>setTab(v)}>
          <Tab label="Simulation Data Charts" />
          <Tab label="AI Closed-Loop Results" />
        </Tabs>
      </Box>

      {tab === 0 && (
        <>
          <Typography variant="body2" color="text.secondary" mb={3}>
            All charts read from <code style={{background:"#F1F5F9",padding:"2px 6px",borderRadius:4}}>
              energyplus/reports/savings_report.csv
            </code>
          </Typography>
          <Grid container spacing={3} mb={3}>
            <Grid item xs={12} lg={8}><EnergyChart/></Grid>
            <Grid item xs={12} lg={4}><OccupancyChart/></Grid>
          </Grid>
          <Grid container spacing={3} mb={3}>
            <Grid item xs={12} lg={6}><PMVChart/></Grid>
            <Grid item xs={12} lg={6}><SetpointChart/></Grid>
          </Grid>
        </>
      )}

      {tab === 1 && <ClosedLoopReport/>}
    </DashboardLayout>
  );
}
