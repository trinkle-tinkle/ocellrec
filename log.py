from datetime import datetime

def log(message, msg_type="INFO", print_to_term=True, save_to_file=True):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Terminal
    if print_to_term:
        print(f"[{timestamp}] {msg_type}: {message}")

    # File
    if save_to_file:
        with open("log.txt", "a") as f:
            f.write(f"[{timestamp}] {msg_type}: {message}\n")


if __name__ == "__main__":
    log("test")