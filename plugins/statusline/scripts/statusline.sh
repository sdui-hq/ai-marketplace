#!/bin/bash
# Claude Code Statusline
set -euo pipefail

input=$(cat)

# ====================================================================================
# CONFIGURATION
# ====================================================================================
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
RESET='\033[0m'

# ====================================================================================
# DATA COLLECTION
# ====================================================================================
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir // "~"')
GIT_BRANCH=$(git -C "$CURRENT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')

# Get PR URL for branch (or fall back to branch tree URL)
BRANCH_URL=""
if [ -n "$GIT_BRANCH" ]; then
    # Try to get PR URL using gh CLI
    PR_URL=$(cd "$CURRENT_DIR" && gh pr view "$GIT_BRANCH" --json url -q '.url' 2>/dev/null || echo '')

    if [ -n "$PR_URL" ]; then
        BRANCH_URL="$PR_URL"
    else
        # Fall back to branch tree URL
        REMOTE_URL=$(git -C "$CURRENT_DIR" remote get-url origin 2>/dev/null || echo '')
        if [ -n "$REMOTE_URL" ]; then
            # Convert SSH to HTTPS format
            if [[ "$REMOTE_URL" == git@* ]]; then
                REMOTE_URL=$(echo "$REMOTE_URL" | sed 's/git@/https:\/\//' | sed 's/:/\//' | sed 's/\.git$//')
            elif [[ "$REMOTE_URL" == *.git ]]; then
                REMOTE_URL="${REMOTE_URL%.git}"
            fi
            BRANCH_URL="${REMOTE_URL}/tree/${GIT_BRANCH}"
        fi
    fi
fi

# Context window
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
CTX_SIZE=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')
MAX_K=$((CTX_SIZE / 1000))
USED_K=$((PCT * MAX_K / 100))
FILLED=$((PCT / 10))

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
if [ -n "$GIT_BRANCH" ]; then
    if [ -n "$BRANCH_URL" ]; then
        # Print in parts to ensure hyperlink closes properly
        printf "› ${CYAN}%s${RESET} ${SEP} ⎇ " "$CURRENT_DIR"
        printf '\e[24m'"${LAVENDER}"'\e]8;;%s\e\\%s\e]8;;\e\\'"${RESET}" "$BRANCH_URL" "$GIT_BRANCH"
        printf " ${SEP} ⚡ ${CTX_COLOR}%dk/%dk${RESET} ${BAR} ${CTX_COLOR}%d%%${RESET}" "$USED_K" "$MAX_K" "$PCT"
    else
        printf "› ${CYAN}%s${RESET} ${SEP} ⎇ ${LAVENDER}%s${RESET} ${SEP} ⚡ ${CTX_COLOR}%dk/%dk${RESET} ${BAR} ${CTX_COLOR}%d%%${RESET}" \
            "$CURRENT_DIR" "$GIT_BRANCH" "$USED_K" "$MAX_K" "$PCT"
    fi
else
    printf "› ${CYAN}%s${RESET} ${SEP} ⚡ ${CTX_COLOR}%dk/%dk${RESET} ${BAR} ${CTX_COLOR}%d%%${RESET}" \
        "$CURRENT_DIR" "$USED_K" "$MAX_K" "$PCT"
fi
