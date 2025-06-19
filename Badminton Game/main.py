import random

# ───────────────────────────────────────────────────────────
#  SETTINGS / CONSTANTS
# ───────────────────────────────────────────────────────────
ACTIONS = ["smash", "drop", "clear"]
POINTS_TO_WIN = 5
INITIAL_VP = 50
VP_COST = {"smash": 5, "drop": 3, "clear": 2}
WIN_RULES = {
    ("smash", "drop"): "player",
    ("drop",  "clear"): "player",
    ("clear", "smash"): "player"
}
# ───────────────────────────────────────────────────────────


def choose_opponent_action(opponent_vp):
    """
    If opponent_vp <= 0, forced to 'clear' (no VP deduction).
    Otherwise, pick randomly among actions they can afford.
    """
    if opponent_vp <= 0:
        return "clear"

    affordable = [a for a in ACTIONS if opponent_vp >= VP_COST[a]]
    return random.choice(affordable) if affordable else "clear"


def rally_winner(player_act, opp_act, player_vp, opponent_vp):
    """
    Decide who wins this rally, or if it's a tie.
    Returns "player", "opponent", or "tie".
    Special‐case probability:
      – If opp_act == "smash" AND player_act == "clear",
        player has a chance to clear successfully based on player_vp.
    """
    if player_act == opp_act:
        return "tie"
    if (player_act, opp_act) in WIN_RULES:
        return "player"
    if (opp_act, player_act) in WIN_RULES:
        # special chance: opponent smashes and player clears
        if opp_act == "smash" and player_act == "clear":
            p_clear = max(0.0, min(1.0, player_vp / 100.0))
            return "player" if random.random() < p_clear else "opponent"
        return "opponent"
    return "tie"


def main():
    print("\n── Welcome to Console Badminton Game ──\n")
    player_name = input("Enter your name: ").strip() or "Player"
    opponent_name = "Lee Chong Wei"

    player_vp = INITIAL_VP
    opponent_vp = INITIAL_VP
    player_score = 0
    opponent_score = 0
    round_num = 1
    match_winner = None  # "player" or "opponent"

    while True:
        # 1) Check score win conditions
        if player_score >= POINTS_TO_WIN:
            match_winner = "player"
            break
        if opponent_score >= POINTS_TO_WIN:
            match_winner = "opponent"
            break

        # 2) Print round header
        print(f"\n        ==== Round {round_num} ====")
        round_num += 1

        # 3) Show current status
        print(f"Score → {player_name}: {player_score}  |  {opponent_name}: {opponent_score}")
        print(f"{player_name} VP: {player_vp}    {opponent_name} VP: {opponent_vp}")

        # 4) Player chooses action
        if player_vp <= 0:
            choice = "clear"
            print(f"● {player_name}, your VP is 0, so you are forced to 'clear'.")
        else:
            while True:
                choice = input("Choose action (smash/drop/clear): ").strip().lower()
                if choice not in ACTIONS:
                    print("  ↪ Invalid. Type smash, drop, or clear.")
                    continue
                cost = VP_COST[choice]
                if player_vp < cost:
                    print(f"  ↪ You have {player_vp} VP but '{choice}' costs {cost}.")
                    continue
                break
            player_vp -= VP_COST[choice]

        # 5) Opponent chooses action
        opp_choice = choose_opponent_action(opponent_vp)
        if opponent_vp > 0 and opp_choice in VP_COST:
            opponent_vp -= VP_COST[opp_choice]
        print(f"🏸 {opponent_name} action: '{opp_choice}'")

        # 6) Resolve rally
        print(f"\n▶ {player_name}: {choice}   |   {opponent_name}: {opp_choice}")
        winner = rally_winner(choice, opp_choice, player_vp, opponent_vp)
        if winner == "tie":
            print("  → Tie rally. No points awarded.")
        elif winner == "player":
            player_score += 1
            print(f"  → {player_name} wins this rally! +1 point.")
        else:
            opponent_score += 1
            print(f"  → {opponent_name} wins this rally. +1 point.")

    # After loop: Game Over and final result
    print("\n        ── Game Over ──")
    print(f"Final Score  {player_name}: {player_score}  |  {opponent_name}: {opponent_score}")

    if match_winner == "player":
        print(f"🏆 Congratulations! {player_name} reached 5 points first and beat Lee Chong Wei!")
    else:
        print(f"Unfortunately, {player_name} lost to Lee Chong Wei, but don’t be discouraged—keep pushing forward!💪")


if __name__ == "__main__":
    main()
