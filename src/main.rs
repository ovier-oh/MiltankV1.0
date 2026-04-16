struct Task {
    id: u32,
    title: String,
    completed: bool,
}

fn main() {
    let task = Task {
        id: 1,
        title: String::from("Lavar Trastos"),
        completed: false,
    };

    println!("Id: {}", task.id);
    println!("Title: {}", task.title);
    println!("Completed: {}", task.completed);
}
