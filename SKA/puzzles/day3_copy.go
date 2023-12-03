package puzzles

// don't judge a man based off his imports
import (
	"bufio"
	"fmt"
	"strconv"
	"unicode"
)

const COLUMNS = 140

func Day3Task2Copy() {
	handle := openTextFile("inputs/aoc03.txt")
	scanner := bufio.NewScanner(handle)
	twodim_array := [ROWS][COLUMNS]rune{}
	linecount := 0
	// for each line
	for scanner.Scan() {
		// for each char
		for count, runeval := range scanner.Text() {
			twodim_array[linecount][count] = runeval
		}
		linecount++
	}
	current_num := ""
	running_count := 0
	hasSurrounded := false
	// map for asterisk positions
	astmap := make(map[int]int)
	// retval for isSurrounded
	retsurr := -1
	// 2d array of each line now exists, iterate through it
	for i := 0; i < ROWS; i++ {
		for j := 0; j < COLUMNS; j++ {
			// lexer moment - if rune is a digit, its under investigation
			if unicode.IsDigit(twodim_array[i][j]) {
				// append rune to string of number
				current_num = current_num + string(twodim_array[i][j])
				// if any other part of the num is not surrounded, check
				if hasSurrounded == false {
					retsurr = starIsSurroundedFails(twodim_array, i, j)
				}
				// if we're now surrounded set it
				if retsurr != -1 {
					hasSurrounded = true
				}
			}
			if !(unicode.IsDigit(twodim_array[i][j])) {
				// number finished
				// if its surrounded
				if hasSurrounded {
					intval, _ := strconv.Atoi(current_num)
					// if map has no value for the asterisk position, add it to the asterisk position
					if astmap[retsurr] == 0 {
						astmap[retsurr] = intval
					}
					// now if the map is occupied AND its not the number we just added, add it to the total
					if astmap[retsurr] != 0 && astmap[retsurr] != intval {
						running_count = (astmap[retsurr] * intval) + running_count
					}
					hasSurrounded = false
				}
				// reset number
				current_num = ""
			}
		}
	}
	fmt.Println(running_count)
}

/*

v v v * *
v 1 v 3 *
v v v * *

possibilities for [r][c]
[r-1][c-1] (top left) v
[r-1][c] (above) v
[r-1][c+1] (top right) v
[r][c-1] (immediate left)
[r][c+1] (immediate right)
[r+1][c-1] (bottom left)
[r+1][c] (below)
[r+1][c+1] (bottom right)

*/

func starIsSurrounded(arr [ROWS][COLUMNS]rune, row int, col int) int {
	// count_from_beginning is the "key" to the map - we store whatever other ratio references it at this place
	// if another ratio later on also touches this asterisk, it'll be the same key to access the other half of the ratio
	// because only 2 numbers touch 1 asterisk, we can do this
	// else it'd be a pain
	count_from_beginning := 0
	if (row-1 != -1) && (col-1 != -1) {
		if arr[row-1][col-1] == '*' {
			count_from_beginning = ((row - 1) * COLUMNS) + col - 1
			return count_from_beginning
		}
	}
	if row-1 != -1 {
		// follows that row-1, col will exist
		if arr[row-1][col] == '*' {
			count_from_beginning = ((row - 1) * COLUMNS) + col
			return count_from_beginning
		}
	}
	// now check if row-1 exists
	if col-1 != -1 {
		if arr[row][col-1] == '*' {
			count_from_beginning = ((row) * COLUMNS) + col - 1
			return count_from_beginning
		}
	}
	// now check if top right exists
	if (row-1 != -1) && (col+1 != COLUMNS) {
		if arr[row-1][col+1] == '*' {
			count_from_beginning = ((row - 1) * COLUMNS) + col + 1
			return count_from_beginning
		}
	}
	// now check if r+1, col-1 exists
	if (row+1 != ROWS) && (col-1 != -1) {
		if arr[row+1][col-1] == '*' {
			count_from_beginning = ((row + 1) * COLUMNS) + col - 1
			return count_from_beginning
		}
	}
	// now check if r+1, col exists
	if row+1 != ROWS {
		if arr[row+1][col] == '*' {
			count_from_beginning = ((row + 1) * COLUMNS) + col
			return count_from_beginning
		}
	}
	// now check if r+1, c+1 exists
	if (row+1 != ROWS) && (col+1 != COLUMNS) {
		if arr[row+1][col+1] == '*' {
			count_from_beginning = ((row + 1) * COLUMNS) + col + 1
			return count_from_beginning
		}
	}
	// now check if r, c+1 exists
	if col+1 != COLUMNS {
		if arr[row][col+1] == '*' {
			count_from_beginning = ((row) * COLUMNS) + col + 1
			return count_from_beginning
		}
	}
	return -1
}
