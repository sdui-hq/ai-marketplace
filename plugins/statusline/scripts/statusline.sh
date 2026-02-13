#!/bin/bash
# Claude Code Statusline
set -uo pipefail

input=$(cat)

# ====================================================================================
# DEPENDENCY CHECK
# ====================================================================================
if ! command -v jq >/dev/null 2>&1; then
    printf "› %s [jq required – see statusline plugin README]" "$(pwd)"
    exit 0
fi

# ====================================================================================
# CONFIGURATION
# ====================================================================================
CONFIG_FILE="$HOME/.claude/statusline-config.json"

if [ -f "$CONFIG_FILE" ]; then
    SHOW_SESSION=$(jq -r '.show_session // true' "$CONFIG_FILE" 2>/dev/null || echo 'true')
    SHOW_BRANCH=$(jq -r '.show_branch // true' "$CONFIG_FILE" 2>/dev/null || echo 'true')
    MAX_SESSION_LEN=$(jq -r '.max_session_len // 30' "$CONFIG_FILE" 2>/dev/null || echo '30')
else
    SHOW_SESSION=true
    SHOW_BRANCH=true
    MAX_SESSION_LEN=30
fi

# Script-level constants (customize by editing script directly)
BAR_LENGTH=10
SEP='┃'

# Colors
CYAN='\033[36m'
LAVENDER='\033[38;5;141m'
MINT='\033[38;5;157m'
AMBER='\033[38;5;221m'
CORAL='\033[38;5;203m'
MINT_BG='\033[48;5;157m'
AMBER_BG='\033[48;5;221m'
CORAL_BG='\033[48;5;203m'
GRAY_BG='\033[48;5;238m'
SOFT_WHITE='\033[38;5;252m'
RESET='\033[0m'

# ====================================================================================
# DATA COLLECTION
# ====================================================================================
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir // "~"' 2>/dev/null || echo '~')

GIT_BRANCH=""
if [ "$SHOW_BRANCH" = true ]; then
    GIT_BRANCH=$(git -C "$CURRENT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')
fi

SESSION_NAME=""
if [ "$SHOW_SESSION" = true ]; then
    SESSION_ID=$(echo "$input" | jq -r '.session_id // ""' 2>/dev/null || echo '')
    if [ -n "$SESSION_ID" ]; then
        PROJECT_DIR=$(echo "$input" | jq -r '.workspace.project_dir // ""' 2>/dev/null || echo '')
        if [ -n "$PROJECT_DIR" ]; then
            ENCODED_PATH=$(echo "$PROJECT_DIR" | sed 's|/|-|g')
            INDEX_FILE="$HOME/.claude/projects/${ENCODED_PATH}/sessions-index.json"
            if [ -f "$INDEX_FILE" ]; then
                SESSION_NAME=$(jq -r --arg sid "$SESSION_ID" \
                    '.entries[] | select(.sessionId == $sid) | .summary // empty' \
                    "$INDEX_FILE" 2>/dev/null || echo '')
            fi
        fi
    fi
    # Truncate if needed
    if [ "$MAX_SESSION_LEN" -gt 0 ] && [ "${#SESSION_NAME}" -gt "$MAX_SESSION_LEN" ]; then
        SESSION_NAME="${SESSION_NAME:0:$MAX_SESSION_LEN}..."
    fi
fi

# Context window
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' 2>/dev/null | cut -d. -f1 || echo '0')
PCT=${PCT:-0}
CTX_SIZE=$(echo "$input" | jq -r '.context_window.context_window_size // 200000' 2>/dev/null || echo '200000')
MAX_K=$((CTX_SIZE / 1000))
USED_K=$((PCT * MAX_K / 100))
FILLED=$((PCT * BAR_LENGTH / 100))

# ====================================================================================
# CONTEXT COLOR (based on usage percentage)
# ====================================================================================
if [ "$PCT" -ge 80 ]; then
    CTX_COLOR="$CORAL"
    CTX_BG="$CORAL_BG"
elif [ "$PCT" -ge 50 ]; then
    CTX_COLOR="$AMBER"
    CTX_BG="$AMBER_BG"
else
    CTX_COLOR="$MINT"
    CTX_BG="$MINT_BG"
fi

# ====================================================================================
# BUILD PROGRESS BAR
# ====================================================================================
BAR=""
for ((i=0; i<BAR_LENGTH; i++)); do
    if [ $i -lt $FILLED ]; then
        BAR="${BAR}${CTX_BG} ${RESET}"
    else
        BAR="${BAR}${GRAY_BG} ${RESET}"
    fi
done

# ====================================================================================
# RENDER STATUSLINE
# ====================================================================================
MIDDLE=""
if [ -n "$SESSION_NAME" ]; then
    MIDDLE="${MIDDLE} ${SEP} ◉ ${SOFT_WHITE}${SESSION_NAME}${RESET}"
fi
if [ -n "$GIT_BRANCH" ]; then
    MIDDLE="${MIDDLE} ${SEP} ⎇ ${LAVENDER}${GIT_BRANCH}${RESET}"
fi

printf "› ${CYAN}%s${RESET}%b ${SEP} ⚡ ${CTX_COLOR}%dk/%dk${RESET} ${BAR} ${CTX_COLOR}%d%%${RESET}" \
    "$CURRENT_DIR" "$MIDDLE" "$USED_K" "$MAX_K" "$PCT"
