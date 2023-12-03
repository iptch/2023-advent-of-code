import Data.List
main :: IO ()
main = do
  linesArray <- fmap lines getContents
  print (sum (fmap printFirstAndLastDigit linesArray))

printFirstAndLastDigit :: String -> Int
printFirstAndLastDigit string = do
  case (firstDigit string, lastDigit string) of
    (Just i, Just j) -> i * 10 + j
    _ -> error "asdf"

lastDigit :: String -> Maybe Int
lastDigit string = let (index, value) = lastDigitIndex string in
  case index of
    Nothing -> Nothing
    Just _ -> Just value


lastDigitIndex :: String -> (Maybe Integer, Int)
lastDigitIndex string = foldr (\digit acc -> case (findStringLast (fst digit) string, fst acc) of
  (Just i, Just j) | i > j -> (Just i, snd digit)
  (Just i, Nothing)  -> (Just i, snd digit)
  _ -> acc) (Nothing, 0) digits

firstDigit :: String -> Maybe Int
firstDigit string = let (index, value) = firstDigitIndex string in
  case index of
    Nothing -> Nothing
    Just _ -> Just value

firstDigitIndex :: String -> (Maybe Integer, Int)
firstDigitIndex string = foldr (\digit acc -> case (findString (fst digit) string, fst acc) of
  (Just i, Just j) | i < j -> (Just i, snd digit)
  (Just i, Nothing)  -> (Just i, snd digit)
  _ -> acc) (Nothing, 0) digits

findString :: String -> String -> Maybe Integer
findString search "" = Nothing
findString search string =
  if take (length search) string == search
    then Just 0
    else fmap (+1) (findString search (tail string))

findStringLast :: String -> String -> Maybe Integer
findStringLast search string =
  let fromLast = findString (reverse search) (reverse string) in
  fmap (\x -> genericLength string - x - genericLength search) fromLast

digits :: [(String, Int)]
digits = [
  ("1", 1),
  ("2", 2),
  ("3", 3),
  ("4", 4),
  ("5", 5),
  ("6", 6),
  ("7", 7),
  ("8", 8),
  ("9", 9),
  ("one", 1),
  ("two", 2),
  ("three", 3),
  ("four", 4),
  ("five", 5),
  ("six", 6),
  ("seven", 7),
  ("eight", 8),
  ("nine", 9)]

