from data import db
from lib import Model

# db.create_tables()

test = Model()
results = test.predict(["Avoid this movie at all costs, everything about it is bad", "I love it", "It's a great movie !"])

print(results)
# for result in results:
#     print(result)