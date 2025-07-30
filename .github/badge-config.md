# 🏷️ Badge Configuration Guide

## Current Badges

### Working Badges (Ready to Use)
```markdown
![Build](https://img.shields.io/github/actions/workflow/status/user/ai-ecosystem-control-center/ci.yml?branch=main&label=build)
![Uptime](https://img.shields.io/badge/uptime-100%25-brightgreen)
![Cost](https://img.shields.io/badge/monthly%20cost-$0-green)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-blue)
```

## How to Update Badges

### 1. GitHub Actions Build Badge
- **Current**: `![Build](https://img.shields.io/github/actions/workflow/status/user/ai-ecosystem-control-center/ci.yml?branch=main&label=build)`
- **To Update**: Replace `user/ai-ecosystem-control-center` with your actual GitHub username/repo
- **Example**: `![Build](https://img.shields.io/github/actions/workflow/status/johndoe/ai-ecosystem-control-center/ci.yml?branch=main&label=build)`

### 2. UptimeRobot Badge (Optional)
If you want real uptime monitoring:

1. Sign up at [UptimeRobot](https://uptimerobot.com)
2. Create a monitor for any public endpoint
3. Get your monitor ID from the dashboard
4. Replace the uptime badge:
   ```markdown
   ![Uptime](https://img.shields.io/uptime-robot/status/YOUR_MONITOR_ID?label=uptime)
   ```

### 3. Cost Badge
- **Current**: Shows $0 (accurate for local-only system)
- **To Update**: Change the amount if you add cloud services
- **Example**: `![Cost](https://img.shields.io/badge/monthly%20cost-$25-yellow)`

### 4. Additional Useful Badges

#### Code Quality
```markdown
![Code Quality](https://img.shields.io/badge/code%20quality-A+-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-85%25-green)
```

#### System Status
```markdown
![Systems](https://img.shields.io/badge/AI%20systems-4%20active-brightgreen)
![Health Score](https://img.shields.io/badge/health%20score-95.6%2F100-brightgreen)
```

#### Technology Stack
```markdown
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue)
![AI](https://img.shields.io/badge/AI-powered-purple)
![Automation](https://img.shields.io/badge/automation-LaunchAgents-orange)
```

## Badge Colors

- **Green**: `brightgreen`, `green`, `success`
- **Blue**: `blue`, `informational`
- **Yellow**: `yellow`, `warning`
- **Red**: `red`, `critical`, `error`
- **Orange**: `orange`
- **Purple**: `purple`, `blueviolet`
- **Grey**: `lightgrey`, `inactive`

## Custom Badge Template

```markdown
![Label](https://img.shields.io/badge/LABEL-MESSAGE-COLOR)
```

Replace:
- `LABEL`: Left side text
- `MESSAGE`: Right side text  
- `COLOR`: Badge color

## Testing Badges

After updating badges:
1. Commit and push changes
2. Wait 2-3 minutes for GitHub Actions to run
3. Refresh your repository page
4. Verify all badges display correctly

## Troubleshooting

### Badge Not Updating
- Check GitHub Actions are enabled in repository settings
- Verify workflow file is in `.github/workflows/ci.yml`
- Ensure branch name matches (main vs master)

### Badge Shows "Unknown"
- Workflow hasn't run yet (wait a few minutes)
- Workflow file has syntax errors (check Actions tab)
- Repository path is incorrect in badge URL

### Badge Shows Error
- Check the Actions tab for failed builds
- Review workflow logs for specific errors
- Ensure all dependencies are in requirements.txt
