use std::io;

struct Task {
    id: u32,
    title: String,
    completed: bool,
    comments: String,
}

impl Task {
    fn new(id: u32, title: String, comments: String) -> Task {
        Task {
            id,
            title,
            completed: false,
            comments,
        }
    }
}

fn create_task() {
    println!("Enter Id:");
    let mut id_input = String::new();
    io::stdin().read_line(&mut id_input).unwrap();
    let id: u32 = id_input.trim().parse().unwrap();

    println!("Enter title:");
    let mut title = String::new();
    io::stdin().read_line(&mut title).unwrap();

    println!("Enter comments:");
    let mut comments = String::new();
    io::stdin().read_line(&mut comments).unwrap();

    let task = Task::new(id, title, comments);

    println!("If: {}", task.id);
    println!("Title: {}", task.title);
    println!("Completed: {}", task.completed);
    println!("Comments: {}", task.comments);
}

fn main() {
    create_task();
}

