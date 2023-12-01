package puzzles

import (
	"bufio"
	"log"
	"regexp"
	"strconv"
	"strings"
)

func Day1Task1() {
	input := openTextFile("inputs/aoc01.txt")
	defer input.Close()

	regexPattern := "[0-9]"
	regex, err := regexp.Compile(regexPattern)
	if err != nil {
		log.Fatal(err)
	}

	sum := 0

	scanner := bufio.NewScanner(input)
	for scanner.Scan() {
		line := scanner.Text()
		digits := regex.FindAllString(line, -1)
		if len(digits) == 0 {
			continue
		} else if len(digits) == 1 {
			numberString := digits[0]
			numberString = strings.Repeat(numberString, 2)
			number := stringToNumber(numberString)
			sum += number
		} else {
			numberString := digits[0] + digits[len(digits)-1]
			number := stringToNumber(numberString)
			sum += number

		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	println(sum)
}

func Day1Task2() {
	input := openTextFile("inputs/aoc01.txt")
	defer input.Close()

	numberMap := map[string]int{
		"one":   1,
		"two":   2,
		"three": 3,
		"four":  4,
		"five":  5,
		"six":   6,
		"seven": 7,
		"eight": 8,
		"nine":  9,
	}

	literalNumberConverter := regexp.MustCompile(`(one|two|three|four|five|six|seven|eight|nine)`)
	digitFinder := regexp.MustCompile("[1-9]")
	sum := 0

	scanner := bufio.NewScanner(input)
	for scanner.Scan() {
		line := scanner.Text()
		replacedNumbersString := literalNumberConverter.ReplaceAllStringFunc(line, func(matched string) string {
			return strconv.Itoa(numberMap[matched])
		})
		digits := digitFinder.FindAllString(replacedNumbersString, -1)

		if len(digits) == 0 {
			println("No digits found")
			continue
		} else if len(digits) == 1 {
			numberString := digits[0]
			numberString = strings.Repeat(numberString, 2)
			number := stringToNumber(numberString)
			sum += number
		} else {
			numberString := digits[0] + digits[len(digits)-1]
			number := stringToNumber(numberString)
			sum += number

		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	println(sum)

}
