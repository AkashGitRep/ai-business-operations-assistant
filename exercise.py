class Business:
    def __init__(self, name: str, industry: str):
        self.name = name
        self.industry = industry

    def introduce(self):
        print(f"{self.name} is a {self.industry} business")
           
ABC_Store = Business("ABC_Store", "Retail")
XYZ_Store = Business("XYZ_Store", "Restaurant")


ABC_Store.introduce()
XYZ_Store.introduce()
    