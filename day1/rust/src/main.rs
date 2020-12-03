use std::collections::{HashMap, HashSet};
use std::fs;

fn main() {
    let text = fs::read_to_string("..\\input.txt").expect("Cannot read file");
    let data: Vec<i32> = text.lines().map(|x| x.parse::<i32>().unwrap()).collect();
    two_sum(&data);
    three_sum(&data);
}

fn two_sum(data: &Vec<i32>) {
    let mut set = HashSet::new();
    let target = 2020;

    for x in data.into_iter() {
        let t = target - x;

        if set.contains(x) {
            println!("two sum: {} * {} = {}", x, t, x * t);
            return;
        } else {
            set.insert(t);
        }
    }
}

fn three_sum(data: &Vec<i32>) {
    let mut map: HashMap<i32, (i32, i32)> = HashMap::new();
    let target = 2020;

    let len = data.len();

    for i in 0..len {
        for j in i..len {
            let t = target - data[i] - data[j];

            if map.contains_key(&data[j]) {
                let entry = map.get(&data[j]).unwrap();

                println!(
                    "three sum: {} ",
                    (data[j] as u64) * (entry.0 as u64) * (entry.1 as u64)
                );
                return;
            } else {
                map.insert(t, (data[i], data[j]));
            }
        }
    }
}
