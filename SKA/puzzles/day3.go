package puzzles

import (
	"bufio"
	"errors"
	"log"
	"strconv"
	"unicode"
)

const ROWS = 140
const COLS = 140

func Day3Task1() {
	input := openTextFile("inputs/aoc03.txt")
	scanner := bufio.NewScanner(input)

	gearPlan := [ROWS][COLS]rune{}
	lineCount := 0

	for scanner.Scan() {
		for count, character := range scanner.Text() {
			gearPlan[lineCount][count] = character
		}
		lineCount++
	}

	currentNumber := ""
	runningCount := 0
	hasSurrounded := false

	for r := 0; r < ROWS; r++ {
		for c := 0; c < COLS; c++ {
			if unicode.IsDigit(gearPlan[r][c]) {
				currentNumber += string(gearPlan[r][c])

				if isSurrounded(gearPlan, r, c) {
					hasSurrounded = true
				}
			} else {
				if hasSurrounded {
					number, err := strconv.Atoi(currentNumber)
					if err != nil {
						err = errors.Join(errors.New("error parsing number"), err)
						log.Fatal(err)
					}
					runningCount += number
					hasSurrounded = false
				}
				// reset current number
				currentNumber = ""
			}
		}
	}
	print(runningCount)
}

func Day3Task2() {
	input := openTextFile("inputs/aoc03.txt")
	scanner := bufio.NewScanner(input)

	gearPlan := [ROWS][COLS]rune{}
	lineCount := 0

	for scanner.Scan() {
		for count, character := range scanner.Text() {
			gearPlan[lineCount][count] = character
		}
		lineCount++
	}

	currentNumber := ""
	runningCount := 0
	hasSurrounded := false

	starMap := make(map[int]int)
	surroundedValue := -1

	for r := 0; r < ROWS; r++ {
		for c := 0; c < COLS; c++ {
			if unicode.IsDigit(gearPlan[r][c]) {
				currentNumber += string(gearPlan[r][c])
				if !hasSurrounded {
					surroundedValue = starIsSurroundedFails(gearPlan, r, c)

				}
				if surroundedValue != -1 {
					hasSurrounded = true
				}
			} else {
				if hasSurrounded {
					number, err := strconv.Atoi(currentNumber)
					if err != nil {
						err = errors.Join(errors.New("error parsing number"), err)
						log.Fatal(err)
					}
					if starMap[surroundedValue] != 0 && starMap[surroundedValue] != number {
						runningCount += (starMap[surroundedValue] * number)
					}
					hasSurrounded = false
				}
				// reset current number
				currentNumber = ""
			}
		}
	}
	print(runningCount)

}

func isSurrounded(arr [ROWS][COLS]rune, row int, col int) bool {
	// if top left exists
	if (row-1 != -1) && (col-1 != -1) {
		if !unicode.IsDigit(arr[row-1][col-1]) && arr[row-1][col-1] != '.' {
			return true
		}
	}
	if row-1 != -1 {
		// follows that row-1, col will exist
		if !unicode.IsDigit(arr[row-1][col]) && arr[row-1][col] != '.' {
			return true
		}
	}
	// now check if row-1 exists
	if col-1 != -1 {
		if !unicode.IsDigit(arr[row][col-1]) && arr[row][col-1] != '.' {
			return true
		}
	}
	// now check if top right exists
	if (row-1 != -1) && (col+1 != COLS) {
		if !unicode.IsDigit(arr[row-1][col+1]) && arr[row-1][col+1] != '.' {
			return true
		}
	}
	// now check if r+1, col-1 exists
	if (row+1 != ROWS) && (col-1 != -1) {
		if !unicode.IsDigit(arr[row+1][col-1]) && arr[row+1][col-1] != '.' {
			return true
		}
	}
	// now check if r+1, col exists
	if row+1 != ROWS {
		if !unicode.IsDigit(arr[row+1][col]) && arr[row+1][col] != '.' {
			return true
		}
	}

	// now check if r+1, c+1 exists
	if (row+1 != ROWS) && (col+1 != COLS) {
		if !unicode.IsDigit(arr[row+1][col+1]) && arr[row+1][col+1] != '.' {
			return true
		}
	}

	if col+1 != COLS {
		if !unicode.IsDigit(arr[row][col+1]) && arr[row][col+1] != '.' {
			return true
		}
	}
	return false
}
func starIsSurroundedFails(arr [ROWS][COLS]rune, row int, col int) int {
	// count_from_beginning is the "key" to the map - we store whatever other ratio references it at this place
	// if another ratio later on also touches this asterisk, it'll be the same key to access the other half of the ratio
	// because only 2 numbers touch 1 asterisk, we can do this
	// else it'd be a pain
	count_from_beginning := 0
	if (row-1 != -1) && (col-1 != -1) {
		if arr[row-1][col-1] == '*' {
			count_from_beginning = ((row - 1) * COLS) + col - 1
			return count_from_beginning
		}
	}
	if row-1 != -1 {
		// follows that row-1, col will exist
		if arr[row-1][col] == '*' {
			count_from_beginning = ((row - 1) * COLS) + col
			return count_from_beginning
		}
	}
	// now check if row-1 exists
	if col-1 != -1 {
		if arr[row][col-1] == '*' {
			count_from_beginning = ((row) * COLS) + col - 1
			return count_from_beginning
		}
	}
	// now check if top right exists
	if (row-1 != -1) && (col+1 != COLS) {
		if arr[row-1][col+1] == '*' {
			count_from_beginning = ((row - 1) * COLS) + col + 1
			return count_from_beginning
		}
	}
	// now check if r+1, col-1 exists
	if (row+1 != ROWS) && (col-1 != -1) {
		if arr[row+1][col-1] == '*' {
			count_from_beginning = ((row + 1) * COLS) + col - 1
			return count_from_beginning
		}
	}
	// now check if r+1, col exists
	if row+1 != ROWS {
		if arr[row+1][col] == '*' {
			count_from_beginning = ((row + 1) * COLS) + col
			return count_from_beginning
		}
	}
	// now check if r+1, c+1 exists
	if (row+1 != ROWS) && (col+1 != COLS) {
		if arr[row+1][col+1] == '*' {
			count_from_beginning = ((row + 1) * COLS) + col + 1
			return count_from_beginning
		}
	}
	// now check if r, c+1 exists
	if col+1 != COLS {
		if arr[row][col+1] == '*' {
			count_from_beginning = ((row) * COLS) + col + 1
			return count_from_beginning
		}
	}
	return -1
}
