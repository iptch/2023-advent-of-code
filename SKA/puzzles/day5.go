package puzzles

import (
	"bufio"
	"fmt"
	"log"
	"strings"

	"github.com/samber/lo"
)

type GardenerMap struct {
	src int
	dst int
	rng int
}

var (
	seed2Soil      = make([]GardenerMap, 0)
	soil2Fert      = make([]GardenerMap, 0)
	fert2Water     = make([]GardenerMap, 0)
	water2Light    = make([]GardenerMap, 0)
	light2Temp     = make([]GardenerMap, 0)
	temp2Humid     = make([]GardenerMap, 0)
	humid2Location = make([]GardenerMap, 0)
)

func Day5Task1() {
	input := openTextFile("inputs/aoc05.txt")
	scanner := bufio.NewScanner(input)

	scanner.Scan()
	firstLine := scanner.Text()
	seedsString := strings.Split(strings.Trim(strings.Split(firstLine, ":")[1], " "), " ")

	seeds := make([]int, 0)
	for _, seed := range seedsString {
		seeds = append(seeds, stringToNumber(seed))
	}

	// skip empty line before mappings start
	scanner.Scan()

	readMaps(scanner, &seed2Soil)
	readMaps(scanner, &soil2Fert)
	readMaps(scanner, &fert2Water)
	readMaps(scanner, &water2Light)
	readMaps(scanner, &light2Temp)
	readMaps(scanner, &temp2Humid)
	readMaps(scanner, &humid2Location)

	locations := make([]int, 0)

	for _, seed := range seeds {
		soil := srcToDst(seed, seed2Soil)
		fert := srcToDst(soil, soil2Fert)
		water := srcToDst(fert, fert2Water)
		light := srcToDst(water, water2Light)
		temp := srcToDst(light, light2Temp)
		humid := srcToDst(temp, temp2Humid)
		loc := srcToDst(humid, humid2Location)

		locations = append(locations, loc)
	}

	fmt.Println(lo.Min(locations))
}

func readMaps(scanner *bufio.Scanner, maps *[]GardenerMap) {
	// title of mapping in text file
	scanner.Scan()

	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			break
		}

		*maps = append(*maps, lineToMap(line))
	}

}

func lineToMap(line string) GardenerMap {
	gardenerMap := new(GardenerMap)
	textSegments := strings.Split(line, " ")

	if len(textSegments) != 3 {
		log.Fatal("wrong input for GardenerMap")
	}

	gardenerMap.src = stringToNumber(textSegments[1])
	gardenerMap.dst = stringToNumber(textSegments[0])
	gardenerMap.rng = stringToNumber(textSegments[2])

	return *gardenerMap
}

func srcToDst(value int, gardenerMap []GardenerMap) int {
	for _, gm := range gardenerMap {
		if value >= gm.src && value <= gm.src+gm.rng {
			return gm.dst + (value - gm.src)
		}
	}
	return value
}
