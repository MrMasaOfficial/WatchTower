import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer, Qt
import logging
import time
import sys

# Setup logging
logging.basicConfig(filename='system_monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Thresholds
CPU_THRESHOLD = 80
RAM_THRESHOLD = 80
DISK_THRESHOLD = 90

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Monitor Pro")
        self.prev_net = psutil.net_io_counters()
        self.prev_time = time.time()
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(2000)  # every 2 seconds
        self.update_info()

    def init_ui(self):
        layout = QVBoxLayout()

        # CPU
        self.cpu_label = QLabel("CPU Usage: 0%")
        layout.addWidget(self.cpu_label)

        # RAM
        self.ram_label = QLabel("RAM Usage: 0%")
        layout.addWidget(self.ram_label)

        # Disk
        self.disk_label = QLabel("Disk Usage: 0%")
        layout.addWidget(self.disk_label)

        # Network
        self.net_label = QLabel("Network: Sent 0 B/s, Recv 0 B/s")
        layout.addWidget(self.net_label)

        # Processes
        self.process_tree = QTreeWidget()
        self.process_tree.setColumnCount(4)
        self.process_tree.setHeaderLabels(['PID', 'Name', 'CPU%', 'Memory%'])
        layout.addWidget(self.process_tree)

        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.update_info)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=0.1)

    def get_ram_usage(self):
        return psutil.virtual_memory().percent

    def get_disk_usage(self):
        return psutil.disk_usage('/').percent

    def get_network_usage(self):
        current_net = psutil.net_io_counters()
        current_time = time.time()
        time_diff = current_time - self.prev_time
        sent_rate = (current_net.bytes_sent - self.prev_net.bytes_sent) / time_diff if time_diff > 0 else 0
        recv_rate = (current_net.bytes_recv - self.prev_net.bytes_recv) / time_diff if time_diff > 0 else 0
        self.prev_net = current_net
        self.prev_time = current_time
        return sent_rate, recv_rate

    def get_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append((proc.info['pid'], proc.info['name'] or 'Unknown', proc.info['cpu_percent'] or 0, proc.info['memory_percent'] or 0))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        # Sort by CPU usage descending
        processes.sort(key=lambda x: x[2], reverse=True)
        return processes[:20]

    def check_alerts(self, cpu, ram, disk):
        if cpu > CPU_THRESHOLD:
            QMessageBox.warning(self, "Alert", f"CPU usage high: {cpu:.1f}%")
            logging.info(f"CPU usage alert: {cpu:.1f}%")
        if ram > RAM_THRESHOLD:
            QMessageBox.warning(self, "Alert", f"RAM usage high: {ram:.1f}%")
            logging.info(f"RAM usage alert: {ram:.1f}%")
        if disk > DISK_THRESHOLD:
            QMessageBox.warning(self, "Alert", f"Disk usage high: {disk:.1f}%")
            logging.info(f"Disk usage alert: {disk:.1f}%")

    def update_info(self):
        cpu = self.get_cpu_usage()
        ram = self.get_ram_usage()
        disk = self.get_disk_usage()
        sent_rate, recv_rate = self.get_network_usage()
        processes = self.get_processes()

        self.cpu_label.setText(f"CPU Usage: {cpu:.1f}%")
        self.ram_label.setText(f"RAM Usage: {ram:.1f}%")
        self.disk_label.setText(f"Disk Usage: {disk:.1f}%")
        self.net_label.setText(f"Network: Sent {sent_rate:.0f} B/s, Recv {recv_rate:.0f} B/s")

        # Clear tree
        self.process_tree.clear()
        for proc in processes:
            item = QTreeWidgetItem([str(proc[0]), proc[1], f"{proc[2]:.1f}", f"{proc[3]:.1f}"])
            self.process_tree.addTopLevelItem(item)

        self.check_alerts(cpu, ram, disk)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    sys.exit(app.exec())