import express from 'express';
import { supabase } from '../config/supabase.js';
import { authenticateToken } from '../middleware/auth.js';

const router = express.Router();

const requireAdmin = (req, res, next) => {
  if (!req.user.is_staff && !req.user.is_superuser) {
    return res.status(403).json({ error: 'Admin access required' });
  }
  next();
};

router.get('/stats', authenticateToken, requireAdmin, async (req, res) => {
  try {
    const [usersResult, agentsResult, projectsResult, workflowsResult] = await Promise.all([
      supabase.from('users').select('id', { count: 'exact', head: true }),
      supabase.from('agents_agenttask').select('id', { count: 'exact', head: true }),
      supabase.from('projects_project').select('id', { count: 'exact', head: true }),
      supabase.from('workflows_workflow').select('id', { count: 'exact', head: true })
    ]);

    res.json({
      stats: {
        users: usersResult.count || 0,
        agents: agentsResult.count || 0,
        projects: projectsResult.count || 0,
        workflows: workflowsResult.count || 0
      }
    });
  } catch (error) {
    console.error('Get stats error:', error);
    res.status(500).json({ error: 'Failed to fetch stats' });
  }
});

router.get('/users', authenticateToken, requireAdmin, async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('users')
      .select('id, username, email, is_staff, is_superuser, is_active, created_at')
      .order('created_at', { ascending: false });

    if (error) throw error;

    res.json({ users: data || [] });
  } catch (error) {
    console.error('Get users error:', error);
    res.status(500).json({ error: 'Failed to fetch users' });
  }
});

router.get('/users/:id', authenticateToken, requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;

    const { data, error } = await supabase
      .from('users')
      .select('id, username, email, is_staff, is_superuser, is_active, created_at')
      .eq('id', id)
      .maybeSingle();

    if (error) throw error;
    if (!data) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({ user: data });
  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({ error: 'Failed to fetch user' });
  }
});

router.put('/users/:id', authenticateToken, requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const { is_staff, is_superuser, is_active } = req.body;

    const updates = {};
    if (typeof is_staff !== 'undefined') updates.is_staff = is_staff;
    if (typeof is_superuser !== 'undefined') updates.is_superuser = is_superuser;
    if (typeof is_active !== 'undefined') updates.is_active = is_active;

    const { data, error } = await supabase
      .from('users')
      .update(updates)
      .eq('id', id)
      .select('id, username, email, is_staff, is_superuser, is_active, created_at')
      .single();

    if (error) throw error;

    res.json({ user: data });
  } catch (error) {
    console.error('Update user error:', error);
    res.status(500).json({ error: 'Failed to update user' });
  }
});

router.delete('/users/:id', authenticateToken, requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;

    if (id === req.user.id) {
      return res.status(400).json({ error: 'Cannot delete your own account' });
    }

    const { error } = await supabase
      .from('users')
      .delete()
      .eq('id', id);

    if (error) throw error;

    res.json({ message: 'User deleted successfully' });
  } catch (error) {
    console.error('Delete user error:', error);
    res.status(500).json({ error: 'Failed to delete user' });
  }
});

export default router;
