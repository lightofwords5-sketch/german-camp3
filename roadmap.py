# roadmap.py

class LearningPath:
    def __init__(self):
        self.days = []
        self.current_day = 0
        self.streak_counter = 0

    def add_day(self, day):
        self.days.append(day)

    def complete_day(self, day):
        if day < len(self.days):
            self.days[day].complete()  # Marks the day as complete
            self.update_streak()

    def update_streak(self):
        # Logic to update streak counter with 🟡 animation
        pass  # To be implemented

    def display_progress(self):
        for index, day in enumerate(self.days):
            if day.completed:
                print("[✔️] Day {}: Completed".format(index + 1))
            elif index == self.current_day:
                print("[✨] Day {}: Current (pulsing animation)".format(index + 1))
            else:
                print("[🔒] Day {}: Locked (grayscale)".format(index + 1))
        print(f"Current streak: {'🔥' * self.streak_counter}")

class Day:
    def __init__(self, title):
        self.title = title
        self.completed = False

    def complete(self):
        self.completed = True

# Example of how to set up the learning path
if __name__ == '__main__':
    learning_path = LearningPath()
    for i in range(10):
        learning_path.add_day(Day(f'Day {i + 1}'))
    learning_path.complete_day(0)  # Completing Day 1
    learning_path.current_day = 1  # Setting Day 2 as current
    learning_path.display_progress()