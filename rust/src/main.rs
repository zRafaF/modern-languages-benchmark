use std::env;
use std::fs::File;
use std::io::Read;
use std::process;

pub mod boxblur;
pub mod bubblesort;

fn main() {
    // Collect command line arguments
    let args: Vec<String> = env::args().collect();

    // Check if we received exactly two arguments (first is program name)
    if args.len() != 3 {
        eprintln!("Usage: {} <path_to_bin_file> <number>", args[0]);
        process::exit(1);
    }

    let file_path = &args[1];
    let benchmark_type: usize = match args[2].parse() {
        Ok(num) => num,
        Err(_) => {
            eprintln!("Error: The second argument must be a valid number.");
            process::exit(1);
        }
    };

    // Read the binary file content into a u8 vector
    let mut file = match File::open(file_path) {
        Ok(file) => file,
        Err(e) => {
            eprintln!("Failed to open file: {}", e);
            process::exit(1);
        }
    };

    let mut buffer = Vec::new();
    if let Err(e) = file.read_to_end(&mut buffer) {
        eprintln!("Failed to read the file: {}", e);
        process::exit(1);
    }

    //switch between benchmarks
    match benchmark_type {
        1 => {
            _ = bubblesort::sort(buffer);
        }
        2 => {
            _ = boxblur::sequential(buffer);
        }
        3 => {
            _ = boxblur::parallel(buffer);
        }
        _ => {
            eprintln!("Error: The second argument must be a valid number.");
            process::exit(1);
        }
    }
}
