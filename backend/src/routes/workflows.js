import express from 'express';
import { supabase } from '../config/supabase.js';
import { authenticateToken } from '../middleware/auth.js';

const router = express.Router();

router.get('/', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('workflows_workflow')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) throw error;

    res.json({ workflows: data || [] });
  } catch (error) {
    console.error('Get workflows error:', error);
    res.status(500).json({ error: 'Failed to fetch workflows' });
  }
});

router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const { data, error } = await supabase
      .from('workflows_workflow')
      .select('*')
      .eq('id', id)
      .maybeSingle();

    if (error) throw error;
    if (!data) {
      return res.status(404).json({ error: 'Workflow not found' });
    }

    res.json({ workflow: data });
  } catch (error) {
    console.error('Get workflow error:', error);
    res.status(500).json({ error: 'Failed to fetch workflow' });
  }
});

router.post('/', authenticateToken, async (req, res) => {
  try {
    const { name, description, definition } = req.body;

    if (!name) {
      return res.status(400).json({ error: 'Name is required' });
    }

    const { data, error } = await supabase
      .from('workflows_workflow')
      .insert([{
        name,
        description,
        definition: definition || {},
        is_active: true,
        created_by_id: req.user.id
      }])
      .select()
      .single();

    if (error) throw error;

    res.status(201).json({ workflow: data });
  } catch (error) {
    console.error('Create workflow error:', error);
    res.status(500).json({ error: 'Failed to create workflow' });
  }
});

router.put('/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;

    const { data, error } = await supabase
      .from('workflows_workflow')
      .update(updates)
      .eq('id', id)
      .select()
      .single();

    if (error) throw error;

    res.json({ workflow: data });
  } catch (error) {
    console.error('Update workflow error:', error);
    res.status(500).json({ error: 'Failed to update workflow' });
  }
});

router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;

    const { error } = await supabase
      .from('workflows_workflow')
      .delete()
      .eq('id', id);

    if (error) throw error;

    res.json({ message: 'Workflow deleted successfully' });
  } catch (error) {
    console.error('Delete workflow error:', error);
    res.status(500).json({ error: 'Failed to delete workflow' });
  }
});

export default router;
