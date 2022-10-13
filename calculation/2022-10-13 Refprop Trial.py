from REFPROPConnector import ThermodynamicPoint

tp = ThermodynamicPoint(["water"], [1.])
tp.set_variable("T", 20)
tp.set_variable("Q", 0)
print(tp.get_variable("P"))