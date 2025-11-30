import express from 'express';
import { supabase } from '../config/supabase.js';
import { authenticateToken } from '../middleware/auth.js';

const router = express.Router();

router.get('/', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('agents_agenttask')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) throw error;

    res.json({ agents: data || [] });
  } catch (error) {
    console.error('Get agents error:', error);
    res.status(500).json({ error: 'Failed to fetch agents' });
  }
});

router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const { data, error } = await supabase
      .from('agents_agenttask')
      .select('*')
      .eq('id', id)
      .maybeSingle();

    if (error) throw error;
    if (!data) {
      return res.status(404).json({ error: 'Agent not found' });
    }

    res.json({ agent: data });
  } catch (error) {
    console.error('Get agent error:', error);
    res.status(500).json({ error: 'Failed to fetch agent' });
  }
});

router.post('/', authenticateToken, async (req, res) => {
  try {
    const { title, description, agent_type, priority } = req.body;

    if (!title || !agent_type) {
      return res.status(400).json({ error: 'Title and agent_type are required' });
    }

    const { data, error } = await supabase
      .from('agents_agenttask')
      .insert([{
        title,
        description,
        agent_type,
        priority: priority || 'medium',
        status: 'pending',
        assigned_to_id: req.user.id
      }])
      .select()
      .single();

    if (error) throw error;

    res.status(201).json({ agent: data });
  } catch (error) {
    console.error('Create agent error:', error);
    res.status(500).json({ error: 'Failed to create agent' });
  }
});

router.put('/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;

    const { data, error } = await supabase
      .from('agents_agenttask')
      .update(updates)
      .eq('id', id)
      .select()
      .single();

    if (error) throw error;

    res.json({ agent: data });
  } catch (error) {
    console.error('Update agent error:', error);
    res.status(500).json({ error: 'Failed to update agent' });
  }
});

router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;

    const { error } = await supabase
      .from('agents_agenttask')
      .delete()
      .eq('id', id);

    if (error) throw error;

    res.json({ message: 'Agent deleted successfully' });
  } catch (error) {
    console.error('Delete agent error:', error);
    res.status(500).json({ error: 'Failed to delete agent' });
  }
});

export default router;
