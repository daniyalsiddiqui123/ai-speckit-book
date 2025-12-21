# Backend API Configuration

To connect the chatbot to your backend API in production, you need to set the appropriate environment variable.

## For Vercel Deployment

Set the `NEXT_PUBLIC_API_BASE_URL` environment variable in your Vercel project settings:

1. Go to your Vercel dashboard
2. Navigate to your project
3. Go to Settings → Environment Variables
4. Add a new variable:
   - Key: `NEXT_PUBLIC_API_BASE_URL`
   - Value: Your backend URL (e.g., `https://your-app-name.up.railway.app` or `https://your-app-name.onrender.com`)

## For Other Deployments

Set the `REACT_APP_API_BASE_URL` environment variable during the build process.

## Example Values

- Railway: `https://your-app-name.up.railway.app`
- Render: `https://your-app-name.onrender.com`
- Other hosting: `https://your-domain.com`

Make sure your backend is deployed and accessible before setting this variable.