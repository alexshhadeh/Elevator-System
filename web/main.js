// Setting the number of elevators
function elevatorsNumber() {
	let number = prompt("Please provide a number of elevators, in range 1-16:");
	if (number == null)
		return
	if (number > 0 && number < 17) {
		eel.setElevNumber(parseInt(number))
		eel.appendElevs()
		status()
	} else {
		alert("Invalid number.");
	}
}

// A function which is called in main.py, displays elevators' status on the page
eel.expose(printElevs);
function printElevs(text) {
	document.getElementById("text").textContent += (text+"\n");
}

// Handling status - shows user information about all elevators
function status() {
	document.getElementById("text").textContent = ""
	eel.clickStatus()
}

// Handling pickup - pick user from floor a to floor b
function pickup() {
	a = prompt("Please provide the pickup floor:");
	if (a == null)
		return
	b = prompt("Please provide the target floor:");
	if (b == null)
		return
	if (a != b) {
		eel.clickPickup(a, b)
		status()
	}
	else
		alert("The floors cannot be the same!")
}

// Handling step
function stepp() {
	eel.clickStep()
	status()
}

// Handling update - shows user information about the specified elevator
function update() {
	let number = prompt("Please provide the elevator number:");
	if (number == null)
		return
	if (number >= 0 && number < 17)
		eel.clickUpdate(number)
	else
		alert("Invalid number.");
}

// Adds info in the updates section
eel.expose(addInfo);
function addInfo(text) {
	document.getElementById("updates").textContent += (text+"\n");

}
