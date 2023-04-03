
...

class AlertMessageComponent:
    

    def show_message_box(warning_text: str) -> bool:
        msg_box: QMessageBox = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(warning_text)
        msg_box.setWindowTitle("Error")
        msg_box.setStandardButtons(QMessageBox.Ok)
        return msg_box.exec()
