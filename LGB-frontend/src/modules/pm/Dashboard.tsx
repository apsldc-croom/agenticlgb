import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Box, Typography, CircularProgress, Alert, Grid, Paper, 
  LinearProgress, Card, CardContent, Chip 
} from '@mui/material';
import ReactECharts from 'echarts-for-react';
import { pmApi } from '../../services/pm.api';
import type { ProjectDashboard } from './types';

const PMDashboard: React.FC = () => {
  // Using the slug 'lgb-platform' as it's the default seeded project
  const { data, isLoading, error } = useQuery<ProjectDashboard>({
    queryKey: ['pm-dashboard', 'lgb-platform'],
    queryFn: () => pmApi.getProjectDashboard('lgb-platform'),
    retry: 1,
  });

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !data) {
    return (
      <Alert severity="error">
        Failed to load Project Management Dashboard. Make sure the backend is running and you are authenticated.
      </Alert>
    );
  }

  const statusPieOption = {
    tooltip: { trigger: 'item' },
    series: [
      {
        name: 'Task Status',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#1e1e1e',
          borderWidth: 2
        },
        label: { show: false, position: 'center' },
        emphasis: {
          label: { show: true, fontSize: 16, fontWeight: 'bold' }
        },
        data: Object.entries(data.status_breakdown).map(([name, value]) => ({
          value,
          name: name.replace('_', ' ').toUpperCase(),
        })),
      }
    ]
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom color="primary">
        Project Tracker: {data.project}
      </Typography>
      
      <Grid container spacing={3}>
        {/* KPI Cards */}
        <Grid size={{ xs: 12, md: 3 }}>
          <Card variant="outlined">
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Overall Progress</Typography>
              <Typography variant="h3">{data.overall_progress}%</Typography>
              <LinearProgress variant="determinate" value={data.overall_progress} sx={{ mt: 2, height: 8, borderRadius: 4 }} />
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, md: 3 }}>
          <Card variant="outlined">
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Total Tasks</Typography>
              <Typography variant="h3">{data.total_tasks}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, md: 3 }}>
          <Card variant="outlined">
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Open Tech Debt</Typography>
              <Typography variant="h3" color={data.open_tech_debt > 0 ? 'error' : 'success'}>
                {data.open_tech_debt}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, md: 3 }}>
          <Card variant="outlined">
            <CardContent>
              <Typography color="textSecondary" gutterBottom>AI Insights</Typography>
              <Typography variant="h3" color="info.main">{data.unresolved_insights}</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Status Breakdown Chart */}
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper sx={{ p: 2, height: '100%' }} variant="outlined">
            <Typography variant="h6" gutterBottom>Task Status</Typography>
            <ReactECharts option={statusPieOption} style={{ height: '300px' }} theme="dark" />
          </Paper>
        </Grid>

        {/* Phase Progress */}
        <Grid size={{ xs: 12, md: 8 }}>
          <Paper sx={{ p: 2, height: '100%' }} variant="outlined">
            <Typography variant="h6" gutterBottom>Phases</Typography>
            <Box sx={{ mt: 2 }}>
              {data.phases.map((phase) => (
                <Box key={phase.phase_number} sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body1">
                      Phase {phase.phase_number}: {phase.name}
                    </Typography>
                    <Box>
                      <Chip 
                        label={phase.status.replace('_', ' ')} 
                        size="small" 
                        color={phase.status === 'completed' ? 'success' : phase.status === 'in_progress' ? 'primary' : 'default'}
                        sx={{ mr: 2 }}
                      />
                      <Typography variant="body2" component="span">{phase.progress}%</Typography>
                    </Box>
                  </Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={phase.progress} 
                    color={phase.status === 'completed' ? 'success' : 'primary'}
                    sx={{ height: 6, borderRadius: 3 }}
                  />
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PMDashboard;
