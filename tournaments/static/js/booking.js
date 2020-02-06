var selectedTimeSlots = [];
var slotPrice = 20;
var totalPrice = 0;
var totalTime = 0;
var maxSlots = 3;
var minSlots = 2;
var slotTime = 60;
var busyColor = "red";
var freeColor = "green";
var multiDays = true;


// Object related methods

function getTableSlots(tableId) {
    var result = [];
    for (var i=0; i<selectedTimeSlots.length; i++){
        if (selectedTimeSlots[i][0] == tableId){
            result.push(selectedTimeSlots[i]);
        }
    }
    return result;
}


function minNextConsecutivesSlots(num, matrix){
    var result = [];
    var maxRow = getMaxRowsTable(matrix[0][0]) - 1;
    var highestRow = matrix[0][1]; // first row element
    for (var i=1; i<matrix.length; i++) {
        if (matrix[i][1] > highestRow){
            highestRow = matrix[i][1];
        }
    }
    var j = 0;
    var row = highestRow + 1;
    while (j < num && row <= maxRow){
        result.push([matrix[0][0], row, matrix[0][2]]);
        j++;
        row++;
    }
    return result;
}


function getSlotIndex(newSlot, slots){
    for (var i = 0; i < slots.length; i++){
        if (newSlot[0] == slots[i][0] && newSlot[1] == slots[i][1] && newSlot[2] == slots[i][2]){
            return i;
        }
    }
    return -1;
}


function addOrRemoveSlot(tableId, row, column){
    var slot = [tableId, row, column];
    let index = getSlotIndex(slot, selectedTimeSlots);
    if (index >= 0) {
        for (var i = selectedTimeSlots.length-1; i >= 0; i--){
            if (selectedTimeSlots[i][0] == tableId){
                changeCellBackgroundColor(selectedTimeSlots[i][0], selectedTimeSlots[i][1], selectedTimeSlots[i][2], freeColor);
                selectedTimeSlots.splice(i, 1);
            }
        }
    } else if (index == -1) {
        var tableSlots = getTableSlots(tableId);
        if (tableSlots.length == 0 && (selectedTimeSlots.length == 0 || multiDays)){ // no selection => add min of possible selections
            selectedTimeSlots.push(slot);
            changeCellBackgroundColor(tableId, row, column, busyColor);
            if (minSlots - 1 > 0){
                var matrix = [slot];
                var extraSlots = minNextConsecutivesSlots(minSlots-1, matrix);
                for (var i=0; i<extraSlots.length; i++){
                    selectedTimeSlots.push(extraSlots[i]);
                    changeCellBackgroundColor(tableId, extraSlots[i][1], extraSlots[i][2], busyColor);
                }
            }

        } else { // already a selection => check if possible to expand
            var nextSlot = minNextConsecutivesSlots(1, tableSlots);
            if (nextSlot.length == 1 && maxSlots > tableSlots.length && nextSlot[0][0] == tableId && nextSlot[0][1] == row && nextSlot[0][2] == column) {
                selectedTimeSlots.push(nextSlot[0]);
                changeCellBackgroundColor(tableId, nextSlot[0][1], nextSlot[0][2], busyColor);
            }
        }
        updatePriceAndTime();
    }
}


function updatePriceAndTime(){
    totalPrice = slotPrice * selectedTimeSlots.length;
    totalTime = slotTime * selectedTimeSlots.length;
    var htmlPrice = document.getElementById("totalPrice");
    htmlPrice.innerHTML = totalTime + "mins - " + totalPrice + "&euro;";
}


// table methods

function getMaxRowsTable(tableId) {
    var table = document.getElementById(tableId);
    return table.rows.length;
}


function changeCellBackgroundColor(tableId, row, column, color) {
    var table = document.getElementById(tableId);
    table.rows[row].cells[column].style.backgroundColor = color;
}


function bindOnClickMethod(tableId){
    var table = document.getElementById(tableId);
    for (var r = 1, n = table.rows.length; r < n; r++) {
        for (var c = 1, m = table.rows[r].cells.length; c < m; c++) {
            var cell = table.rows[r].cells[c];
            cell.style.backgroundColor = freeColor;
            cell.onclick = function(r, c) {
                easyPeasy(tableId, this.parentNode.rowIndex, this.cellIndex);
            }
        }
    }
}


function easyPeasy(tableId, row, column){
    addOrRemoveSlot(tableId, row, column);
}


function getCellValues(tableId) {
    var table = document.getElementById(tableId);
    for (var r = 1, n = table.rows.length; r < n; r++) {
        for (var c = 1, m = table.rows[r].cells.length; c < m; c++) {
            //console.log(table.rows[r].cells[c].innerHTML);
        }
    }
}
