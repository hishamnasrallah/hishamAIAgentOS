# HishamOS Frontend

React + TypeScript + Vite frontend for HishamOS.

## Environment Variables

Create a `.env` file in the `frontend/` directory:

```bash
# Backend API URL
VITE_API_URL=http://localhost:8000  # For local development
# VITE_API_URL=https://your-backend.herokuapp.com  # For production
```

### How It Works

The frontend uses the `VITE_API_URL` environment variable to connect to the backend API:

- **Local Development**: `VITE_API_URL=http://localhost:8000`
- **Production (Separate Deploy)**: `VITE_API_URL=https://your-backend-domain.com`
- **Production (Monolithic)**: Leave empty, auto-detects using `window.location.origin`

## Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Deployment

### Option 1: Monolithic (with Django)

Frontend is automatically built and served by Django:

```bash
# From project root
npm run build
python manage.py collectstatic
```

Access at: `https://your-domain.com/`

### Option 2: Separate Frontend Deployment

Deploy to Vercel/Netlify/Cloudflare Pages:

1. **Vercel**:
   ```bash
   # vercel.json
   {
     "buildCommand": "npm run build",
     "outputDirectory": "dist",
     "env": {
       "VITE_API_URL": "https://your-backend-url.com"
     }
   }
   ```

2. **Netlify**:
   ```bash
   # netlify.toml
   [build]
     command = "npm run build"
     publish = "dist"
   
   [build.environment]
     VITE_API_URL = "https://your-backend-url.com"
   ```

3. **Environment Variables**:
   - Set `VITE_API_URL` to your backend URL
   - Update backend's `CORS_ALLOWED_ORIGINS` to include frontend URL

## Features

- ✅ TypeScript for type safety
- ✅ Tailwind CSS for styling
- ✅ Environment-based API configuration
- ✅ Automatic backend URL detection
- ✅ Production-ready build configuration
- ✅ Fast refresh with Vite

## Project Structure

```
frontend/
├── src/
│   ├── App.tsx           # Main application component
│   ├── config.ts         # Configuration helper
│   ├── main.tsx          # Entry point
│   └── index.css         # Global styles
├── public/               # Static assets
├── dist/                 # Build output (auto-generated)
├── .env                  # Environment variables (local)
├── .env.example          # Environment template
└── vite.config.ts        # Vite configuration
```

## Configuration

### `vite.config.ts`

```typescript
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: false,
  },
});
```

### Environment Variables

Vite exposes environment variables starting with `VITE_` to the client:

- `VITE_API_URL` - Backend API URL
- `VITE_SUPABASE_URL` - Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Supabase anonymous key

## Troubleshooting

### API Calls Go to Localhost

**Problem**: Links/buttons navigate to `localhost` instead of production backend.

**Solution**: Set the `VITE_API_URL` environment variable:
```bash
# On deployment platform
VITE_API_URL=https://your-backend-domain.com
```

### CORS Errors

**Problem**: Browser blocks API requests due to CORS.

**Solution**: Update backend CORS settings:
```python
# Backend .env
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Build Fails

**Problem**: TypeScript or build errors.

**Solution**:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json dist
npm install
npm run build
```

## Support

For deployment questions, see:
- `../QUICKSTART_DEPLOYMENT.md` - Quick deployment guide
- `../BACKEND_DEPLOYMENT.md` - Backend deployment details
- `../DEPLOYMENT.md` - General deployment guide
