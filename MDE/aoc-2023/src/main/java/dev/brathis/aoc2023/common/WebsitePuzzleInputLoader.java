package dev.brathis.aoc2023.common;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class WebsitePuzzleInputLoader implements PuzzleInputLoader {
    private static final String PUZZLE_INPUT_URI = "https://adventofcode.com/%d/day/%d/input";
    private final Integer year;

    public WebsitePuzzleInputLoader(Integer year) {
        this.year = year;
    }

    private URI getRequestUri(Integer day) {
        return URI.create(PUZZLE_INPUT_URI.formatted(this.year, day));
    }

    @Override
    public BufferedReader getTestPuzzleInput(Integer day) {
        // Currently, there is no endpoint for the test puzzle data.
        return null;
    }

    @Override
    public BufferedReader getPuzzleInput(Integer day) {
        HttpClient httpClient = HttpClient.newHttpClient();
        HttpRequest httpRequest = HttpRequest.newBuilder()
                .uri(getRequestUri(day))
                .build();
        try {
            HttpResponse<String> httpResponse = httpClient.send(httpRequest, HttpResponse.BodyHandlers.ofString());
            StringReader stringReader = new StringReader(httpResponse.body());
            return new BufferedReader(stringReader);
        } catch (IOException | InterruptedException e) {
            return null;
        }
    }
}
