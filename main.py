import eel

# Name of folder where the html, css, js, image files are located
eel.init('web')

class elevator:

	myID = 0
	goals = [] # Floors it must reach
	direction = 0
	currentFloor = 0
	futurePickup = -1
	futureGoal = -1

	def __init__(self, setID):
		self.myID = setID
		self.goals = []
		self.direction = 0
		self.currentFloor = 0
	
	def setUp(self):
		self.direction = 1 # Setting direction to up

	def setDown(self):
		self.direction = -1 # Setting direction to down

	def addGoal(self, add):
		if not (add in self.goals):
			self.goals.append(add)
			# Going up
			if (self.direction == 1):
				self.goals.sort(reverse = True);
			# Going down
			else:
				self.goals.sort()

	def step(self):
		# Add floors according to direction
		if (self.direction == 1):
			self.currentFloor = self.currentFloor + 1
		elif (self.direction == -1):
			self.currentFloor = self.currentFloor - 1

        # If the visited floor is a part of goals, let user know
		if (self.currentFloor in self.goals):
			self.goals.remove(self.currentFloor)
			eel.addInfo("Elevator #" + str(self.myID) + " is stopping on floor " + str(self.currentFloor))
			if (len(self.goals) == 0):
				# Set future pickups and future goals
				if (self.futurePickup != -1):
					if (self.currentFloor != self.futurePickup):
						self.goals.append(self.futurePickup);
					self.goals.append(self.futureGoal)
					if (self.futurePickup > self.futureGoal):
						self.setDown()
					else:
						self.setUp();
					self.futureGoal = -1
					self.futurePickup = -1
				else:
					self.direction = 0

	# Gives status update on all the elevators
	def status(self, isUpdate=False):
		if isUpdate == False: # If it's not an update, print in Status
			if (self.direction == 1):
				eel.printElevs("Elevator #" + str(self.myID) + " is currently on floor " + str(self.currentFloor) + ", headed up towards floor " + str(self.goals[0]))
			elif (self.direction == -1):
				eel.printElevs("Elevator #" + str(self.myID) + " is currently on floor " + str(self.currentFloor) + ", headed down towards floor " + str(self.goals[len(self.goals) - 1]))
			else:
				eel.printElevs("Elevator #" + str(self.myID) + " is currently waiting on floor " + str(self.currentFloor))
		else: # Otherwise, if it's an update, print in another section
			if (self.direction == 1):
				eel.addInfo("Elevator #" + str(self.myID) + " is currently on floor " + str(self.currentFloor) + ", headed up towards floor " + str(self.goals[0]))
			elif (self.direction == -1):
				eel.addInfo("Elevator #" + str(self.myID) + " is currently on floor " + str(self.currentFloor) + ", headed down towards floor " + str(self.goals[len(self.goals) - 1]))
			else:
				eel.addInfo("Elevator #" + str(self.myID) + " is currently waiting on floor " + str(self.currentFloor))

# This function is called when a request is made to go upwards
def pickupUp (myElevs, wordList, myUnprocessed, elevNumber):
	done = False
	closest = -1 # Keeps track of the closest elevator

	# Find any idle elevator. We want to run as many elevators as possible to reduce waiting time
	for i in range(0, elevNumber):
		if (myElevs[i].direction == 0):
			if (closest != -1):
				if (abs(myElevs[closest].currentFloor - wordList[1]) > abs(myElevs[i].currentFloor - wordList[1])):
					closest = i
			else:
				closest = i
				done = True

	if (done):
		# Elevator needs to go up to pick up the user, goal is also up, hence, the elevator goes up
		if (myElevs[closest].currentFloor < wordList[1]):
			myElevs[closest].addGoal(wordList[1])
			myElevs[closest].addGoal(wordList[2])
			myElevs[closest].setUp()
		# Elevator is on the pick up floor, needs to go up, direction is up as well
		elif (myElevs[closest].currentFloor == wordList[1]):
			myElevs[closest].addGoal(wordList[2])
			myElevs[closest].setUp()

		# Elevator needs to go down to pick up the user. The user wants to go up,
		# so we set the elevator to go down and set the pickup floor as a goal.
		# This way, the elevator will also process requests as it travels down.
		# It will keep serving as a downwards elevator until it has no job left for downwards.
		# At this time, it will process the future requests and start moving upwards.
		# Overall, the waiting time will be reduced, even though in some specific
		# cases it might be increased.
		else:
			myElevs[closest].futurePickup = wordList[1]
			myElevs[closest].futureGoal = wordList[2]
			myElevs[closest].addGoal(wordList[1])
			myElevs[closest].setDown()
		return done;
	# All elevators are busy, so find an elevator that goes the same way and is yet to reach the pickup floor.
	if not (done):
		for i in range(0, elevNumber):
			if (myElevs[i].direction == 1 and (myElevs[i].currentFloor <= wordList[1])):
				if (closest == -1):
					closest = i
					done = True
				else:
					if (abs(myElevs[closest].currentFloor - wordList[1]) > abs(myElevs[i].currentFloor - wordList[1])):
						closest = i

	if (done):
		if (myElevs[closest].currentFloor < wordList[1]):
			myElevs[closest].addGoal(wordList[1])
			myElevs[closest].addGoal(wordList[2])
		else:
			myElevs[closest].addGoal(wordList[2])

	# If request has been added to an elevator, returns true.
	return done;



# This function is called when a request is made to go downwards
def pickupDown (myElevs, wordList, myUnprocessed, elevNumber):
	done = False;
	closest = -1;
	for i in range(0, elevNumber):
		if (myElevs[i].direction == 0):
			if (closest != -1):
				if (abs(myElevs[closest].currentFloor - wordList[1]) > abs(myElevs[i].currentFloor - wordList[1])):
					closest = i
			else:
				closest = i
				done = True

	if (done):	
		if (myElevs[closest].currentFloor > wordList[1]):
			myElevs[closest].addGoal(wordList[1])
			myElevs[closest].addGoal(wordList[2])
			myElevs[closest].setDown()
		elif (myElevs[closest].currentFloor == wordList[1]):
			eel.addInfo("Elevator #" + str(myElevs[closest].myID) + " is currently waiting on floor " + str(wordList[1]))
			myElevs[closest].addGoal(wordList[2])
			myElevs[closest].setDown()
		else:
			myElevs[closest].futurePickup = wordList[1]
			myElevs[closest].futureGoal = wordList[2]
			myElevs[closest].addGoal(wordList[1])
			myElevs[closest].setUp()
		return done;
			
	if not (done):
		for i in range(0, elevNumber):
			if (myElevs[i].direction == -1 and (myElevs[i].currentFloor >= wordList[1])):
				if (closest == -1):
					closest = i
					done = True
				else:
					if (abs(myElevs[closest].currentFloor - wordList[1]) > abs(myElevs[i].currentFloor - wordList[1])):
						closest = i

	if (done):
		if (myElevs[closest].currentFloor > wordList[1]):
			myElevs[closest].addGoal(wordList[1])
			myElevs[closest].addGoal(wordList[2])
		else:
			eel.addInfo("Elevator #" + str(myElevs[closest].myID) + " is currently waiting on floor " + str(wordList[1]))
			myElevs[closest].addGoal(wordList[2])

	return done;


@eel.expose
class Main:

	def __init__(self):
		self.elevNumber = 0
		self.myElevs = []
		self.myUnprocessed = []

	def setElevNumber(self, elevNumber):
		self.elevNumber = elevNumber

	def appendElevs(self):
		for i in range(0, self.elevNumber):
			self.myElevs.append(elevator(i))

	def clickStatus(self):
		for i in range(0, self.elevNumber):
			self.myElevs[i].status();

	def clickPickup(self, a, b):
		a=int(a)
		b=int(b)
		wordList=['pickup', a, b]

		# Adding to the list of unprocessed pickups, had it not been done before,
		# while checking the direction
		if b > a:
			if not (pickupUp(self.myElevs, wordList, self.myUnprocessed, self.elevNumber)):
				self.myUnprocessed.append(wordList)
		elif b < a:
			if not (pickupDown(self.myElevs, wordList, self.myUnprocessed, self.elevNumber)):
				self.myUnprocessed.append(wordList)

	def clickStep(self):
		# Deal with unprocessed requests
		for i in range(0, len(self.myUnprocessed)):
			if (self.myUnprocessed[i][2] > self.myUnprocessed[i][1]):
				if (pickupUp(self.myElevs, self.myUnprocessed[i], self.myUnprocessed, self.elevNumber)):
					self.myUnprocessed.remove(self.myUnprocessed[i])

			elif (self.myUnprocessed[i][2] < self.myUnprocessed[i][1]):
				if (pickupDown(self.myElevs, self.myUnprocessed[i], self.myUnprocessed, self.elevNumber)):
					self.myUnprocessed.remove(self.myUnprocessed[i])

		# Step forward all elevators
		for i in range(0, self.elevNumber):
			self.myElevs[i].step()

	def clickUpdate(self, number):
		number=int(number)
		self.myElevs[number].status(True)

if __name__ == "__main__":
	app = Main()
	# Exposing the Main class functions for Eel to be able to use them in the .js file
	eel.expose(app.setElevNumber)
	eel.expose(app.appendElevs)
	eel.expose(app.clickStatus)
	eel.expose(app.clickPickup)
	eel.expose(app.clickStep)
	eel.expose(app.clickUpdate)

# 1000 is width of window and 600 is the height
eel.start('index.html', size=(1500, 900))