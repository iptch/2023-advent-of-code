use std::collections::HashMap;
use std::io;
use std::io::Lines;
use std::io::StdinLock;

use anyhow::Context;
use anyhow::Result;
use regex::Regex;

fn parse_map(stdin: &mut Lines<StdinLock<'_>>) -> Result<HashMap<String, (String, String)>> {
    let mut map: HashMap<String, (String, String)> = HashMap::new();
    let re = Regex::new(r"([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)")?;
    for line in stdin {
        let line = line?;
        let (_, [from, to_left, to_right]) = re.captures(&line).context("capture line")?.extract();
        map.insert(
            from.to_string(),
            (to_left.to_string(), to_right.to_string()),
        );
    }
    Ok(map)
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
struct Position {
    instruction: usize,
    node: String,
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
struct Jump {
    distance: usize,
    node: String,
}

#[derive(Debug, PartialEq, Eq, Clone)]
struct Ghost {
    instructions_len: usize,

    current_distance: usize,
    current_node: String,

    graph: HashMap<Position, Jump>,
}

impl Ghost {
    fn jump(&mut self) {
        let jump = self.graph.get(&self.current_position()).unwrap();
        self.current_node = jump.node.clone();
        self.current_distance += jump.distance;
    }

    fn current_position(&self) -> Position {
        return Position {
            instruction: self.current_distance % self.instructions_len,
            node: self.current_node.clone(),
        };
    }
}

fn build_ghosts(map: &HashMap<String, (String, String)>, instruction_sequence: &str) -> Vec<Ghost> {
    let ghosts = map.keys().filter(|s| s.ends_with("A"));
    let mut built_ghosts = vec![];

    for mut ghost_node in ghosts {
        let mut ghost_distance = 0;
        let mut instructions = instruction_sequence.chars().cycle();
        let mut advance = || {
            while !ghost_node.ends_with("Z") {
                let instruction = instructions.next().unwrap();
                let moves = map.get(ghost_node).unwrap();
                ghost_node = match instruction {
                    'L' => &moves.0,
                    'R' => &moves.1,
                    _ => panic!(),
                };
                ghost_distance += 1;
            }
            (ghost_distance, ghost_node.clone())
        };
        // find ghost's initial Z node
        let (initial_distance, initial_node) = advance();
        // build ghost's graph
        let mut current_distance = initial_distance;
        let mut current_position = Position {
            instruction: initial_distance % instruction_sequence.len(),
            node: initial_node.clone(),
        };
        let mut graph: HashMap<Position, Jump> = HashMap::new();
        while !graph.contains_key(&current_position) {
            let (distance, node) = advance();
            graph.insert(
                current_position.clone(),
                Jump {
                    distance,
                    node: node.clone(),
                },
            );
            current_distance += distance;
            current_position = Position {
                instruction: current_distance % instruction_sequence.len(),
                node: node.clone(),
            };
        }

        built_ghosts.push(Ghost {
            instructions_len: instruction_sequence.len(),
            current_distance: initial_distance,
            current_node: initial_node,
            graph,
        })
    }
    built_ghosts
}

fn main() -> Result<()> {
    let mut stdin = io::stdin().lines();

    let instruction_sequence: String = stdin.next().expect("")?;
    stdin.next();

    let map = parse_map(&mut stdin)?;
    let mut ghosts = build_ghosts(&map, &instruction_sequence);
    dbg!(&ghosts);

    while !ghosts
        .iter()
        .all(|g| g.current_distance == ghosts[0].current_distance)
    {
        ghosts
            .iter_mut()
            .min_by_key(|g| g.current_distance)
            .context("computing minimum ghost")?
            .jump();
    }

    println!("{}", ghosts[0].current_distance);

    Ok(())
}
