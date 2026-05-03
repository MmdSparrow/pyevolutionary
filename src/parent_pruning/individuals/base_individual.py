class Individual:
    def __init__(self):
        self.genome= None
        self.fitness= None
        self.age= 0
        self.crossover_attendance= 0
        self.bad_parent_score= 0

    def __len__(self):
        return len(self.genome)

    def __str__(self) -> str:
        return f"Genome: {self.genome}\
        \nFitness: {self.fitness}\
        \nAge: {self.age}\
        \nCrossover Attendance: {self.crossover_attendance}\
        \nBad Parent Score: {self.bad_parent_score}\
        "

    def __repr__(self):
        return self.__str__()

    def __eq__(self, value: object) -> bool:
        return self.genome == value.genome
        
    def to_dict(self):
        return {
            'genome': self.genome,
            'fitness': self.fitness,
        }
        
    def to_dict_full_details(self):
        return {
            'genome': self.genome,
            'fitness': self.fitness,
            'age': self.age,
            'crossover_attendance': self.crossover_attendance,
            'bad_parent_score': self.bad_parent_score,
        }
        
    def increase_age(self):
        self.age+= 1

    def increase_crossover_attendace(self):
        self.crossover_attendance+= 1
        
    def increase_bad_parent_score(self):
        self.bad_parent_score += 1

    def decrease_bad_parent_score(self):
        self.bad_parent_score-= 1