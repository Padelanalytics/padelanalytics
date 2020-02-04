var selectedTimeSlots = [];
var consecutiveSlots = 1;
var busyColor = "red";
var freeColor = "green";


function changeCellBackgroundColor(tableId, row, column, color) {
    var table = document.getElementById(tableId);
    table.rows[row].cells[column].style.backgroundColor = color;
}


function getSlotIndex(newSlot, slots){
    for (var i = 0; i < slots.length; i++){
        if (newSlot[0] == slots[i][0] && newSlot[1] == slots[i][1] && newSlot[2] == slots[i][2]){
            return i;
        }
    }
    return -1;
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
    var slot = [tableId, row, column];
    let index = getSlotIndex(slot, selectedTimeSlots);

    if (index < 0){
        selectedTimeSlots.push(slot);
        changeCellBackgroundColor(tableId, row, column, busyColor);
    } else {
        selectedTimeSlots.splice(index, 1);
        changeCellBackgroundColor(tableId, row, column, freeColor);
    }
    console.log(selectedTimeSlots);
}


function getCellValues(tableId) {
    var table = document.getElementById(tableId);
    for (var r = 1, n = table.rows.length; r < n; r++) {
        for (var c = 1, m = table.rows[r].cells.length; c < m; c++) {
            //console.log(table.rows[r].cells[c].innerHTML);
        }
    }
}
