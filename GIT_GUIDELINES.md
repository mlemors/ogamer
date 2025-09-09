# Git Commit Guidelines für OGame Bot

## 🎯 Repository
**GitHub:** https://github.com/mlemors/ogamer.git

## 🎯 Commit Types

- `🚀 feat:` - Neue Features
- `🐛 fix:` - Bug Fixes
- `⚡ perf:` - Performance Verbesserungen
- `🔧 config:` - Konfiguration Änderungen
- `📝 docs:` - Dokumentation
- `♻️ refactor:` - Code Refactoring
- `✅ test:` - Tests
- `🎨 style:` - Code Formatting

## 📋 Beispiele

```bash
# Neue Features
git commit -m "🚀 feat: Add advanced raid target scoring"
git commit -m "🚀 feat: Implement resource prediction algorithm"

# Bug Fixes  
git commit -m "🐛 fix: Handle browser reconnection gracefully"
git commit -m "🐛 fix: Prevent building when resources insufficient"

# Performance
git commit -m "⚡ perf: Optimize galaxy scanning speed"
git commit -m "⚡ perf: Reduce memory usage in resource tracking"

# Configuration
git commit -m "🔧 config: Adjust raid cycle timing for better results"
git commit -m "🔧 config: Update building priorities for faster growth"
```

## 🏷️ Releases

```bash
git tag -a v1.0.0 -m "🎉 Release v1.0.0: Complete automation system"
git tag -a v1.1.0 -m "🚀 Release v1.1.0: Enhanced raiding intelligence"
```

## 🌿 Branching

```bash
# Feature development
git checkout -b feature/advanced-colonization
git checkout -b feature/research-automation

# Bug fixes
git checkout -b fix/browser-crash-handling
git checkout -b fix/resource-parsing-error

# Merge back to main
git checkout main
git merge feature/advanced-colonization
```

## 🌐 Repository Commands

```bash
# Status & Updates
git status
git pull origin main
git push origin main

# Clone Repository
git clone https://github.com/mlemors/ogamer.git

# Remote Info
git remote -v
```
