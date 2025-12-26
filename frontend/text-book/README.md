# Physical AI & Humanoid Robotics Documentation

This is a Docusaurus documentation site for the Physical AI & Humanoid Robotics textbook. This site is strictly for documentation and content delivery only.

## Architecture Constraint
- **Documentation Only**: This site must remain purely for documentation
- **No Authentication**: Authentication functionality is completely separate
- **Preserve Classic UI**: Default Docusaurus theme must be maintained
- **Content Focus**: Only documentation-related features are allowed

## Local Development

```bash
npm run start
```

This command starts a local development server at http://localhost:3000.

## Build

```bash
npm run build
```

This command generates static content into the `build` directory.

## Important Notes
- This site is completely separated from authentication systems
- All user authentication happens in a separate backend service
- This site should never contain auth components or UI
- Maintain the default Docusaurus classic theme styling
