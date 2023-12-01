package puzzles

import (
	"errors"
	"fmt"
	"log"
	"os"
	"strconv"
)

func openTextFile(path string) *os.File {
	input, err := os.Open(path)
	if err != nil {
		err = errors.Join(fmt.Errorf("could not open file %s", path), err)
		log.Fatal(err)
	}

	return input
}

func stringToNumber(str string) int {
	number, err := strconv.Atoi(str)
	if err != nil {
		err = errors.Join(errors.New("could not convert string to number"), err)
		log.Fatal(err)
	}
	return number
}
