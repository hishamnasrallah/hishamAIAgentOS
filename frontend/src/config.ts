export const config = {
  apiUrl: import.meta.env.VITE_API_URL || window.location.origin,
  supabaseUrl: import.meta.env.VITE_SUPABASE_URL || '',
  supabaseAnonKey: import.meta.env.VITE_SUPABASE_ANON_KEY || '',
};

export default config;
