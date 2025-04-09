import random
import csv
import logging
import statistics
import math

# For debugging purposes you can still log detailed events by setting VERBOSE = True.
VERBOSE = False

# Configure logging (you might lower the logging level during batch runs)
logging.basicConfig(filename='detailed_simulation.log', level=logging.INFO, format='%(message)s')

# Set seed for reproducibility
random.seed(42)

def roll_dice(num_dice, sides):
    return sum(random.randint(1, sides) for _ in range(num_dice))

class Cleric:
    def __init__(self, id, hp=10, ac=18, dc=13, tempest_uses=3):
        self.id = id         # Unique identifier for tracking
        self.hp = hp         # Starting hit points (e.g., 10 at level 1)
        self.ac = ac         # Armor Class
        self.dc = dc         # Difficulty Class for saving throws (e.g., 13 for Sacred Flame)
        self.tempest_uses = tempest_uses  # Total Tempest reaction uses available
        self.reaction_available = True if tempest_uses > 0 else False

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage

    def reset_reaction(self):
        # At the start of each round, if the cleric still has Tempest uses, allow them to react once.
        self.reaction_available = True if self.tempest_uses > 0 else False

    def tempest_reaction(self):
        # Use Tempest Reaction if available. Deals 2d8 thunder damage.
        if self.reaction_available and self.tempest_uses > 0:
            self.reaction_available = False
            self.tempest_uses -= 1
            roll = max(random.randint(1, 20), random.randint(1, 20))
            base_damage = roll_dice(2, 8)
            if roll >= 13:
                damage = base_damage // 2
            else:
                damage = base_damage
            if VERBOSE:
                logging.info(f"Cleric {self.id} uses Tempest reaction for {damage} thunder damage! ({self.tempest_uses} uses remaining)")
            return damage
        return 0

def simulate_battle(num_clerics, initial_tarrasque_hp):
    """
    Runs a single simulation of the battle.
    Returns a tuple:
      (win: bool, rounds: int, body_count: int)
    where body_count is the number of clerics that died.
    """
    # (Optional) Set seed for reproducibility if desired
    #random.seed(42)

    # Create a list of cleric instances
    clerics = [Cleric(i) for i in range(num_clerics)]
    tarrasque_hp = initial_tarrasque_hp
    rounds = 0

    while tarrasque_hp > 0 and any(cleric.is_alive() for cleric in clerics):
        rounds += 1
        if VERBOSE:
            logging.info(f"\n--- Round {rounds} ---")
        
        # Reset each cleric's per-round reaction
        for cleric in clerics:
            if cleric.is_alive():
                cleric.reset_reaction()
        
        # Clerics' turn: each living cleric casts sacred flame.
        # Using a mechanic where they roll 2d20 and if the higher result meets or exceeds dc, it counts as success.
        successes = 0
        for cleric in clerics:
            if cleric.is_alive():
                # Roll 2d20 and take the higher result (simulating advantage in a saving throw)
                roll = max(random.randint(1, 20), random.randint(1, 20))
                if roll <= cleric.dc:
                    successes += 1

        # Roll damage for each successful sacred flame (1d8 damage per success)
        flame_damage = sum(random.randint(1, 8) for _ in range(successes))
        tarrasque_hp -= flame_damage
        if VERBOSE:
            logging.info(f"Clerics cast sacred flame {successes} times for {flame_damage} damage.")
            logging.info(f"Tarrasque HP after sacred flame: {tarrasque_hp}")

        # Check if the Tarrasque is defeated
        if tarrasque_hp <= 0:
            if VERBOSE:
                logging.info("The Tarrasque has been defeated by the clerics!")
            # Calculate body count at end of battle
            body_count = len([cleric for cleric in clerics if not cleric.is_alive()])
            return (True, rounds, body_count)
        
        # Tarrasque's turn: it makes 8 attacks
        for attack in range(8):
            alive_clerics = [cleric for cleric in clerics if cleric.is_alive()]
            if not alive_clerics:
                break  # All clerics are dead
            
            target = random.choice(alive_clerics)
            attack_roll = random.randint(1, 20)
            if attack_roll == 1:
                if VERBOSE:
                    logging.info(f"Attack {attack+1}: Tarrasque rolled a 1 and missed cleric {target.id}.")
                continue

            if (attack_roll + 19) >= target.ac:
                damage = roll_dice(4, 8) + 10
                target.take_damage(damage)
                if VERBOSE:
                    logging.info(f"Attack {attack+1}: Tarrasque hits cleric {target.id} for {damage} damage (Cleric HP now: {target.hp}).")
                # Use Tempest reaction if available
                reaction_damage = target.tempest_reaction()
                if reaction_damage:
                    tarrasque_hp -= reaction_damage
                    if VERBOSE:
                        logging.info(f"Tarrasque takes {reaction_damage} thunder damage from cleric {target.id}'s Tempest reaction.")
                        logging.info(f"Tarrasque HP is now: {tarrasque_hp}")
            else:
                if VERBOSE:
                    logging.info(f"Attack {attack+1}: Tarrasque rolled {attack_roll} (+19 = {attack_roll + 19}) and missed cleric {target.id}.")
            
            if tarrasque_hp <= 0:
                if VERBOSE:
                    logging.info("The Tarrasque has been defeated mid-round by reactive damage!")
                body_count = len([cleric for cleric in clerics if not cleric.is_alive()])
                return (True, rounds, body_count)
    
    # If the loop ends and the Tarrasque is still alive, the clerics have failed.
    # End of battle: if tarrasque survived, body count is all clerics that died.
    body_count = len([cleric for cleric in clerics if not cleric.is_alive()])
    if tarrasque_hp <= 0:
        if VERBOSE:
            logging.info("The Tarrasque has been defeated by the clerics!")
        return (True, rounds, body_count)
    else:
        if VERBOSE:
            logging.info("All clerics have fallen. The Tarrasque prevails.")
        return (False, rounds, body_count)

def run_batch_simulations(min_clerics, max_clerics, num_simulations, output_csv='simulation_summary.csv'):
    """
    Runs simulations for cleric counts in the range [min_clerics, max_clerics].
    For each count, it runs num_simulations battles and records:
      - The win rate (with 95% confidence intervals).
      - The average number of rounds (with 95% confidence intervals).
    The summary is written to a CSV file.
    """
    summary_results = []

    for num_clerics in range(min_clerics, max_clerics + 1):
        wins = 0
        rounds_list = []
        body_counts = []

        for sim in range(num_simulations):
            tarrasque_hp = sum(random.randint(1, 20) for _ in range(33)) + 330
            win, rounds, body_count = simulate_battle(num_clerics, tarrasque_hp)
            if win:
                wins += 1
            rounds_list.append(rounds)
            body_counts.append(body_count)
        
        win_rate = wins / num_simulations
        
        # Calculate confidence intervals for the win rate.
        se_win = math.sqrt((win_rate * (1 - win_rate)) / num_simulations)
        ci_win_lower = win_rate - 1.96 * se_win
        ci_win_upper = win_rate + 1.96 * se_win

        # For rounds, compute mean and standard error.
        avg_rounds = sum(rounds_list) / num_simulations
        if num_simulations > 1:
            stdev_rounds = statistics.stdev(rounds_list)
        else:
            stdev_rounds = 0
        se_rounds = stdev_rounds / math.sqrt(num_simulations)
        ci_rounds_lower = avg_rounds - 1.96 * se_rounds
        ci_rounds_upper = avg_rounds + 1.96 * se_rounds

        # Average body count and confidence intervals
        avg_body_count = sum(body_counts) / num_simulations
        stdev_body = statistics.stdev(body_counts) if num_simulations > 1 else 0
        se_body = stdev_body / math.sqrt(num_simulations)
        ci_body_lower = avg_body_count - 1.96 * se_body
        ci_body_upper = avg_body_count + 1.96 * se_body

        summary_results.append({
            'num_clerics': num_clerics,
            'simulations': num_simulations,
            'win_rate': win_rate,
            'wins': wins,
            'losses': num_simulations - wins,
            'ci_win_lower': ci_win_lower,
            'ci_win_upper': ci_win_upper,
            'avg_rounds': avg_rounds,
            'ci_rounds_lower': ci_rounds_lower,
            'ci_rounds_upper': ci_rounds_upper,
            'avg_body_count': avg_body_count,
            'ci_body_lower': ci_body_lower,
            'ci_body_upper': ci_body_upper
        })

        print(f"Clerics: {num_clerics}, Win Rate: {win_rate:.3f}, Avg Rounds: {avg_rounds:.2f}, Avg Body Count: {avg_body_count:.2f}")


    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['num_clerics', 'simulations', 'win_rate', 'wins', 'losses', 'ci_win_lower', 'ci_win_upper',
                      'avg_rounds', 'ci_rounds_lower', 'ci_rounds_upper', 'avg_body_count', 'ci_body_lower', 'ci_body_upper']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_results:
            writer.writerow(row)

    print(f"Summary of simulations written to '{output_csv}'.")

# Warning: This could take a while to run!
run_batch_simulations(1, 500, 1000)

#simulate_battle(49, 676)  # Example run with 49 clerics and Tarrasque HP of 330 for testing purposes.
#simulate_battle(50, 676)  # Example run with 50 clerics and Tarrasque HP of 330 for testing purposes.
#simulate_battle(51, 676)  # Example run with 51 clerics and Tarrasque HP of 330 for testing purposes.
#simulate_battle(52, 676)  # Example run with 52 clerics and Tarrasque HP of 330 for testing purposes.
#simulate_battle(53, 676)  # Example run with 53 clerics and Tarrasque HP of 330 for testing purposes.
#simulate_battle(54, 676)  # Example run with 54 clerics and Tarrasque HP of 330 for testing purposes.