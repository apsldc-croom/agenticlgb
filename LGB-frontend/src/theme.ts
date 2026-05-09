import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#4dabf5', // Soft blue for focus actions
      dark: '#1769aa',
    },
    secondary: {
      main: '#f48fb1',
      dark: '#ad1457',
    },
    error: {
      main: '#f44336', // Critical alerts
    },
    warning: {
      main: '#ff9800', // Warnings (e.g., congestion approaching limits)
    },
    info: {
      main: '#29b6f6',
    },
    success: {
      main: '#4caf50', // Normal operation
    },
    background: {
      default: '#121212', // Deep dark for operational consoles
      paper: '#1e1e1e', // Slightly lighter for panels/widgets
    },
  },
  typography: {
    fontFamily: '"Roboto", "Inter", "Helvetica", "Arial", sans-serif',
    h6: {
      fontWeight: 600,
      letterSpacing: '0.05em',
      textTransform: 'uppercase', // Industrial dashboard look
      fontSize: '1.1rem',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none', // Remove default MUI dark mode elevation gradient
          border: '1px solid #333', // Sharp borders for dashboard modules
        },
      },
    },
  },
});

export default theme;
