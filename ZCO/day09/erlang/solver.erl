-module(solver).
-export([main/0]).

parse_line(Line) ->
  lists:map(fun(I) -> erlang:list_to_integer(I) end, string:tokens(Line, " \n")).

parse_stdin() ->
  case io:get_line("") of
    eof -> [];
    Line -> [parse_line(Line) | parse_stdin()]
  end.

expand(TestCase) ->
  [H | _] = TestCase,
  [_ | Tail] = H,
  Differences = lists:map(fun({I1, I2}) -> I2 - I1 end, lists:zip(H, Tail, trim)),
  AllZeros = lists:all(fun(I) -> I == 0 end, Differences),
  if AllZeros ->
       TestCase;
    true ->
       expand([Differences | TestCase])
  end.

solve_part1_testcase(ExpandedTestCase) ->
  lists:foldl(fun(L, Accu) -> Accu + lists:last(L) end, 0, ExpandedTestCase).

solve_part2_testcase(ExpandedTestCase) ->
  lists:foldl(fun([H | _], Accu) -> H - Accu end, 0, ExpandedTestCase).

main() ->
  ExpandedTestCases = lists:map(fun(T) -> expand([T]) end, parse_stdin()),
  % solve part 1
  erlang:display(lists:foldl(fun(TC, Accu) -> Accu + solve_part1_testcase(TC) end, 0, ExpandedTestCases)),
  % solve part 2
  erlang:display(lists:foldl(fun(TC, Accu) -> Accu + solve_part2_testcase(TC) end, 0, ExpandedTestCases)).
