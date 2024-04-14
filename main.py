import math
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QFrame
from FGC_gui import Ui_Frame

class Window(QFrame):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Frame()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.old_pos = None

        self.ui.title_bar.mousePressEvent = self.mouse_press_event
        self.ui.title_bar.mouseMoveEvent = self.mouse_move_event
        self.ui.title_bar.mouseReleaseEvent = self.mouse_release_event

        self.ui.CloseButton.clicked.connect(self.close)
        self.ui.MinButton.clicked.connect(self.showMinimized)

        self.ui.CalculateButton.clicked.connect(self.Calculate)


    def Calculate(self):
        fuel_gen_values = {
            "fuel_per_min": 12,
            "MW": 150,
            "fluid_per_minute_with_plus": 6,
            "Computers": 5,
            "Heavy_Modular_Frame": 10,
            "Rotors": 15,
            "Rubber": 50,
            "Quickwire": 50
        }

        oil_rare_val = {
            "impure": 60,
            "normal": 120,
            "pure": 240,
        }

        refinery_val = {
            "need_oil_Fuel_processing_permin": 60,
            "fuel_ouptut_permin": 40
        }
        MW = fuel_gen_values["MW"]
        Fuel_PerMin = fuel_gen_values["fuel_per_min"]
        refinery_fuel_output = refinery_val["fuel_ouptut_permin"]


        input_user_energy = float(self.ui.MWEntry.text())

        input_user_div_MW =  input_user_energy / MW

        input_rare_of_oil = None

        if self.ui.ImpureRadioButton.isChecked():
            input_rare_of_oil = 1
        elif self.ui.NormalRadioButton.isChecked():
            input_rare_of_oil = 2
        elif self.ui.PureRadioButton.isChecked():
            input_rare_of_oil = 3

        if input_rare_of_oil is not None:
            if input_user_energy == 0:
                pass
            else:
                ######################################################
                ### Calculate how many Fuel Generators
                self.ui.FuelGen_Output.setText(str(math.ceil(input_user_div_MW)))

                ######################################################
                ### Calculate how many Fuel Per/Min
                calc_fuel_permin_round = round(input_user_div_MW * Fuel_PerMin, 2)
                self.ui.FuelPerMin_Output.setText(str(calc_fuel_permin_round))

                ######################################################
                ### Calculate how many Refineries
                refineries = (Fuel_PerMin * input_user_div_MW) / refinery_fuel_output
                self.ui.Refineries_Output.setText(str(round(refineries, 1)))

                ######################################################
                ### Calculate how many oil extracts]
                refinery_oil_processing_PerMin = refinery_val["need_oil_Fuel_processing_permin"]
                oil_extractors = refineries * refinery_oil_processing_PerMin

                if input_rare_of_oil == 1:
                    oil_extractors_result = oil_extractors / oil_rare_val["impure"]
                elif input_rare_of_oil == 2:
                    oil_extractors_result = oil_extractors / oil_rare_val["normal"]
                elif input_rare_of_oil == 3:
                    oil_extractors_result = oil_extractors / oil_rare_val["pure"]
                self.ui.OilExt_Output.setText(str(round(oil_extractors_result, 2)))


    def mouse_press_event(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition()

    def mouse_move_event(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.old_pos:
            delta = event.globalPosition() - self.old_pos
            self.move(int(self.x() + delta.x()), int(self.y() + delta.y()))

            self.old_pos = event.globalPosition()

    def mouse_release_event(self, event):
        self.old_pos = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()  # Показываем окно только здесь
    sys.exit(app.exec())
