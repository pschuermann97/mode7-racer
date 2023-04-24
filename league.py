# A league consists of 5 consecutive races (stored as a list)
# that the player must complete in order to complete the league. 
class League:
    def __init__(self, races):
        self.races = races
        self.current_race_index = 0 # index of the race that the player is currently playing

    # Returns the number of races that this league consists of.
    def length(self):
        return len(self.races)

    # Returns the data object representing the race that the player is currently playing.
    def current_race(self):
        return self.races[current_race_index]

    # Moves the index to the next race and returns that race.
    def next_race(self):
        self.current_race_index += 1
        return self.races[current_race_index]

    # Returns True if and only if the player has completed this league.
    def is_completed(self):
        return self.current_race_index >= self.length()

    # Resets the index to the first race of the league.
    def reset(self):
        self.current_race_index = 0