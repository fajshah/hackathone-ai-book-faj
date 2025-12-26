# Architecture Lock - Docusaurus + Separate Auth

## Current Architecture State (Locked)

### Docusaurus Documentation Site
- **Location**: `frontend/text-book/`
- **URL**: http://localhost:3000
- **Purpose**: Pure documentation and content delivery
- **Technology**: Docusaurus with @docusaurus/preset-classic
- **UI**: Default classic theme with proper styling
- **No authentication**: Completely isolated from auth functionality

### Authentication Backend Service
- **Location**: `backend/`
- **URL**: http://localhost:8001
- **Purpose**: User authentication and profile management
- **Technology**: FastAPI backend service
- **API Endpoints**: `/api/auth/*` and `/api/content/*`
- **No UI integration**: Backend-only service

## Architecture Constraints (Locked)

### Docusaurus Site Rules
1. **Content Only**: Docusaurus must only serve documentation content
2. **No Auth Integration**: Authentication code must never touch Docusaurus
3. **Preserve Classic UI**: Maintain default @docusaurus/preset-classic styling
4. **No Global Styles**: No external CSS that could override theme styles
5. **Documentation Focus**: Only documentation-related features allowed

### Auth Service Rules
1. **Backend Only**: Authentication remains API-only service
2. **Separate Deployment**: Auth service runs independently
3. **API Interface**: Only provides endpoints for external consumption
4. **No UI Components**: No frontend UI in Docusaurus codebase

## Forbidden Operations
- ❌ Adding auth components to Docusaurus
- ❌ Including auth routes in Docusaurus
- ❌ Adding global CSS that affects Docusaurus theme
- ❌ Installing auth-related dependencies in Docusaurus
- ❌ Creating auth UI pages in Docusaurus directory
- ❌ Modifying Docusaurus config to include auth features

## Allowed Operations
- ✅ Adding documentation content to Docusaurus
- ✅ Updating documentation pages and blog posts
- ✅ Maintaining Docusaurus theme and styling
- ✅ Improving documentation search and navigation
- ✅ Adding documentation-specific plugins
- ✅ Enhancing content delivery in Docusaurus

## Integration Pattern
If future integration is needed, it must be done through:
1. External auth application (separate Next.js app)
2. API calls to backend service
3. Never direct integration with Docusaurus codebase

## Verification Checklist
Before any changes, verify:
- [ ] Docusaurus site runs independently
- [ ] No auth code in `frontend/text-book/` directory
- [ ] Docusaurus uses default classic theme
- [ ] Auth service runs separately at different port
- [ ] No cross-dependencies between systems