import {
  Drawer,
  Box,
  Typography,
  Divider,
  List,
  ListItem,
} from "@mui/material";

function NotificationDrawer({
  open,
  onClose,
}) {
  const notifications = [
    "Simulation completed successfully.",
    "Prediction generated.",
    "Recommendation updated.",
    "Energy usage increased by 8%.",
    "Comfort score improved.",
  ];

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
    >
      <Box
        sx={{
          width: 320,
          p: 3,
        }}
      >
        <Typography
          variant="h6"
          fontWeight={700}
        >
          Notifications
        </Typography>

        <Divider sx={{ my: 2 }} />

        <List>
          {notifications.map((item, index) => (
            <ListItem key={index}>
              {item}
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  );
}

export default NotificationDrawer;