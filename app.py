from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import text_operations
import solution
import end_program


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, path, alert_file):
        self.file_name = alert_file
        self.path = path
        self.observer = Observer()
        self.text_operations = text_operations.TextOperations(self.file_name)
        self.solution = solution.Solution()
        self.end_program = end_program.EndProgram()
        self.today_events = []

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(self.file_name):
            new_event = self.text_operations.new_alert()
            if new_event:
                self.today_events.append(new_event)

    def observe(self):
        self.observer.schedule(self, self.path, recursive=False)
        self.observer.start()
        try:
            while self.observer.is_alive():
                self.observer.join(1)
        except KeyboardInterrupt:
            self.observer.stop()
            self.end_program.check_firewall()
            self.end_program.make_email_message(self.today_events)
            print('Bye!')


if __name__ == "__main__":
    alert_file = 'alert'
    handler = MyEventHandler('.', alert_file)
    handler.observe()
