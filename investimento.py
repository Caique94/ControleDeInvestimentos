from datetime import datetime
import sys
import json
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QMessageBox, QDialog
)

DATA_FILE = "progress_data.json"

class SetupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.goal_label = QLabel("Defina sua meta financeira (R$):")
        self.layout.addWidget(self.goal_label)

        self.goal_input = QLineEdit()
        self.layout.addWidget(self.goal_input)

        self.max_deposits_label = QLabel("Defina o número máximo de depósitos:")
        self.layout.addWidget(self.max_deposits_label)

        self.max_deposits_input = QLineEdit()
        self.layout.addWidget(self.max_deposits_input)

        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self.confirm)
        self.layout.addWidget(self.confirm_button)

        self.setLayout(self.layout)
        self.setWindowTitle("Configuração Inicial")
        self.resize(300, 150)

    def confirm(self):
        try:
            goal = float(self.goal_input.text())
            max_deposits = int(self.max_deposits_input.text())

            if goal <= 0 or max_deposits <= 0:
                raise ValueError("Os valores devem ser maiores que zero.")

            self.goal = goal
            self.max_deposits = max_deposits
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Erro", "Insira valores válidos para a meta e o número de depósitos.")

class ProgressTracker(QWidget):
    def __init__(self, goal, max_deposits):
        super().__init__()
        self.goal = goal
        self.max_deposits = max_deposits
        self.total_deposited = 0
        self.deposit_count = 0
        self.deposit_history = []

        self.init_ui()
        self.load_data()  # Mover para depois da inicialização da interface
    
    def show_history(self):
        history_window = DepositHistoryWindow(self.deposit_history)
        history_window.exec_()


    def init_ui(self):
        self.layout = QVBoxLayout()

        self.goal_label = QLabel(f"Meta total: R${self.goal:,.2f}")
        self.layout.addWidget(self.goal_label)

        self.deposit_label = QLabel("Valor do depósito:")
        self.layout.addWidget(self.deposit_label)

        self.deposit_input = QLineEdit()
        self.layout.addWidget(self.deposit_input)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.update_progress_bar()
        self.layout.addWidget(self.progress_bar)

        self.add_deposit_button = QPushButton("Adicionar Depósito")
        self.add_deposit_button.clicked.connect(self.add_deposit)
        self.layout.addWidget(self.add_deposit_button)

        self.history_button = QPushButton("Ver Histórico de Depósitos")
        self.history_button.clicked.connect(self.show_history)
        self.layout.addWidget(self.history_button)

        self.reset_button = QPushButton("Resetar Progresso")
        self.reset_button.clicked.connect(self.reset_tracker)
        self.layout.addWidget(self.reset_button)

        self.reset_to_setup_button = QPushButton("Redefinir Meta e Depósitos")
        self.reset_to_setup_button.clicked.connect(self.reset_to_setup)
        self.layout.addWidget(self.reset_to_setup_button)

        self.status_label = QLabel(self.get_status_text())
        self.layout.addWidget(self.status_label)

        self.deposit_count_label = QLabel(self.get_deposit_count_text())
        self.layout.addWidget(self.deposit_count_label)

        self.setLayout(self.layout)
        self.setWindowTitle("Calculadora de Meta Financeira")
        self.resize(400, 200)

    def add_deposit(self):
        try:
            deposit = float(self.deposit_input.text())
            if deposit <= 0:
                raise ValueError("O depósito deve ser maior que zero.")

            deposit_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            self.total_deposited += deposit
            self.deposit_count += 1
            self.deposit_history.append({"value": deposit, "date": deposit_date})
            self.save_data()

            self.update_progress_bar()
            self.status_label.setText(self.get_status_text())
            self.deposit_count_label.setText(self.get_deposit_count_text())

            if self.total_deposited >= self.goal or self.deposit_count >= self.max_deposits:
                self.prompt_new_goal()

            self.deposit_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Erro", "Insira um valor válido para o depósito.")

    def prompt_new_goal(self):
        reply = QMessageBox.question(self, "SUCESSO ! Meta atingida!", "Você deseja estabelecer uma nova meta?", 
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.reset_to_setup(preserve_history=True)
        else:
            self.export_to_csv()

    def export_to_csv(self):
        file_name = f"deposit_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Meta", "Depósitos Máximos", "Total Depositado", "Contagem de Depósitos"])
            writer.writerow([self.goal, self.max_deposits, self.total_deposited, self.deposit_count])
            writer.writerow([])
            writer.writerow(["Depósito", "Valor", "Data"])
            for i, entry in enumerate(self.deposit_history, 1):
                writer.writerow([i, entry['value'], entry['date']])

        QMessageBox.information(self, "CSV Gerado", f"Histórico salvo em {file_name}")

    def reset_tracker(self):
        self.total_deposited = 0
        self.deposit_count = 0
        self.deposit_history = []
        self.save_data()
        self.update_progress_bar()
        self.status_label.setText(self.get_status_text())
        self.deposit_count_label.setText(self.get_deposit_count_text())

    def reset_to_setup(self, preserve_history=False):
        self.hide()
        setup_window = SetupWindow()
        if setup_window.exec_() == QDialog.Accepted:
            self.goal = setup_window.goal
            self.max_deposits = setup_window.max_deposits

            if not preserve_history:
                self.reset_tracker()

            self.goal_label.setText(f"Meta total: R${self.goal:,.2f}")
            self.show()

    def get_status_text(self):
        remaining = max(self.goal - self.total_deposited, 0)
        return f"Progresso: R${self.total_deposited:,.2f} de R${self.goal:,.2f} (Faltam: R${remaining:,.2f})"

    def get_deposit_count_text(self):
        return f"Depósitos realizados: {self.deposit_count}/{self.max_deposits}"

    def update_progress_bar(self):
        progress = min((self.total_deposited / self.goal) * 100, 100)
        self.progress_bar.setValue(int(progress))

        if progress == 100:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: white; }")
        else:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")

    def save_data(self):
        data = {
            "goal": self.goal,
            "max_deposits": self.max_deposits,
            "total_deposited": self.total_deposited,
            "deposit_count": self.deposit_count,
            "deposit_history": self.deposit_history
        }
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                self.goal = data.get("goal", 0)
                self.max_deposits = data.get("max_deposits", 0)
                self.total_deposited = data.get("total_deposited", 0)
                self.deposit_count = data.get("deposit_count", 0)
                self.deposit_history = data.get("deposit_history", [])
        except FileNotFoundError:
            print("Arquivo de dados não encontrado. Iniciando com valores padrão.")
        except json.JSONDecodeError:
            print("Erro ao decodificar o arquivo JSON. Reiniciando valores.")
            self.reset_tracker()
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.reset_tracker()

class DepositHistoryWindow(QMessageBox):
    def __init__(self, history):
        super().__init__()
        self.setWindowTitle("Histórico de Depósitos")
        self.setText(self.format_history(history))

    def format_history(self, history):
        if not history:
            return "Que triste! Nenhum depósito registrado ainda."
        return "\n".join([
            f"Depósito {i + 1}: R${entry['value']:,.2f} em {entry['date']}" 
            for i, entry in enumerate(history)
        ])

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            goal = data["goal"]
            max_deposits = data["max_deposits"]
            tracker = ProgressTracker(goal, max_deposits)
            tracker.show()
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        setup_window = SetupWindow()
        if setup_window.exec_() == QDialog.Accepted:
            goal = setup_window.goal
            max_deposits = setup_window.max_deposits

            tracker = ProgressTracker(goal, max_deposits)
            tracker.show()

    sys.exit(app.exec_())
