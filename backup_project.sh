#!/bin/bash
# Automatic backup script for Football Statistics project

echo ""
echo "================================================"
echo "⚽ Football Statistics Project - Backup Tool"
echo "================================================"
echo ""

# Configuration
PROJECT_DIR="$HOME/football_statistics"
BACKUP_DIR="$HOME/Desktop"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="football_stats_backup_${TIMESTAMP}"

# Check if project exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Error: Project directory not found at $PROJECT_DIR"
    exit 1
fi

echo "📂 Project: $PROJECT_DIR"
echo "💾 Backup location: $BACKUP_DIR"
echo ""

# Create backup
echo "🔄 Creating backup..."
cd "$HOME"

tar -czf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" \
    --exclude='football_statistics/venv' \
    --exclude='football_statistics/__pycache__' \
    --exclude='football_statistics/.git' \
    --exclude='football_statistics/*.pyc' \
    football_statistics/

if [ $? -eq 0 ]; then
    BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" | cut -f1)
    echo ""
    echo "✅ Backup completed successfully!"
    echo ""
    echo "📦 Backup file: ${BACKUP_NAME}.tar.gz"
    echo "📍 Location: ${BACKUP_DIR}/"
    echo "💾 Size: ${BACKUP_SIZE}"
    echo ""
    echo "================================================"
    
    # Also create a "latest" symlink
    cd "$BACKUP_DIR"
    ln -sf "${BACKUP_NAME}.tar.gz" "football_stats_latest.tar.gz"
    echo "🔗 Latest backup: football_stats_latest.tar.gz"
    echo "================================================"
else
    echo ""
    echo "❌ Backup failed!"
    exit 1
fi

echo ""
echo "💡 To restore:"
echo "   cd ~/Desktop"
echo "   tar -xzf ${BACKUP_NAME}.tar.gz"
echo ""

